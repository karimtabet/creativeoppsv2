from app import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<Admin %r>' % (self.username)


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about_us = db.Column(db.String(4096))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    description = db.Column(db.String(380))
    location = db.Column(db.String(240))
    body = db.Column(db.String(2048))
    date = db.Column(db.String(120))
    avatar_url = db.Column(db.String(380))
    album_url = db.Column(db.String(380))
    thumbnail_url = db.Column(db.String(380))
    video_urls = db.Column(db.String(860))
    pictures = db.relationship('Picture', backref='projects', lazy='dynamic')
    videos = db.relationship('Video', backref='projects', lazy='dynamic')


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thumbnail_url = db.Column(db.String(140))
    image_url = db.Column(db.String(140))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return self.image_url


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(140))
    thumbnail_url = db.Column(db.String(140))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return self.video_url
