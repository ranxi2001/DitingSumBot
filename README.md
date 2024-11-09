# TG群聊土狗交易总结机器人 Docker部署教程

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