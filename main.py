from app_config import app, db, csrf
from flask import render_template, request, redirect, url_for, make_response
from forms.register import RegisterForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        return redirect(url_for('home'))
    if request.method == 'POST':
        pass
    return render_template('user_related/register.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
