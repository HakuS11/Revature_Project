import psycopg2
from util.db_util import get_conn_string

def run_schema():
    with open("project_1/sql/schema.sql", "r") as f:
        schema_sql = f.read()

    with psycopg2.connect(get_conn_string()) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()

if __name__ == "__main__":
    run_schema()
    print("Schema created.")