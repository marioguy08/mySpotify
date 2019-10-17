from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db, login_manager
from app.auth.models import User
from app.profiles.models import Profile
from app.spotify.models import Spotify
from app.profiles.forms import DeleteForm, SearchForm

profiles = Blueprint('profiles', __name__, url_prefix='/profile')

# TODO: Edit profiles
@profiles.route('/me', methods=['GET', 'POST']) 
@login_required
def me():
    profile         = Profile.get(current_user.get_id())
    user            = User.get(current_user.get_id())
    spotify_handler = Spotify()

    user.update_token(spotify_handler.refresh_access_token(user.refresh_token))
    
    return render_template('profiles/me.html', profile=profile)

@profiles.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form        = DeleteForm(request.form)
    user        = Profile.get(current_user.get_id())
    credentials = User.get(current_user.get_id())

    if request.method == 'POST' and form.validate():
        db.session.delete(user)
        db.session.delete(credentials)
        db.session.commit()

        return redirect(url_for('site.home'))
    
    return render_template('profiles/delete.html', form=form)

@profiles.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm(request.form)
    results = []

    if request.method == 'POST' and form.validate():
        results = Profile.query.filter(Profile.username.contains(form.data['username'])).all()

        if len(results) == 1:
            return redirect(url_for('profiles.user_page', id=results[0].id))

    return render_template('profiles/search.html', form=form, results=results)

@profiles.route('/user/<id>', methods=['GET'])
@login_required
def user_page(id):
    profile         = Profile.get(id)
    user            = User.get(id)
    spotify_handler = Spotify()


    if profile:
        user.update_token(spotify_handler.refresh_access_token(user.refresh_token))
        return render_template('profiles/profile.html', profile=Profile.get(id), spotify_id=spotify_handler.get_spotify_user_id(user.access_token))
    else:
        return 404
