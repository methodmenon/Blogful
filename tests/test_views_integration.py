import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

#configure the app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
	def setUp(self):
		"""Test setup"""
		#create test client using the app.test_client function
		#--> allows us to make requests to views and inspect the responses we get from the app
		self.client = app.test_client()

		#set up the tables in the database
		Base.metadata.create_all(engine)

		#create an example user --> use this user to login and be the author of our test post
		self.user = models.User(name="Alice", email="alice@example.com",
			password=generate_password_hash("test"))

		#add user to the database
		session.add(self.user)
		session.commit()

	def tearDown(self):
		"""Test teardown"""
		#remove the tables and data from database
		Base.metadata.drop_all(engine)

	def simulate_login(self):
		"""mimics what Flask-login looks for when determinging whether a user is logged in"""
		#self.client.session_transaction method used to get access to a variable representing..
		#the HTTP session
		with self.client.session_transaction() as http_session:
			#add id of user
			http_session["user_id"] = str(self.user.id)
			#variable which tells Flask-Login that session is till active
			http_session["_fresh"] = True

	def testAddPost(self):
		#call simulate_login method to act as a logged in user.
		self.simulate_login()

		#send POST request to /post/add using self.client.post method.
		#use data paramter to provide the form data for an example post
		response = self.client.post("/post/add", data={
			"title": "Test Post",
			"content": "Test content"
			})

		"""check response from app looks correct"""

		#make sure user is being redirected to / route by checking status code
		#and location header of the response
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/")

		#look to see that only one post has been added
		posts = session.query(models.Post).all()
		self.assertEqual(len(posts),1)

		#verifying post has been added to db correctly by making sure title and content values are correct
		post = posts[0]
		self.assertEqual(post.title, "Test Post")
		self.assertEqual(post.content, "<p>Test content</p>\n")
		self.assertEqual(post.author, self.user)


if __name__ == "__main__":
	unittest.main()