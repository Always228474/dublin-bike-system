import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# === 设置路径 ===
file_path = "final_merged_data.csv"
model_dir = "models_with_weather"
os.makedirs(model_dir, exist_ok=True)

# === 加载数据（包含天气字段） ===
use_cols = ['last_reported', 'station_id',
            'num_bikes_available', 'num_docks_available',
            'max_air_temperature_celsius', 'min_air_temperature_celsius',
            'air_temperature_std_deviation']
df = pd.read_csv(file_path, usecols=use_cols)
df['last_reported'] = pd.to_datetime(df['last_reported'])

# === 时间特征 ===
df['hour'] = df['last_reported'].dt.hour
df['weekday'] = df['last_reported'].dt.weekday
df['is_weekend'] = df['weekday'].apply(lambda x: 1 if x >= 5 else 0)

# === 天气特征 ===
# 计算平均温度
df['avg_temp'] = (df['max_air_temperature_celsius'] + df['min_air_temperature_celsius']) / 2
# 温度范围
df['temp_range'] = df['max_air_temperature_celsius'] - df['min_air_temperature_celsius']
# 温度标准差
df['temp_std'] = df['air_temperature_std_deviation']

# 删除原始天气列，保留处理后的特征
weather_cols = ['max_air_temperature_celsius', 'min_air_temperature_celsius', 'air_temperature_std_deviation']
df = df.drop(columns=weather_cols)

# 删除包含NaN的行
df = df.dropna()

# === 获取站点列表 ===
station_ids = df['station_id'].unique()
print(f"共检测到 {len(station_ids)} 个站点")

# === 对每个站点训练模型 ===
for station_id in station_ids:
    df_station = df[df['station_id'] == station_id]
    if len(df_station) < 100:
        print(f"⏭️ 跳过站点 {station_id}（数据不足）")
        continue

    features = ['hour', 'weekday', 'is_weekend', 'avg_temp', 'temp_range', 'temp_std']
    targets = ['num_bikes_available', 'num_docks_available']

    X = df_station[features]
    y = df_station[targets]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae_bikes = mean_absolute_error(y_test['num_bikes_available'], y_pred[:, 0])
    mae_docks = mean_absolute_error(y_test['num_docks_available'], y_pred[:, 1])

    model_path = os.path.join(model_dir, f"model_station_{station_id}.pkl")
    joblib.dump(model, model_path)

    print(f"✅ 模型完成 - 站点 {station_id}（MAE: bikes={mae_bikes:.2f}, docks={mae_docks:.2f}）")

print(f"\n🎉 所有模型训练完成！模型保存在 {model_dir} 目录")
