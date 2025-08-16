{{ config(
    materialized='view',
    alias='agriculture_metric_top3_irrigation_avg_yield'
) }}

WITH irrigation_yield AS (
    SELECT
        irrigation_type,
        ROUND(AVG(yield_tons), 4) AS avg_yield_tons
    FROM {{ ref('fact_farm_production') }}
    GROUP BY irrigation_type
)

SELECT
    irrigation_type,
    avg_yield_tons
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY avg_yield_tons DESC) AS rn
    FROM irrigation_yield
) ranked
WHERE rn <= 3
ORDER BY avg_yield_tons DESC
