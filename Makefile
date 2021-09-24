
runserver:
	uvicorn main:app --reload --log-config log.ini

test:
	py.test -v

coverage:
	mkdir -p .reports
	coverage run -m pytest
	coverage report -m
	coverage xml
	coverage html

quality:
	mkdir -p .reports
	flake8 -q --format=html --htmldir=.reports/flake8 --exit-zero
	flake8

docker-runserver:
	docker build -t portal-api .
	docker run -d --name portal-api -p 8000:8000 portal-api
