{{ config(
    materialized='view',
    alias='agriculture_metric_water_productivity_per_crop'
) }}

SELECT
    crop_type,
    SUM(yield_tons) AS total_yield_tons,
    SUM(water_usage_m3) AS total_water_m3,
    ROUND(SUM(yield_tons) / NULLIF(SUM(water_usage_m3), 0), 6) AS water_productivity
FROM {{ ref('fact_farm_production') }}
GROUP BY crop_type
ORDER BY water_productivity DESC
