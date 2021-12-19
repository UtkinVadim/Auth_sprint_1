.PHONY: env dbs down

env:
	cp .env.template .env

dbs:
	docker compose up postgres_auth -d --build
	docker compose up redis_auth -d --build
	docker exec -it postgres_auth psql -U postgres

down:
	docker compose down

init_db:
	cd src && alembic upgrade head

migrations:
	cd src && alembic revision --autogenerate

run:
	cd src && python run.py

run_debug:
	cd src && python run.py -d
