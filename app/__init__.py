from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = config.login_manager_secret_key

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

from app.auth.controllers import auth
from app.site.controllers import site

app.register_blueprint(auth)
app.register_blueprint(site)
# app.register_bluebrint(x)

db.create_all()