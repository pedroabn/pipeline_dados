# Makefile - Marketing Data Pipeline
# Comandos úteis para desenvolvimento e operação

.PHONY: help setup install test validate-env clean docker-up docker-down dbt-run dbt-test format lint run-pipeline backup

# ============================================
# HELP - Lista todos os comandos disponíveis
# ============================================
help:
	@echo "=========================================="
	@echo "Marketing Data Pipeline - Comandos"
	@echo "=========================================="
	@echo ""
	@echo "📦 SETUP:"
	@echo "  make setup          - Setup completo do projeto"
	@echo "  make install        - Instala dependências Python"
	@echo "  make validate-env   - Valida arquivo .env"
	@echo ""
	@echo "🧪 TESTES:"
	@echo "  make test           - Roda todos os testes"
	@echo "  make test-unit      - Roda apenas testes unitários"
	@echo "  make test-integration - Roda testes de integração"
	@echo "  make coverage       - Gera relatório de cobertura"
	@echo ""
	@echo "🐳 DOCKER:"
	@echo "  make docker-up      - Sobe containers (Airflow + Postgres)"
	@echo "  make docker-down    - Para containers"
	@echo "  make docker-logs    - Mostra logs dos containers"
	@echo "  make docker-rebuild - Rebuilda imagens Docker"
	@echo ""
	@echo "📊 DBT:"
	@echo "  make dbt-run        - Executa modelos DBT"
	@echo "  make dbt-test       - Roda testes DBT"
	@echo "  make dbt-docs       - Gera documentação DBT"
	@echo "  make dbt-clean      - Limpa artifacts DBT"
	@echo ""
	@echo "🚀 PIPELINE:"
	@echo "  make run-pipeline   - Executa pipeline completo"
	@echo "  make run-ingestion  - Apenas ingestão de dados"
	@echo "  make run-processing - Apenas processamento"
	@echo ""
	@echo "🛠️  UTILS:"
	@echo "  make format         - Formata código (black + isort)"
	@echo "  make lint           - Verifica qualidade do código"
	@echo "  make clean          - Remove arquivos temporários"
	@echo "  make gcs-lifecycle  - Configura lifecycle GCS (90 dias)"
	@echo ""

# ============================================
# SETUP - Configuração inicial
# ============================================
setup:
	@echo "🔧 Configurando projeto..."
	@echo ""
	@echo "1️⃣  Criando arquivo .env..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "   ✅ .env criado (EDITE COM SUAS CREDENCIAIS!)"; \
	else \
		echo "   ℹ️  .env já existe"; \
	fi
	@echo ""
	@echo "2️⃣  Instalando dependências..."
	$(MAKE) install
	@echo ""
	@echo "3️⃣  Validando configurações..."
	$(MAKE) validate-env
	@echo ""
	@echo "✅ Setup concluído!"
	@echo ""
	@echo "📝 Próximos passos:"
	@echo "   1. Edite o arquivo .env com suas credenciais"
	@echo "   2. Execute: make validate-env"
	@echo "   3. Execute: make docker-up"
	@echo "   4. Acesse Airflow: http://localhost:8080"

install:
	@echo "📦 Instalando dependências..."
	pip install --upgrade pip
	pip install -e .
	@echo "✅ Dependências instaladas"

validate-env:
	@echo "🔍 Validando arquivo .env..."
	python scripts/setup/validate_env.py

# ============================================
# TESTES
# ============================================
test:
	@echo "🧪 Rodando todos os testes..."
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

test-unit:
	@echo "🧪 Rodando testes unitários..."
	pytest tests/unit/ -v

test-integration:
	@echo "🧪 Rodando testes de integração..."
	pytest tests/integration/ -v

coverage:
	@echo "📊 Gerando relatório de cobertura..."
	pytest tests/ --cov=src --cov-report=html
	@echo "✅ Relatório disponível em: htmlcov/index.html"
	@echo "   Abra com: open htmlcov/index.html (Mac) ou xdg-open htmlcov/index.html (Linux)"

# ============================================
# DOCKER
# ============================================
docker-up:
	@echo "🐳 Subindo containers Docker..."
	docker-compose -f docker/docker-compose.yml up -d
	@echo "✅ Containers iniciados"
	@echo ""
	@echo "📊 Airflow Web UI: http://localhost:8080"
	@echo "   User: airflow"
	@echo "   Password: airflow"

docker-down:
	@echo "🛑 Parando containers..."
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	@echo "📋 Logs dos containers..."
	docker-compose -f docker/docker-compose.yml logs -f

docker-rebuild:
	@echo "🔨 Rebuilding Docker images..."
	docker-compose -f docker/docker-compose.yml build --no-cache
	docker-compose -f docker/docker-compose.yml up -d

# ============================================
# DBT
# ============================================
dbt-run:
	@echo "📊 Executando modelos DBT..."
	cd dbt && dbt run --target dev

dbt-test:
	@echo "🧪 Rodando testes DBT..."
	cd dbt && dbt test --target dev

dbt-docs:
	@echo "📚 Gerando documentação DBT..."
	cd dbt && dbt docs generate && dbt docs serve

dbt-clean:
	@echo "🧹 Limpando artifacts DBT..."
	cd dbt && dbt clean

# ============================================
# PIPELINE
# ============================================
run-pipeline:
	@echo "🚀 Executando pipeline completo..."
	@echo ""
	@echo "1️⃣  Ingestão de dados..."
	python -m src.ingestion.meta_ads
	python -m src.ingestion.ga4
	@echo ""
	@echo "2️⃣  Processamento e upload GCS..."
	python -m src.processing.run_processing
	@echo ""
	@echo "3️⃣  Transformação DBT..."
	$(MAKE) dbt-run
	@echo ""
	@echo "✅ Pipeline concluído!"

run-ingestion:
	@echo "📥 Executando apenas ingestão..."
	python -m src.ingestion.meta_ads
	python -m src.ingestion.ga4

run-processing:
	@echo "⚙️  Executando processamento..."
	python -m src.processing.run_processing

# ============================================
# QUALIDADE DE CÓDIGO
# ============================================
format:
	@echo "🎨 Formatando código..."
	black src/ tests/
	isort src/ tests/
	@echo "✅ Código formatado"

lint:
	@echo "🔍 Verificando qualidade do código..."
	@echo ""
	@echo "1️⃣  Ruff (linting)..."
	ruff check src/ tests/
	@echo ""
	@echo "2️⃣  MyPy (type checking)..."
	mypy src/ --ignore-missing-imports
	@echo ""
	@echo "✅ Verificação concluída"

# ============================================
# UTILS
# ============================================
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -rf dbt/target/ dbt/dbt_packages/ dbt/logs/
	@echo "✅ Limpeza concluída"

gcs-lifecycle:
	@echo "⏰ Configurando lifecycle policy GCS (90 dias)..."
	python scripts/setup/setup_gcs_lifecycle.py
	@echo "✅ Lifecycle configurado"

# ============================================
# BACKFILL
# ============================================
backfill:
	@echo "⏮️  Executando backfill..."
	@read -p "Data inicial (YYYY-MM-DD): " start_date; \
	read -p "Data final (YYYY-MM-DD): " end_date; \
	python scripts/backfill.py --start-date $$start_date --end-date $$end_date

# ============================================
# CI/CD (usado em GitHub Actions)
# ============================================
ci-test:
	@echo "🔄 CI: Rodando testes..."
	pytest tests/ -v --cov=src --cov-report=xml

ci-lint:
	@echo "🔄 CI: Verificando código..."
	ruff check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/