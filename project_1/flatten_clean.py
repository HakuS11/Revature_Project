import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "weather_flat.csv"


def run_flatten_clean():
    json_files = [
        DATA_DIR / "mesa_raw.json",
        DATA_DIR / "tokyo_raw.json",
        DATA_DIR / "london_raw.json",
    ]

    all_rows = []

    for file_path in json_files:
        with open(file_path, "r") as f:
            data = json.load(f)

        city_name = data["city"]
        daily = data["daily"]

        dates = daily["time"]
        temp_maxes = daily["temperature_2m_max"]
        temp_mins = daily["temperature_2m_min"]
        precipitation_sums = daily["precipitation_sum"]
        windspeed_maxes = daily["windspeed_10m_max"]

        for i in range(len(dates)):
            all_rows.append({
                "city": city_name,
                "date": dates[i],
                "temp_max": temp_maxes[i],
                "temp_min": temp_mins[i],
                "precipitation_sum": precipitation_sums[i],
                "windspeed_max": windspeed_maxes[i],
            })

    df = pd.DataFrame(all_rows)

    # Drop rows with null values
    df = df.dropna()

    # Drop duplicate rows based on city and date
    df = df.drop_duplicates(subset=["city", "date"])

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved cleaned, flattened data to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_flatten_clean()