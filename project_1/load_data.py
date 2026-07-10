import json
from pathlib import Path

import pandas as pd

from dao.city_dao import CityDAO
from dao.weather_dao import WeatherDAO

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

JSON_FILES = [
    DATA_DIR / "mesa_raw.json",
    DATA_DIR / "tokyo_raw.json",
    DATA_DIR / "london_raw.json",
]

CSV_FILE = DATA_DIR / "weather_flat.csv"


def load_weather_data():
    city_dao = CityDAO()
    weather_dao = WeatherDAO()

    # Insert cities first from raw JSON so latitude and longitude are included
    for file_path in JSON_FILES:
        with open(file_path, "r") as f:
            data = json.load(f)

        city_name = data["city"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        city_dao.insert_city(city_name, latitude, longitude)

    city_id_map = city_dao.get_city_id_map()

    # Load cleaned weather rows from CSV
    df = pd.read_csv(CSV_FILE)

    for _, row in df.iterrows():
        city_id = city_id_map[row["city"]]

        weather_dao.insert_weather_record(
            city_id,
            row["date"],
            row["temp_max"],
            row["temp_min"],
            row["precipitation_sum"],
            row["windspeed_max"]
        )


if __name__ == "__main__":
    load_weather_data()
    print("Loaded cities and weather records.")