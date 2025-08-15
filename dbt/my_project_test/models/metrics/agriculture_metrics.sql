{{ config(
    materialized='table',  
    alias='agriculture_metrics_daily'
) }}

WITH base AS (
    SELECT
        crop_type,
        season,
        SUM(yield_tons) AS total_yield,
        SUM(farm_area_acres) AS total_area,
        SUM(fertilizer_used_tons) AS total_fertilizer,
        SUM(water_usage_m3) AS total_water,
        irrigation_type,
        farm_id
    FROM {{ ref('fact_farm_production') }}
    GROUP BY crop_type, season, irrigation_type, farm_id
)

SELECT
    crop_type,
    season,
    SUM(total_yield) AS total_yield,
    SUM(total_yield)/SUM(total_area) AS yield_per_acre,
    SUM(total_yield)/SUM(total_fertilizer) AS fertilizer_efficiency,
    SUM(total_yield)/SUM(total_water) AS water_productivity
FROM base
GROUP BY crop_type, season
