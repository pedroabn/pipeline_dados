# config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    Configurações centralizadas do projeto.
    Lê automaticamente do .env e valida os valores.
    """
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'  # Ignora variáveis extras
    )
    
    # ============================================
    # CONFIGURAÇÕES GERAIS
    # ============================================
    environment: str = Field(default='dev', description='Ambiente de execução')
    project_name: str = Field(default='marketing-data-pipeline')
    log_level: str = Field(default='INFO')
    
    # ============================================
    # META ADS
    # ============================================
    meta_ads_access_token: str = Field(..., description='Token de acesso Meta Ads')
    meta_ads_account_id: str = Field(..., description='ID da conta Meta Ads')
    meta_ads_api_version: str = Field(default='v18.0')
    
    # ============================================
    # GOOGLE ANALYTICS 4
    # ============================================
    ga4_property_id: str = Field(..., description='Property ID do GA4')
    ga4_credentials_path: Optional[str] = None
    ga4_credentials_json: Optional[str] = None
    
    @validator('ga4_credentials_path', 'ga4_credentials_json')
    def validate_ga4_credentials(cls, v, values):
        """Garante que pelo menos uma forma de credencial existe"""
        if not values.get('ga4_credentials_path') and not values.get('ga4_credentials_json'):
            raise ValueError('Forneça ga4_credentials_path OU ga4_credentials_json')
        return v
    
    # ============================================
    # GOOGLE CLOUD PLATFORM
    # ============================================
    gcp_project_id: str = Field(..., description='GCP Project ID')
    gcp_region: str = Field(default='us-central1')
    gcp_credentials_path: Optional[str] = None
    
    # BigQuery
    bq_dataset_bronze: str = Field(default='marketing_bronze')
    bq_dataset_silver: str = Field(default='marketing_silver')
    bq_dataset_gold: str = Field(default='marketing_gold')
    
    # Cloud Storage
    gcs_bucket_raw: str = Field(..., description='Bucket para dados raw')
    gcs_bucket_processed: str = Field(..., description='Bucket para dados processados')
    gcs_retention_days: int = Field(default=90)
    
    # ============================================
    # AIRFLOW
    # ============================================
    airflow__core__executor: str = Field(default='LocalExecutor')
    airflow__core__sql_alchemy_conn: str = Field(
        default='postgresql+psycopg2://airflow:airflow@postgres:5432/airflow'
    )
    airflow__core__fernet_key: Optional[str] = None
    airflow__webserver__secret_key: Optional[str] = None
    
    # ============================================
    # ALERTAS
    # ============================================
    slack_webhook_url: Optional[str] = None
    slack_channel: str = Field(default='#data-alerts')
    
    # ============================================
    # OUTROS
    # ============================================
    timezone: str = Field(default='America/Sao_Paulo')
    retry_max_attempts: int = Field(default=3)
    retry_delay_seconds: int = Field(default=60)
    
    @validator('environment')
    def validate_environment(cls, v):
        """Valida ambiente"""
        allowed = ['dev', 'staging', 'prod']
        if v not in allowed:
            raise ValueError(f'Environment deve ser um de: {allowed}')
        return v
    
    @property
    def is_production(self) -> bool:
        """Checa se está em produção"""
        return self.environment == 'prod'
    
    @property
    def is_development(self) -> bool:
        """Checa se está em desenvolvimento"""
        return self.environment == 'dev'


# ============================================
# SINGLETON - Instância única
# ============================================
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Retorna instância única de Settings"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Atalho para importação fácil
settings = get_settings()