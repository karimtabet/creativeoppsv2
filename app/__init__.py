from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
admin = Admin(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from app import views, models
