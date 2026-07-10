-- Largest temperature gap and average daily temperature recorded per city
WITH gap_stats AS (
    SELECT
        wr.city_id,
        MAX(wr.temp_max - wr.temp_min) AS largest_temp_gap,
        AVG(wr.temp_max - wr.temp_min) AS avg_daily_temp_gap
    FROM weather.weather_records wr
    GROUP BY wr.city_id
),
gap_days AS (
    SELECT
        wr.city_id,
        wr.weather_date,
        (wr.temp_max - wr.temp_min) AS temp_gap,
        ROW_NUMBER() OVER (
            PARTITION BY wr.city_id
            ORDER BY (wr.temp_max - wr.temp_min) DESC
        ) AS rn
    FROM weather.weather_records wr
)
SELECT
    c.city_name,
    gs.avg_daily_temp_gap,
	gs.largest_temp_gap,
    gd.weather_date AS largest_gap_date
FROM gap_stats gs
JOIN gap_days gd
    ON gs.city_id = gd.city_id
   AND gd.rn = 1
JOIN weather.cities c
    ON gs.city_id = c.city_id
ORDER BY gs.largest_temp_gap DESC;

-- Most precipitation
-- Most precipitation per city, with date
WITH max_rain AS (
    SELECT
        wr.city_id,
        MAX(wr.precipitation_sum) AS highest_precipitation
    FROM weather.weather_records wr
    GROUP BY wr.city_id
),
rain_days AS (
    SELECT
        wr.city_id,
        wr.weather_date,
        wr.precipitation_sum,
        ROW_NUMBER() OVER (
            PARTITION BY wr.city_id
            ORDER BY wr.precipitation_sum DESC
        ) AS rn
    FROM weather.weather_records wr
)
SELECT
    c.city_name,
    mr.highest_precipitation,
    rd.weather_date AS highest_precipitation_date
FROM max_rain mr
JOIN rain_days rd
    ON mr.city_id = rd.city_id
   AND rd.rn = 1
JOIN weather.cities c
    ON mr.city_id = c.city_id
ORDER BY mr.highest_precipitation DESC;

-- Count of days above 100 degrees per city
WITH heat_counts AS (
    SELECT
        wr.city_id,
        COUNT(*) AS extreme_heat_days
    FROM weather.weather_records wr
    WHERE wr.temp_max >= 100
    GROUP BY wr.city_id
),
hottest_days AS (
    SELECT
        wr.city_id,
        wr.weather_date,
        wr.temp_max,
        ROW_NUMBER() OVER (
            PARTITION BY wr.city_id
            ORDER BY wr.temp_max DESC
        ) AS rn
    FROM weather.weather_records wr
)
SELECT
    c.city_name,
    hc.extreme_heat_days,
    hd.weather_date AS hottest_day,
    hd.temp_max     AS hottest_temp
FROM heat_counts hc
JOIN hottest_days hd
    ON hc.city_id = hd.city_id
   AND hd.rn = 1
JOIN weather.cities c
    ON hc.city_id = c.city_id
ORDER BY hc.extreme_heat_days DESC, hd.temp_max DESC;

-- Number of rainy days per city
SELECT
    c.city_name,
    COUNT(*) AS rainy_days,
    SUM(wr.precipitation_sum) AS total_annual_precipitation,
    AVG(wr.precipitation_sum) AS avg_rain_per_rainy_day
FROM weather.weather_records wr
JOIN weather.cities c
    ON wr.city_id = c.city_id
WHERE wr.precipitation_sum > 0
GROUP BY c.city_name
ORDER BY total_annual_precipitation DESC;


-- Number of dry days per city
SELECT
    c.city_name,
    SUM(CASE WHEN wr.precipitation_sum = 0 THEN 1 ELSE 0 END) AS dry_days,
    ROUND(
        100.0 * SUM(CASE WHEN wr.precipitation_sum = 0 THEN 1 ELSE 0 END)
        / COUNT(*),
        1
    ) AS dry_day_percent
FROM weather.weather_records wr
JOIN weather.cities c
    ON wr.city_id = c.city_id
GROUP BY c.city_name
ORDER BY dry_day_percent DESC;