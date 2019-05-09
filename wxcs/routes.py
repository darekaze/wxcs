"""File handling routes."""
from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user
from . import app
from .forms import LoginForm, StarterForm
from .models import Admin, UserLog


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


# ADMIN ROUTES
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
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin/login.jinja', title='Login', form=form)


@app.route('/admin/logout')
def logout():
    """Admin logout."""
    logout_user()
    return redirect(url_for(starter))
