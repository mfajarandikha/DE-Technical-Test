{{ config(
    materialized='view',
    alias='agriculture_metric_top3_crops_yield_per_acre'
) }}

WITH crop_yield AS (
    SELECT
        crop_type,
        SUM(yield_tons) AS total_yield_tons,
        SUM(farm_area_acres) AS total_area_acres,
        ROUND(SUM(yield_tons) / NULLIF(SUM(farm_area_acres), 0), 4) AS yield_per_acre
    FROM {{ ref('fact_farm_production') }}
    GROUP BY crop_type
)

SELECT
    crop_type,
    total_yield_tons,
    total_area_acres,
    yield_per_acre
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY yield_per_acre DESC) AS rn
    FROM crop_yield
) ranked
WHERE rn <= 3
ORDER BY yield_per_acre DESC
