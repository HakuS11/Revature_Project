import json
from pathlib import Path

from dao.city_dao import CityDAO
from dao.weather_dao import WeatherDAO


BASE_DIR = Path(__file__).resolve().parent
JSON_FILES = [
    BASE_DIR / "data" / "mesa_raw.json",
    BASE_DIR / "data" / "tokyo_raw.json",
    BASE_DIR / "data" / "london_raw.json",
]


def load_weather_data():
    city_dao = CityDAO()
    weather_dao = WeatherDAO()

    # Insert cities first so weather records can reference city_id
    for file_path in JSON_FILES:
        with open(file_path, "r") as f:
            data = json.load(f)

        city_name = data["city"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        city_dao.insert_city(city_name, latitude, longitude)

    city_id_map = city_dao.get_city_id_map()

    # Insert weather records after city IDs are available
    for file_path in JSON_FILES:
        with open(file_path, "r") as f:
            data = json.load(f)

        city_name = data["city"]
        city_id = city_id_map[city_name]
        daily = data["daily"]

        dates = daily["time"]
        temp_maxes = daily["temperature_2m_max"]
        temp_mins = daily["temperature_2m_min"]
        precipitation_sums = daily["precipitation_sum"]
        windspeed_maxes = daily["windspeed_10m_max"]

        for i in range(len(dates)):
            weather_dao.insert_weather_record(
                city_id,
                dates[i],
                temp_maxes[i],
                temp_mins[i],
                precipitation_sums[i],
                windspeed_maxes[i]
            )


if __name__ == "__main__":
    load_weather_data()
    print("Loaded cities and weather records.")