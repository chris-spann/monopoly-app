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

test:
	cd backend && poetry run pytest

# deploy:
# 	# deploy commands
# 	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 168495394202.dkr.ecr.us-east-1.amazonaws.com
# 	docker build -t micro .
# 	docker tag micro:latest 168495394202.dkr.ecr.us-east-1.amazonaws.com/micro:latest

# all: install lint format test deploy
