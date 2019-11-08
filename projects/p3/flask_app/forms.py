from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, NumberRange, Length

class PostForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=1, max=128)])
    email  = StringField('Email',  validators=[DataRequired(), Length(min=1, max=128)])

    # post data
    title   = StringField('Title',   validators=[DataRequired(), Length(min=1, max=128)])
    content = StringField('Content', validators=[DataRequired(), Length(min=1, max=2048)])
    date    = DateField('Date',      validators=[DataRequired()], format='%B %d, %Y')
    # example date: September 30, 2019

class CommentForm(FlaskForm):
    author  = StringField('Author',  validators=[DataRequired(), Length(min=1, max=128)])
    content = StringField('Content', validators=[DataRequired(), Length(min=1, max=2048)])

    date    = DateField('Date',      validators=[DataRequired()], format='%B %d, %Y')