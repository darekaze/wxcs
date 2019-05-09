"""File handling routes."""
from flask import flash, redirect, render_template, url_for

from wxcs import app
from wxcs.forms import LoginForm, StarterForm
from wxcs.models import Admin, UserLog


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


@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dashboard():
    """Dashboard route."""
    return render_template('admin/dashboard.jinja')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Render admin login page."""
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'r2admin' and form.password.data == 'password':
            flash('Welcome!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin/login.jinja', title='Login', form=form)
