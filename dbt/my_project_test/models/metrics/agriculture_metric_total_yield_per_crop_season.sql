{{ config(
    materialized='view',
    alias='agriculture_metric_total_yield_per_crop_season'
) }}

SELECT
    crop_type,
    season,
    SUM(yield_tons) AS total_yield_tons
FROM {{ ref('fact_farm_production') }}
GROUP BY crop_type, season
ORDER BY crop_type, season