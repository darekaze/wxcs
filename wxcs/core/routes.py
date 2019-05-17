"""File handling core routes."""
from flask import Blueprint, flash, redirect, render_template, url_for, session
from wxcs.core.forms import StarterForm
from wxcs.core.utils import load_cases, get_cases_list, add_userlog

core = Blueprint('core', __name__)


@core.route('/', methods=['GET', 'POST'])
def starter():
    """Render starter page on start.

    Prevent starter again after simulation begins
    redirect user to progress
    """
    if 'userlog' in session:
        return redirect(url_for('core.drill'))

    cases = load_cases()
    case_menu = get_cases_list(cases)

    form = StarterForm()
    form.wxid.choices = [(0, 'Please Select...')] + case_menu

    if form.validate_on_submit():
        userlog = {field.name: field.data for field in form}
        add_userlog(userlog)
        session['userlog'] = userlog
        flash(f'Hi {form.name.data}! Welcome to the drill...', 'success')
        return redirect(url_for('core.drill'))

    return render_template('sim/starter.jinja', form=form)


@core.route('/drill')
def drill():
    """Route for handling drill case."""
    if 'userlog' not in session:
        return redirect(url_for('core.starter'))

    print(session['userlog'])
    # TODO: If ok, change the time and activate session['drilling'] = True
    return render_template('sim/drill.jinja')


@core.route('/ends')
def ender():
    """Display after the drill has ended."""
    session.pop('userlog', None)
    # TODO: Remove drilling status
    return render_template('sim/ender.jinja')
