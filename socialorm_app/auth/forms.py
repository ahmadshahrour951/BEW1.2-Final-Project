from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email
from socialorm_app.models import Institution, Residence, User
from socialorm_app import bcrypt
from wtforms.fields.html5 import DateField


class SignUpForm(FlaskForm):
    name = StringField(label='Name',  validators=[DataRequired(), Length(min=3, max=50)])
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    institution = QuerySelectField(label='Institution', query_factory=lambda: Institution.query, allow_blank=False, get_label='name')
    residence = QuerySelectField(label='Residence', query_factory=lambda: Residence.query, allow_blank=False, get_label='name')
    dorm_room = StringField(label='Dorm Room', validators=[DataRequired(), Length(min=3, max=5)])
    email = StringField(label='Email', validators=[DataRequired(), Length(min=3, max=80), Email(message='Invalid email format')], )
    password = PasswordField(label='Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
    def validate_residence(self, residence):
        if residence.data.institution != self.institution.data:
          raise ValidationError(f'{residence.data.name} is not part of {self.institution.data.name}')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No user with that email. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')