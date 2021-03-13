import os

import pymongo
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

client = pymongo.MongoClient(os.getenv('DATABASE_URL'))
db = client.test

app.config['SECRET_KEY'] = os.urandom(32)
