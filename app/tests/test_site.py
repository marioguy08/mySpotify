import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Flask, render_template, current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.auth.controllers import auth
from app.auth.models import User
from flask_login import login_user
from app import db, login_manager

from app.api.controllers import api
from app.auth.controllers import auth
from app.site.controllers import site
from app.profiles.controllers import profiles

from app import app
import config

class APITests(unittest.TestCase):
    def create_app(self):

        app = Flask('Testing')
        app.config.from_object('config') 
        app.jinja_env.cache = {} # https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679?gi=a8f7d3ec3e71

        db = SQLAlchemy(app)

        login_manager = LoginManager()
        login_manager.init_app(app)
        app.secret_key = config.login_manager_secret_key

        @app.errorhandler(404)
        def not_found(e):
            return render_template('404.html'), 404
        app.register_blueprint(api)
        app.register_blueprint(auth)
        app.register_blueprint(site)
        app.register_blueprint(profiles)

        db.create_all()

        
        return app
        
    # executed prior to each test
    def setUp(self):
        #need to create a fake user to run tests on 
        db.session.commit()
        db.drop_all()
        db.create_all()
        app.config.from_object('config') 
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        login_manager = LoginManager()
        login_manager.init_app(app)
        app.secret_key = config.login_manager_secret_key

        app.register_blueprint(auth)

        self.app = app.test_client()

        self.user = User('marioguy4699@gmail,com','marioguy08','hello1234')
        db.session.add(self.user)
        db.session.commit()
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        with app.app_context(), app.test_request_context():
            response = self.app.get(url_for('site.home'))
            self.assertEqual(response.status_code,200)

if __name__ == "__main__":
    unittest.main()
