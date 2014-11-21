from flask.ext.wtf import Form
from wtforms import StringField, DateField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class ProjectForm(Form):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    location = StringField('location')
    body = StringField('body', validators=[DataRequired()])
    date = StringField('date')
    avatar_url = StringField('avatar_url')
    album_url = StringField('album_url')
    thumbnail_url = StringField('thumbnail_url')
    video_urls = StringField('video_urls')