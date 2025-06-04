start:
	uvicorn src.main:app --reload --port 8000

lint:
	ruff check --fix

test:
	pytest -v

up:
	docker compose up

up-build:
	docker compose up --build

down:
	docker compose down -v

docker-alembic-upg:
	docker exec -it myclassapi-class_api-1 alembic upgrade head
