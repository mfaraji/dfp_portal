.PHONY: clean init assets server db


init:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt

clean:
	rm -rf venv
	find . -name '*.pyc' -delete

assets:
	bower install

server:
	@( \
       source ./venv/bin/activate; \
       python3 src/manage.py runserver 0.0.0.0:8000; \
    )

db:
	@( \
       source ./venv/bin/activate; \
       python manage.py migrate; \
    )


cleanup:
	@( \
       source ./venv/bin/activate; \
       python manage.py stacks-delete; \
    )

list:
	@( \
       source ./venv/bin/activate; \
       python manage.py stacks; \
    )

update:
	git pull
	bower install
	@( \
		source ./venv/bin/activate; \
		pip install -r requirements/prod; \
		python src/manage.py migrate; \
		python src/manage.py collectstatic; \
    )
