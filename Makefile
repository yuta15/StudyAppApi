COMPOSE_DEV = docker compose --env-file .env -f infra/compose.dev.yaml

container-up:
	$(COMPOSE_DEV) up -d

container-down:
	$(COMPOSE_DEV) down

db-ps:
	$(COMPOSE_DEV) ps -a

db-shell:
	$(COMPOSE_DEV) exec db /bin/bash

db-psql:
	$(COMPOSE_DEV) exec db sh -c 'psql -U "$$DB_ADMIN_USER" -d "$$DB_NAME"'

db-seed-dev:
	$(COMPOSE_DEV) exec -T db sh -c 'psql -U "$$DB_ADMIN_USER" -d "$$DB_NAME"' < infra/db/seed/dev.sql


ALEMBIC_DEV = uv run --env-file .env alembic

migration-revision:
	$(ALEMBIC_DEV) revision --autogenerate -m "$(message)"

migration-upgrade:
	$(ALEMBIC_DEV) upgrade head

migration-downgrade:
	$(ALEMBIC_DEV) downgrade -1

migration-downgrade-specified-version:
	$(ALEMBIC_DEV) downgrade ${version}

migration-current:
	$(ALEMBIC_DEV) current

migration-history:
	$(ALEMBIC_DEV) history


PYTEST = uv run pytest --env-file .env 
unit-test:
	$(PYTEST) -svv

integration-test:
	$(PYTEST) -svv src/test/integration


dev:
	uv run --env-file .env fastapi dev src/app/main.py