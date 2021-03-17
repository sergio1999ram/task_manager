from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length


class TaskForm(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired(), Length(min=5, max=99,
                                                                           message='Title must be between 5 and 99 characters long.')])
    description = TextAreaField(label="Description", validators=[
        Length(min=10, max=255, message='Description must be between 10 and 255 characters long.')])
