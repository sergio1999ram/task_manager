from app_config import app, db
from flask import render_template
from models import user


@app.route('/')
def home():
    print(db.users.insert_one(user).inserted_id)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=8080)
