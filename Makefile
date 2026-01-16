# Makefile

.PHONY: test dbt-run validate docker-up format

test:
	pytest tests/ -v --cov=src --cov-report=html

dbt-run:
	cd dbt && dbt run --target prod

validate:
	python scripts/setup/validate_env.py

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

format:
	black src/ && isort src/ && ruff check src/