from flask import render_template, url_for, flash, redirect
from wxcs import app
from wxcs.forms import RegistrationForm

app.config['SECRET_KEY'] = 'lalalalala' # HACK: temp

"""
Render register page on start, and prevent register and redirect
user to progress while simulation begins
"""
@app.route("/", methods=['GET', 'POST'])
@app.route("/start", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  form.cases.choices = [(1, 'Choose...')]
  # TODO: fetch weather case selections from database

  if form.validate_on_submit():
    flash(f'Drill Start!! {form.name.data}', 'success')
    return redirect(url_for('temp'))
  return render_template('start.jinja', form=form)

@app.route("/temp")
def temp():
  return render_template('temp.jinja')
