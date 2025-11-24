APP_DIR := hexlet-code
RUN := cd $(APP_DIR) && uv run
MANAGE := $(RUN) python manage.py

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
	$(MANAGE) migrate

collectstatic:
	$(MANAGE) collectstatic --noinput

setup:
	cp -n .env.example .env || true
	$(MAKE) install
	$(MAKE) migrate

start:
	$(MANAGE) runserver 0.0.0.0:8000

lint:
	uv run ruff check .

test:
	$(MANAGE) test

check: test lint

test-coverage:
	cd $(APP_DIR) && uv run coverage run manage.py test task_manager
	cd $(APP_DIR) && uv run coverage html
	cd $(APP_DIR) && uv run coverage report

render-start:
	cd $(APP_DIR) && uv run gunicorn task_manager.wsgi

build:
	./build.sh