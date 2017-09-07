

# inspire

inspire is a an inventory tools to aggragate data comming from DFP and stored on Inspire Inc. database. It is built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* dfp: contains all modules to fetch data from dfp and aws and aggreate them
* inspire: contains the settings for the project

## Setup

### 1. virtualenv / virtualenvwrapper
You should already know what is [virtualenv](http://www.virtualenv.org/), preferably [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/) at this stage. So, simply create it in the project folder.
```
$ easy_install pip
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements/development.txt
```

or 

```
make init
```

### 2. Create tables/ load fixtures
After setting up the environment, you need to create the tables and load the fixtures:

First, you need to set database url
```
export DATABASE_URL="mysql://test:test@localhost/db"
```
Then, run the migration

```
make db
make fixture
```
### 3. Run the docker image
First setup the environment variables in a file named local.env in the root of the project. You can find a sample file there.
Then, run the docker image by:

```
docker-compose run -d web
```