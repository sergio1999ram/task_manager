from json import encoder

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, current_user, logout_user

from app_config import app, db, login_manager, bcrypt
from forms.login import LoginForm
from forms.register import RegisterForm
from model.user import User


@app.route('/')
def home():
    total_users = db.users.count_documents({})
    return render_template('home.html', total_users=total_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    errors = []
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            # JSON object
            user = db.users.find_one({"username": username})

            if user:
                if username == user["username"] and bcrypt.check_password_hash(user["password"], password):
                    # model_user for login reasons
                    model_user = User(user_json=user)
                    # Printing JSON object
                    session["username"] = user["username"]
                    session["fullname"] = user["fullname"]
                    login_user(model_user)
                    flash('Login successful')
                    return redirect(url_for('tasks'))
            else:
                errors.append('Username or password incorrect')
    return render_template('user_related/login.html', form=form, errors=errors)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pw_hashed = bcrypt.generate_password_hash(form.password.data)
            print(f'Password: {form.password.data}')
            print(f'Hashed: {pw_hashed}')
            user = {
                "fullname": form.fullname.data,
                "email": form.email.data,
                "username": form.username.data,
                "password": pw_hashed
            }
            db.users.insert_one(user)
            return redirect(url_for('home'))
    return render_template('user_related/register.html', form=form)


@app.route('/contact')
def contact():
    return render_template('under_construction.html')


@app.route('/user/tasks')
@login_required
def tasks():
    return render_template('tasks.html', user=db.users.find_one({"username": session["username"]}))


@login_manager.user_loader
def load_user(user_id):
    return User(db.users.find_one({"username": user_id}))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
