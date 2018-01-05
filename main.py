from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import urllib3
import base64

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog_app_user:{}@jasongoebel.com:3306/blog_app_db'.format('f1nc53pM6fz0apb7ms')
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
http = urllib3.PoolManager()

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    edited_on = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, body, image):
        self.title = title
        self.body = body
        self.image = image

def is_valid(field):
    if field == '':
        return "This field is required."

def sort_data(sort_on=None, sort_direction='asc'):
    if sort_on:
        result = Blog.query.order_by(getattr(getattr(Blog, sort_on), sort_direction)()).all()
        return result
    return Blog.query.all()

def get_post(get_by='id', target=''):
    if get_by=='id':
        result = Blog.query.get(target)
        return result

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    errors = {}

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']

        if is_valid(post_title):  errors['title'] = is_valid(post_title)
        if is_valid(post_body):  errors['body'] = is_valid(post_body)

        if len(errors) > 0:
            return render_template('newpost.html', location="New Post",  title=post_title, body=post_body, errors=errors)
        
        r = http.request('GET', 'https://source.unsplash.com/400x300/?nature')

        image = base64.b64encode(r.data)
        
        new_post = Blog(post_title, post_body, image)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/blog?id={}'.format(new_post.id))

    return render_template('newpost.html', location="New Post", errors=errors)

@app.route('/blog', methods=['GET'])
def blog():
    posts = sort_data('id', 'desc')

    if 'id' in request.args:
        # If id is not an int just return all entries
        try:
            index = int(request.args['id'])
            if index > 0 and len(posts) > index-1:
                return render_template('showpost.html', location="All Post", post=get_post('id', index))
        except:
            pass

    return render_template('blog.html', location="All Post", posts=posts)

if __name__ == '__main__':
    app.run()