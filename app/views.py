from flask import render_template, request, flash
from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import Required

from app.app import app, db, admin
from app.models import Project, Image, Video
from app.flickr import get_pictures
from app.youtube import get_videos


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
  ProjectModelView(Project, db.session, endpoint='projects')
)


class GetFlickrForm(Form):
    projects = db.session.query(Project).all()
    album_id = TextField('Album ID', [Required()])
    project_id = SelectField(
      'Project',
      choices=[(project.id, project.title) for project in projects],
      validators=[Required()]
    )


class GetFlickrView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = GetFlickrForm(request.form)
        if form.validate_on_submit():
            get_pictures(form.data["album_id"], form.data["project_id"])
            flash('Succesffully added images to {project_id}'.format(
              project_id=form.data["project_id"])
            )
        return self.render('admin/get_flickr.html', form=form)

admin.add_view(GetFlickrView(name='Get Flickr Content', url='get_flickr'))


class GetYoutubeForm(Form):
    projects = db.session.query(Project).all()
    video_urls = TextField('Video URLs (comma separated)', [Required()])
    project_id = SelectField(
      'Project',
      choices=[(project.id, project.title) for project in projects],
      validators=[Required()]
    )


class GetYoutubeView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = GetYoutubeForm(request.form)
        if form.validate_on_submit():
            get_videos(form.data["video_urls"], form.data["project_id"])
            flash('Succesffully added images to {project_id}'.format(
              project_id=form.data["project_id"])
            )
        return self.render('admin/get_youtube.html', form=form)

admin.add_view(GetYoutubeView(name='Get Youtube Content', url='get_youtube'))
