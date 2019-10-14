from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.auth.models import User

class SignupForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])                           
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired()])
    recaptcha   = RecaptchaField()

    def validate_username(self, username):
        if not username.data:
            raise ValidationError('Please enter a username.')
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('That username is taken. Please choose another.')
        if len(username.data) > 32:
            raise ValidationError('That username is too long. Please enter another.')

    def validate_email(self, email):
        if not email.data:
            raise ValidationError('Please enter an email.')
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('That email is taken. Please choose another.')

class SigninForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])                           
    password    = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, username):
        if not username.data:
            raise ValidationError('Please enter a username.')
        if len(username.data) > 32:
            raise ValidationError('That username is too long. Please try again.')