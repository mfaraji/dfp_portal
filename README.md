

# inspire

inspire is a an inventory tools to aggragate data comming from DFP and stored on Inspire Inc. database. It is built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* dfp: contains all modules to fetch data from dfp and aws and aggreate them
* inspire: contains the settings for the project

## Installation

### 1. virtualenv / virtualenvwrapper
You should already know what is [virtualenv](http://www.virtualenv.org/), preferably [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/) at this stage. So, simply create it in the project folder.
```
$ easy_install pip
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements/development.txt
```

### 2. Create tables/ load fixtures
After setting up the environment, you need to create the tables and load the fixtures
### Quick start

The product is shipped as a docker image. The docker image requires the following variables in order to run:
* DATABASE_URL: which contains the data 
To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv inspire`
    2. `$ . inspire/bin/activate`

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

### Detailed instructions

Take a look at the docs for more information.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
