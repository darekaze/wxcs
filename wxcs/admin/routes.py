"""File handling admin routes."""
from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from wxcs.models import Admin
from wxcs.admin.forms import LoginForm

admin = Blueprint('admin', __name__)

# ADMIN ROUTES
@admin.route('/admin')
@admin.route('/admin/dashboard')
@login_required
def dashboard():
    """Dashboard route."""
    return render_template('admin/dashboard.jinja')


@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Render admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin/login.jinja', title='Login', form=form)


@admin.route('/admin/logout')
@login_required
def logout():
    """Admin logout."""
    logout_user()
    return redirect(url_for('core.starter'))
