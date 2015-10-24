from flask import render_template
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from app.app import app, db, admin
from app.models import Project, Image, Video


@app.route('/')
def index():
    projects = db.session.query(Project).all()
    return render_template('index.html',
                           projects=projects)


@app.route('/project/<project_id>', methods=['GET'])
def project(project_id):
    project = db.session.query(Project).filter(id=project_id).first()
    images = db.session.query(Image).filter(project_id=project_id).all()
    videos = db.session.query(Video).filter(project_id=project_id).all()
    return render_template('project.html',
                           project=project,
                           images=images,
                           videos=videos)


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProjectModelView(ModelView):
    form_columns = [
      'title',
      'avatar_url',
      'location',
      'datetime',
      'description',
      'body',
      'images',
      'videos'
    ]
    form_overrides = {
        'body': CKTextAreaField
    }

    def on_model_change(self, form, model, is_created):
        model.id = form.title.data.lower().replace(' ', '-')

admin.add_view(
  ProjectModelView(Project, db.session, endpoint='project_model_view')
)
