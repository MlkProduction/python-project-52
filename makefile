compose-setup: compose-build compose-install

compose-build:
	docker compose build

compose-install:
	docker compose run app make install

compose-bash:
	docker compose run app bash

compose:
	docker compose up

compose-lint:
	docker compose run app make lint

compose-test:
	docker compose run app make test

install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

setup:
	cp -n .env.example .env || true
	make install
	make migrate
	make collectstatic

start:
	uv run python manage.py runserver 0.0.0.0:8000

lint:
	uv run ruff check .

test:
	uv run python manage.py test

check: test lint

test-coverage:
	uv run coverage run manage.py test task_manager
	uv run coverage html
	uv run coverage report

render-start:
	uv run python manage.py migrate
	uv run python manage.py collectstatic --noinput
	uv run -- gunicorn task_manager.wsgi

build:
	./build.sh