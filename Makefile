.PHONY: clean init assets server db


init:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements/development.txt

clean:
	rm -rf venv
	find . -name '*.pyc' -delete

assets:
	bower install

server:
	venv/bin/python src/manage.py runserver 0.0.0.0:8000

db:
	@( \
		export AWS_DATABASE_URL='test'; \
		venv/bin/python src/manage.py migrate; \
	)

fixture:
	@( \
		export AWS_DATABASE_URL='test'; \
		venv/bin/python src/manage.py loaddata fixtures/*; \
	)
	
image:
	init
	rm -rf ./statcs
	yarn install

	@( \
       source ./venv/bin/activate; \
       python manage.py collectstatic; \
    )
    
