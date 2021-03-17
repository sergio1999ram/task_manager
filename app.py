from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

from app_config import app, db, login_manager, bcrypt
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.task import TaskForm
from model.user import User


@app.route('/', methods=['GET', 'POST'])
def home():
    form = TaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            task = {
                "title": form.title.data,
                "description": form.description.data
            }
            if current_user.is_authenticated:
                db.users.update_one({"username": session["username"]}, {'$push': {'tasks': task}})
                return redirect(url_for('home'))

    return render_template('home.html', form=form, db=db)


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
                    return redirect(url_for('home'))
            else:
                errors.append('Username or password incorrect')
    return render_template('user_related/login.html', form=form, errors=errors)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop("fullname", None)
    session.pop("username", None)
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
            model_user = User(user_json=user)
            login_user(model_user)
            session["username"] = user["username"]
            return redirect(url_for('tasks'))
    return render_template('user_related/register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User(db.users.find_one({"username": user_id}))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
