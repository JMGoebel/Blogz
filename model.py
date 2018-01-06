''' MODEL '''
from main import db

class Blog(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), unique=True, nullable=False)
  body = db.Column(db.Text, nullable=False)

  def __init__(self, title, body):
    self.title = title
    self.body = body