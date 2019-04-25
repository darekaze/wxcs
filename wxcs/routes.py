from flask import render_template, url_for, flash, redirect
from wxcs import app
from wxcs.forms import StarterForm

"""
Render starter page on start, and prevent starter again after simulation begins
redirect user to progress
"""
@app.route("/", methods=['GET', 'POST'])
@app.route("/start", methods=['GET', 'POST'])
def starter():
  form = StarterForm()
  form.cases.choices = [(1, 'Choose...')]
  # TODO: fetch weather case selections from database

  if form.validate_on_submit():
    # TODO: insert record to userlog table
    flash(f'Drill initialized!! {form.name.data}', 'success')
    return redirect(url_for('temp'))
  return render_template('starter.jinja', form=form)

@app.route("/temp")
def temp():
  return render_template('temp.jinja')
