import pymongo
from flask import Flask

db = pymongo.MongoClient(
    'mongodb+srv://admin:admin@cluster0.xddvb.mongodb.net/task-manager?retryWrites=true&w=majority')
db.client.test

app = Flask(__name__)
