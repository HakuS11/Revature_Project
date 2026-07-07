import psycopg2
from psycopg2.extras import RealDictCursor
from util.db_util import get_conn_string


class CityDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def insert_city(self, city_name, latitude, longitude):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO weather.cities (city_name, latitude, longitude)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (city_name) DO NOTHING;
                    """,
                    (city_name, latitude, longitude)
                )

    def get_all_cities(self):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM weather.cities;")
                return cur.fetchall()
    
    def get_city_id_map(self):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT city_id, city_name FROM weather.cities;")
                rows = cur.fetchall()
                return {name: cid for cid, name in rows}