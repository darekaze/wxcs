from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

class StarterForm(FlaskForm):
  name = StringField(u'Name',
    validators=[DataRequired(), Length(min=2, max=30)])
  post = StringField(u'Post',
    validators=[DataRequired(), Length(min=1, max=20)])
  cases = SelectField(u'Weather Case', coerce=int)
  role = SelectField(u'Role', coerce=int,
    validators=[InputRequired()],
    choices=[(0, 'Forecaster'), (1, 'TC Consultant'), (2, 'Assistant Forecaster')]
  )
  submit = SubmitField('Start')
