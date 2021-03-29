server:
	poetry run python manage.py runserver

reqs:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

translations:
	poetry run django-admin makemessages -l en

compile-translations:
	poetry run django-admin compilemessages

migrate:
	poetry run python ./manage.py migrate

install: 
	poetry install

selfcheck:
	poetry check

lint:
	poetry run flake8 task_manager

test:
	poetry run python manage.py test

coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage xml
	poetry run coverage report
