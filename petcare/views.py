from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, login_user, current_user, logout_user
from petcare import app, db, login_manager

from petcare.mailSender import send_registration_confirmation_mail
from petcare.token import generate_confirmation_token, confirm_token

from sqlalchemy.exc import IntegrityError

import datetime

from petcare.forms import UserForm, ServiceForm, LoginForm
from petcare.models import User, Service

############################################


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


def store_user(email, display_name, password, role=0,
               first_name=None, surname=None):

    u = User(email=email, password=password,
             display_name=display_name, role=role,
             first_name=first_name, surname=surname)
    try:
        db.session.add(u)
        db.session.commit()
    except IntegrityError:
        return False
    return u


def store_service(service_name, description=None):
    s = Service(service_name=service_name, user=current_user, description=description)
    try:
        db.session.add(s)
        db.session.commit()
    except IntegrityError:
        return False
    return True
############################################


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/login', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    # If method == POST
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)

        if user is not None:
            if user.check_password(password):
                if user.confirmed:
                    login_user(user, form.remember_me.data)
                    flash(f'Succesfully logged in as {email}')
                    return redirect(request.args.get('next') or url_for('index'))
                else:
                    flash('Please confirm your email first!')
            else:
                flash('Incorrect password')
        else:
            flash(f'User with email {email} does not exist.')
    
    # If method == GET
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        display_name = form.display_name.data
        first_name = form.first_name.data
        surname = form.surname.data

        if user := store_user(email, password, display_name, first_name=first_name,
                      surname=surname):

            token = generate_confirmation_token(user.email)

            confirm_url = url_for('confirm_email', token=token, _external=True)
            send_registration_confirmation_mail(email, confirm_url)
            flash("Your account has succesfully been created. Please login.")
            return redirect(url_for('login'))
        else:
            flash(f'There is already an account registered with this email \
                ({email}).')
    return render_template('user/register.html', form=form)

@app.route('/user/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    
    user = User.get_by_email(email)
    if user.confirmed:
        flash('Account already confirmed. Please login.')
        return redirect(url_for('login'))
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        User.update(user)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))


@app.route('/service/add', methods=['GET', 'POST'])
@login_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service_name = form.service_name.data
        description = form.description.data

        if store_service(service_name, description=description):
            return redirect(url_for('index'))
        else:
            flash(f'An error occured.')
    return render_template('add_service.html', form=form)
