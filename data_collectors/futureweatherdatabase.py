import requests
from datetime import datetime
from sqlalchemy import create_engine, text
from config import DB_CONFIG

API_KEY = DB_CONFIG['Weather_KEY']
LAT, LON = 53.3498, -6.2603  
API_URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude=current,minutely,alerts&appid={API_KEY}&units=metric"

connection_string = f"mysql+pymysql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['FUTURE_DB']}"
engine = create_engine(connection_string, echo=True)

def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def insert_hourly_weather(hourly_data):
    hourly_insert = text("""
    INSERT INTO hourly_weather (dt, temp, feels_like, pressure, humidity, dew_point, uvi, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_id, weather_main, weather_desc, weather_icon, pop)
    VALUES (:dt, :temp, :feels_like, :pressure, :humidity, :dew_point, :uvi, :clouds, :visibility, :wind_speed, :wind_deg, :wind_gust, :weather_id, :weather_main, :weather_desc, :weather_icon, :pop)
    ON DUPLICATE KEY UPDATE 
    temp=VALUES(temp), feels_like=VALUES(feels_like), pressure=VALUES(pressure), humidity=VALUES(humidity),
    dew_point=VALUES(dew_point), uvi=VALUES(uvi), clouds=VALUES(clouds), visibility=VALUES(visibility),
    wind_speed=VALUES(wind_speed), wind_deg=VALUES(wind_deg), wind_gust=VALUES(wind_gust),
    weather_id=VALUES(weather_id), weather_main=VALUES(weather_main), weather_desc=VALUES(weather_desc),
    weather_icon=VALUES(weather_icon), pop=VALUES(pop);
    """)

    try:
        with engine.connect() as conn:
            with conn.begin():
                for hourly in hourly_data:
                    hourly_vals = {
                        "dt": datetime.utcfromtimestamp(hourly["dt"]),
                        "temp": hourly["temp"],
                        "feels_like": hourly["feels_like"],
                        "pressure": hourly["pressure"],
                        "humidity": hourly["humidity"],
                        "dew_point": hourly.get("dew_point", None),
                        "uvi": hourly.get("uvi", None),
                        "clouds": hourly["clouds"],
                        "visibility": hourly.get("visibility", None),
                        "wind_speed": hourly["wind_speed"],
                        "wind_deg": hourly["wind_deg"],
                        "wind_gust": hourly.get("wind_gust", None),
                        "weather_id": hourly["weather"][0]["id"],
                        "weather_main": hourly["weather"][0]["main"],
                        "weather_desc": hourly["weather"][0]["description"],
                        "weather_icon": hourly["weather"][0]["icon"],
                        "pop": hourly.get("pop", 0),
                    }
                    conn.execute(hourly_insert, hourly_vals)

        print("Hourly data inserted successfully!")
    except Exception as e:
        print(f"Hourly database insert failed: {e}")

def insert_daily_weather(daily_data):
    daily_insert = text("""
    INSERT INTO daily_weather (dt, sunrise, sunset, moonrise, moonset, moon_phase, summary, temp_day, temp_min, temp_max, temp_night, temp_eve, temp_morn, feels_like_day, feels_like_night, feels_like_eve, feels_like_morn, pressure, humidity, dew_point, clouds, wind_speed, wind_deg, wind_gust, weather_id, weather_main, weather_desc, weather_icon, pop, rain, uvi)
    VALUES (:dt, :sunrise, :sunset, :moonrise, :moonset, :moon_phase, :summary, :temp_day, :temp_min, :temp_max, :temp_night, :temp_eve, :temp_morn, :feels_like_day, :feels_like_night, :feels_like_eve, :feels_like_morn, :pressure, :humidity, :dew_point, :clouds, :wind_speed, :wind_deg, :wind_gust, :weather_id, :weather_main, :weather_desc, :weather_icon, :pop, :rain, :uvi)
    ON DUPLICATE KEY UPDATE 
    temp_day=VALUES(temp_day), temp_min=VALUES(temp_min), temp_max=VALUES(temp_max), temp_night=VALUES(temp_night),
    temp_eve=VALUES(temp_eve), temp_morn=VALUES(temp_morn), feels_like_day=VALUES(feels_like_day),
    feels_like_night=VALUES(feels_like_night), feels_like_eve=VALUES(feels_like_eve), feels_like_morn=VALUES(feels_like_morn),
    pressure=VALUES(pressure), humidity=VALUES(humidity), dew_point=VALUES(dew_point), clouds=VALUES(clouds),
    wind_speed=VALUES(wind_speed), wind_deg=VALUES(wind_deg), wind_gust=VALUES(wind_gust),
    weather_id=VALUES(weather_id), weather_main=VALUES(weather_main), weather_desc=VALUES(weather_desc),
    weather_icon=VALUES(weather_icon), pop=VALUES(pop), rain=VALUES(rain), uvi=VALUES(uvi);
    """)

    try:
        with engine.connect() as conn:
            with conn.begin():
                for daily in daily_data:
                    daily_vals = {
                        "dt": datetime.utcfromtimestamp(daily["dt"]),
                        "sunrise": datetime.utcfromtimestamp(daily["sunrise"]),
                        "sunset": datetime.utcfromtimestamp(daily["sunset"]),
                        "moonrise": datetime.utcfromtimestamp(daily["moonrise"]) if daily.get("moonrise") else None,
                        "moonset": datetime.utcfromtimestamp(daily["moonset"]) if daily.get("moonset") else None,
                        "moon_phase": daily["moon_phase"],
                        "summary": daily.get("summary", ""),
                        "temp_day": daily["temp"]["day"],
                        "temp_min": daily["temp"]["min"],
                        "temp_max": daily["temp"]["max"],
                        "temp_night": daily["temp"]["night"],
                        "temp_eve": daily["temp"]["eve"],
                        "temp_morn": daily["temp"]["morn"],
                        "feels_like_day": daily["feels_like"]["day"],
                        "feels_like_night": daily["feels_like"]["night"],
                        "feels_like_eve": daily["feels_like"]["eve"],
                        "feels_like_morn": daily["feels_like"]["morn"],
                        "pressure": daily["pressure"],
                        "humidity": daily["humidity"],
                        "dew_point": daily["dew_point"],
                        "clouds": daily["clouds"],
                        "wind_speed": daily["wind_speed"],
                        "wind_deg": daily["wind_deg"],
                        "wind_gust": daily.get("wind_gust", None),
                        "weather_id": daily["weather"][0]["id"],
                        "weather_main": daily["weather"][0]["main"],
                        "weather_desc": daily["weather"][0]["description"],
                        "weather_icon": daily["weather"][0]["icon"],
                        "pop": daily.get("pop", 0),
                        "rain": daily.get("rain", None),  
                        "uvi": daily.get("uvi", 0),
                    }
                    conn.execute(daily_insert, daily_vals)

        print("Daily data inserted successfully!")
    except Exception as e:
        print(f"Daily database insert failed: {e}")

def main():
    data = fetch_data()
    if data:
        insert_hourly_weather(data.get("hourly", []))
        insert_daily_weather(data.get("daily", []))

if __name__ == "__main__":
    main()

