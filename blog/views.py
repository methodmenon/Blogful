from flask import render_template

from blog import app
from database import session
from models import Post
import mistune
from flask import request, redirect, url_for

@app.route("/")
#new route created to take us to a specific page of content
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
	"""2 args: 
	1) page - a page number
	2) paginate_by - indicates how many items should be on each page
	"""
	#zero-indexed page
	page_index = page - 1

	#use the count method of a Post query object to find total number of items
	count = session.query(Post).count()

	#the index of the first item we should see
	start = page_index * paginate_by
	#the index of the last itme we should see
	end = start + paginate_by

	#total number of (pages of content)
	total_pages = (count - 1) / (paginate_by) + 1
	#is there a page after the current one
	has_next = page_index < (total_pages - 1)
	#is there a page before the current one
	has_prev = page_index > 0

	#construct a query of Post objects
	posts = session.query(Post)
	#order the posts by the datetime column, getting the most recent posts first
	posts = posts.order_by(Post.datetime.desc())
	#slice the posts query so that we only find posts between the start and end indicies
	posts = posts[start:end]
	#render a template called posts.html, passing in all the posts we want
	return render_template("posts.html", 
		posts=posts,
		has_next=has_next,
		has_prev=has_prev,
		page=page,
		total_pages=total_pages
		)

"""
login_required decorator will be used to protect the resources which require authentication
--> used here to prevent unauthorized users from adding posts, so edit views to include the decorator
"""
from flask.ext.login import login_required

""" New view created to display the form, structured in add_post.html"""

#methods["GET"] parameter in route decorator - specifies the route with ONLY BE USED for GET requests to the page
@app.route("/post/add", methods=["GET"])
#login_required decorator - used here to prevent unauthorized users from accessing the form
@login_required
def add_post_get():
	return render_template("add_post.html")

"""New view created to take our form data and create a new post"""

from flask.ext.login import current_user

#methods["POST"] paramter in route decorator - specifies the route will ONLY ACCEPT POST requests
@app.route("/post/add", methods=["POST"])
#login_required decorator - used here to prevent a user from manually constructing the form data, and sending it to the POST endpoint
@login_required
def add_post_post():
	#create a new Post object
	post = Post(
		#use Flask's request.form dictionary --> access the data submitted with our form, and assign it to the correct fields in the post
		title=request.form["title"],
		#preprocess the content using mistune, a Markdown parser
		# --> allows one to Markdown syntax in posts, making it simpler to write well formatted blog posts
		content=mistune.markdown(request.form["content"]),
		#current_user variable from Flask-Login to set the author attribute
		#--> add {{post.author.name}} to the metadata div in macros.html
		author=current_user
	)
	#add post to our session and commit to database
	session.add(post)
	session.commit()
	return redirect(url_for("posts"))

@app.route("/post/<int:post_id>")
def view_post(post_id):
	post = session.query(Post).filter(Post.id==post_id).first()
	return render_template("single_post.html",
		post=post)

@app.route("/post/<int:post_id>/edit", methods=["GET"])
def edit_post_get(post_id):
	post = session.query(Post).filter(Post.id==post_id).first()
	title = post.title
	content = post.content
	return render_template("edit_post.html", title=title,
		content=content, post=post)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post_post(post_id):
	post = session.query(Post).filter(Post.id==post_id).first()
	post.title = request.form["title"]
	post.content = mistune.markdown(request.form["content"])
	#session.add(post)
	session.commit()
	return redirect(url_for("posts"))

@app.route("/post/<int:post_id>/delete", methods=["GET"])
def delete_post(post_id):
	post = session.query(Post).filter(Post.id==post_id).delete()
	session.commit()
	return redirect(url_for("posts"))

#GET route for login
@app.route("/login", methods=["GET"])
def login_get():
	return render_template("login.html")

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from models import User

#POST route for login
@app.route("/login", methods=["POST"])
def login_post():
	"""we read the email address and password, which was entered by the user, from the requests.form dictionary"""
	email = request.form["email"]
	password = request.form["password"]
	#query to find the user object with the matching email address
	#then check the user exits
	#and also compare (via check_password_hash function) the password enterd by the user with the hash stored in the database
	user = session.query(User).filter_by(email=email).first()
	if not user or not check_password_hash(user.password, password):
		#flash function used to store a message which can be used when we render the next page
		flash("Incorrect username or password", "danger")
		#redirect user back to the login
		return redirect(url_for("login_get"))

	#login_user function--> sends a cookie(small chunk of data) to the user's browser which will be used to identify the user, which can be used for later for the user
	login_user(user)
	#after user is logged in, redirect the user
	"""
	1) normally redirected to the posts page, but if 
	2) there is a next paramter in the URL's query string --> we redirect to that page 
	"""
	return redirect(request.args.get('next') or url_for("posts"))