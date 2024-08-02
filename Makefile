.PHONY: help api_run build up down migrate gen_migration install app restart_api generate_certs

help:
	@echo "Available commands:"
	@echo "  api_run        - Run the Uvicorn server"
	@echo "  build          - Build the Docker containers"
	@echo "  up             - Start Docker containers"
	@echo "  down           - Stop Docker containers"
	@echo "  migrate        - Run database migrations"
	@echo "  gen_migration  - Generate new database migrations"
	@echo "  install        - Install dependencies using Poetry"
	@echo "  app            - Start Docker containers and run Uvicorn server"
	@echo "  restart_api    - Restart the Uvicorn server"
	@echo "  generate_certs - Generate JWT certificates"

api_run:
	uvicorn cryptoapp.main.web:create_app --host 0.0.0.0 --port 8000 --reload --factory

build:
	docker-compose up --build -d

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	alembic upgrade head

gen_migration:
	@echo "Enter migration message: "; \
	read MESSAGE; \
	alembic revision --autogenerate -m "$$MESSAGE"

install:
	pip install poetry
	poetry install

restart_api:
	@echo "Killing process on port 8000 (if any)..."; \
	PID=$$(lsof -t -i :8000); \
	if [ ! -z "$$PID" ]; then kill -9 $$PID; fi; \
	echo "Restarting Uvicorn server..."; \
	uvicorn --factory app.main:create_app


