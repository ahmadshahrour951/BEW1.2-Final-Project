from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from socialorm_app.models import User
from socialorm_app.auth.forms import SignUpForm, LoginForm
from socialorm_app import bcrypt, db

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            email=form.email.data,
            password=hashed_password,
            name=form.name.data,
            dob=form.dob.data,
            dorm_room=form.dorm_room.data,
            residence=form.residence.data,
        )

        db.session.add(user)
        db.session.commit()

        flash('Account Created.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
  
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
