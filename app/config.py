import os


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    FLICKR_API_KEY = os.environ["FLICKR_API_KEY"]
