from flask import render_template
from flask.ext.admin.contrib.sqla import ModelView

from app.app import app, db, admin
from app.models import Project, Image, Video
from app.flickr import get_pictures as get_flickr_pictures
from app.youtube import get_videos as get_youtube_videos


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html',
                           projects=projects)


@app.route('/project/<project_id>', methods=['GET'])
def project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    pictures = Image.query.filter_by(project_id=project_id)
    videos = Video.query.filter_by(project_id=project_id)
    return render_template('project.html',
                           project=project,
                           pictures=pictures,
                           videos=videos)


class AdminView(ModelView):
    def on_model_change(self, form, model, is_created):
        if model.album_url:
            album_id = model.album_url[model.album_url.find('sets/')+5:-1]
            get_flickr_pictures(album_id, model.id)
        if model.video_urls:
            get_youtube_videos(model.video_urls, model.id)

    def __init__(self, session, **kwargs):
        super(AdminView, self).__init__(Project, session, **kwargs)

admin.add_view(AdminView(db.session, endpoint='model_view_project'))
