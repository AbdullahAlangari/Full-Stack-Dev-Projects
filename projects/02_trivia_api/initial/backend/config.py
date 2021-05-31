import os
SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abodov1281@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False