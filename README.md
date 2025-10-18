# 🚲 Dublin Bike System - 智能出行解决方案

**Dublin Bike System** 是一个基于机器学习的智能自行车共享系统，提供实时站点信息、天气预测和需求预测功能。帮助都柏林市民和游客更好地规划骑行出行。

## ✨ 主要功能

- **📍 实时站点地图**: 使用Google Maps API展示所有自行车站点，实时显示可用车辆和停车位
- **🌤️ 天气集成**: 集成OpenWeather API，提供当前天气和5天天气预报
- **🔮 智能预测**: 基于Random Forest机器学习模型，融合时间特征和天气因素预测站点可用性
- **📊 数据可视化**: 使用Chart.js展示历史数据和趋势分析
- **🗺️ 路线规划**: 集成Google Maps路线规划功能

## 🏗️ 技术架构

### 后端技术栈
- **Python 3.11+** - 主要开发语言
- **Flask 3.1.0** - Web框架
- **SQLAlchemy 2.0** - ORM数据库操作
- **MySQL** - 数据存储
- **scikit-learn** - 机器学习模型
- **pandas** - 数据处理

### 前端技术栈
- **HTML5/CSS3** - 页面结构和样式
- **JavaScript** - 交互逻辑
- **Google Maps API** - 地图服务
- **Chart.js** - 数据可视化

### 机器学习
- **Random Forest** - 回归预测模型
- **时间特征**: 小时、星期、周末标识
- **天气特征**: 平均温度、温度范围、温度标准差
- **多站点模型**: 为115个站点分别训练独立模型

## 📁 项目结构

```
dublin-bike-system/
├── find-my-bicycle/              # Flask Web应用
│   ├── app.py                   # 主应用文件
│   ├── requirements.txt         # Python依赖
│   ├── templates/               # HTML模板
│   └── static/                  # 静态资源
├── data_collectors/              # 数据收集器
│   ├── stationdatabase.py       # 自行车数据收集
│   ├── currentweatherdatabase.py # 当前天气数据
│   ├── futureweatherdatabase.py  # 天气预报数据
│   └── train_with_weather.py     # 模型训练脚本
├── data/                        # 数据文件
│   ├── final_merged_data.csv    # 训练数据
│   └── bikestation.ipynb       # 数据分析
├── utils/                       # 工具模块
│   ├── database.py             # 数据库管理
│   └── api_client.py           # API客户端
├── models_with_weather/         # 训练模型
├── config.py                    # 配置文件
└── env_example.txt             # 环境变量示例
```

## 🚀 快速开始

### 1. 环境要求
- Python 3.11+
- MySQL 8.0+
- 有效的API Keys:
  - JCDecaux API Key
  - OpenWeather API Key
  - Google Maps API Key

### 2. 安装依赖
```bash
# 克隆项目
git clone <your-repo-url>
cd dublin-bike-system

# 进入应用目录
cd find-my-bicycle

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp ../env_example.txt .env

# 编辑.env文件，填入真实API keys
nano .env
```

环境变量配置：
```env
JCDECAUX_API_KEY=你的JCDecaux API key
OPENWEATHER_API_KEY=你的OpenWeather API key
GOOGLE_MAPS_API_KEY=你的Google Maps API key
DB_PASSWORD=你的数据库密码
FLASK_SECRET_KEY=你的Flask密钥
```

### 4. 数据库设置
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

### 5. 运行应用
```bash
# 启动Flask应用
python app.py

# 访问应用
open http://localhost:5000
```

## 📊 数据收集和模型训练

### 数据收集
```bash
# 收集自行车数据
python ../data_collectors/stationdatabase.py

# 收集天气数据
python ../data_collectors/currentweatherdatabase.py
python ../data_collectors/futureweatherdatabase.py
```

### 模型训练
```bash
# 训练带天气特征的模型
python ../data_collectors/train_with_weather.py
```

## 🔐 安全配置

### API Key管理
1. **永远不要**将`.env`文件提交到Git
2. **使用环境变量**管理敏感信息
3. **定期轮换**API keys
4. **配置.gitignore**防止敏感信息泄露

### 生产环境部署
```bash
# 设置环境变量
export JCDECAUX_API_KEY="your_key"
export OPENWEATHER_API_KEY="your_key"
export GOOGLE_MAPS_API_KEY="your_key"
export FLASK_SECRET_KEY="your_secret_key"
```

## 🧪 API测试

```bash
# 测试站点API
curl http://localhost:5000/api/stations

# 测试天气API
curl http://localhost:5000/api/weather

# 测试预测API
curl "http://localhost:5000/predict?station_id=42&date=2025-04-10&time=10:30"
```

## 📈 机器学习模型

### 特征工程
- **时间特征**: 小时、星期、周末标识
- **天气特征**: 平均温度、温度范围、温度标准差
- **目标变量**: 可用自行车数量、可用停车位数量

### 模型性能
- **算法**: Random Forest回归
- **评估指标**: MAE (Mean Absolute Error)
- **模型数量**: 115个站点独立模型
- **准确率**: MAE控制在2-7辆之间

## 🚀 部署指南

### AWS EC2部署
1. 启动EC2实例
2. 安装Python和依赖
3. 配置环境变量
4. 使用PM2管理进程
5. 配置Nginx反向代理

详细部署说明请参考 [DEPLOYMENT.md](DEPLOYMENT.md)


Made with ❤️ for Dublin cyclists! 🚴‍♀️🚴‍♂️
