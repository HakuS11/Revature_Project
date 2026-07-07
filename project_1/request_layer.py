import requests
import json
from pathlib import Path


URL = "https://archive-api.open-meteo.com/v1/archive"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Cities and with their latitude and longitude that will be analyzed
# Used in the next for loop for params
CITIES = [
    {"name": "Mesa", "latitude": 33.42227, "longitude": -111.82264},
    {"name": "Tokyo", "latitude": 35.6895, "longitude": 139.69171},
    {"name": "London", "latitude": 51.50853, "longitude": -0.12574}
]


def run_request_layer():
    DATA_DIR.mkdir(exist_ok=True)

    for city in CITIES:
        # URL parameters to call the API for specific info
        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
            "temperature_unit": "fahrenheit",
            "timezone": "auto"
        }

        try:
            # Make API request for each city and also catch errors
            response = requests.get(URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            data["city"] = city["name"]

            # Save raw data into JSON based on city name
            filename = DATA_DIR / f"{city['name'].lower()}_raw.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)

            print(f"Saved {filename}")

        # Throw exception if request fails
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city['name']}: {e}")


if __name__ == "__main__":
    run_request_layer()