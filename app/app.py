from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

from app.config import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql+psycopg2://{role}:{password}@{host}:{port}/{db}'
    .format(
        **config['postgresql']
    )
)
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3

admin = Admin(app)
db = SQLAlchemy(app)
