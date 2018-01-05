from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

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