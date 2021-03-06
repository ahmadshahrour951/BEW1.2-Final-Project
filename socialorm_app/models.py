from sqlalchemy.orm import backref
from socialorm_app import db
from flask_login import UserMixin

class Institution(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  # one-to-many relation
  residences = db.relationship('Residence', back_populates='institution')

  def __str__(self):
    return f'<Institution: {self.name}>'

  def __repr__(self):
    return f'<Institution: {self.name}>'

class Residence(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  address = db.Column(db.String(200), nullable=False)
  institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
  # one-to-many relation
  institution = db.relationship('Institution', back_populates='residences')
  # one-to-many relation
  users = db.relationship('User', back_populates='residence')

  def __str__(self):
    return f'<Residence: {self.name}>'

  def __repr__(self):
    return f'<Residence: {self.name}>'

#Creating the many-tomany table for future relationship creation in the User Table
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
  status = db.Column(db.String(80), nullable=False, default='Available')
  dob = db.Column(db.Date, nullable=False)
  dorm_room = db.Column(db.String(5), nullable=False)
  residence_id = db.Column(db.Integer, db.ForeignKey('residence.id'), nullable=False)
  # populate the residence when requested in code
  residence = db.relationship('Residence', back_populates='users')
  # Many to many relationship creation is created here by self reference via user_followers table
  followers = db.relationship(
  'User', 
  secondary=user_followers, 
  primaryjoin=id==user_followers.c.followee_id, 
  secondaryjoin=id==user_followers.c.follower_id, 
  backref=backref('followees')
  )

  def __str__(self):
        return f'<User: {self.email}>'

  def __repr__(self):
        return f'<User: {self.email}>'

