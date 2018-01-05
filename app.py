app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz_app:{}@localhost:8889/blogz'.format('f1nc53pM6fz0apb7ms')
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

if __name__ == '__main__':
  app.run()