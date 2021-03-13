from app_config import app, db, csrf
from flask import render_template, request, redirect, url_for
from forms.register import RegisterForm
import jsonify

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = {
                "fullname": form.fullname.data,
                "email": form.email.data,
                "username": form.username.data,
                "password": form.password.data
            }
            db.users.insert_one(user)
            return redirect(url_for('home'))
    return render_template('user_related/register.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)


