COMPOSE_DEV = docker compose --env-file .env -f infra/compose.dev.yaml

db-up:
	$(COMPOSE_DEV) up -d

db-down:
	$(COMPOSE_DEV) down

db-ps:
	$(COMPOSE_DEV) ps -a

db-shell:
	$(COMPOSE_DEV) exec db /bin/bash

db-psql:
	$(COMPOSE_DEV) exec db sh -c 'psql -U "$$DB_ADMIN_USER" -d "$$DB_NAME"'
