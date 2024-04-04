from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from yord_website.extensions import db, login_manager
from yord_website.models import User, LoginForm


auth_bp = Blueprint(
    'auth', __name__, 
    template_folder='templates',
    url_prefix='/auth'
)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page
    
    For GET requests, the login form is displayed.
    For POST requests, the user is logged in by submitting the form.
    """

    if current_user.is_authenticated:
            return redirect(url_for('mailing.view_members'))
    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.username.data
        password = form.password.data

        user = db.session.scalar(db.select(User).filter_by(email=email))

        if user is None or not user.check_password(password):
            error_login_alert = True
            return render_template('auth/login.html', error_login_alert=error_login_alert, form=form)
        
        user.is_active = True
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('mailing.view_members'))
    print(form.errors)
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    """Logout the current user"""
    logout_user()

    return redirect(url_for('general.home'))