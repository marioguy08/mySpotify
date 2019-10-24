import requests, urllib
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user

import config
from app import db, login_manager
from app.auth.forms import SigninForm, SignupForm
from app.auth.models import User
from app.profiles.models import Profile
from app.spotify.models import Spotify

api = Blueprint('api', __name__, url_prefix='/api')

def init(current_user, id=None):
    if id:
        user        = User.get(id)
    else:
        user        = User.get(current_user.get_id())
        
    spotify_handler = Spotify()

    user.update_token(spotify_handler.refresh_access_token(user.refresh_token))

    return user, spotify_handler

@api.route('/playlists/<id>', methods=['GET'])
@login_required
def playlists(id):
    user, spotify_handler = init(current_user)
    return jsonify({ 'playlists' : spotify_handler.get_spotify_user_playlists(user.access_token, id) })


@api.route('/playlists/me', methods=['GET'])
@login_required
def playlists_me():
    user, spotify_handler = init(current_user)
    return jsonify({ 'playlists' : spotify_handler.get_spotify_current_user_playlists(user.access_token) })


@api.route('/playlist/<id>', methods=['GET'])
@login_required
def playlist(id):
    user, spotify_handler = init(current_user)
    return jsonify({'tracks': spotify_handler.get_spotify_playlist_tracks(user.access_token, id)})

@api.route('/profiles/follow/<id>', methods=['POST'])
@login_required
def follow(id):
    s_user = Profile.get(id)
    c_user = Profile.get(current_user.get_id())

    if c_user.username in s_user.followers.split(','): #if already following user, remove from following
        s_user.followers = ','.join(list(filter(None, s_user.followers.replace(c_user.username, '').split(','))))
        c_user.following = ','.join(list(filter(None, c_user.following.replace(s_user.username, '').split(','))))
    else: 
        if s_user.followers == '':
            s_user.followers = c_user.username
        else:
            s_user.followers = '{},{}'.format(s_user.followers, c_user.username)

        if c_user.following == '':
            c_user.following = s_user.username
        else:
            c_user.following = '{},{}'.format(s_user.following, s_user.username)

    db.session.commit()

    return jsonify({ s_user.username: { 'following': s_user.following, 'followers': s_user.followers }, c_user.username: { 'following': s_user.following, 'followers': s_user.followers } })

@api.route('/profiles/followers/<id>', methods=['GET'])
@login_required
def followers(id):
    return jsonify({'followers' : Profile.get(id).followers})
        

@api.route('/profiles/following/<id>', methods=['GET'])
@login_required
def following(id):
    return jsonify({'following': Profile.get(id).following})
