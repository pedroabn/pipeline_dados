{{
    config(
        materialized='view',
        tags=['staging', 'meta_ads']
    )
}}

WITH source AS (
    SELECT * FROM {{ source('gcs_bronze', 'meta_ads_raw') }}
),

cleaned AS (
    SELECT
        -- Identificadores
        CAST(campaign_id AS STRING) AS campaign_id,
        campaign_name,
        CAST(adset_id AS STRING) AS adset_id,
        adset_name,
        
        -- Data
        PARSE_DATE('%Y-%m-%d', data_date) AS data_date,
        
        -- Plataforma
        'meta_ads' AS platform,
        COALESCE(publisher_platform, 'unknown') AS publisher_platform,
        COALESCE(device_platform, 'unknown') AS device_platform,
        
        -- Status e Objetivo
        LOWER(status) AS status,
        LOWER(objective) AS objective,
        
        -- Métricas de Alcance
        CAST(impressions AS INT64) AS impressions,
        CAST(reach AS INT64) AS reach,
        CAST(COALESCE(frequency, 0) AS FLOAT64) AS frequency,
        
        -- Métricas de Engajamento
        CAST(clicks AS INT64) AS clicks,
        CAST(COALESCE(ctr, 0) AS FLOAT64) AS ctr,
        CAST(post_engagements AS INT64) AS post_engagements,
        
        -- Métricas Financeiras
        CAST(spend AS FLOAT64) AS spend,
        CAST(COALESCE(cpc, 0) AS FLOAT64) AS cpc,
        CAST(COALESCE(cpm, 0) AS FLOAT64) AS cpm,
        
        -- Conversões
        CAST(COALESCE(conversions, 0) AS INT64) AS conversions,
        CAST(COALESCE(conversion_values, 0) AS FLOAT64) AS conversion_value,
        
        -- Metadados
        CAST(ingestion_date AS TIMESTAMP) AS ingestion_timestamp,
        CURRENT_TIMESTAMP() AS dbt_updated_at
        
    FROM source
    WHERE data_date IS NOT NULL
      AND campaign_id IS NOT NULL
)

SELECT 
    *,
    -- Métricas Calculadas
    SAFE_DIVIDE(spend, NULLIF(clicks, 0)) AS calculated_cpc,
    SAFE_DIVIDE(clicks, NULLIF(impressions, 0)) * 100 AS calculated_ctr,
    SAFE_DIVIDE(spend, NULLIF(conversions, 0)) AS cpa,
    SAFE_DIVIDE(conversion_value, NULLIF(spend, 0)) AS roas
    
FROM cleaned