import os

import pymongo
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

client = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0.xddvb.mongodb.net/task-manager?retryWrites=true&w=majority')
db = client.test

app.config['SECRET_KEY'] = os.urandom(32)
app.config['WTF_CSRF_ENABLED'] = os.getenv('WTF_CSRF_STATUS')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')
app.config['DEBUG'] = os.getenv('DEBUG')
