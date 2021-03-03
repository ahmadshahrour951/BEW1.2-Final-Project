from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
# from datetime import date, datetime
from socialorm_app.models import Institution, Residence, User
# from socialorm_app.main.forms import 
from socialorm_app import bcrypt

# Import app and db from events_app package so that we can run app
from socialorm_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
@login_required
def homepage():
  #DONT FORGET TO REMOVE current_user FROM users
    users = User.query.filter_by(residence_id=current_user.residence_id)
    return render_template('home.html', users=users)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required
def user_detail(user_id):
  pass
