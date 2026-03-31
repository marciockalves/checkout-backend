# Variáveis
DC = docker compose
UV = uv run
ALEMBIC = $(UV) alembic

.PHONY: help up down build ps logs shell-db migrate-gen migrate-up migrate-down test-products

help: ## Mostra os comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- DOCKER ---
up: ## Sobe os containers (Banco de Dados) em background
	$(DC) up -d

down: ## Para e remove os containers
	$(DC) down

build: ## Reconstrói os containers
	$(DC) build

ps: ## Lista os containers ativos
	$(DC) ps

logs: ## Exibe os logs dos containers
	$(DC) logs -f

# --- DATABASE / MIGRATIONS ---
migrate-gen: ## Gera uma nova migração (Ex: make migrate-gen m="nome_da_migracao")
	$(ALEMBIC) revision --autogenerate -m "$(m)"

migrate-up: ## Aplica as migrações no banco de dados
	$(ALEMBIC) upgrade head

migrate-down: ## Reverte a última migração
	$(ALEMBIC) downgrade -1

shell-db: ## Entra no terminal interativo do Postgres
	$(DC) exec db psql -U postgres -d checkout_db

# --- DEV ---
run: ## Inicia o servidor FastAPI em modo de desenvolvimento (uvicorn)
	$(UV) uvicorn app.main:app --reload --host 0.0.0.1 --port 8000

install: ## Instala as dependências usando o uv
	uv sync