dev:
	ENV=dev fastapi dev app/main.py

prod:
	ENV=prod fastapi run app/main.py

format:
	uv run ruff format .

lint:
	uv run ruff check .

fix:
	uv run ruff check . --fix