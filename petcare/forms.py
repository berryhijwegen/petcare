from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, email, EqualTo


class UserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), email()])
    password = PasswordField('Password ', validators=[DataRequired()])
    password_validate = PasswordField('Validate password ', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    display_name = StringField('Display Name', validators=[DataRequired()])
    first_name = StringField('First Name')
    surname = StringField('Surname')


class ServiceForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired()])
    description = StringField('Description')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), email()])
    password = PasswordField('Password ', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
