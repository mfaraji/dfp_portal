.PHONY: clean init assets server db


init:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements/development

clean:
	rm -rf venv
	find . -name '*.pyc' -delete

assets:
	bower install

server:
	@( \
       source ./venv/bin/activate; \
       python src/manage.py runserver 0.0.0.0:8000; \
    )

db:
	@( \
       source ./venv/bin/activate; \
       python src/manage.py migrate; \
    )

fixture:
	@( \
       source ./venv/bin/activate; \
       python src/manage.py loaddata fixtures/fixture.json; \
    )

image:
	init
	rm -rf ./statcs
	yarn install

	@( \
       source ./venv/bin/activate; \
       python manage.py collectstatic; \
    )
    
