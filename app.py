from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app_config import app, db, login_manager, bcrypt, session
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.task import TaskForm
from model.task import Task
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
                if "max_id" not in session:
                    session["max_id"] = 0
                print("User authenticated")
                if list(db.users.aggregate(
                        [{"$project": {"username": session["username"], "max_id": {"$max": "$tasks.task_id"}}}]))[0][
                    "max_id"] is None:
                    session["max_id"] = 1
                    task["task_id"] = session["max_id"]
                else:
                    id = session["max_id"]
                    task["task_id"] = id + 1
                    session["max_id"] = id + 1
                print(session["max_id"])
                db.users.update_one({"username": session["username"]}, {'$push': {'tasks': task}})
                return redirect(url_for('home'))
            else:
                if "tasks" not in session:
                    session["tasks"] = []
                else:
                    tasks = session["tasks"]
                    print(f'session["tasks"]: {session["tasks"]}')
                    tasks.append(task)
                    session["tasks"] = tasks
                    print(f'session["tasks"]: {session["tasks"]}')
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
                    session["name"] = user["fullname"].split()
                    login_user(model_user)
                    return redirect(url_for('home'))
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
                "password": pw_hashed,
                "tasks": []
            }
            db.users.insert_one(user)
            model_user = User(user_json=user)
            return redirect(url_for('home'))
    return render_template('user_related/register.html', form=form)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
    db.users.update_one({'username': session["username"], 'tasks.task_id': id},
                        {'$pull': {"tasks": {'task_id': id}}})
    return redirect(url_for('home'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    user = db.users.find_one({"username": session["username"]})
    task = None
    task_id = None
    for item in list(user["tasks"]):
        if id == item["task_id"]:
            task = {
                'title': item["title"],
                'description': item["description"]
            }
            task_id = item["task_id"]
    print(task_id)
    task_model = Task(task_json=task)
    form = TaskForm(obj=task_model)

    if request.method == 'POST':
        if form.validate_on_submit():
            db.users.update_one({'username': session["username"], 'tasks.task_id': id},
                                {'$set': {"tasks.$.title": form.title.data,
                                          "tasks.$.description": form.description.data}})
            return redirect(url_for('home'))
    return render_template('task/edit_task.html', form=form, task_id=id)


@app.route('/complete/<int:id>')
def complete_task(id):
    if current_user.is_authenticated:
        db.users.update_one({'username': session["username"], 'tasks.task_id': id},
                            {'$pull': {"tasks": {'task_id': id}}})
    else:
        tasks = session["tasks"]
        tasks.pop(id)
        session["tasks"] = tasks
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    return User(db.users.find_one({"username": user_id}))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
