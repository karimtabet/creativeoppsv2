from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

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
        return '<Admin %r>' % (self.nickname)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(240))
    description = db.Column(db.String(380))
    location = db.Column(db.String(240))
    body = db.Column(db.String(2048))
    date = db.Column(db.Date)
    avatar_url = db.Column(db.String(380))
    album_url = db.Column(db.String(380))
    video_url = db.Column(db.String(380))

    def __repr__(self):
        return '<Post %r>' % (self.body)