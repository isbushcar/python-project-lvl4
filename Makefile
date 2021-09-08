dev-server:
	poetry run python manage.py runserver 8080

test:
	poetry run python3 manage.py test task_manager/tests

makemigrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate