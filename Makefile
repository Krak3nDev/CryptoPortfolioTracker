.PHONY: help api_run build up down migrate gen_migration install app restart_api generate_certs test_up

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
	@echo "  test_up        - Start Docker containers for testing environment"

api_run:
	uvicorn cryptoapp.main.web:create_app --host 0.0.0.0 --port 8000 --reload --factory

build:
	docker-compose up --build -d

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	cd backend && alembic upgrade head

test_up:
	docker-compose -f docker-compose-test.yml up -d
