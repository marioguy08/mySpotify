from flask_login import current_user
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.auth.models import User


class DeleteForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    def validate_username(self, username):
        if not username.data \
            or len(username.data) > 32 \
            or username.data != User.get(current_user.get_id()).username:
            raise ValidationError('Input doesn\'t match username.')


class SearchForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    def validate_username(self, username):
        if not username.data or len(username.data) > 32:
            raise ValidationError('Input doesn\'t match username.')
