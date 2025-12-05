install:
	uv sync

migrate:
	uv run manage.py migrate

collectstatic:
	uv run manage.py collectstatic --no-input

setup:
	cp -n .env.example .env || true
	make install
	make collectstatic
	make migrate

start:
	uv run manage.py runserver 0.0.0.0:8000

lint:
	uv run ruff check .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=task_manager --cov-report=xml:coverage.xml

check: test lint


render-start:
	uv run gunicorn task_manager.wsgi


build:
	./build.sh

.PHONY: install migrate collectstatic setup start lint test test-coverage check render-start build
