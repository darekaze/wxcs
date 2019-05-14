"""File Handling forms in admin."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Return the login form (for admin)."""

    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField(
        'Password', validators=[DataRequired()])
    submit = SubmitField('Login')
