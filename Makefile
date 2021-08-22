dev-server:
	poetry run python manage.py runserver 8080

test:
	poetry run python3 manage.py test task_manager/tests