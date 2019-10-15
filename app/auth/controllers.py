import requests, urllib
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug import generate_password_hash

import config
from app import db, login_manager
from app.auth.forms import SigninForm, SignupForm
from app.auth.models import User
from app.profiles.models import Profile
from app.spotify.models import Spotify

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))

    form = SigninForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.data['username']).first()

        if not user or not user.check_password(form.data['password']):
            flash('Invalid Username or Password.')
            return redirect(url_for('auth.signin'))
        
        user.update_token(Spotify().refresh_access_token(user.refresh_token))
        
        login_user(user, remember=True)
        
        return redirect(url_for('site.home'))

    return render_template('auth/signin.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user = User(form.data['email'], form.data['username'], generate_password_hash(form.data['password']))

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        return redirect(url_for('auth.spotify', id=user.id))
       
    return render_template("auth/signup.html", form=form)


@auth.route('/spotify', methods=['GET'])
@login_required
def spotify():
    params = {
        'client_id' : config.SPOTIFY_CLIENT_ID,
        'response_type' : 'code',
        'redirect_uri' : config.SPOTIFY_REDIRECT_URI,
        'scope' : config.SPOTIFY_SCOPE
    }
   
    return redirect(config.SPOTIFY_AUTH_URL + '/authorize?' + urllib.parse.urlencode(params))

@auth.route('/callback', methods=['GET'])
@login_required
def callback():
    if request.args.get('error') or not request.args.get('code'):
        abort(404)
    
    sportify_handler = Spotify(request.args.get('code'))
    user = User.get(current_user.get_id())
    user.access_token, user.refresh_token = sportify_handler.get_tokens()
    user.spotify_username = sportify_handler.get_spotify_username(user.access_token)

    db.session.add(Profile(user.username, user.spotify_username, ppd=sportify_handler.get_spotify_profile_picture_url(user.access_token)))
    db.session.commit()

    return redirect(url_for('site.home'))

@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('site.home'))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

