from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import secrets, hashlib

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz_app:{}@localhost:8889/blogz'.format('f1nc53pM6fz0apb7ms')
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'woof'
db = SQLAlchemy(app)

from model import *

def is_valid(field, length=0):
  # Return error if field is left blank
  if field == '':
    return "This field is required."

  # if length is defined and field is not in range return error
  if len(field) < length:
    return "This field is to short."

def sort_data(sort_on=None, sort_direction='asc'):
    if sort_on:
        result = Blog.query.order_by(getattr(getattr(Blog, sort_on), sort_direction)()).all()
        return result
    return Blog.query.all()

def get_post(get_by='id', target=''):
    if get_by=='id':
        result = Blog.query.get(target)
        return result

def salt_password():
  return secrets.token_hex(16)

def hash_password(password, salt=None):
  if salt is None:
    salt = salt_password()
  pw_hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
  return '{},{}'.format(pw_hash, salt)

def check_pw_hash(password, hash, salt):
  if hash_password(password, salt).split(',')[0] == hash:
    return True

@app.before_request
def require_login():
  allowed_routes = [
    'login',
    'blog',
    'index',
    'signup',
    'static'
  ]

  # Redirect user to login if not logged in
  if request.endpoint not in allowed_routes and 'user' not in session:
    return redirect('/login')

  # Redirect user to home if trying to log in while logged in
  if request.endpoint == 'login' and 'user' in session:
    return redirect('/')

@app.route('/')
def index():
    users = User.query.all()

    return render_template('index.html', location="Home", users=users)

@app.route('/login', methods=['GET','POST'])
def login():

  errors = {}

  if request.method == 'POST':
    # Grab input from form
    post_username = request.form['username']
    post_password = request.form['password']

    # Check for valid entry
    if is_valid(post_username):  errors['username'] = is_valid(post_username)
    if is_valid(post_password):  errors['password'] = is_valid(post_password)

    # If invalid entry
    if len(errors) > 0:
        return render_template('login.html', location="Login",  username=post_username, errors=errors)

    # Grab user from database
    user = User.query.filter_by(username=post_username).first()

    # Check if user exist
    if not user:
      errors['username'] = "User does not exist!"
      return render_template('login.html', location="Login",  username=post_username, errors=errors)

    # Cheack if users password is correct
    if not check_pw_hash(post_password, user.pw_hash, user.pw_salt):
      errors['password'] = "Password is incorrect!"
      return render_template('login.html', location="Login",  username=post_username, errors=errors)

    # If all is well start a session
    session['user'] = post_username
    return redirect('/newpost')

  return render_template('login.html', location="Login", errors=errors)

@app.route('/signup', methods=['POST', 'GET'])
def signup(): 
  errors = {}

  if request.method == 'POST':
    # Grab input from form
    post_username = request.form['username']
    post_password = request.form['password']
    post_verify = request.form['verify']

    # Check for valid entry
    if is_valid(post_username, 3):  errors['username'] = is_valid(post_username, 3)
    if is_valid(post_password, 3):  errors['password'] = is_valid(post_password, 3)
    if is_valid(post_verify):  errors['password'] = is_valid(post_verify)

    # Check is password match verfiy password
    if not post_password == post_verify:
      errors['verify'] = "Does not match password!"

    # Check if user exist
    if User.query.filter_by(username=post_username).first() is not None:
      errors['username'] = "User name already esist!"

    # If errors exist
    if len(errors) > 0:
        return render_template('signup.html', location="signup",  username=post_username, errors=errors)


    # All is well create user in db and add to session then redirct
    # get tuple that is hashed password and salt
    pw_hash = hash_password(post_password)

    user = User(post_username, pw_hash.split(',')[0], pw_hash.split(',')[1])
    db.session.add(user)
    db.session.commit()
    session['user'] = post_username
    return redirect('/newpost')

  return render_template('signup.html', location="signup", errors=errors)

@app.route('/logout')
def logout():
  del session['user']
  return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    errors = {}

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        owner = User.query.filter_by(username=session['user']).first()
        print(owner)
        if is_valid(post_title):  errors['title'] = is_valid(post_title)
        if is_valid(post_body):  errors['body'] = is_valid(post_body)

        if len(errors) > 0:
            return render_template('newpost.html', location="New Post",  title=post_title, body=post_body, errors=errors)

        new_post = Blog(post_title, post_body, owner)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/blog?id={}'.format(new_post.id))

    return render_template('newpost.html', location="New Post", errors=errors)

@app.route('/blog', methods=['GET'])
def blog():
    
    # Display individual blog post
    if 'id' in request.args:
      index = int(request.args['id'])
      post=Blog.query.get(index)
      return render_template('showpost.html', location=post.title, post=post)
    # Display all blogs post from specific user
    elif 'user' in request.args:
      user=User.query.filter_by(username=request.args['user']).first()
      return render_template('userspost.html', location=user, user=user)
    # Display all blog post
    else:
      posts = sort_data('id', 'desc')

    return render_template('blog.html', location="All Post", posts=posts)

if __name__ == '__main__':
  app.run()