{{ config(
    materialized='view',
    alias='agriculture_metric_yield_per_acre_per_crop'
) }}

SELECT
    crop_type,
    SUM(yield_tons) AS total_yield_tons,
    SUM(farm_area_acres) AS total_area_acres,
    ROUND(SUM(yield_tons) / NULLIF(SUM(farm_area_acres), 0), 2) AS yield_per_acre
FROM {{ ref('fact_farm_production') }}
GROUP BY crop_type
ORDER BY yield_per_acre DESC
