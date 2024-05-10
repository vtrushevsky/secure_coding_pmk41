from flask import Blueprint, render_template, request, flash, redirect, url_for, escape
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re
from datetime import datetime
from .logger import Logger


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. Log out first!', category='LoginError')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = escape(request.form.get('email'))
        password = escape(request.form.get('password'))

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                           f'({email}) logged in successfully.')
                return redirect(url_for('views.home'))
            else:
                # Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                #            f'({email}) failed to logged in.')
                flash('Incorrect password, try again.', category='LoginError')
        else:
            # Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] User: '
            #            f'({email}) attempted to log in. No such user in DB.')
            flash('Email does not exist.', category='LoginError')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        flash('You are already logged in. Log out first!', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        surname = request.form.get('surname')
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        phone_number = request.form.get('phone_number')
        role = 'User'
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='SignUpError')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='SignUpError')
        elif not re.match(r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]{2,}$', email):
            flash('Email pattern should be like "email_address@your_domain.tld.', category='SignUpError')
        elif len(surname) < 2:
            flash('Username must be greater than 1 character.', category='SignUpError')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='SignUpError')
        elif len(password1) < 12 or not \
                re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', password1):
            flash('Password must be at least 12 characters, '
                  'contain uppercase and lowercase letters and special characters.', category='SignUpError')
        else:
            new_user = User(email=email, surname=surname, name=name, birth_date=birth_date, phone_number=phone_number,
                            role=role, password=generate_password_hash(password=password1, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            print(db.Table.columns)
            login_user(new_user, remember=True)
            Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                       f'({email}) has registered successfully.')
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signUp.html", user=current_user)
