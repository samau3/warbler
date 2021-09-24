from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows, Like

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


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


    



    # def test_homepage(self):
    #     """Test user homepage without following any users"""
    #     with app.test_client() as client:
    #         resp = client.get('/')

    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn(f'@{self.user1.username}', html)
    #         self.assertIn(f'<h4> <a href="/users/{self.user1.id}"> 1', html)
