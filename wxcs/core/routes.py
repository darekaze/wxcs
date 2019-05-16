"""File handling core routes."""
from flask import Blueprint, flash, redirect, render_template, url_for
from wxcs.core.forms import StarterForm

core = Blueprint('core', __name__)


@core.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('core.drill'))
    return render_template('sim/starter.jinja', form=form)


@core.route('/drill')
def drill():
    """Temp route."""
    return render_template('sim/drill.jinja')
