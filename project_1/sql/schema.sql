-- Create a dedicated schema for this project
CREATE SCHEMA IF NOT EXISTS weather;

-- Cities lookup table
CREATE TABLE IF NOT EXISTS weather.cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    latitude NUMERIC(8,4),
    longitude NUMERIC(8,4)
);

-- Daily weather table
CREATE TABLE IF NOT EXISTS weather.weather_records (
    record_id SERIAL PRIMARY KEY,
    city_id INT NOT NULL REFERENCES weather.cities(city_id) ON DELETE CASCADE,
    weather_date DATE NOT NULL,
    temp_max NUMERIC(5,2),
    temp_min NUMERIC(5,2),
    precipitation_sum NUMERIC(8,2),
    windspeed_max NUMERIC(6,2),
    UNIQUE (city_id, weather_date)
);