from sqlalchemy.orm import backref
from socialorm_app import db
from flask_login import UserMixin

class Institution(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)

  def __repr__(self):
    return f'<Institution: {self.name}>'

class Residence(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
  institution = db.relationship('Institution', back_populates='residences')

  def __repr__(self):
    return f'<Residence: {self.name}>'

user_followers = db.Table('user_followers',
    db.Column('user_follower_id', db.Integer, primary_key=True),
    db.Column('followee_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  name = db.Column(db.String(80), nullable=False)
  status = db.Column(db.String(80), nullable=False)
  dob = db.Column(db.DateTime, nullable=False)
  dorm_room = db.Column(db.String(5), nullable=False)
  residence_id = db.Column(db.Integer, db.ForeignKey('residence.id'), nullable=False)
  residence = db.relationship('Residence', back_populates='users')
  followers = db.relationship('User', secondary=user_followers, 
  primaryjoin=id==user_followers.c.followee_id, 
  secondaryjoin=id==user_followers.c.follower_id, 
  backref=backref('followers')
  )

  def __repr__(self):
        return f'<User: {self.email}>'

