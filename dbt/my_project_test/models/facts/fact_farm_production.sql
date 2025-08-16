{{ config(
    materialized='table',
    alias='fact_farm_production'
) }}

SELECT 
    "Farm_ID" AS farm_id,
    "Crop_Type" AS crop_type,
    "Farm_Area(acres)"::numeric AS farm_area_acres,
    "Irrigation_Type" AS irrigation_type,
    "Fertilizer_Used(tons)"::numeric AS fertilizer_used_tons,
    "Pesticide_Used(kg)"::numeric AS pesticide_used_kg,
    "Yield(tons)"::numeric AS yield_tons,
    "Soil_Type" AS soil_type,
    "Season" AS season,
    "Water_Usage(cubic meters)"::numeric AS water_usage_m3
FROM {{ source('dev', 'stg_farm_productions') }}    
