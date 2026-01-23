FROM apache/airflow:2.8.1-python3.11

USER root
RUN apt-get update && apt-get install -y git

USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copia código do projeto
COPY --chown=airflow:airflow src/ /opt/airflow/src/
COPY --chown=airflow:airflow config/ /opt/airflow/config/