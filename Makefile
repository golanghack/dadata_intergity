format:
	poetry run isort config/
	poetry run isort registration/
	poetry run isort devices/
check:
	poetry run isort config/
	poetry run isort registration/
	poetry run isort devices/
	
	poetry run ruff check config/
	poetry run ruff check registration/
	poetry run ruff check devices/
tests_python:
	poetry run pytest
test_coverage:
	poetry run pytest --cov
pre-commit:
	poetry run pre-commit run --all-files
health-check:
	poetry run python3 manage.py health_check
test_in_docker:
	docker-compose exec web poetry run pytest -v
