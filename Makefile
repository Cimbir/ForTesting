install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install --no-root

lock:
	poetry lock

update:
	poetry update

format:
	poetry run ruff format finalproject tests
	poetry run ruff check finalproject tests --fix

lint:
	poetry run ruff check finalproject tests
	poetry run mypy finalproject tests
