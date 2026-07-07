CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    latitude NUMERIC(8,4),
    longitude NUMERIC(8,4)
);

CREATE TABLE IF NOT EXISTS weather_records (
    record_id SERIAL PRIMARY KEY,
    city_id INT NOT NULL REFERENCES cities(city_id),
    weather_date DATE NOT NULL,
    temp_max NUMERIC(5,2),
    temp_min NUMERIC(5,2),
    precipitation_sum NUMERIC(8,2),
    windspeed_max NUMERIC(6,2),
    UNIQUE (city_id, weather_date)
);