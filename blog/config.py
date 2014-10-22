import os
"""
The DevelopmentConfig class will be used to contain the configuration variables 
which control the Flask app
"""
class DevelopmentConfig(object):
	#set the location of the database
	SQLALCHEMY_DATABASE_URI = "sqlite:///blog-development.db"
	#tell Flask to use its debug mode to help track down any erros in the application
	DEBUG = True
	#secret_key used to cryptographically secure the application
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")
	"""
	Not good ide to store key in application configuration,
	use os.environ.get to obtain the secret key from an environmental variable
	"""

"""
class pointed to from CONFIG_PATH environmental variable in test_filter.py
"""
class TestingConfig(object):
	#set location of testing database
	SQLALCHEMY_DATABASE_URI = "sqlite:///blog-testing.db"
	#debug mode turned off
	DEBUG = False
	#no need for secret key
	SECRET_KEY = "Not Secret"