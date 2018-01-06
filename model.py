''' MODEL '''
from main import db

class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), unique=True, nullable=False)
  body = db.Column(db.Text, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __init__(self, title, body):
    self.title = title
    self.body = body

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(32), unique=True, nullable=False)
  password = db.Column(db.String(64), nullable=False)
  blogs = db.relationship('Blog', backref='user', lazy=True)

  def __init__(self, title, body):
    self.title = title
    self.body = body