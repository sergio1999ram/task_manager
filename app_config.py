import os

import pymongo
from flask import Flask
from flask_wtf.csrf import CSRFProtect

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0.xddvb.mongodb.net/task-manager?retryWrites=true&w=majority")
db = client.test

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['WTF_CSRF_ENABLED'] = True
