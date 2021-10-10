# Task manager
[![Actions Status](https://github.com/isbushcar/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/isbushcar/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/44bfa6df75a69a0728d3/maintainability)](https://codeclimate.com/github/isbushcar/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/44bfa6df75a69a0728d3/test_coverage)](https://codeclimate.com/github/isbushcar/python-project-lvl4/test_coverage)
## Description
Task manager is a simple web-application for (surprise!) task management.  
It allows creating tasks and custom statuses and labels for them, assign executors and so on.  
[You can take look at deployed app here.](https://fierce-beyond-80531.herokuapp.com/)
## Local deployment (requires Poetry)
1. Clone repository: `git clone https://github.com/isbushcar/python-project-lvl4.git`
2. Go to directory python-project-lvl4 `cd python-project-lvl4`
3. Install dependencies by `poetry install`
4. Apply migrations by `make migrate`
5. Create superuser if you need `poetry run python3 manage.py createsuperuser`
6. Now application can be started by `make dev-server`
7. Create your first task "Conquer the world!"
### Notes
This guide doesn't affect some important aspects of development and deployment
such as using Django secret key and other environment variables, setting up databases and so on.
In case you are going to use this app in production, please read the [official docs.](https://docs.djangoproject.com/)