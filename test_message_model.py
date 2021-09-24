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

# PLANNING FOR SETTUP
# CREATE: A user and a message in setup
# When settup append message to user
# 4th


class MessageModelTestCase(TestCase):
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

        db.session.add(test_message_1)

        test_user_1.messages.append(test_message_1)

        db.session.commit()

        self.user1 = test_user_1
        self.message1 = test_message_1

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_message_model(self):
        """Testing if the message model works"""

        message = Message(text="This is a test 2 message",
                          user_id=self.user1.id)

        db.session.add(message)
        db.session.commit()

        self.assertTrue(isinstance(message, Message))

    def test_user_for_message(self):
        """Testing if the user has messages"""

        test1 = self.user1.messages

        self.assertEqual(len(test1), 1)
        self.assertEqual(self.user1.messages[0].text, "This is a test message")

    def test_user_liked_messages(self):
        """Testing if the user has any liked messages"""

        # Adding a new user
        test2 = User.signup("test_user_2",
                            "test2@email.com",
                            "testing2",
                            "/static/images/default-pic.png"
                            )
        db.session.commit()

        # Add new messages
        message_1 = Message(text="This is a test 2 message",
                            user_id=test2.id)

        message_2 = Message(text="This is a test 3 message",
                            user_id=test2.id)

        db.session.add_all([message_1, message_2])

        self.user1.liked_messages.append(message_1)

        test1 = self.user1.liked_messages

        db.session.commit()

        self.assertEqual(len(test1), 1)
        self.assertFalse(message_2 in test1)

    def test_message_without_user_id(self):
        """Testing if a messge without user_id raises an error"""

        message = Message(text="This is a test 2 message", user_id=None)
        db.session.add(message)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def test_too_many_characters(self):
        """Testing a message with more than 140 characters"""

        message = Message(text="""Lorem ipsum dolor sit amet, consectetuer 
                                    adipiscing elit. Aenean commodo ligula 
                                    eget dolor. Aenean massa. Cum sociis 
                                    natoque penatibus et magnis dis parturient 
                                    montes, nascetur arcu. In enim justo, rhoncus 
                                    ut, imperdiet a, venenatis vitae, justo. Nullam 
                                    dictum felis eu pede """, user_id=self.user1.id)
        db.session.add(message)

        with self.assertRaises(exc.DataError):
            db.session.commit()
