from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '75fc0be48e8f8889688aa3e7'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)  # encrypt - decrypt password

login_manager=LoginManager(app) # for logging in

login_manager.login_view = 'login_page' # redirect to login page before accessing the market page
login_manager.login_message_category ='info'

from market import routes
