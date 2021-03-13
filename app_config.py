import os

import pymongo
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect

load_dotenv('.env')

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

client = pymongo.MongoClient(
    'mongodb+srv://admin:admin@cluster0.xddvb.mongodb.net/task-manager?retryWrites=true&w=majority')
db = client.test

app.config['SECRET_KEY'] = os.getenv('SECRETKEY')
