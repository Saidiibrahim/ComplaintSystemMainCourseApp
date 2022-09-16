# ComplaintSystem App

![Alt Text](https://media.giphy.com/media/Xw6yFn7frR3Y4/giphy.gif)


### This is the main app for the Udemy course on FastAPI

### Packages installed via command line:
    - pip install asyncpg psycopg2 psycopg2-binary sqlalchemy 
    - pip install python-decouple (to configure database url)
    - pip install databases
    - pip install alembic  


### Useful Pycharm tricks
1. Optimising order of imports:
    Optimise imports or Ctrl + Option + O
2. next trick here


## Setting up alembic and secrets
alembic init migrations   -> this is the initial migration

### Inside the env.py file:
#### We're fetching the values using the config() function from decouple
#### These values are used to set the credentials inside the alembic.ini file

So in the env.py file, we have this code chunk:

section = config.config_ini_section

config.set_section_option((section, "DB_USER", env_config("DB_USER")))
config.set_section_option((section, "DB_PASS", env_config("DB_PASSWORD")))`

In other words, set the DB_PASS used in the alembic.ini file is the DB_PASSWORD 
from the .env file

Finally, don't forget to set the target_metadata = metadata (not None)


alembic  revision --autogenerate -m "Initial" 


## Mangers
### Responsible for handling business logic
#### pip install pyjwt 
