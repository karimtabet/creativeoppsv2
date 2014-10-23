from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, ProjectForm
from models import Admin, Project, Picture
import urllib2

@app.route('/')
def index():
    projects = Project.query.all()
    pictures = Picture.query.all()
    return render_template('index.html',
                            projects=projects,
                            pictures=pictures)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

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
        # nickname = resp.nickname
        # if nickname is None or nickname == "":
        #     nickname = resp.email.split('@')[0]
        # admin = Admin(nickname=nickname, email=resp.email)
        # db.session.add(admin)
        # db.session.commit()
        flash('Admin does not exist')
        return redirect(url_for('login'))
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(admin, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

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
                        video_url=form.video_url.data)
      db.session.add(project)
      db.session.commit()
      db.session.refresh(project)
      if project.album_url:
        album_id = project.album_url[project.album_url.find('sets/')+5:-1]
        get_pictures(album_id, project.id)
      return redirect(url_for('admin'))
    return render_template('project.html',
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
    picture_id_list = []
    response = urllib2.urlopen("https://api.flickr.com/services/rest/" + 
                              "?method=flickr.photosets.getPhotos" + 
                              "&api_key=d8e4ad571b7215e272e295dfc8aac114" + 
                              "&photoset_id=" + album_id +
                              "&format=rest" + 
                              "&api_sig=82c0055d337d39cbe34f080b93a6ef59").read()
    picture_xml_list = response.split('/>')
    for xml in picture_xml_list:
      if len(xml) > 50 and len(xml) < 150:
        picture_id = xml[13:24]
        picture_secret = xml[34:44]
        picture_server = xml[54:58]
        picture_farm = xml[66:67]

        picture_url = "https://www.flickr.com/photos/128639640@N03/" + picture_id + "/player/"
        thumbnail_url = ("https://farm" + picture_farm + ".staticflickr.com/" + 
                          picture_server + "/" + picture_id + "_" + picture_secret + "_q.jpg")

        picture = Picture(thumbnail_url=thumbnail_url,
                        image_url=picture_url,
                        project_id=project_id)
        db.session.add(picture)
        db.session.commit()