# 📊 Marketing Data Pipeline – Campaign Intelligence Platform

Este projeto documenta e implementa a construção de um **pipeline de dados para marketing digital**, com foco em **análise de campanhas ativas**, **segmentação de públicos** e **modelagem de probabilidade de sucesso de campanhas**, utilizando dados oriundos das APIs do **Meta Ads** e **Google Analytics 4 (GA4)**.

O objetivo central é transformar dados brutos de plataformas de mídia em **insights acionáveis**, por meio de uma arquitetura enxuta, escalável e de baixo custo, adequada para **pequenas e médias empresas de marketing**.

---

## 🎯 Objetivo do Projeto

* Automatizar a ingestão diária de dados de campanhas **ativas**
* Tratar e padronizar dados antes do armazenamento em nuvem
* Criar uma base analítica confiável para:

  * comparação de públicos
  * análise de performance por campanha
  * modelagem preditiva de probabilidade de sucesso
* Disponibilizar dashboards atualizados automaticamente no **Looker Studio**

---

## 🧠 Conceito de Negócio

> Uma única ingestão diária consolida todas as campanhas ativas, evitando duplicações, reduzindo custos e permitindo análises comparativas entre públicos e campanhas ao longo do tempo.

---

## 🏗️ Arquitetura Geral

```text
Meta Ads API / GA4 API
        ↓
Ingestão Python (Docker)
        ↓
Tratamento e Validação (Local)
        ↓
Camada Silver (GCS – retenção 90 dias)
        ↓
Modelagem Analítica (dbt)
        ↓
Camada Gold (BigQuery)
        ↓
Looker Studio (Dashboards automáticos)
```

---

## 🧱 Camadas de Dados

### 🔹 Bronze (não persistida)

* Dados brutos coletados via API
* Existência apenas em memória (DataFrame)
* Usada exclusivamente para tratamento inicial

---

### 🔹 Silver (Google Cloud Storage)

* Dados tratados, padronizados e enriquecidos
* Armazenados em **Parquet**
* Retenção de **90 dias**
* Particionados por data e plataforma

```text
gs://<bucket-name>/silver/
 └── platform=meta_ads/
     └── date=YYYY-MM-DD/
         └── data.parquet
```

---

### 🔹 Gold (BigQuery)

* Dados consolidados para análise e visualização
* Métricas de marketing calculadas
* Base para dashboards e modelos preditivos

Exemplo de estrutura:

```text
date
campaign_id
campaign_name
audience
spend
clicks
conversions
ctr
cpa
roas
performance_score
```

---

## 🔄 Orquestração e Execução

### Estratégia Atual

* Execução **diária**
* Pode ser realizada via:

  * Airflow em Docker (opcional)
  * Cloud Scheduler + script Python
* Foco em **baixo custo operacional**

### Importante

* **Não existe uma DAG por campanha**
* Todas as campanhas ativas são processadas em uma única execução

---

## 📈 Critério de Campanhas Ativas

### Meta Ads

* `status = ACTIVE`
* `effective_status = ACTIVE`

### GA4

* Campanhas com eventos/métricas > 0 no período

---

## 📊 Visualização (Looker Studio)

* Conexão direta com **BigQuery**
* Atualização automática após cada execução do pipeline
* Dashboards focados em:

  * performance por campanha
  * comparação de públicos
  * evolução temporal
  * suporte à tomada de decisão em campanhas sazonais (ex.: Black Friday)

---

## 🔮 Modelagem Preditiva (Gold)

O projeto permite a aplicação de modelos como:

* Regressão logística
* Scoring de performance
* Probabilidade de sucesso da campanha X com público Y

Exemplo de pergunta respondida:

> “Qual a chance dessa campanha performar bem com este público?”

---

## 🧪 Ferramentas Utilizadas

* **Python** (ingestão, tratamento e modelagem)
* **Docker** (replicabilidade do ambiente)
* **dbt** (transformações e métricas analíticas)
* **Google Cloud Storage** (camada Silver)
* **BigQuery** (camada Gold)
* **Looker Studio** (visualização)
* **.env** (segurança de credenciais)

---

## 💰 Considerações de Custo

* Arquitetura desenhada para custar **menos de R$ 40/mês**
* Airflow não é obrigatório
* Armazenamento e consultas otimizadas
* Escalável para múltiplos clientes sem crescimento linear de custos

---

## 🚀 Diferencial do Projeto

✔ Foco em marketing real
✔ Pipeline simples, porém profissional
✔ Baixo custo
✔ Escalável
✔ Pronto para venda como produto ou serviço

---

## 📌 Próximos Passos

* Evoluir modelo preditivo
* Automatizar feature engineering
* Criar templates de dashboards por tipo de cliente
* Adicionar alertas de performance

---

## 📄 Licença

Projeto acadêmico e experimental – MBA em Marketing
Uso educacional e demonstrativo.
