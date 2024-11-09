from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import re
import redis
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 从环境变量获取配置信息
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Redis 连接
try:
    REDIS_CLIENT = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        decode_responses=True  # 自动解码响应
    )
    # 测试连接
    REDIS_CLIENT.ping()
    logger.info("Successfully connected to Redis")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

# 代理设置
REQUEST_KWARGS = {
    'proxy_url': 'http://127.0.0.1:7890',
}

class TokenStats:
    def __init__(self):
        self.redis = REDIS_CLIENT
        
    def parse_message(self, text):
        logger.info(f"Parsing message: {text}")
        if "交易买入通知" in text:
            pattern = r"钱包里交易买入:(.*?)\n.*?合约：(.*?)\n.*?单价：\$(.*?)\n.*?总金额：\$(.*?)\n"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                result = {
                    'type': 'buy',
                    'token_name': match.group(1).strip(),
                    'contract': match.group(2).strip(),
                    'price': float(match.group(3)),
                    'amount': float(match.group(4))
                }
                logger.info(f"Parsed buy transaction: {result}")
                return result
        elif "交易卖出通知" in text:
            pattern = r"钱包里交易卖出:(.*?)\n.*?合约：(.*?)\n.*?单价：\$(.*?)\n.*?总金额：\$(.*?)\n"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                result = {
                    'type': 'sell',
                    'token_name': match.group(1).strip(),
                    'contract': match.group(2).strip(),
                    'price': float(match.group(3)),
                    'amount': float(match.group(4))
                }
                logger.info(f"Parsed sell transaction: {result}")
                return result
        logger.info("No matching transaction found")
        return None

    def process_transaction(self, data):
        logger.info(f"Processing transaction: {data}")
        token_key = f"token:{data['token_name']}"
        current_time = datetime.now().timestamp()
        
        try:
            if data['type'] == 'buy':
                self.redis.hincrby(token_key, 'buy_count', 1)
                self.redis.hset(token_key, 'contract', data['contract'])  # 保存合约地址
                price_data = f"{current_time}:{data['price']}"
                self.redis.rpush(f"{token_key}:prices", price_data)
                self.redis.expire(token_key, 86400)
                self.redis.expire(f"{token_key}:prices", 86400)
                logger.info(f"Processed buy transaction for {data['token_name']}")
                
            elif data['type'] == 'sell':
                if not self.redis.exists(f"{token_key}:first_sell"):
                    self.redis.set(f"{token_key}:first_sell", 1, ex=86400)
                    result = {
                        'first_sell': True,
                        'token_name': data['token_name'],
                        'price': data['price'],
                        'amount': data['amount']
                    }
                    logger.info(f"First sell detected: {result}")
                    return result
            return None
        except Exception as e:
            logger.error(f"Error processing transaction: {e}")
            raise

    def get_token_stats(self, token_name):
        token_key = f"token:{token_name}"
        
        # 获取买入次数和合约地址
        token_data = self.redis.hgetall(token_key)
        if not token_data or 'buy_count' not in token_data:
            return None
            
        # 获取价格历史
        prices = self.redis.lrange(f"{token_key}:prices", 0, -1)
        if not prices:
            return None
            
        # 解析价格历史
        price_list = [float(p.split(':')[1]) for p in prices]
        
        return {
            'token_name': token_name,
            'contract': token_data.get('contract', 'Unknown'),
            'buy_count': int(token_data['buy_count']),
            'earliest_price': min(price_list),
            'latest_price': max(price_list)
        }

def handle_message(update: Update, context: CallbackContext):
    try:
        stats = TokenStats()
        message = update.message.text
        logger.info(f"Received message: {message}")
        
        result = stats.parse_message(message)
        if result:
            sell_info = stats.process_transaction(result)
            
            if result['type'] == 'buy':
                # 获取并发送统计信息
                token_stats = stats.get_token_stats(result['token_name'])
                if token_stats:
                    stats_message = (
                        f"📊 代币统计信息\n"
                        f"代币: {token_stats['token_name']}\n"
                        f"合约: {token_stats['contract']}\n"
                        f"买入次数: {token_stats['buy_count']}\n"
                        f"最早买入价: ${token_stats['earliest_price']:.8f}\n"
                        f"最新买入价: ${token_stats['latest_price']:.8f}"
                    )
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=stats_message
                    )
            
            if sell_info and sell_info.get('first_sell'):
                reminder = (
                    f"🔔 首次卖出提醒\n"
                    f"代币: {sell_info['token_name']}\n"
                    f"卖出价格: ${sell_info['price']:.8f}\n"
                    f"总金额: ${sell_info['amount']:.2f}"
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=reminder
                )
                logger.info(f"Sent first sell reminder for {sell_info['token_name']}")
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        raise

def error_handler(update: Update, context: CallbackContext):
    """处理错误的回调函数"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    try:
        updater = Updater(
            token=TOKEN,
            request_kwargs=REQUEST_KWARGS,
            use_context=True
        )
        
        dispatcher = updater.dispatcher
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))
        dispatcher.add_error_handler(error_handler)
        
        logger.info("Bot started")
        updater.start_polling(
            timeout=30,
            read_latency=5,
            drop_pending_updates=True
        )
        updater.idle()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == '__main__':
    main()