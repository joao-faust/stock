api\:run:
	fastapi dev ./app/main.py

reqs\:up:
	pip freeze > requirements.txt

migrate\:make:
	alembic revision --autogenerate -m "$(NAME)"
migrate\:down:
	alembic downgrade -1
migrate\:up:
	alembic upgrade head

style:
	ruff format ./app
style\:check:
	ruff format --check ./app
lint:
	ruff check ./app
lint\:fix:
	ruff check ./app --fix