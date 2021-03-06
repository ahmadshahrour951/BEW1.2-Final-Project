from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from socialorm_app.models import User
from socialorm_app.main.forms import ProfileForm
from socialorm_app import db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


# all pages are required to have login, this is because all features are only available in a residence
@main.route('/')
@login_required
def homepage():
   # Providing the list of users within the same residence
    users = User.query.filter_by(residence_id=current_user.residence_id).all()
    users.remove(current_user)
    return render_template('home.html', users=users)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  # Displaying the current users details, and the user can update them
  form = ProfileForm(obj=current_user)
  if form.validate_on_submit():
    current_user.dob = form.dob.data
    current_user.residence = form.residence.data
    current_user.dorm_room = form.dorm_room.data
    current_user.status = form.status.data

    db.session.commit()
  return render_template('profile.html',  form=form)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required
def user_detail(user_id):
  # Displaying another use within the same residence details
  user = User.query.get(user_id)
  is_following = user in current_user.followees
  return render_template('user_detail.html', user=user, is_following=is_following)

@main.route('/follow', methods=['POST'])
@login_required
def follow():
  # Providing the follow fuctionality, this is where the many to many inserts happens
  followee_id = request.form.get('followee_id')
  followee = User.query.get(followee_id)
  current_user.followees.append(followee)
  db.session.commit()
  return redirect(url_for('main.user_detail', user_id=followee_id))

@main.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
  # Providing the unfollow fuctionality, this is where row can be removed based on many to many
  followee_id = request.form.get('followee_id')
  followee = User.query.get(followee_id)
  current_user.followees.remove(followee)
  db.session.commit()
  return redirect(url_for('main.user_detail', user_id=followee_id))

@main.route('/followers', methods=['GET'])
@login_required
def followers():
  # this just displays all followers of the current user.
  return render_template('followers.html')
