import psycopg2
from util.db_util import get_conn_string


class WeatherDAO:
    def insert_weather_record(self, city_id, weather_date, temp_max, temp_min, precipitation_sum, windspeed_max):
        with psycopg2.connect(get_conn_string()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO weather.weather_records
                    (city_id, weather_date, temp_max, temp_min, precipitation_sum, windspeed_max)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (city_id, weather_date) DO NOTHING;
                    """,
                    (city_id, weather_date, temp_max, temp_min, precipitation_sum, windspeed_max)
                )
            conn.commit()