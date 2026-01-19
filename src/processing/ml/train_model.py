from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
from google.cloud import bigquery

def train_campaign_scorer():
    """Treina modelo para prever sucesso de campanhas"""
    
    # 1. Carrega dados históricos do BigQuery
    client = bigquery.Client()
    query = """
        SELECT 
            objective,
            platform,
            budget_daily,
            impressions,
            clicks,
            ctr,
            CASE WHEN roas >= 2.0 THEN 1 ELSE 0 END as success
        FROM `marketing_silver.int_campaigns_unified`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    """
    df = client.query(query).to_dataframe()
    
    # 2. Feature engineering
    X = df[['objective', 'platform', 'budget_daily', 'ctr']]
    X = pd.get_dummies(X, columns=['objective', 'platform'])
    y = df['success']
    
    # 3. Treina modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 4. Salva modelo no GCS
    model_path = '/tmp/campaign_scorer.pkl'
    joblib.dump(model, model_path)
    
    # Upload para GCS
    from src.storage.gcs_manager import GCSManager
    gcs = GCSManager('seu-bucket-models')
    gcs.upload_file(model_path, 'models/campaign_scorer_v1.pkl')
    
    print(f"Model trained with accuracy: {model.score(X, y):.2%}")