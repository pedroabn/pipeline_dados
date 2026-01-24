import pandas as pd
from google.cloud import storage
import io

def upload_dataframe_as_parquet(df, bucket_name, destination_blob_name):
    """
    Converte um DataFrame para Parquet e faz o upload para o GCS.
    Esta função encapsula a complexidade da biblioteca oficial.
    """
    # 1. Inicializa o cliente do GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # 2. Converte o DataFrame para o formato Parquet em memória (buffer)
    # O formato Parquet é escolhido pela alta compressão e performance no BigQuery
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)

    # 3. Realiza o upload para o caminho especificado
    blob.upload_from_file(buffer, content_type='application/octet-stream')
    
    print(f"Dados ingeridos com sucesso em: gs://{bucket_name}/{destination_blob_name}")

# Exemplo de uso seguindo o padrão da Camada Bronze do seu projeto:
# Caminho sugerido: bronze/platform=meta_ads/date=2025-01-22/dados.parquet
data = {'campanha_id': [1, 2], 'cliques': [100, 200]}
df_marketing = pd.DataFrame(data)

upload_dataframe_as_parquet(
    df=df_marketing,
    bucket_name="seu-bucket-bronze",
    destination_blob_name="bronze/platform=meta_ads/date=2025-01-22/data.parquet"
)

