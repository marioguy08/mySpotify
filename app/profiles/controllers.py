from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db, login_manager
from app.auth.models import User
from app.profiles.models import Profile
from app.spotify.models import Spotify
from app.profiles.forms import DeleteForm

profiles = Blueprint('profiles', __name__, url_prefix='/profile')

# TODO: Edit profiles
@profiles.route('/me', methods=['GET', 'POST']) 
@login_required
def me():
    user        = Profile.get(current_user.get_id())
    credentials = User.get(current_user.get_id())
    spotify     = Spotify()

    credentials.update_token(spotify.refresh_access_token(credentials.refresh_token))

    # ... you could always paginate this data to save load times
    playlists = spotify.get_spotify_user_playlists(credentials.access_token)
    
    names = []
    for playlist in playlists:
        names.append(playlist['name'])
    
    return render_template('profiles/me.html', user=user, number_of_playlists=len(playlists), playlists=names)

@profiles.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm(request.form)
    
    user        = Profile.get(current_user.get_id())
    credentials = User.get(current_user.get_id())

    if request.method == 'POST' and form.validate():
        db.session.delete(user)
        db.session.delete(credentials)
        db.session.commit()

        return redirect(url_for('site.home'))
    
    return render_template('profiles/delete.html', form=form)
