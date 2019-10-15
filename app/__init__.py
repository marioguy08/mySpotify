from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

app = Flask(__name__)
app.config.from_object('config') 
app.jinja_env.cache = {} # https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679?gi=a8f7d3ec3e71

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = config.login_manager_secret_key

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

from app.auth.controllers import auth
from app.site.controllers import site
from app.profiles.controllers import profiles

app.register_blueprint(auth)
app.register_blueprint(site)
app.register_blueprint(profiles)
# app.register_blueprint(x)

db.create_all()
