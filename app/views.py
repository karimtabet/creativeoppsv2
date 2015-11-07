from flask import render_template, request, flash
from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.model.template import macro
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import Required

from app.app import app, db, admin
from app.models import Project, Image
from app.images import get_flickr_images
from app.videos import get_youtube_videos


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about_us():
    return render_template('about.html')


@app.route('/projects', methods=['GET'])
def projects():
    projects = db.session.query(Project).all()
    return render_template('projects.html', projects=projects)


@app.route('/project/<project_id>', methods=['GET'])
def project(project_id):
    project = db.session.query(Project).get(project_id)
    return render_template('project.html', project=project)


@app.route('/galleries', methods=['GET'])
def galleries():
    projects = db.session.query(Project).join(Image).all()
    return render_template('galleries.html', projects=projects)


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
    list_template = 'admin/list_projects.html'
    edit_template = 'admin/edit_project.html'
    form_columns = [
      'title',
      'location',
      'datetime',
      'avatar_url',
      'description',
      'body'
    ]
    column_list = ('avatar_url', 'title', 'location', 'datetime')
    column_formatters = {'avatar_url': macro("preview_avatar")}
    column_labels = {'avatar_url': 'Avatar'}
    form_overrides = {'body': CKTextAreaField, 'description': CKTextAreaField}

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
            get_flickr_images(form.data["album_id"], form.data["project_id"])
            flash('Succesffully added images to {project_id}'.format(
              project_id=form.data["project_id"])
            )
        return self.render('admin/get_flickr.html', form=form)

admin.add_view(GetFlickrView(name='Get Flickr Content', url='get_flickr'))


class GetYoutubeForm(Form):
    projects = db.session.query(Project).all()
    video_urls = CKTextAreaField('Video URLs (comma separated)', [Required()])
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
            get_youtube_videos(
              form.data["video_urls"], form.data["project_id"]
            )
            flash('Succesffully added images to {project_id}'.format(
              project_id=form.data["project_id"])
            )
        return self.render('admin/get_youtube.html', form=form)

admin.add_view(GetYoutubeView(name='Get Youtube Content', url='get_youtube'))
