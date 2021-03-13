import os

import pymongo
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

load_dotenv('.env')

app = Flask(__name__)
csrf = CSRFProtect()
login_manager = LoginManager()

bcrypt = Bcrypt(app)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

client = pymongo.MongoClient(os.getenv('DATABASE_URL'))
db = client.test

app.config['SECRET_KEY'] = os.getenv('SECRETKEY')
