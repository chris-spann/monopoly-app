backend:
	cd backend

build: backend
	docker-compose build

up: backend
	docker-compose up -d

down: backend
	docker-compose down

restart: backend
	docker-compose restart

start: backend
	docker-compose up -d --build

start_monopoly_cli:
	cd backend && poetry run python monopoly.py

reset_db: backend
	docker-compose down -v
	docker-compose up -d --build

