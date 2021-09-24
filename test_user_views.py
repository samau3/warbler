from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from models import db, User, Message, Follows, Like
from flask import session

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test messages model"""

    def setUp(self):
        """Create test client, add sample data."""

        Message.query.delete()
        Follows.query.delete()
        Like.query.delete()
        User.query.delete()

        self.client = app.test_client()
        test_user_1 = User.signup("test_user_1",
                                  "test1@email.com",
                                  "testing1",
                                  "/static/images/default-pic.png"
                                  )
        test_message_1 = Message(text="This is a test message")

        test_user_2 = User.signup("test_user_2",
                                  "test2@email.com",
                                  "testing2",
                                  "/static/images/default-pic.png"
                                  )
        test_message_1 = Message(text="This is a test message")
        test_message_2 = Message(text="This is a second test message")

        db.session.add_all([test_message_1, test_message_2])

        test_user_1.messages.append(test_message_1)
        test_user_2.messages.append(test_message_2)

        db.session.commit()

        self.user1 = test_user_1
        self.user2 = test_user_2
        self.message1 = test_message_1
        self.message2 = test_message_2
        self.user1_id = test_user_1.id
        self.user2_id = test_user_2.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_homepage(self):
        """Test user homepage without a logged in account"""
        with app.test_client() as client:
            resp = client.get('/')

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>What's Happening?</h1>", html)
            self.assertIn('<a href="/login">Log in', html)

    def test_login(self):
        """Test login"""
        with app.test_client() as client:

            post_data = {"username": "test_user_1", "password": "testing1"}
            resp = client.post('/login', data=post_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(session), 1)
            self.assertIn(f'@{self.user1.username}', html)
            self.assertIn(f'<a href="/users/{self.user1.id}">', html)

    def test_logout(self):
        """Test logout"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = client.post('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(session), 0)
            self.assertIn('<h2 class="join-message">Welcome back.</h2>', html)

    def test_following(self):
        """Test if a user is following another user"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            resp = client.post(
                f'/users/follow/{self.user2_id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn(
                f'<form method="POST" action="/users/stop-following/{self.user2_id}"', html)

    def test_deleting_user(self):
        """Test if a user is deleted"""

        with app.test_client() as client:

            resp = client.post('/users/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertTrue(len(User.query.all()), 1)
            self.assertIn('<h1>What\'s Happening?</h1>', html)

# doesn't work, need to refine edit posting
    # def test_edit_user(self):
    #     """Test if a user can edit their profile"""
    #     with app.test_client() as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.user1_id

    #         # post_data = {"username": "new_test_name",
    #         #              "email": "test1@email.com",
    #         #              "image_url": "/static/images/default-pic.png",
    #         #              "header_url": "",
    #         #              "bio": "",
    #         #              "password": "testing1"}

    #         resp = client.post(
    #             '/users/profile', data={"username": "new_test_name",
    #                                     "email": "test1@email.com",
    #                                     "image_url": "/static/images/default-pic.png",
    #                                     "header_url": "",
    #                                     "bio": "",
    #                                     "password": "testing1"},
    #             follow_redirects=True)
    #         breakpoint()
    #         html = resp.get_data(as_text=True)

    #         self.assertIn(
    #             f'<form method="POST" action="/users/stop-following/{self.user2_id}"', html)
