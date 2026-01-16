marketing-data-pipeline/
│
├── README.md
├── .gitignore                         # ⭐ CRÍTICO: adicionar .env aqui
├── .env.example                       # ⭐ Template versionado no Git
├── .env                               # ⭐ NUNCA comitar (secrets reais)
├── .env.dev                           # ⭐ Ambiente local
├── .env.prod                          # ⭐ Ambiente produção (não comitar)
│
├── pyproject.toml
├── Makefile
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml             # ⭐ Carrega .env automaticamente
│
├── config/
│   ├── __init__.py
│   ├── settings.py                    # ⭐ Classe que lê .env
│   └── validators.py                  # Valida secrets obrigatórios
│
├── airflow/
│   ├── dags/
│   │   └── marketing_pipeline_dag.py
│   │
│   ├── plugins/
│   └── airflow.cfg                    # ⭐ Referencia variáveis do .env
│
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── base_client.py             # Classe base reutilizável
│   │   ├── meta_ads.py                # API Meta Ads → DataFrame
│   │   └── ga4.py                     # API GA4 → DataFrame
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── cleaner.py                 # Limpeza (nulls, duplicatas)
│   │   ├── transformer.py             # Transformações Silver
│   │   └── validator.py               # Validação Pydantic
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   │
│   │   ├── gcs_manager.py             # Upload Silver → GCS
│   │   │
│   │   └── bigquery_manager.py        # (Opcional) Helpers BigQuery
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── exceptions.py
│
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml                   # Usa .env
│   │
│   ├── models/
│   │   ├── sources/
│   │   │   └── _sources.yml           # GCS como source externo
│   │   │
│   │   ├── silver/                    # Views sobre GCS
│   │   │   ├── _silver__models.yml
│   │   │   ├── stg_campaigns.sql
│   │   │   └── stg_ga4_events.sql
│   │   │
│   │   ├── gold/                      # Tabelas BigQuery
│   │   │   ├── _gold__models.yml
│   │   │   ├── campaign_performance.sql
│   │   │   └── audience_performance.sql
│   │   │
│   │   └── marts/                     # Looker Studio
│   │       └── looker_campaign_dashboard.sql
│   │
│   ├── tests/
│   │   └── not_null_tests.yml
│   │
│   └── macros/
│       └── marketing_metrics.sql
│
├── tests/
│   ├── conftest.py                    # ⭐ Carrega .env.test
│   ├── .env.test                      # ⭐ Credenciais fake para testes
│   ├── test_ingestion.py
│   └── test_processing.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb     # ⭐ Carrega .env no primeiro cell
│
└── alert/
    ├── setup/
    │   └── validate_env.py            # ⭐ Script para validar .env
    │
    ├── backfill.py
    └── manual_run.py