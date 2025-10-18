"""
数据库连接和操作工具模块
"""
from sqlalchemy import create_engine, text
from config import DB_CONFIG


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.bikes_engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@"
            f"{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['BIKES_DB']}"
        )
        self.weather_engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@"
            f"{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['WEATHER_DB']}"
        )
        self.future_engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@"
            f"{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['FUTURE_DB']}"
        )
        self.user_engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@"
            f"{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['LOGIN_DB']}"
        )
    
    def get_engine(self, db_type):
        """获取指定类型的数据库引擎"""
        engines = {
            'bikes': self.bikes_engine,
            'weather': self.weather_engine,
            'future': self.future_engine,
            'user': self.user_engine
        }
        return engines.get(db_type, self.bikes_engine)


# 全局数据库管理器实例
db_manager = DatabaseManager()
