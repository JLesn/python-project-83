dev:
	poetry run flask --app page_analyzer:app run

dev-debug:
	flask --app page_analyzer --debug run

PORT ?= 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

reinstall:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_analyzer

build:
	./build.sh

psql-start:
	sudo service postgresql start
