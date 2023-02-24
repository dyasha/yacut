import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


ONE_DIGIT = 1
SIXTEEN_DIGIT = 16
TWO_HUND_FIFTY_SIX_DIGIT = 256