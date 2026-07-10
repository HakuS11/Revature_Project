-- Largest temperature gap and average daily temperature recorded per city
SELECT c.city_name, MAX(wr.temp_max - wr.temp_min) AS largest_temp_gap, AVG(wr.temp_max - wr.temp_min) AS avg_daily_temp_gap
FROM weather.weather_records wr
JOIN weather.cities c
ON wr.city_id = c.city_id
GROUP BY c.city_name
ORDER BY largest_temp_gap DESC;

-- Most precipitation
SELECT c.city_name, MAX(wr.precipitation_sum) AS highest_precipitation
FROM weather.weather_records wr
JOIN weather.cities c
ON wr.city_id = c.city_id
GROUP BY c.city_name
ORDER BY highest_precipitation DESC;

-- Count of days above 100 degrees per city
SELECT c.city_name, COUNT(*) AS extreme_heat_days
FROM weather.weather_records wr
JOIN weather.cities c
ON wr.city_id = c.city_id
WHERE wr.temp_max >= 100
GROUP BY c.city_name
ORDER BY extreme_heat_days DESC;

-- Number of rainy days per city
SELECT c.city_name, COUNT(*) AS rainy_days
FROM weather.weather_records wr
JOIN weather.cities c
ON wr.city_id = c.city_id
WHERE wr.precipitation_sum > 0
GROUP BY c.city_name
ORDER BY rainy_days DESC;

-- Number of dry days per city
SELECT c.city_name, COUNT(*) AS dry_days
FROM weather.weather_records wr
JOIN weather.cities c
ON wr.city_id = c.city_id
WHERE wr.precipitation_sum = 0
GROUP BY c.city_name
ORDER BY dry_days DESC;