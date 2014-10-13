import os

#import the Flask object
from flask import Flask

#create the app in the usual way
app = Flask(__name__)

#load the configuration using the class created in config.py which contains the configuration variables
#--> if variable is not set, we default to our development configuration
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
#use .config.from_object method to configure our app using the object specified (config_path)
app.config.from_object(config_path)

#NOW OUR APP IS CONFIGURED

#import views and Jinja filters
'''
1) imports come after app creation sine both views.py and filters.py files 
   make use of the app object, so need importing after object has been created
'''
import views
import filters