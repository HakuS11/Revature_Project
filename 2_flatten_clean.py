import json
import os
import pandas as pd

files = [
    "data/mesa_raw.json",
    "data/tokyo_raw.json",
    "data/london_raw.json"
]

records = []

for file in files:
    with open(file, "r") as f:
        data = json.load(f)

    city = data["city"]
    daily = data["daily"]

    for i in range(len(daily["time"])):
        row = {
            "city": city,
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "precipitation_sum": daily["precipitation_sum"][i],
            "windspeed_max": daily["windspeed_10m_max"][i]
        }
        records.append(row)

df = pd.DataFrame(records)

print(df.head())
print(df.info())

df["date"] = pd.to_datetime(df["date"])

print(df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())

df.to_csv("data/weather_flat.csv", index=False)

print("Saved data/weather_flat.csv")