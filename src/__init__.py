from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SECRET_KEY'] = '76aaa0abbe2803cd3e0cfc3b91ce500f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init api
api = Api(app, title='goTourApi')

# init bcrypt
bcrypt = Bcrypt(app)


from src import urls