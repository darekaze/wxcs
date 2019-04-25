"""File handling routes."""
from flask import flash, redirect, render_template, url_for

from wxcs import app, db
from wxcs.forms import StarterForm


class User(db.Model):
    """The user model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    post = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
@app.route('/start', methods=['GET', 'POST'])
def starter():
    """Render starter page on start.

    Prevent starter again after simulation begins
    redirect user to progress
    """
    form = StarterForm()
    form.cases.choices = [(1, 'Choose...')]
    # TODO: fetch weather case selections from database

    if form.validate_on_submit():
        # TODO: insert record to userlog table
        flash(f'Drill initialized!! {form.name.data}', 'success')
        return redirect(url_for('temp'))
    return render_template('starter.jinja', form=form)


@app.route('/temp')
def temp():
    """Temp route."""
    return render_template('temp.jinja')
