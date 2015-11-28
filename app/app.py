from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

from app.config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
print(app.config["SQLALCHEMY_DATABASE_URI"])

admin = Admin(app)
db = SQLAlchemy(app)
