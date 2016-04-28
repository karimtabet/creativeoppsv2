from uuid import uuid4

from flask import render_template, request, flash
from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.model.template import macro
from flask.ext.mail import Message
from sqlalchemy import desc

from app.app import app, db, admin, mail
from app.models import (IndexCarouselItem, IndexContent, Project, Image, Video,
                        Policy)
from app.images import get_flickr_images
from app.videos import get_youtube_videos
from app.forms import (
    CKTextAreaField,
    GetFlickrForm,
    GetYoutubeForm,
    ContactForm
)


@app.route('/')
def index():
    carousel_items = db.session.query(IndexCarouselItem).all()
    content = db.session.query(IndexContent).one()
    recent_images = db.session.query(Image).join(Project).order_by(
        desc(Project.datetime)
    ).all()[:3]
    return render_template(
        'index.html',
        carousel_items=carousel_items,
        content=content.as_dict(),
        recent_images=recent_images
    )


@app.route('/about', methods=['GET'])
def about_us():
    return render_template('about.html')


@app.route('/projects', methods=['GET'])
def projects():
    projects = db.session.query(Project).order_by(desc(Project.datetime)).all()
    return render_template('projects.html', projects=[project.as_dict()
                                                      for project in projects])


@app.route('/project/<project_id>', methods=['GET'])
def project(project_id):
    project = db.session.query(Project).get(project_id)
    return render_template('project.html', project=project.as_dict())


@app.route('/galleries', methods=['GET'])
def galleries():
    projects = db.session.query(Project).join(Image).all()
    return render_template('galleries.html', projects=projects)


@app.route('/gallery/<project_id>', methods=['GET'])
def gallery(project_id):
    project = db.session.query(Project).get(project_id)
    return render_template('gallery.html', project=project)


@app.route('/publications', methods=['GET'])
def publications():
    policies = db.session.query(Policy).all()
    return render_template('publications.html',
                           policies=[policy.as_dict() for policy in policies])


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form
        try:
            msg = Message(email.get('subject'),
                          sender='contact@creativeopportunities.co.uk',
                          recipients=['contact@creativeopportunities.co.uk'],
                          body=('New Email from: {} {} \n\n{}'.format(
                                email.get('name'), email.get('email'),
                                email.get('message'))))
            mail.send(msg)
            flash('Message succesffully sent')
        except Exception:
            flash('Message failed')

    return render_template('contact.html', form=ContactForm(request.form))


class IndexCarouselItemModelView(ModelView):
    list_template = 'admin/list_macros.html'
    column_list = ('image_url', 'title', 'description', 'read_more_url')
    column_formatters = {'image_url': macro('preview_avatar')}
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
    list_template = 'admin/list_index_content.html'
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
    list_template = 'admin/list_macros.html'
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
    column_formatters = {'avatar_url': macro('preview_avatar')}
    column_labels = {'avatar_url': 'Avatar'}
    form_overrides = {'body': CKTextAreaField, 'description': CKTextAreaField}

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = form.title.data.lower().replace(' ', '-')

admin.add_view(
    ProjectModelView(Project, db.session, endpoint='projects', name='Projects')
)


class ImageModelView(ModelView):
    list_template = 'admin/list_macros.html'
    column_list = ('thumbnail_url', 'image_url', 'project')
    column_formatters = {'thumbnail_url': macro('preview_avatar')}
    form_columns = ['image_url', 'thumbnail_url', 'project']


admin.add_view(
    ImageModelView(
        Image,
        db.session,
        endpoint='images',
        name='Images'
    )
)


class VideoModelView(ModelView):
    list_template = 'admin/list_macros.html'
    column_list = ('thumbnail_url', 'video_url', 'project')
    column_formatters = {'thumbnail_url': macro('preview_avatar')}
    form_columns = ['video_url', 'thumbnail_url', 'project']


admin.add_view(
    VideoModelView(
        Video,
        db.session,
        endpoint='videos',
        name='Videos'
    )
)


class PolicyModelView(ModelView):
    list_template = 'admin/list_macros.html'
    form_overrides = {'body': CKTextAreaField, 'description': CKTextAreaField}
    column_formatters = {'body': macro('render_markdown')}

admin.add_view(
    PolicyModelView(
        Policy,
        db.session,
        endpoint='policies',
        name='Policies'
    )
)


class GetFlickrView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = GetFlickrForm(request.form)
        if form.validate_on_submit():
            get_flickr_images(form.data['album_id'], form.data['project_id'])
            flash('Succesffully added images to {project_id}'.format(
                project_id=form.data['project_id'])
            )
        return self.render('admin/get_flickr.html', form=form)

admin.add_view(
    GetFlickrView(
        name='Get Flickr Content',
        url='get_flickr',
        category='Grab Content'
    )
)


class GetYoutubeView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = GetYoutubeForm(request.form)
        if form.validate_on_submit():
            get_youtube_videos(
                form.data['video_urls'], form.data['project_id']
            )
            flash('Succesffully added images to {project_id}'.format(
                project_id=form.data['project_id'])
            )
        return self.render('admin/get_youtube.html', form=form)

admin.add_view(
    GetYoutubeView(
        name='Get Youtube Content',
        category='Grab Content',
        url='get_youtube'
    )
)
