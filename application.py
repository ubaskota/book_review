import os
import requests
from flask import Flask, render_template, session, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker




app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# @app.route("/")
# def index():
# 	#flights = db.execute("SELECT * FROM login_signup").fetchall()
# 	return render_template("index.html")



@app.route("/", methods = ["POST", "GET"])
def registration_login():

	if 'username' in session:
		session.pop('username', None)
		return render_template("login.html")

	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		re_password = request.form.get('re_password')

		if len(username) < 5 or len(username) > 30 or len(password) < 5 or len(password) > 30:
			message = "Username/Password should be of length between 5 and 30!"
			return render_template("index.html", message=message)

		elif password != re_password:
			message = "Please, make sure your passwords are same!"
			return render_template("index.html", message=message)

		else:
			if db.execute('SELECT username FROM login_signup WHERE username=:username', {'username': username}).rowcount == 0:
				db.execute('INSERT INTO login_signup (username, password) VALUES(:username, :password)',{'username':username, 'password':password})
				db.commit()
				message = "Congratulations %s!!! Account successfully created." % (username)
				return render_template("success.html", message=message)
			else:
				message = "The account with provided information already exists!"
				return render_template("index.html", message=message)
	else:
		return render_template("index.html")



@app.route("/login", methods = ["POST", "GET"])
def login():
	# print(session['username'])
	return render_template("login.html")




@app.route("/login_submit", methods = ["POST", "GET"])
def login_submit():

	# if 'username' not in session:
	# 	message = "Please, login again!"
	# 	return render_template("login.html", message=message)

	username = request.form.get('username')
	password = request.form.get('password')

	if db.execute("SELECT * FROM login_signup WHERE username=:username and password=:password", {'username':username, 'password':password}).fetchone():
		session['username'] = username
		message = "Welcome %s" % (username)
		return render_template("welcome.html", message=message)
	else:
		message = "Incorrect Password or the the username doesn't exist."
		return render_template("login.html", message=message)



@app.route("/logout", methods = ["POST", "GET"])
def logout_user():
	session.pop('username', None)
	flash('You are successfully logged out.')
	# return render_template("login.html")
	return redirect(url_for('login'))



@app.route("/success")
def success_message():
	message = "Congratulations, you successfully created an account!!!"
	return render_template("success.html", message = message)



@app.route("/search_results", methods = ["POST", "GET"])
def search():

	if 'username' not in session:
		message = "Please, login again!"
		return render_template("login.html", message=message)

	elif session != None:
		if request.method == 'POST':
			search = str(request.form.get('search_tag'))
			search = search.lower()
			search_input = '%' + search + '%'

			if search == None:
				message = "The search Field can't be empty!"
				return render_template("error.html", message=message)
				#Add exception try/except statement
			else:
				results = db.execute("SELECT * FROM books_des WHERE (LOWER(title) LIKE :search_term OR LOWER(author) LIKE :search_term\
				OR isbn_num LIKE :search_term OR publish_year LIKE :search_term)", {"search_term":search_input}).fetchall()
				return render_template('search_results.html', samples=results, page_title="Search Results:")
		else:
			message = "You can search as many times as you want!"
			return render_template('welcome.html', message=message)
	else:
		return render_template('login.html')



@app.route("/post_review", methods = ["POST", "GET"])
def post_review():

	if 'username' not in session:
		message = "Please, login again!"
		return render_template("login.html", message=message)

	elif session != None:
		if request.method == 'POST':
			try:
				username = session['username']
			except Exception as e:
				print("Error, please fix the error")
			print(session['username'])
			#username = session['username']
			isbn_num = request.form.get('book_isbn')
			review = request.form.get('thoughts')
			print(isbn_num)
			print(review)
			if username != None and isbn_num != None and review != None:
				db.execute('INSERT INTO book_reviews (username, isbn_num, review) VALUES(:username, :isbn_num, :review)',{'username':username, 'isbn_num':isbn_num, 'review':review})
				db.commit()
				book_name = db.execute('SELECT title FROM books_des WHERE isbn_num=:isbn_num', {'isbn_num':isbn_num}).fetchone()
				return render_template('review_post.html', message = book_name)
			else:
				message = "The search Field can't be empty!"
				return render_template("error.html", message=message)

	else:
		return render_template('login.html')















		
		
