from werkzeug import check_password_hash

import config
from app import db

class User(db.Model):
    __tablename__ = 'credentials'

    id                  = db.Column(db.Integer,     primary_key=True)
    email               = db.Column(db.String(128), nullable=False, unique=True)
    username            = db.Column(db.String(128), nullable=False, unique=True)
    password            = db.Column(db.String(128), nullable=False)
    spotify_username    = db.Column(db.String(128), nullable=True)
    auth_token          = db.Column(db.String(128), nullable=True)
    refresh_token       = db.Column(db.String(128), nullable=True)
    
    def __init__(self, email, username, password, spotify_username="", auth_token="", refresh_token=""):
        self.email              = email
        self.username           = username
        self.password           = password
        self.spotify_username   = spotify_username
        self.auth_token         = auth_token
        self.refresh_token      = refresh_token

    def __repr__(self):
        return '<User %r>' % (self.username)

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return not self.is_authenticated()

    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")
    
    def get(id):
        return User.query.get(id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_token(self, new_token):
        self.auth_token = new_token
        db.session.commit()
