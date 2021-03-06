from unittest import TestCase

from datetime import date

from socialorm_app import app, db, bcrypt
from socialorm_app.models import Institution, Residence, User

"""
Run these tests with the command:
python3 -m unittest socialorm_app.auth.tests
"""

#################################################
# Setup
#################################################


def create_residences():
    # Mock an institution and residence, this is required to create a user
    in1 = Institution(name='Make School')
    res1 = Residence(name='The Herbert Hotel',
                     address='161 Powell St, San Francisco', institution=in1)

    db.session.add(in1)
    db.session.add(res1)
    db.session.commit()


def create_user():
   # Mock a user, a user belongs to a residence that we created above
    res_1 = Residence.query.filter_by(name='The Herbert Hotel').one()

    user_1_obj = {
        'email': 'test_1@gmail.com',
        'password': 'password_1',
        'name': 'test_1',
        'dob': date(2000, 1, 1),
        'residence_id': res_1.id,
        'dorm_room': '100'
    }

    password_hash_1 = bcrypt.generate_password_hash(
        user_1_obj['password']).decode('utf-8')
    user_1_obj['password'] = password_hash_1

    user = User(
        email=user_1_obj['email'],
        password=user_1_obj['password'],
        name=user_1_obj['name'],
        dob=user_1_obj['dob'],
        residence_id=user_1_obj['residence_id'],
        dorm_room=user_1_obj['dorm_room']
    )
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        # this test should succesffully allow a user to signup
        create_residences()
        in1 = Institution.query.filter_by(name='Make School').one()
        res1 = Residence.query.filter_by(name='The Herbert Hotel').one()

        data = {
            'email': 'test_1@gmail.com',
            'password': 'password_1',
            'confirm_password': 'password_1',
            'name': 'test_1',
            'dob': date(2000, 1, 1),
            'institution': in1.id,
            'residence': res1.id,
            'dorm_room': '100'
        }

        self.app.post('/signup', data=data)

        user = User.query.filter_by(email='test_1@gmail.com').first()

        self.assertIsNotNone(user)
        self.assertEqual('test_1@gmail.com', user.email)

    def test_signup_existing_user(self):
        # This should reject the user if the user wants to signup again with an existing account in the database
        create_residences()
        in1 = Institution.query.filter_by(name='Make School').one()
        res1 = Residence.query.filter_by(name='The Herbert Hotel').one()

        data = {
            'email': 'test_1@gmail.com',
            'password': 'password_1',
            'confirm_password': 'password_1',
            'name': 'test_1',
            'dob': date(2000, 1, 1),
            'institution': in1.id,
            'residence': res1.id,
            'dorm_room': '100'
        }

        self.app.post('/signup', data=data)

        response = self.app.post('/signup', data=data)
        response_text = response.get_data(as_text=True)

        self.assertIn(
            'That email is taken. Please choose a different one.', response_text)

    def test_login_correct_password(self):
        # This test should succesffully log a user in knowing the password and email are correct
        create_residences()
        create_user()

        data = {
            'email': 'test_1@gmail.com',
            'password': 'password_1'
        }

        response = self.app.post(
            '/login', data=data,  follow_redirects=True)
        response_text = response.get_data(as_text=True)

        # This is a direct way to know if the user is actually logged in from the navbar in base.html
        self.assertNotIn('Log In', response_text)
        self.assertIn('Profile', response_text)

    def test_login_nonexistent_user(self):
      # Testing a login which does not exist in the database, it should reject the request
        create_residences()
        create_user()

        data = {
            'email': 'test_2@gmail.com',
            'password': 'password_1',
        }

        res = self.app.post('/login', data=data,  follow_redirects=True)
        res_text = res.get_data(as_text=True)

        self.assertNotIn('Log Out', res_text)
        self.assertIn('No user with that email. Please try again.', res_text)

    def test_login_incorrect_password(self):
      # This tests if the passwords do not match, it should reject the user
        create_residences()
        create_user()

        data = {
            'email': 'test_1@gmail.com',
            'password': 'password_2',
        }

        res = self.app.post('/login', data=data,  follow_redirects=True)
        res_text = res.get_data(as_text=True)

        self.assertNotIn('Log Out', res_text)
        self.assertIn(
            "Password doesn&#39;t match. Please try again.", res_text)

    def test_logout(self):
        # This tests when a user does login, and then logs out.
        create_residences()
        create_user()

        data = {
            'email': 'test_1@gmail.com',
            'password': 'password_1',
        }

        self.app.post('/login', data=data,  follow_redirects=True)

        res = self.app.get('/logout', follow_redirects=True)
        res_text = res.get_data(as_text=True)
        self.assertIn('Log In', res_text)
