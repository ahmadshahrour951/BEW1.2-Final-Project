from unittest import TestCase

from datetime import date

from socialorm_app import app, db, bcrypt
from socialorm_app.models import Institution, Residence, User

"""
Run these tests with the command:
python3 -m unittest socialorm_app.main.tests
"""

#################################################
# Setup
#################################################

#################################################
# Setup
#################################################


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def create_residences():
    in1 = Institution(name='Make School')
    res1 = Residence(name='The Herbert Hotel',
                     address='161 Powell St, San Francisco', institution=in1)

    in2 = Institution(name='University of California, Berkeley')
    res2 = Residence(name='Nob Hill Guesthouse by FOUND',
                     address='851 California St, San Francisco', institution=in2)

    db.session.add(in1)
    db.session.add(res1)

    db.session.add(in2)
    db.session.add(res2)

    db.session.commit()


def create_users():
    res_1 = Residence.query.filter_by(name='The Herbert Hotel').one()
    res_2 = Residence.query.filter_by(
        name='Nob Hill Guesthouse by FOUND').one()

    user_1_obj = {
        'email': 'test_1@gmail.com',
        'password': 'password_1',
        'name': 'test_1',
        'dob': date(2000, 1, 1),
        'residence_id': res_1.id,
        'dorm_room': '101'
    }

    user_1_obj['password'] = bcrypt.generate_password_hash(
        user_1_obj['password']).decode('utf-8')

    user_1 = User(
        email=user_1_obj['email'],
        password=user_1_obj['password'],
        name=user_1_obj['name'],
        dob=user_1_obj['dob'],
        residence_id=user_1_obj['residence_id'],
        dorm_room=user_1_obj['dorm_room']
    )
    db.session.add(user_1)

    user_2_obj = {
        'email': 'test_2@gmail.com',
        'password': 'password_2',
        'name': 'test_2',
        'dob': date(2000, 1, 1),
        'residence_id': res_1.id,
        'dorm_room': '102'
    }

    user_2_obj['password'] = bcrypt.generate_password_hash(
        user_2_obj['password']).decode('utf-8')

    user_2 = User(
        email=user_2_obj['email'],
        password=user_2_obj['password'],
        name=user_2_obj['name'],
        dob=user_2_obj['dob'],
        residence_id=user_2_obj['residence_id'],
        dorm_room=user_2_obj['dorm_room']
    )
    db.session.add(user_2)

    user_3_obj = {
        'email': 'test_3@gmail.com',
        'password': 'password_3',
        'name': 'test_3',
        'dob': date(2000, 1, 1),
        'residence_id': res_2.id,
        'dorm_room': '103'
    }

    user_3_obj['password'] = bcrypt.generate_password_hash(
        user_3_obj['password']).decode('utf-8')

    user_3 = User(
        email=user_3_obj['email'],
        password=user_3_obj['password'],
        name=user_3_obj['name'],
        dob=user_3_obj['dob'],
        residence_id=user_3_obj['residence_id'],
        dorm_room=user_3_obj['dorm_room']
    )
    db.session.add(user_3)

    db.session.commit()

#################################################
# Tests
#################################################


