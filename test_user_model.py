"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# need two test user instances
# place creation of the two instances outside of test class?

# two test cases for validating sign up should try to use an existing username and email

TEST_USER_DATA = {
    "email": "test1@email.com",
    "username": "test_user_1",
    "image_url": "",
    "header_image_url": "",
    "bio": "test_user_bio_1",
    "location": "test_location_1",
    "password": "testing1"
}

TEST_USER_DATA_2 = {
    "email": "test2@email.com",
    "username": "test_user_2",
    "image_url": "",
    "header_image_url": "",
    "bio": "test_user_bio_2",
    "location": "test_location_2",
    "password": "testing2"
}


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Like.query.delete()

        test_user = User(**TEST_USER_DATA)
        db.session.add(test_user)
        db.session.commit()

        self.user = test_user

        self.client = app.test_client()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_repr(self):
        """Does user __repr__ work?"""

        self.assertEqual(
            f"{self.user}",
            f"<User #{self.user.id}: {self.user.username}, {self.user.email}>")

    def test_is_following(self):
        """Testing if user1 is following user2"""

        test_user_2 = User(**TEST_USER_DATA_2)
        db.session.add(test_user_2)
        db.session.commit()

        test_user_1 = User.query.get(self.user)  # this line doesn't work
        test_user_1.following.append(test_user_2)
        db.session.commit()
        breakpoint()
        self.assertEqual(len(test_user_1.following), 1)
        self.assertEqual(len(test_user_2.followers), 1)
