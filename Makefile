.PHONY: env dbs down

env:
	cp .env.template .env

dbs:
	docker compose up redis_auth -d --build
	docker compose up postgres_auth -d --build

down:
	docker compose down

