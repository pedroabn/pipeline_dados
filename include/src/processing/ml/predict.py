import joblib
import pandas as pd
from google.cloud import bigquery

def predict_campaign_success(execution_date: str):
    """Gera predições para campanhas ativas"""
    
    # 1. Carrega modelo do GCS
    from src.storage.gcs_manager import GCSManager
    gcs = GCSManager('seu-bucket-models')
    model_path = gcs.download_file('models/campaign_scorer_v1.pkl', '/tmp/')
    model = joblib.load(model_path)
    
    # 2. Carrega campanhas ativas
    client = bigquery.Client()
    query = f"""
        SELECT * 
        FROM `marketing_silver.int_campaigns_unified`
        WHERE date = '{execution_date}'
    """
    df = client.query(query).to_dataframe()
    
    # 3. Prepara features (mesmo processo do treinamento)
    X = df[['objective', 'platform', 'budget_daily', 'ctr']]
    X = pd.get_dummies(X, columns=['objective', 'platform'])
    
    # 4. Gera predições
    df['predicted_success_prob'] = model.predict_proba(X)[:, 1]
    df['predicted_class'] = model.predict(X)
    
    # 5. Salva predições no BigQuery
    predictions = df[['date', 'campaign_id', 'predicted_success_prob', 'predicted_class']]
    predictions.to_gbq(
        destination_table='marketing_gold.ml_predictions',
        project_id='seu-projeto',
        if_exists='append'
    )