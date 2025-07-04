from flask import render_template, flash, redirect
from app.main import bp 
from app.login import LoginForm

@bp.route('/')
@bp.route('/index')
def index():
    user = {"username": "Ewan"}
    return render_template("index.html", title="Home", user=user)

@bp.route('/api')
def api():
    return "Hello world!" 

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Login', form=form)
