from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField

from models import User


class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[validators.InputRequired(), validators.Length(min=1, max=99,
                                                                                               message='Name must be between 1 and 99 letters.')],
                       render_kw={'style': 'clear:both; width:100%'})
    lastname = StringField(label='Lastname', validators=[validators.InputRequired(), validators.Length(min=1, max=99,
                                                                                                       message='Lastname must be between 1 and 99 letters.')],
                           render_kw={'style': 'clear:both; width:100%'})
    email = EmailField(label='Email', validators=[validators.InputRequired(), validators.Length(min=1, max=140,
                                                                                                message='Email must be between 1 and 140 letters.')],
                       render_kw={'style': 'clear:both; width:100%'})
    username = StringField(label='Username', validators=[validators.InputRequired(), validators.Length(min=1, max=99,
                                                                                                       message='Username must be between 1 and 99 letters.')],
                           render_kw={'style': 'clear:both; width:100%'})
    password = PasswordField(label='Password', validators=[validators.InputRequired(), validators.Length(min=1, max=150,
                                                                                                         message='Password must be between 1 and 150 letters.'),
                                                           validators.EqualTo('confirm',
                                                                              message='Passwords don\'t match')],
                             render_kw={'style': 'clear:both; width:100%'})
    confirm = PasswordField(label='Confirm Password', validators=[validators.InputRequired()],
                            render_kw={'style': 'clear:both; width:100%'})

    def validate_email(forms, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already in use')
        if '@' not in field.data:
            raise ValidationError('Type a valid email')

    def validate_username(forms, field):
        user = User.query.filter_by(username=field.data)
        if user:
            return ValidationError('Username already in use')