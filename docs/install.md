# 股票基金投资论坛 - 安装部署指南

## 1. 系统要求

### 1.1 硬件要求
- CPU: 2核及以上
- 内存: 4GB及以上
- 硬盘: 10GB可用空间
- 网络: 需要互联网连接（用于安装依赖）

### 1.2 软件要求
- 操作系统: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- Python: 3.8 - 3.11
- Node.js: 16.x 或更高版本
- npm: 8.x 或更高版本
- PostgreSQL: 12.x 或更高版本
- Git: 任意版本

## 2. 项目获取

### 2.1 克隆项目
```bash
git clone https://github.com/group10086/stock-investment-forum.git
cd stock-investment-forum
```

### 2.2 项目结构
```
stock-investment-forum/
├── backend/          # 后端代码
│   ├── app/         # 应用主目录
│   ├── requirements.txt  # Python依赖
│   └── ...
├── frontend/        # 前端代码
│   ├── src/        # 源代码
│   ├── package.json  # Node依赖
│   └── ...
├── sql/            # 数据库脚本
│   ├── init.sql    # 建表脚本
│   └── sample_data.sql  # 测试数据
└── docs/           # 文档
```

## 3. 数据库配置

### 3.1 安装PostgreSQL

**Windows:**
1. 访问 https://www.postgresql.org/download/windows/
2. 下载并运行安装程序
3. 安装时设置postgres用户密码（建议：postgres123）
4. 默认端口：5432

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3.2 创建数据库

使用psql命令行工具或pgAdmin：

```bash
# 连接到PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE stock_forum;

# 退出
\q
```

### 3.3 初始化数据库表结构

```bash
# 执行建表脚本
psql -U postgres -d stock_forum -f sql/init.sql

# （可选）导入测试数据
psql -U postgres -d stock_forum -f sql/sample_data.sql
```

### 3.4 验证数据库

```bash
psql -U postgres -d stock_forum

# 查看表
\dt

# 应该看到以下表：
# users, posts, comments, follows, post_likes, 
# bookmarks, comment_likes, messages, groups, 
# group_members, reports, sensitive_words, star_follows

# 退出
\q
```

## 4. 后端部署

### 4.1 创建虚拟环境

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4.2 安装Python依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

主要依赖包括：
- FastAPI 0.104.1 - Web框架
- SQLAlchemy 2.0.23 - ORM
- psycopg2-binary 2.9.9 - PostgreSQL驱动
- python-jose 3.3.0 - JWT认证
- passlib 1.7.4 - 密码加密
- uvicorn 0.24.0 - ASGI服务器

### 4.3 配置环境变量

编辑 `backend/app/config.py` 文件：

```python
# 数据库配置
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/stock_forum"

# JWT密钥（生产环境请使用强随机字符串）
SECRET_KEY = "your-secret-key-change-in-production"

# JWT过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7天

# CORS配置
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
```

**重要提示：**
- 将 `DATABASE_URL` 中的密码改为你实际的PostgreSQL密码
- 生产环境必须修改 `SECRET_KEY` 为强随机字符串
- 可以使用以下命令生成随机密钥：
  ```python
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### 4.4 启动后端服务

```bash
# 开发模式（带热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4.5 验证后端

访问以下地址验证服务是否正常：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/health

应该返回：
```json
{"status": "ok", "message": "股票基金投资论坛 API 运行正常"}
```

## 5. 前端部署

### 5.1 安装Node依赖

```bash
cd frontend

# 安装依赖
npm install

# 或使用yarn
yarn install
```

主要依赖包括：
- Vue 3.5.34 - 前端框架
- Vite 8.0.12 - 构建工具
- Element Plus 2.14.0 - UI组件库
- Pinia 3.0.4 - 状态管理
- Vue Router 5.0.7 - 路由管理
- Axios 1.16.1 - HTTP客户端

### 5.2 配置API地址

编辑 `frontend/vite.config.js`：

```javascript
export default defineConfig({
  // ... 其他配置
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端API地址
        changeOrigin: true
      }
    }
  }
})
```

### 5.3 启动开发服务器

```bash
npm run dev
```

服务启动后访问：http://localhost:5173

### 5.4 生产构建

```bash
# 构建生产版本
npm run build

# 构建产物在 dist/ 目录
# 可以将 dist/ 目录部署到Nginx等Web服务器
```

### 5.5 预览生产版本

```bash
npm run preview
```

## 6. 完整启动流程

### 6.1 一键启动脚本（开发环境）

创建 `start.sh`（Linux/macOS）或 `start.bat`（Windows）：

**Linux/macOS (start.sh):**
```bash
#!/bin/bash

echo "启动数据库..."
# 确保PostgreSQL已启动

echo "启动后端服务..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &

echo "启动前端服务..."
cd ../frontend
npm run dev &

echo "服务启动完成！"
echo "前端: http://localhost:5173"
echo "后端: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
```

