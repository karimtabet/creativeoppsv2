import urllib2
import urlparse
import json
from flask import render_template, redirect, url_for, request
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import login_user, logout_user, current_user
from passlib.hash import sha256_crypt
from app import app, db, admin, login_manager
from models import Project, Picture, Video, Admin


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html',
                           projects=projects)


@app.route('/project/<project_id>', methods=['GET'])
def project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    pictures = Picture.query.filter_by(project_id=project_id)
    videos = Video.query.filter_by(project_id=project_id)
    return render_template('project.html',
                           project=project,
                           pictures=pictures,
                           videos=videos)


def get_pictures(album_id, project_id):
    thumbnail_url = ''
    picture_url = ''
    last_picture = ''
    response = urllib2.urlopen(
        "https://api.flickr.com/services/rest/" +
        "?method=flickr.photosets.getPhotos" +
        "&api_key=c5abbe4d732f631c72a743855fc5b47c&photoset_id=" +
        album_id + "&format=json&nojsoncallback=1"
      ).read()
    response_json = json.loads(response)
    for line in response_json['photoset']['photo']:
        photo_id = line['id']
        response = urllib2.urlopen(
            "https://api.flickr.com/services/rest/" +
            "?method=flickr.photos.getSizes&" +
            "api_key=c5abbe4d732f631c72a743855fc5b47c&photo_id=" + photo_id +
            "&format=json&nojsoncallback=1").read()
        response_json = json.loads(response)
        for line in response_json['sizes']['size']:
            if line['label'] == 'Medium':
                thumbnail_url = line['source']
            if line['label'] == 'Original':
                picture_url = line['source']

            if picture_url and picture_url != last_picture:
                last_picture = picture_url
                picture = Picture(thumbnail_url=thumbnail_url,
                                  image_url=picture_url,
                                  project_id=project_id)
                db.session.add(picture)
    db.session.commit()


def get_videos(video_urls, project_id):
    for video_url in video_urls.split(','):
        video_url = video_url.strip()
        url_data = urlparse.urlparse(video_url)
        query = urlparse.parse_qs(url_data.query)
        video_id = query["v"][0]
        thumbnail_url = (
            'http://img.youtube.com/vi/' +
            video_id + '/default.jpg'
        )
        video = Video(video_url=video_url,
                      thumbnail_url=thumbnail_url,
                      project_id=project_id)
        db.session.add(video)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = Admin.query.filter_by(
          username=request.form["username"]).first()
        if user:
            if sha256_crypt.verify(request.form['password'], user.password):
                login_user(user)
                return redirect(url_for('model_view_project.index_view'))
            else:
                error = 'Invalid Credentials. Please try again.'
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

    def on_model_change(self, form, model, is_created):
        if model.album_url:
            album_id = model.album_url[model.album_url.find('sets/')+5:-1]
            get_pictures(album_id, model.id)
        if model.video_urls:
            get_videos(model.video_urls, model.id)

    def __init__(self, session, **kwargs):
        super(AdminView, self).__init__(Project, session, **kwargs)

admin.add_view(AdminView(db.session, endpoint="model_view_project"))
