from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(240))
    description = db.Column(db.String(380))
    location = db.Column(db.String(240))
    body = db.Column(db.String(2048))
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Post %r>' % (self.body)