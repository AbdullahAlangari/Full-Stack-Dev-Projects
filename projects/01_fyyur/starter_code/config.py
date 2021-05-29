import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

#app.config['DEBUG'] = True
#app.config[''] =False


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abodov1281@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False

