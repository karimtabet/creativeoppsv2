from uuid import uuid4

from flask import render_template, request, flash
from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.model.template import macro


from app.app import app, db, admin
from app.models import IndexCarouselItem, IndexContent, Project, Image
from app.images import get_flickr_images
from app.videos import get_youtube_videos
from app.forms import CKTextAreaField, GetFlickrForm, GetYoutubeForm


@app.route('/')
def index():
    carousel_items = db.session.query(IndexCarouselItem).all()
    return render_template('index.html', carousel_items=carousel_items)


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


@app.route('/gallery/<project_id>', methods=['GET'])
def gallery(project_id):
    project = db.session.query(Project).get(project_id)
    return render_template('gallery.html', project=project)


class IndexCarouselItemModelView(ModelView):
    list_template = 'admin/list_projects.html'
    column_list = ('image_url', 'title', 'description', 'read_more_url')
    column_formatters = {'image_url': macro("preview_avatar")}
    column_labels = {'image_url': 'Image'}
    form_overrides = {'description': CKTextAreaField}

    def on_model_change(self, form, model, is_created):
        model.uuid = uuid4()

admin.add_view(
    IndexCarouselItemModelView(
        IndexCarouselItem,
        db.session,
        endpoint='index-carousel-items',
        category='Index Page',
        name='Carousel Items'
    )
)


class IndexContentModelView(ModelView):
    can_create = False
    can_delete = False
    column_list = ()
    form_overrides = {
      'feature_1_description': CKTextAreaField,
      'feature_2_description': CKTextAreaField,
      'feature_3_description': CKTextAreaField,
      'mid_page_text': CKTextAreaField,
      'mid_page_feature_1_description': CKTextAreaField,
      'mid_page_feature_2_description': CKTextAreaField,
      'mid_page_feature_3_description': CKTextAreaField
    }

    def on_model_change(self, form, model, is_created):
        model.uuid = uuid4()

admin.add_view(
    IndexContentModelView(
        IndexContent,
        db.session,
        endpoint='index-descriptive-content',
        category='Index Page',
        name='Descriptive Content'
    )
)


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
  ProjectModelView(Project, db.session, endpoint='projects', name='Projects')
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
