import pymongo
from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = pymongo.MongoClient(
    'mongodb+srv://admin:admin@cluster0.xddvb.mongodb.net/task-manager?retryWrites=true&w=majority')
db.client.test


app = Flask(__name__)
csrf.init_app(app)