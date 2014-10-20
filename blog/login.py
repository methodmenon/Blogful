from flask.ext.login import LoginManager

from blog import app
from database import session
from models import User

#create an instance of the LoginManager class from Flask-Login
#then initialize the instance
login_manager = LoginManager()
login_manager.init_app(app)

#login_view is name of view which an unauthorized user will be re-directed to, when they try to access a protected source
#login_message_category --> category used to classify any error messages from Flask-Login
##-----> used in conjuction with Bootstrap's alerts system, to give the user information about the login process
login_manager.login_view = "login_get"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
	"""function that tells Flask-Login
	1) How to access an object representing a user, via their id
	"""
	return session.query(User).get(int(id))
	