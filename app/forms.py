from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import Required

from app.app import db
from app.models import Project


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class GetFlickrForm(Form):
    projects = db.session.query(Project).all()
    album_id = TextField('Album ID', [Required()])
    project_id = SelectField(
      'Project',
      choices=[(project.id, project.title) for project in projects],
      validators=[Required()]
    )


class GetYoutubeForm(Form):
    projects = db.session.query(Project).all()
    video_urls = CKTextAreaField('Video URLs (comma separated)', [Required()])
    project_id = SelectField(
      'Project',
      choices=[(project.id, project.title) for project in projects],
      validators=[Required()]
    )
