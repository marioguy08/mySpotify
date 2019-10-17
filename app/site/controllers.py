from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db, login_manager
from app.auth.models import User
from app.profiles.models import Profile
from app.spotify.models import Spotify

site = Blueprint('site', __name__, url_prefix='/')

@site.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return render_template('site/index_anonymous.html')

    profile         = Profile.get(current_user.id)
    user            = User.get(current_user.get_id())
    spotify_handler = Spotify()

    user.update_token(spotify_handler.refresh_access_token(user.refresh_token))

    return render_template('site/index_signedin.html', current_user=current_user)
