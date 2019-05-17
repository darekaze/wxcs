"""File Handling forms in core module."""
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class StarterForm(FlaskForm):
    """Return the Starter form."""

    name = StringField(
        'Name', validators=[DataRequired(), Length(min=2, max=30)])
    post = StringField(
        'Post', validators=[DataRequired(), Length(min=1, max=20)])
    wxid = SelectField(
        'Weather Case', coerce=int, validators=[DataRequired()])
    role = SelectField(
        'Role', coerce=int, validators=[DataRequired()],
        choices=[(1, 'Forecaster'), (2, 'TC Consultant'), (3, 'Assistant Forecaster')])
    submit = SubmitField('Start')
