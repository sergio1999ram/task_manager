from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length


class TaskForm(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired(), Length(min=5, max=99,
                                                                           message='Title must have from 5 to 99 characters long.')])
    description = TextAreaField(label="Description", validators=[Length(min=10, max=255)])
