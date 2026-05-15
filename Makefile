.PHONY: install dev test lint format typecheck check docker-build docker-up

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app tests

check: lint typecheck test

docker-build:
	docker build -t fastapi-python-monolithic-boilerplate .

docker-up:
	docker compose up --build
