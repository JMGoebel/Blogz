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