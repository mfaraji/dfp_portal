.PHONY: clean init assets server db


init:
	virtualenv venv
	(\
		source venv/bin/activate; \
		pip install -r requirements/development.txt; \
	)

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
		source venv/bin/activate; \
		venv/bin/python src/manage.py migrate; \
	)

fixture:
	@( \
		export AWS_DATABASE_URL='test'; \
		source venv/bin/activate; \
		venv/bin/python src/manage.py loaddata fixtures/*; \
	)
	
image:
	init
	rm -rf ./statics
	rm -rf ./node_modules
	yarn install
	@( \
	   export AWS_DATABASE_URL='test';\
	   export DATABASE_URL='test';\
       source ./venv/bin/activate; \
       python src/manage.py collectstatic; \
    )
    sudo docker-compose build web	
    
upload:
	./script/upload_docker_image.sh