test:
	python -m unittest tests/*/*.py

up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose build

run:
	docker-compose up --build