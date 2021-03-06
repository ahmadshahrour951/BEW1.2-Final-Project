# BEW1.2-Final-Project

## Project Intro
An webapp that helps create a community within student dorms! The idea is simple, students can socialize and create communities within their dorms. This is all done by having pre-aggregated data provided by the education body, and that ideally would feed into the app. Students would then have something similar to Tinder (without the dating aspect) but more so towards a Facebook attitude. A nice little project I hope to expand on in the future.

## Project Tech Stack
- Language: Python v3.85
- Framework: Flask v1.1.2
- Template Engine: Jinja2 v2.11.3
- Database ORM: Sqlalchemy v1.3.23

## Project Database Structure
![Image of Data structure](https://drive.google.com/file/d/1jqdPoUGf-EBR7w2jbYoO6jdaPUvvARHN/view?usp=sharing)

The data structure mimics reality, where institutions have many residences in different locations. In those residences you have many students (which are called users in the app for simplicity). Those students can follow other students. (Follow in this app just simply means a simple click of a button, no further functionility). Following requires a followee and a follower, so the many-to-many table for user_followers was created by referencing itself.

First Table | Second Table | Relationship
------------ | -------------
Institutions | Residences | One-to-Many
Residences | Users | One-to-Many
Users (Followee) | Users (Follower) | Many-to-Many

## Project Directory structure
- `models.py` handles the Table Models and their relationships
- `/auth` modular tests, routes, and forms for authentication
- `/main` modular tests, routes, and forms for main logic of the app
- `/templates` all the frontend views

## Setup

**Create your virtual environment**:
```
python3 -m venv env
```

**Activate your environment**:
```
source env/bin/activate
```

**Install the required packages**:
```
pip3 install -r requirements.txt
```

**Copy the `.env.example` file to `.env`**:
```
cp .env.example .env
```

**Run the Flask server**:
```
python3 app.py
```

## Running Tests
**To run all of the tests**, you can run the following from the root project directory:
```
python3 -m unittest discover
```

(Make sure you have unittest installed.)

**To run all tests from a single file**, run the following example:
```
python3 -m unittest socialorm_app.main.tests
```

**To run one specific test**, run the following example:
```
python3 -m unittest socialorm_app.main.tests.MainTests.test_homepage_logged_in
```

##