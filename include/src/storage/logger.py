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