import psycopg2
from util.db_util import get_conn_string

with psycopg2.connect(get_conn_string()) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Connected to database. Version: {db_version[0]}")