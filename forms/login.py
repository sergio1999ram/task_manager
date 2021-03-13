from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired(), Length(min=1, max=99,
                                                                                 message='Username must be between 1 and 99 letters.')],
                           render_kw={'style': 'clear:both; width:100%'})
    password = PasswordField('Password', [InputRequired()], render_kw={'style': 'clear:both; width:100%'})
