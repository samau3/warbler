"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        Message.query.delete()
        Follows.query.delete()
        Like.query.delete()
        User.query.delete()

        self.client = app.test_client()
        test_data_1 = User.signup("test_user_1",
                                  "test1@email.com",
                                  "testing1",
                                  "/static/images/default-pic.png"
                                  )

        # breakpoint()
        test_data_2 = User.signup("test_user_2",
                                  "test2@email.com",
                                  "testing2",
                                  "/static/images/default-pic.png"
                                  )
        db.session.commit()

        self.user1 = test_data_1
        self.user2 = test_data_2

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
            f"{self.user1}",
            f"<User #{self.user1.id}: {self.user1.username}, {self.user1.email}>")

    def test_is_following(self):
        """Testing if user1 is following user2"""

        self.user1.following.append(self.user2)
        db.session.commit()
    
        self.assertEqual(len(self.user1.following), 1)
        self.assertEqual(len(self.user2.followers), 1)

    def test_is_not_following(self):
        """Testing if user1 is following user2"""

        self.assertEqual(len(self.user1.following), 0)
        self.assertEqual(len(self.user2.followers), 0)

    def test_user_signup(self):
        """Testing if signup with valid credentials creates a user successfully"""
        test_data_3 = User.signup('test3',
                                  'test3@email.com',
                                  'testing3',
                                  '/static/images/default-pic.png'
                                  )

        db.session.commit()
        self.assertEqual(test_data_3, User.query.get(test_data_3.id))

    def test_existing_user_email_signup(self):
        """Testing if signup with existing email does not create a user"""

        User.signup('test3',
                    'test1@email.com',
                    'testing3',
                    '/static/images/default-pic.png'
                    )

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def test_existing_user_username_signup(self):
        """Testing if signup with existing username does not create a user"""

        User.signup('test_user_1',
                    'test3@email.com',
                    'testing3',
                    '/static/images/default-pic.png'
                    )

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def test_null_email_signup(self):
        """Testing if signup with null email does not create a user"""

        User.signup('test_user_1', 
                    None,
                    'testing3',
                    '/static/images/default-pic.png'
                    )
    
        with self.assertRaises(exc.IntegrityError): 
            db.session.commit()
    
    def test_missing_argument_signup(self):
        """Testing if signup with a missing argument does not create a user"""

        with self.assertRaises(TypeError): 
            User.signup('test_user_1', 
                    'testing3',
                    '/static/images/default-pic.png'
                    )
    
    def test_authentication(self):
        """Testing if user has a valid credentials"""

        check_auth = User.authenticate(self.user1.username, "testing1")

        self.assertTrue(check_auth)
    
    def test_invalid_username(self):
        """Testing if invalid username"""

        check_auth_1 = User.authenticate("failfail", "testing1")
        check_auth_2 = User.authenticate("124", "testing1")
        check_auth_3 = User.authenticate(None, "testing1")
        
        self.assertFalse(check_auth_1)
        self.assertFalse(check_auth_2)
        self.assertFalse(check_auth_3)
    
    def test_invalid_password(self):
        """Testing if invalid password"""

        check_auth_1 = User.authenticate(self.user1.username, "testing2")
        check_auth_2 = User.authenticate(self.user1.username, "")
        
        self.assertFalse(check_auth_1)
        self.assertFalse(check_auth_2)
     



    

