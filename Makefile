install:
	poetry install

PORT ?= 8000
start:
        poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

reinstall:
	python3 -m pip install --user dist/*.whl --force-reinstall

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer
