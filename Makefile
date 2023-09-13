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
	docker exec -it app alembic downgrade base
	docker exec -it app alembic upgrade head


new_game:
	make reset_db
	make start_monopoly_cli

test:
	docker-compose exec -T app pytest
