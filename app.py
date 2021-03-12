from app_config import app
from flask import render_template


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=8080)
