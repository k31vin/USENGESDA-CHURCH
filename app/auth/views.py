from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from . import auth
from ..models import User, Role
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # Log user in
            login_user(user, form.remember_me.data)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                if user.role.name == 'Administrator':
                    next_url = url_for('admin.dashboard')
                elif user.role.name == 'User':
                    next_url = url_for('main.index')
                else:
                    next_url = url_for('main.index')
            return redirect(next_url)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    role = Role.query.filter_by(name='User').first()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role=role)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
