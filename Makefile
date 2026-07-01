.PHONY: install run test lint format check docker-build docker-up

install:
	python -m pip install -r requirements-dev.txt

run:
	python run.py

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff check . --fix
	python -m ruff format .

check:
	python -m ruff check .
	python -m ruff format --check .
	python -m pytest

docker-build:
	docker build -t python-api-code-design .

docker-up:
	docker compose up --build
