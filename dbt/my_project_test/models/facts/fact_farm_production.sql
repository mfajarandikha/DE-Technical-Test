{{ config(
    materialized='table',
    alias='fact_farm_production'
) }}

SELECT 
    "Farm_ID" AS farm_id,
    "Crop_Type" AS crop_type,
    "Farm_Area(acres)" AS farm_area_acres,
    "Irrigation_Type" AS irrigation_type,
    "Fertilizer_Used(tons)" AS fertilizer_used_tons,
    "Pesticide_Used(kg)" AS pesticide_used_kg,
    "Yield(tons)" AS yield_tons,
    "Soil_Type" AS soil_type,
    "Season" AS season,
    "Water_Usage(cubic meters)" AS water_usage_m3
FROM {{ source('dev', 'stg_farm_productions') }}
