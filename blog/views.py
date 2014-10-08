from flask import render_template

from blog import app
from database import session
from models import Post

@app.route("/")
def posts():
	#construct a query of Post objects
	posts = session.query(Post)
	#order the posts by the datetime column, getting the most recent posts first
	posts = posts.order_by(Post.datetime.desc())
	#use posts.all method to retrieve all the posts
	posts = posts.all()
	#render a template called posts.html, passing in all the posts
	return render_template("posts.hmtl", posts=posts,)