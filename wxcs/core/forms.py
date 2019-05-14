"""File Handling forms in core module."""
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length


class StarterForm(FlaskForm):
    """Return the Starter form."""

    name = StringField(
        'Name', validators=[DataRequired(), Length(min=2, max=30)])
    post = StringField(
        'Post', validators=[DataRequired(), Length(min=1, max=20)])
    cases = SelectField('Weather Case', coerce=int)
    role = SelectField(
        'Role', coerce=int, validators=[InputRequired()],
        choices=[(0, 'Forecaster'), (1, 'TC Consultant'), (2, 'Assistant Forecaster')])
    submit = SubmitField('Start')