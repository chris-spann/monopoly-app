# add descriptions for each command
.PHONY:
	backend build install format lint \
	restart start start_monopoly_cli \
	stop reset_db new_game test

help:
	@echo "Makefile commands:"
	@echo "  build: build docker containers"
	@echo "  install: install dependencies"
	@echo "  format: format code"
	@echo "  lint: lint code"
	@echo "  new_game: start new game"
	@echo "  reset_db: reset database"
	@echo "  restart: restart docker containers"
	@echo "  start: start docker containers"
	@echo "  start_monopoly_cli: start monopoly cli"
	@echo "  stop: stop docker containers"
	@echo "  test: run tests"

backend:
	cd backend

build: backend
	docker-compose build

install:
	cd backend && pip install --upgrade pip &&\
		pip install poetry &&\
			poetry install

format:
	cd backend && poetry run black *.py

lint:
	cd backend && poetry run ruff check .

restart: backend
	docker-compose restart

start: backend
	docker-compose up -d --build

start_monopoly_cli:
	cd backend && poetry run python monopoly.py

stop: backend
	docker-compose down

reset_db: backend
	docker exec -it app alembic downgrade base
	docker exec -it app alembic upgrade head

new_game:
	make reset_db
	make start_monopoly_cli

test: backend
	docker exec -it app alembic downgrade base
	cd backend && poetry run pytest

test_cli: backend
	make start
	cd backend && poetry run pytest

# deploy:
# 	# deploy commands
# 	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 168495394202.dkr.ecr.us-east-1.amazonaws.com
# 	docker build -t micro .
# 	docker tag micro:latest 168495394202.dkr.ecr.us-east-1.amazonaws.com/micro:latest

# all: install lint format test deploy
