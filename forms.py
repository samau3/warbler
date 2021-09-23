from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, Optional


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditProfileForm(FlaskForm):
    """Form to edit current user profile."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_url = StringField('Header URL')
    bio = TextAreaField('BIO')
    password = PasswordField('Password', validators=[Length(min=6)])


class OnlyCsrfForm(FlaskForm):
    """For actions where we want CSRF protection, but don't need any fields.

    Currently used for our "delete" buttons, which make POST requests, and the
    logout button, which makes POST requests.
    """

# ADDING LIKES: 
# Each like and unlike will be a post request. 
# Need to tie to user, and how many likes each user has 
# Update Message displays to have like buttons, 

#######################In HTML
# Update ALL message cards to have a like button 
# Need to include hidden tag
# Needs to be a post  
# Include font awesome star 
###########PART 2 for User
# Display on their nav bar the count of likes 
# Need to include a link that show the LIKED messages 

##################Models
# Add likes to database 
# Need to keep track of likes if likes or not. 
# MESSAGE AUTHENTICATE? (class method)


######################ROUTE 
# Handle the like button, if it's liked or if it's not liked 
# Need to include CSRF 
# Need to check if message exist in database 
