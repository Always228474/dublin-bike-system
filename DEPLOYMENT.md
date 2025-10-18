# 🚀 部署指南

## 📋 部署前准备

### 1. 环境要求
- Python 3.11+
- MySQL 8.0+
- 有效的API Keys:
  - JCDecaux API Key
  - OpenWeather API Key  
  - Google Maps API Key

### 2. 数据库设置
```sql
-- 创建数据库
CREATE DATABASE dublinbikes;
CREATE DATABASE dublinweather;
CREATE DATABASE futureweather;
CREATE DATABASE login;

-- 创建用户表
USE login;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

## 🔧 本地部署

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd dublin-bike-system
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp env_example.txt .env

# 编辑.env文件，填入真实API keys
nano .env
```

### 4. 运行数据收集器（可选）
```bash
# 收集自行车数据
python stationdatabase.py

# 收集天气数据
python currentweatherdatabase.py
python futureweatherdatabase.py
```

### 5. 训练机器学习模型
```bash
python train_with_weather.py
```

### 6. 启动Web应用
```bash
cd find-my-bicycle
python app.py
```

访问: http://localhost:5000

## ☁️ AWS EC2部署

### 1. 启动EC2实例
- 选择Ubuntu 20.04 LTS
- 实例类型: t2.micro (免费层)
- 安全组: 开放端口22(SSH), 80(HTTP), 443(HTTPS)

### 2. 连接并设置环境
```bash
# 连接EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python和依赖
sudo apt install python3-pip python3-venv -y
```

### 3. 部署应用
```bash
# 克隆项目
git clone <your-repo-url>
cd dublin-bike-system

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export JCDECAUX_API_KEY="your_key"
export OPENWEATHER_API_KEY="your_key"
export GOOGLE_MAPS_API_KEY="your_key"
export FLASK_SECRET_KEY="your_secret_key"
```

### 4. 配置Nginx（可选）
```bash
# 安装Nginx
sudo apt install nginx -y

# 创建配置文件
sudo nano /etc/nginx/sites-available/dublin-bike

# 配置内容
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 启用配置
sudo ln -s /etc/nginx/sites-available/dublin-bike /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. 使用PM2管理进程（推荐）
```bash
# 安装PM2
npm install -g pm2

# 创建PM2配置文件
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'dublin-bike',
    script: 'app.py',
    interpreter: 'python3',
    cwd: '/home/ubuntu/dublin-bike-system/find-my-bicycle',
    env: {
      JCDECAUX_API_KEY: 'your_key',
      OPENWEATHER_API_KEY: 'your_key',
      GOOGLE_MAPS_API_KEY: 'your_key',
      FLASK_SECRET_KEY: 'your_secret_key'
    }
  }]
}
EOF

# 启动应用
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 🔍 监控和维护

### 1. 查看日志
```bash
# PM2日志
pm2 logs dublin-bike

# Nginx日志
sudo tail -f /var/log/nginx/access.log
```

### 2. 重启服务
```bash
# 重启应用
pm2 restart dublin-bike

# 重启Nginx
sudo systemctl restart nginx
```

### 3. 更新应用
```bash
# 拉取最新代码
git pull origin main

# 重启应用
pm2 restart dublin-bike
```

## 🛡️ 安全建议

1. **使用HTTPS**: 配置SSL证书
2. **防火墙**: 只开放必要端口
3. **定期更新**: 保持系统和依赖最新
4. **监控**: 设置日志监控和告警
5. **备份**: 定期备份数据库和代码
