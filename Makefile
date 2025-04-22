build:
	sudo docker-compose build

up:
	sudo docker-compose up

down: 
	sudo docker-compose down

run:
	sudo docker-compose up

bash:
	sudo docker compose run --rm web bash

migrate:
	sudo docker compose run --rm web python manage.py migrate

test:
	sudo docker compose run --rm web coverage run manage.py test

coverage:
	sudo docker compose run --rm web coverage html

shell:
	sudo docker compose run --rm web python manage.py shell

startapp:
	@$(eval APP_NAME := $(word 2,$(MAKECMDGOALS)))
	docker compose run --rm web python manage.py startapp $(APP_NAME)

migrations:
	sudo docker compose run --rm web python manage.py makemigrations

createsuperuser:
	sudo docker compose run --rm web python manage.py createsuperuser

check:
	sudo docker compose run --rm web python manage.py check
