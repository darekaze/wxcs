"""File handling core routes."""
from flask import Blueprint, flash, redirect, render_template, url_for
from wxcs.core.forms import StarterForm
from wxcs.core.utils import load_cases, get_cases_list

core = Blueprint('core', __name__)


@core.route('/', methods=['GET', 'POST'])
def starter():
    """Render starter page on start.

    Prevent starter again after simulation begins
    redirect user to progress
    """
    cases = load_cases()
    case_menu = get_cases_list(cases)

    form = StarterForm()
    form.cases.choices = [(0, 'Please Select...')] + case_menu

    if form.validate_on_submit():
        if form.cases.data:
            # TODO: insert record to userlog table
            flash(f'Hi {form.name.data}! Welcome to ...', 'success')
            return redirect(url_for('core.drill'))
        else:
            flash('Please select a weather case to continue...', 'warning')
    return render_template('sim/starter.jinja', form=form)


@core.route('/drill')
def drill():
    """Route for handling drill case."""
    return render_template('sim/drill.jinja')
