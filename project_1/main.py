from create_schema import run_schema
from request_layer import run_request_layer
from flatten_clean import run_flatten_clean
from load_data import load_weather_data


def main():
    run_schema()
    run_request_layer()
    run_flatten_clean()
    load_weather_data()
    print("Data pipeline complete.")


if __name__ == "__main__":
    main()