class MainTests(TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)

        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)
        self.assertIn('Enter your credentials', response_text)

        self.assertNotIn('Profile', response_text)
        self.assertNotIn('Followers', response_text)
        self.assertNotIn('Log Out', response_text)

    def test_homepage_logged_in(self):
        create_residences()
        create_users()
        login(self.app, 'test_1@gmail.com', 'password_1')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)

        self.assertIn('Profile', response_text)
        self.assertIn('Followers', response_text)
        self.assertIn('Log Out', response_text)

        self.assertIn('test_2', response_text)
        self.assertIn('Status: Available', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)
        self.assertNotIn('test_3', response_text)

    def test_user_detail_logged_in(self):
        create_residences()
        create_users()
        login(self.app, 'test_1@gmail.com', 'password_1')

        response = self.app.get('/user/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Profile', response_text)
        self.assertIn('Followers', response_text)
        self.assertIn('Log Out', response_text)

        self.assertIn('test_2', response_text)
        self.assertIn('Birthday: 2000-01-01', response_text)
        self.assertIn('Dorm room: 102', response_text)
        self.assertIn('Status: Available', response_text)
        self.assertIn('Follow', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)
        self.assertNotIn('Unfollow', response_text)
    
    def test_user_follow(self):
      create_residences()
      create_users()
      login(self.app, 'test_1@gmail.com', 'password_1')

      data = {
        'followee_id': 2
      }

      response = self.app.post('/follow', data=data, follow_redirects=True)
      self.assertEqual(response.status_code, 200)

      response_text = response.get_data(as_text=True)
      self.assertIn('Profile', response_text)
      self.assertIn('Followers', response_text)
      self.assertIn('Log Out', response_text)

      self.assertIn('test_2', response_text)
      self.assertIn('Birthday: 2000-01-01', response_text)
      self.assertIn('Dorm room: 102', response_text)
      self.assertIn('Status: Available', response_text)
      self.assertIn('Unfollow', response_text)

      self.assertNotIn('Log In', response_text)
      self.assertNotIn('Sign Up', response_text)
      # self.assertNotIn('Follow', response_text)

    def test_user_unfollow(self):
      create_residences()
      create_users()
      login(self.app, 'test_1@gmail.com', 'password_1')

      data = {
          'followee_id': 2
      }

      self.app.post('/follow', data=data, follow_redirects=True)
      response = self.app.post('/unfollow', data=data, follow_redirects=True)
      self.assertEqual(response.status_code, 200)

      response_text = response.get_data(as_text=True)
      self.assertIn('Profile', response_text)
      self.assertIn('Followers', response_text)
      self.assertIn('Log Out', response_text)

      self.assertIn('test_2', response_text)
      self.assertIn('Birthday: 2000-01-01', response_text)
      self.assertIn('Dorm room: 102', response_text)
      self.assertIn('Status: Available', response_text)
      self.assertIn('Follow', response_text)

      self.assertNotIn('Log In', response_text)
      self.assertNotIn('Sign Up', response_text)
      self.assertNotIn('Unfollow', response_text)

    def test_get_profile_logged_in(self):
        create_residences()
        create_users()
        login(self.app, 'test_1@gmail.com', 'password_1')

        response = self.app.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Profile', response_text)
        self.assertIn('Followers', response_text)
        self.assertIn('Log Out', response_text)

        self.assertIn('test_1', response_text)
        self.assertIn('2000-01-01', response_text)
        self.assertIn('Make School', response_text)
        self.assertIn('The Herbert Hotel', response_text)
        self.assertIn('101', response_text)
        self.assertIn('Available', response_text)
        self.assertIn('Update', response_text)


    def test_update_profile_logged_in(self):
        create_residences()
        create_users()
        login(self.app, 'test_1@gmail.com', 'password_1')

        in1 = Institution.query.filter_by(name='Make School').one()
        res2 = Residence.query.filter_by(
            name='Nob Hill Guesthouse by FOUND').one()


        data = {
            'dob': date(2000, 1, 2),
            'institution': in1.id,
            'residence': res2.id,
            'dorm_room': '107',
            'status': 'On Vacation'
        }


        response = self.app.post('/profile', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Profile', response_text)
        self.assertIn('Followers', response_text)
        self.assertIn('Log Out', response_text)

        self.assertIn('test_1', response_text)
        self.assertIn('2000-01-02', response_text)
        self.assertIn('Make School', response_text)
        self.assertIn('Nob Hill Guesthouse by FOUND', response_text)
        self.assertIn('107', response_text)
        self.assertIn('On Vacation', response_text)
        self.assertIn('Update', response_text)

        
