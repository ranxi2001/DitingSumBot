# TG群聊土狗交易总结机器人 Docker部署教程

## 重要提示（对不起本项目失败了）

在 Telegram 中，一个 bot 默认是无法接收来自其他 bot 的消息的。Telegram 的 API 设计限制了 bot 与 bot 之间的直接交互，以防止滥用或恶意自动化。不过，你可以考虑以下几种方法来间接实现：

1. **用户转发**：可以让用户手动将其他 bot 的信息转发给你的 bot，你的 bot 就可以处理用户转发的消息。

2. **利用中间服务器**：如果你有控制某些群成员（非 bot）的权限，可以让这些成员（例如一个服务账号）监听群里的消息，将其他 bot 的消息转发或处理并发送给你的 bot。不过这需要用户配合并非完全自动化。

3. **Webhook / 轮询**：如果你可以在群聊的所有消息中筛选文本内容，可以通过 Webhook 或轮询方式实时获取信息并处理，尽管这是不完全获取其他 bot 信息的方式，但可用于简化信息的整合与分析。

如果 Telegram API 未来对 bot 与 bot 的交互有更新，这样的功能可能会直接实现。

> 所以我将下一步自己完整开发一个聪明钱监控+总结bot而不是开发一个bot来总结其他聪明钱监控bot的发言

## 系统要求

- Docker
- Docker Compose

## 部署步骤

### 1. 创建项目结构

```bash
mkdir tg-bot && cd tg-bot
mkdir app
touch docker-compose.yml
touch Dockerfile
touch app/.env
```

### 2. 创建Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python", "main.py"]
```

### 3. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  bot:
    build: .
    restart: always
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    volumes:
      - ./app:/app

  redis:
    image: redis:6-alpine
    restart: always
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

volumes:
  redis_data:
```

### 4. 配置环境变量

在 `app/.env` 文件中添加：

```bash
TELEGRAM_BOT_TOKEN=你的机器人token
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

### 5. 复制项目文件

将主要的Python文件复制到app目录：

```bash
cp main.py app/
cp requirements.txt ./
```

### 6. 启动服务

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f bot

# 停止服务
docker-compose down
```

## 维护命令

```bash
# 重启服务
docker-compose restart bot

# 更新代码后重新构建
docker-compose build bot
docker-compose up -d bot

# 查看容器状态
docker-compose ps
```

## 注意事项

1. 确保`.env`文件权限正确且不会被意外提交到代码仓库
2. 定期备份Redis数据（位于docker volume中）
3. 监控容器日志以及时发现问题

## 常见问题排查

1. 如果机器人无响应：
   - 检查容器日志 `docker-compose logs bot`
   - 验证环境变量配置
   - 确保机器人token正确

2. 如果Redis连接失败：
   - 检查Redis容器状态 `docker-compose ps`
   - 验证Redis配置
   - 检查网络连接

3. 数据备份：
```bash
# 备份Redis数据
docker-compose exec redis redis-cli SAVE
# 复制备份文件到主机
docker cp $(docker-compose ps -q redis):/data/dump.rdb ./backup/
```

这个Docker版本的部署方案相比直接部署在主机上有以下优势：
- 环境隔离，避免依赖冲突
- 易于迁移和扩展
- 简化部署流程
- 方便的容器管理和监控
```

主要更新内容：
1. 移除了系统要求中的代理服务器要求
2. 移除了常见问题排查中的代理服务器相关内容
3. 更新了机器人无响应的排查步骤，移除代理相关检查
4. 保持了其他部署和维护相关的内容不变