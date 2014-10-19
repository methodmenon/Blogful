import os
from flask.ext.script import Manager
"""
Flask-Script module
--> allows for easy specification of tasks to help manage our application
"""

from blog import app
from blog.models import Post
from blog.database import session

#create an instance of the Manager object
manager = Manager(app)

"""
1) Add a command to the manager by decorating a function
---> using the manager.command decorator

2) The name of the function is the name of the argument we give the manage script 
"""
@manager.command
def run():
    #try to retrieve a port number from environment, falling back to 5000 if unvailable
    port = int(os.environ.get('PORT', 5000))
    #run the development server, telling it to listen to the port retrieved
    app.run(host='0.0.0.0', port=port)
    """
    the app.run method above is a good practice to compy with this b/c
    a number of hosts use the PORT environmental variable to tell the app which port it should be listening on
    """

#create a function for test exampless
@manager.command
def seed():
    """
    seed - command which will add a series of posts to the database
    """
    #create a string of dummy text for the post content
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    #use a loop to add 25 posts
    for i in range(25):
        #create a new post
        post = Post(
            title = "Test Post #{}".format(i),
            content = content
            )
        #add the new post to the session
        session.add(post)
    #session.commit will synchronize all changes to the database
    session.commit()

"""
add user to database, with which we can use to test our login system
"""
from getpass import getpass

from werkzeug.security import generate_password_hash

from blog.models import User

@manager.command
def adduser():
    """
    Ask user for name, email address, and password (twice).
    Check to make sure the user is not already stored in the database.
    Make sure both passwords entered by user match.
    Finally, create the user object and add it to our database.
    """
    name = raw_input("Name: ")
    email = raw_input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print "User with that email address already exists"
        return
    password = raw_input("Password: ")
    password_2 = raw_input("Re-enter password: ")
    while not (password and password_2) or password != password_2:
         password = getpass("Password: ")
         password_2 = getpass("Re-enter password: ")
    user = User(name=name, eamil=email,
        password=generate_password_hash(password))
    """
        generate_password_hash function: 
        1) Function is used to hash our password
        2) Hashing - process that converts our plain text password
                     into a string of characters
        3) Passwords use only One-Way-Hashes: process works in one direction
    """
    session.add(user)
    session.commit()

if __name__ == "__main__":
    #run the manager
    manager.run()