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
# 1st test: testing if message is connected to user
# 2rd test: testing if message is liked 
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

        m = Message(text="This is a test 2 message", 
        user_id=self.user1.id) 

        db.session.add(m)
        db.session.commit()

        self.assertTrue(isinstance(m, Message))
    
    def test_user_for_message(self):
        """Testing if the user has messages"""

        test1 = self.user1.messages

        self.assertEqual(len(test1), 1) 
        self.assertEqual(self.user1.messages[0].text, "This is a test message")

    def test_user_liked_messages(self): 
        """Testing if the user has any liked messages"""

        # Add new messages
        message_1 = Message(text="This is a test 2 message", user_id=self.user1.id)

        message_2 = Message(text="This is a test 3 message", user_id=self.user1.id) 

    
        # Adding a new user 
        test2 = User.signup("test_user_2",
                                  "test2@email.com",
                                  "testing2",
                                  "/static/images/default-pic.png"
                                  )
        
        db.session.commit()
        
        message_3 = Message(text="This is a test 4 message", user_id=test2.id)

        db.session.add_all([message_1, message_2, message_3])

        self.user1.liked_messages.append(message_1)
        self.user1.liked_messages.append(message_2)
        test2.liked_messages.append(message_3)

        test1 = self.user1.liked_messages

        db.session.commit()

        self.assertEqual(len(test1), 2) 
        self.assertEqual(len(test2.liked_messages), 1)

    

 
        
    



