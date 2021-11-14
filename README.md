# Warbler  <img src="/static/images/warbler-logo.png" alt="logo" width="50" height="50">

- An application based off of a twitter clone that utilizes Flask, PostgreSQL, WTForms, and Jinja.
- To see live demo click [here](https://warbler-samau3.herokuapp.com/).

## Current Features 
- A user can login and signup if they don't have an account
- A user can follow and unfollow other users
- A user can like and unlike a message from another user
- Can write messages and post them 
- Can search for users 
- Can edit their own user profile

## Features to add 
- Custom 404 Page
- Adding AJAX
- Drying up templates, urls, and authorization
- Add a change password form 
- Create private accounts
- User blocking features

## Installation
**Create Virtual Environment**
- Once in you're in your venv install the requirements needed for the application
```console
python3 -m venv venv
source venv/bin/activate
(venv) pip3 install -r requirements.txt
```
**Start your local server** 
- Run the second command if Flask environment is not set to development
```console
(venv) flask run
(venv) FLASK_ENV=development flask run
```
## Testing
- To run your unittest type in the following command
```console
FLASK_ENV=production python3 -m unittest <FILE-NAME>
```
