"""
Create a SQLAlchemy model, which will be used to store and retrieve blog posts
"""

import datetime

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime

from database import Base, engine

from flask.ext.login import UserMixin

#create a new class, which inherits from the declaritive base object
class Post(Base):
	#give model a table name
	__tablename__ = "posts"

	#primary key id column
	id = Column(Integer, Sequence("post_id_sequence"), primary_key=True)
	#column for title of the post
	title = Column(String(1024))
	#column for the content of the post
	content = Column(Text)
	#date and time the post was created
	datetime = Column(DateTime, default=datetime.datetime.now)

#for our user model, create a new class for Users, which inherits from
## 1) the declarative base object
"""2) Flask-Login's UserMixin class:
		adds a series of defualt methods, used by Flask-Login
		to make authentication work """
class User(Base, UserMixin):
	__tablename__ = "users"

	id = Column(Integer, Sequence("user_id_sequence"), primary_key=True)
	name = Column(String(128))
	#email address - unique, because it will be used to identify a user
	email = Column(String(128), unique=True)
	password = Column(String(128))

#use the following function to create the table in the database
Base.metadata.create_all(engine)