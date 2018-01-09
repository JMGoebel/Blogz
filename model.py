''' MODEL '''
import datetime
from main import db

class Blog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), unique=True, nullable=False)
  body = db.Column(db.Text, nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
  edited_on = db.Column(db.DateTime, nullable=True)

  def __init__(self, title, body, owner):
    self.title = title
    self.body = body
    self.owner = owner

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(32), unique=True, nullable=False)
  pw_hash = db.Column(db.String(64), nullable=False)
  pw_salt = db.Column(db.String(64), nullable=False)
  blogs = db.relationship('Blog', backref='owner', lazy=True)
  created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())

  def __init__(self, username, pw_hash, pw_salt):
    self.username = username
    self.pw_hash = pw_hash
    self.pw_salt = pw_salt