"""
Ingestão de dados do Meta Ads (Facebook/Instagram)
Coleta métricas de campanhas ativas
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import pandas as pd
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

import sys
sys.path.insert(0, '/usr/local/airflow/include')
from config.settings import get_settings


class MetaAdsClient:
    """Cliente para API do Meta Ads"""
    
    def __init__(self):
        settings = get_settings()
        
        # Inicializa API do Meta
        FacebookAdsApi.init(
            access_token=settings.meta_ads_access_token,
            api_version=settings.meta_ads_api_version
        )
        
        self.account_id = settings.meta_ads_account_id
        self.account = AdAccount(f'act_{self.account_id}')
    
    def get_campaigns_insights(
        self, 
        start_date: str,
        end_date: Optional[str] = None,
        level: str = 'campaign'
    ) -> pd.DataFrame:
        """
        Busca insights de campanhas do Meta Ads
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD), default = start_date
            level: Nível de agregação (campaign, adset, ad)
        
        Returns:
            DataFrame com métricas das campanhas
        """
        if end_date is None:
            end_date = start_date
        
        # Campos que queremos buscar
        fields = [
            # Identificação
            'campaign_id',
            'campaign_name',
            'adset_id',
            'adset_name',
            'ad_id',
            'ad_name',
            
            # Objetivo e status
            'objective',
            'status',
            
            # Métricas de performance
            'impressions',
            'reach',
            'frequency',
            'clicks',
            'ctr',
            'cpc',
            'cpm',
            'cpp',
            
            # Investimento
            'spend',
            
            # Conversões
            'actions',
            'action_values',
            'conversions',
            'conversion_values',
            
            # Engajamento
            'post_engagements',
            'post_reactions',
            'comments',
            'shares',
            
            # Vídeo (se aplicável)
            'video_views',
            'video_avg_time_watched_actions',
        ]
        
        # Parâmetros da consulta
        params = {
            'time_range': {
                'since': start_date,
                'until': end_date
            },
            'level': level,
            'filtering': [
                {
                    'field': 'campaign.effective_status',
                    'operator': 'IN',
                    'value': ['ACTIVE', 'PAUSED']  # Apenas campanhas ativas ou pausadas
                }
            ],
            'breakdowns': ['publisher_platform', 'device_platform'],
            'time_increment': 1,  # Dados diários
        }
        
        print(f"🔄 Buscando dados do Meta Ads: {start_date} a {end_date}")
        
        # Faz a requisição
        try:
            insights = self.account.get_insights(
                fields=fields,
                params=params
            )
            
            # Converte para lista de dicionários
            data = []
            for insight in insights:
                row = insight.export_all_data()
                
                # Processa conversões (vem como lista de dicts)
                row = self._process_conversions(row)
                
                data.append(row)
            
            print(f"✅ {len(data)} linhas coletadas")
            
            # Converte para DataFrame
            df = pd.DataFrame(data)
            
            if df.empty:
                print("⚠️  Nenhum dado encontrado para o período")
                return pd.DataFrame()
            
            # Limpa e padroniza
            df = self._clean_dataframe(df, start_date)
            
            return df
            
        except Exception as e:
            print(f"❌ Erro ao buscar dados do Meta Ads: {e}")
            raise
    
    def _process_conversions(self, row: Dict) -> Dict:
        """Processa campo de conversões que vem como lista"""
        
        # Conversões
        if 'actions' in row and row['actions']:
            for action in row['actions']:
                action_type = action.get('action_type', '')
                value = action.get('value', 0)
                row[f'action_{action_type}'] = value
        
        # Valores de conversões
        if 'action_values' in row and row['action_values']:
            for action in row['action_values']:
                action_type = action.get('action_type', '')
                value = action.get('value', 0)
                row[f'action_value_{action_type}'] = value
        
        # Remove campos originais (já processados)
        row.pop('actions', None)
        row.pop('action_values', None)
        
        return row
    
    def _clean_dataframe(self, df: pd.DataFrame, date: str) -> pd.DataFrame:
        """Limpa e padroniza o DataFrame"""
        
        # Adiciona metadados
        df['ingestion_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['data_date'] = date
        df['source'] = 'meta_ads'
        
        # Converte tipos
        numeric_cols = [
            'impressions', 'reach', 'frequency', 'clicks', 
            'spend', 'conversions', 'post_engagements'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Padroniza nomes de colunas
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Garante que IDs são strings
        id_cols = ['campaign_id', 'adset_id', 'ad_id']
        for col in id_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
        
        return df
    
    def get_active_campaigns(self) -> List[Dict]:
        """Retorna lista de campanhas ativas"""
        
        campaigns = self.account.get_campaigns(
            fields=['id', 'name', 'status', 'objective', 'effective_status'],
            params={'effective_status': ['ACTIVE']}
        )
        
        return [c.export_all_data() for c in campaigns]


def ingest_meta_ads(execution_date: str, save_to: str = '/tmp') -> str:
    """
    Função principal de ingestão
    
    Args:
        execution_date: Data de execução (YYYY-MM-DD)
        save_to: Pasta para salvar o arquivo
    
    Returns:
        Caminho do arquivo salvo
    """
    print("="*60)
    print("🚀 INICIANDO INGESTÃO META ADS")
    print("="*60)
    
    # Inicializa cliente
    client = MetaAdsClient()
    
    # Busca dados
    df = client.get_campaigns_insights(
        start_date=execution_date,
        level='campaign'  # ou 'adset' ou 'ad'
    )
    
    if df.empty:
        print("⚠️  DataFrame vazio, nada para salvar")
        return None
    
    # Salva em Parquet
    output_path = f"{save_to}/meta_ads_{execution_date}.parquet"
    df.to_parquet(output_path, index=False, engine='pyarrow')
    
    print(f"✅ Dados salvos em: {output_path}")
    print(f"📊 Total de linhas: {len(df)}")
    print(f"📊 Total de colunas: {len(df.columns)}")
    print("="*60)
    
    return output_path


# Para testar localmente
if __name__ == "__main__":
    from datetime import date
    
    # Data de ontem
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Executa ingestão
    file_path = ingest_meta_ads(execution_date=yesterday)
    
    if file_path:
        # Mostra preview
        df = pd.read_parquet(file_path)
        print("\n📋 Preview dos dados:")
        print(df.head())
        print(f"\n📊 Shape: {df.shape}")
        print(f"\n📋 Colunas: {df.columns.tolist()}")