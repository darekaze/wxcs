"""File handling core routes."""
from flask import Blueprint, redirect, render_template, url_for, session
from wxcs import pages
from wxcs.core.forms import StarterForm
from wxcs.core.utils import load_cases, get_cases_list, set_userlog, init_drill, end_drill

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
        set_userlog(userlog)
        return redirect(url_for('core.drill'))

    return render_template('sim/starter.jinja', form=form)


@core.route('/drill')
def drill():
    """Route for handling drill case."""
    if 'userlog' not in session:
        return redirect(url_for('core.starter'))

    if 'drill' not in session:
        init_drill(session['userlog']['wxid'])
    case = session['drill']
    guide = pages.get(f'contents/{case["codename"]}')
    log = pages.get(f'logs/{case["log"]}')
    return render_template('sim/drill.jinja', case=case, guide=guide, log=log)


@core.route('/ends')
def ender():
    """Display after the drill has ended."""
    end_drill() if 'drill' in session else None
    return render_template('sim/ender.jinja')
