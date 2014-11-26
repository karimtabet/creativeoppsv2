from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import ProjectForm
from models import Admin, Project, Picture, Video
import urllib2, urlparse, json

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html',
                            projects=projects)

@app.route('/project/<project_id>', methods=['GET'])
def project(project_id):
  project = Project.query.filter_by(id=project_id).first()
  pictures = Picture.query.filter_by(project_id=project_id)
  for picture in pictures:
    print picture.image_url
  videos = Video.query.filter_by(project_id=project_id)
  return render_template('project.html',
                            project=project,
                            pictures=pictures,
                            videos=videos)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    return oid.try_login('https://www.google.com/accounts/o8/id', 
                              ask_for=['nickname', 'email'])

@lm.user_loader
def load_user(id):
    return Admin.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    admin = Admin.query.filter_by(email=resp.email).first()
    if admin is None:
        flash('Admin does not exist')
        return redirect(url_for('login'))
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(admin, remember = remember_me)
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    projects = Project.query.all()
    return render_template('admin.html',
                           projects=projects)

@app.route('/admin/project', defaults = {'project_id':None},
          methods=['GET', 'POST'])
@app.route('/admin/project/<project_id>',
          methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    form = ProjectForm()
    if form.validate_on_submit():
      project = Project(title=form.title.data,
                        description=form.description.data,
                        location=form.location.data,
                        body=form.body.data,
                        date=form.date.data,
                        album_url=form.album_url.data,
                        thumbnail_url=form.thumbnail_url.data,
                        video_urls=form.video_urls.data)
      db.session.add(project)
      db.session.commit()
      db.session.refresh(project)
      if project.album_url:
        album_id = project.album_url[project.album_url.find('sets/')+5:-1]
        print project.id
        get_pictures(album_id, project.id)
      if project.video_urls:
        get_videos(project.video_urls, project.id)
      return redirect(url_for('admin'))
    return render_template('project_form.html',
                           form=form)

@app.route('/admin/project/delete/<project_id>',
          methods=['GET', 'POST'])
@login_required
def deleteProject(project_id):
    if request.method == 'POST':
      project = Project.query.filter_by(id=project_id).first()
      db.session.delete(project)

      pictures = Picture.query.filter_by(project_id=project_id).all()
      for pic in pictures:
        db.session.delete(pic)

      db.session.commit()
      return redirect(url_for('admin'))

def get_pictures(album_id, project_id):
    print "YE " + project_id
    picture_id_list = []
    response = urllib2.urlopen("https://api.flickr.com/services/rest/?method=flickr.photosets.getPhotos" + 
                                "&api_key=28b8b728bfb3dda2af61f99f29d98334&photoset_id=" + album_id + 
                                "&format=json&nojsoncallback=1").read()
    response_json = json.loads(response)

    for line in response_json['photoset']['photo']:
      photo_id = line['id']
      response = urllib2.urlopen("https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&" +
                                  "api_key=28b8b728bfb3dda2af61f99f29d98334&photo_id=" + photo_id +
                                  "&format=json&nojsoncallback=1").read()
      response_json = json.loads(response)
      for line in response_json['sizes']['size']:
        if line['label'] == 'Small':
          thumbnail_url = line['source']
        if line['label'] == 'Original':
          picture_url = line['source']

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
    thumbnail_url = 'http://img.youtube.com/vi/' + video_id + '/default.jpg'
    video = Video(video_url=video_url,
                        thumbnail_url=thumbnail_url,
                        project_id=project_id)
    db.session.add(video)
    db.session.commit()