# Nomes de schemas BigQuery
BRONZE_SCHEMA = "bronze_external"
SILVER_SCHEMA = "marketing_silver"
GOLD_SCHEMA = "marketing_gold"

# Paths GCS
GCS_BRONZE_PATH_TEMPLATE = "bronze/platform={platform}/date={date}/"

# Configurações de retenção
BRONZE_RETENTION_DAYS = 90
LOGS_RETENTION_DAYS = 30