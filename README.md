## Versions

App | Version
--- | ---
Python | 3.9.1
Django | 3.1.3
DRF | 3.12.2

## Docker Compose containers

- db (Django PostgreSQL database)
- app (Django application)

# Setup & Run

## Run on docker

    # build docker containers
    docker-compose build

    # option 1: up docker containers
    docker-compose up

You can also run manage.py commands using docker environment, for example tests.

    docker-compose run web python ./manage.py test

See docker's logs

    docker-compose logs --tail 5

## Run on local machine

    pip install -r requirements.txt
    cd project
    python manage.py runserver