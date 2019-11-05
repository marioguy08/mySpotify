import config
from app import db

class Profile(db.Model):
    __tablename__ = 'profiles'

    id                  = db.Column(db.Integer,     primary_key=True)
    username            = db.Column(db.String(128), nullable=False, unique=True)
    spotify_username    = db.Column(db.String(128), nullable=True)
    following           = db.Column(db.String,      default='')
    followers           = db.Column(db.String,      default='')
    ppd                 = db.Column(db.String(128), nullable=True)
    status              = db.Column(db.String(128), default='') 
    def __init__(self, username, spotify_username, ppd=''):
        self.username           = username
        self.spotify_username   = spotify_username
        self.followers          = ''
        self.following          = ''
        self.ppd                = ppd
        self.status             = ''
        
    def __repr__(self):
        return '<Profile %r>' % (self.username)

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return not self.is_authenticated()

    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")
    
    def get(id):
        return Profile.query.get(id)
