from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db, login_manager

site = Blueprint('site', __name__, url_prefix='/')

@site.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('site/index_signedin.html', current_user=current_user)
    else:
        return render_template('site/index_anonymous.html')