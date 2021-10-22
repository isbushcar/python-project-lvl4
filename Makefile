dev-server:
	poetry run python manage.py runserver 8080

test:
	poetry run python3 manage.py test task_manager

makemigrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate

makemessages:
	poetry run django-admin makemessages -a

compilemessages:
	poetry run django-admin compilemessages

lint:
	poetry run flake8 task_manager

coverage:
	poetry run coverage run --source='task_manager' manage.py test task_manager
	poetry run coverage xml
