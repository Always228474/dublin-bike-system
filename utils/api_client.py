"""
API客户端模块 - 统一管理外部API调用
"""
import requests
from config import DB_CONFIG
from datetime import datetime
import random


class APIClient:
    """API客户端管理器"""
    
    def __init__(self):
        self.jcdecaux_key = DB_CONFIG['API_KEY']
        self.weather_key = DB_CONFIG['Weather_KEY']
        self.contract_name = "dublin"
        self.lat, self.lon = 53.3498, -6.2603
        
    def get_bike_stations(self):
        """获取自行车站点数据"""
        try:
            url = f"https://api.jcdecaux.com/vls/v1/stations?contract={self.contract_name}&apiKey={self.jcdecaux_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取自行车站点数据失败: {e}")
            return None
    
    def get_current_weather(self):
        """获取当前天气数据"""
        try:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self.lat}&lon={self.lon}&exclude=minutely,hourly,daily,alerts&appid={self.weather_key}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取天气数据失败: {e}")
            return None
    
    def get_weather_forecast(self):
        """获取天气预报数据"""
        try:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self.lat}&lon={self.lon}&exclude=current,minutely,hourly,alerts&appid={self.weather_key}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取天气预报失败: {e}")
            return None
    
    def get_simulated_weather_features(self):
        """获取模拟天气特征（当API不可用时）"""
        # 模拟都柏林4月份的典型天气
        base_temp = 12  # 都柏林4月平均温度
        temp_variation = random.uniform(-3, 3)
        avg_temp = base_temp + temp_variation
        temp_range = random.uniform(2, 8)  # 日温差
        temp_std = random.uniform(0.5, 2.0)  # 温度标准差
        wind_speed = random.uniform(2, 15)  # 风速
        
        return {
            'avg_temp': avg_temp,
            'temp_range': temp_range,
            'temp_std': temp_std,
            'wind_speed': wind_speed
        }


# 全局API客户端实例
api_client = APIClient()
