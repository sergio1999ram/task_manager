from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import *

from app_config import db


class RegisterForm(FlaskForm):
    fullname = StringField(label='Full Name', validators=[InputRequired(), Length(min=1, max=99,
                                                                                  message='Name must be between 1 and 99 letters.')],
                           render_kw={'style': 'clear:both; width:100%'})
    email = EmailField(label='Email', validators=[InputRequired(), Length(min=1, max=140,
                                                                          message='Email must be between 1 and 140 letters.')],
                       render_kw={'style': 'clear:both; width:100%'})
    username = StringField(label='Username', validators=[InputRequired(), Length(min=1, max=99,
                                                                                 message='Username must be between 1 and 99 letters.')],
                           render_kw={'style': 'clear:both; width:100%'})
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')],
                             render_kw={'style': 'clear:both; width:100%'})
    confirm = PasswordField('Repeat Password',
                            render_kw={'style': 'clear:both; width:100%'})

    def validate_email(forms, field):
        temp_user = db.users.find_one({"email": field.data})
        if temp_user:
            raise ValidationError('Email already in use')
        if '@' not in field.data:
            raise ValidationError('Type a valid email')

    def validate_username(forms, field):
        temp_user = db.users.find_one({"username": field.data})
        if temp_user:
            raise ValidationError('Username already in use')
