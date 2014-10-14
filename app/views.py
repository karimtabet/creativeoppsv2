from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, ProjectForm
from models import Admin, Project
# , ROLE_USER, ROLE_ADMIN

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html',
                            projects=projects)

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
        print "HI"
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
    # user = User.query.filter_by(nickname=nickname).first()
    # if user == None:
    #     flash('User %s not found.' % nickname)
    #     return redirect(url_for('index'))
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    projects = Project.query.all()
    return render_template('admin.html',
                           projects=projects)

@app.route('/admin/project', defaults = {'project_id':None},
          methods=['GET', 'POST'])
@app.route('/admin/project/<project_id>',
          methods=['GET', 'POST'])
@login_required
def updateProject(project_id):
    form = ProjectForm()
    project = Project(title=form.title.data,
                      description=form.description.data,
                      location=form.location.data,
                      body=form.body.data,
                      date=form.date.data,
                      album_url=form.album_url.data,
                      video_url=form.video_url.data)
    db.session.add(project)
    db.session.commit()
    return render_template('project.html',
                           form=form)