**Windows (start.bat):**
```batch
@echo off
echo 启动后端服务...
cd backend
call venv\Scripts\activate
start "Backend" uvicorn app.main:app --reload --port 8000

echo 启动前端服务...
cd ..\frontend
start "Frontend" npm run dev

echo 服务启动完成！
pause
```

### 6.2 手动启动顺序

1. 启动PostgreSQL数据库
2. 启动后端服务（端口8000）
3. 启动前端服务（端口5173）

## 7. 常见问题

### 7.1 数据库连接失败

**错误信息:** `could not connect to server`

**解决方案:**
1. 检查PostgreSQL服务是否启动
   ```bash
   # Windows
   net start postgresql-x64-14
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```

2. 检查数据库配置是否正确
   - 确认用户名、密码、主机、端口、数据库名

3. 检查防火墙设置
   - 确保5432端口未被阻止

### 7.2 后端启动失败

**错误信息:** `ModuleNotFoundError`

**解决方案:**
```bash
# 确保在虚拟环境中
cd backend
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

**错误信息:** `relation "users" does not exist`

**解决方案:**
```bash
# 执行数据库初始化脚本
psql -U postgres -d stock_forum -f sql/init.sql
```

### 7.3 前端启动失败

**错误信息:** `npm ERR! code EACCES`

**解决方案:**
```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install
```

**错误信息:** `Cannot connect to backend API`

**解决方案:**
1. 确认后端服务已启动（http://localhost:8000）
2. 检查vite.config.js中的代理配置
3. 确认端口8000未被占用

### 7.4 端口被占用

**解决方案:**
```bash
# 查找占用端口的进程
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# macOS/Linux
lsof -i :8000
lsof -i :5173

# 杀死进程（替换PID）
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

或修改配置文件使用其他端口：
- 后端: 修改启动命令的 `--port` 参数
- 前端: 修改 `vite.config.js` 添加 `port: 3000`

### 7.5 JWT Token过期

**现象:** 登录后一段时间操作提示未授权

**解决方案:**
修改 `backend/app/config.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7天
# 或更长时间
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # 30天
```

重启后端服务生效。

## 8. 生产环境部署

### 8.1 后端部署

**使用Gunicorn + Uvicorn:**
```bash
# 安装gunicorn
pip install gunicorn

# 启动（4个worker）
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**使用Docker:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.2 前端部署

**使用Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 8.3 安全配置

1. **修改SECRET_KEY:**
   ```python
   SECRET_KEY = "your-strong-random-secret-key"
   ```

2. **配置CORS:**
   ```python
   CORS_ORIGINS = ["https://your-domain.com"]
   ```

3. **启用HTTPS:**
   - 使用Nginx反向代理配置SSL证书
   - 或使用Let's Encrypt免费证书

4. **数据库安全:**
   - 使用强密码
   - 限制数据库访问IP
   - 定期备份数据

## 9. 性能优化

### 9.1 数据库优化

1. **创建索引:**
   ```sql
   -- init.sql已包含常用索引
   CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   ```

2. **连接池配置:**
   ```python
   # backend/app/database.py
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=40,
       pool_pre_ping=True
   )
   ```

### 9.2 后端优化

1. **启用缓存:**
   - 使用Redis缓存热点数据
   - 配置适当的缓存过期时间

2. **异步处理:**
   - 使用异步数据库驱动: asyncpg
   - 使用异步HTTP客户端: httpx

### 9.3 前端优化

1. **代码分割:**
   ```javascript
   // vite.config.js
   build: {
     rollupOptions: {
       output: {
         manualChunks: {
           'element-plus': ['element-plus'],
           'vue-vendor': ['vue', 'vue-router', 'pinia']
         }
       }
     }
   }
   ```

2. **启用Gzip:**
   ```nginx
   # Nginx配置
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

## 10. 监控与日志

### 10.1 后端日志

```python
# backend/app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 10.2 健康检查

```bash
# 检查后端服务
curl http://localhost:8000/api/health

# 检查数据库连接
psql -U postgres -d stock_forum -c "SELECT 1"
```

## 11. 备份与恢复

### 11.1 数据库备份

```bash
# 备份整个数据库
pg_dump -U postgres stock_forum > backup_$(date +%Y%m%d).sql

# 备份特定表
pg_dump -U postgres -t users stock_forum > users_backup.sql
```

### 11.2 数据库恢复

```bash
# 恢复数据库
psql -U postgres -d stock_forum < backup_20240101.sql
```

## 12. 技术支持

如遇到安装问题，请提供以下信息：
1. 操作系统版本
2. Python/Node.js版本
3. PostgreSQL版本
4. 完整的错误日志
5. 已尝试的解决方案

---

**文档版本:** 1.0  
**最后更新:** 2024-01-01  
**维护者:** 股票基金投资论坛开发团队
