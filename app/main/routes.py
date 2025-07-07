from flask import render_template
from app.main import bp 

@bp.route('/')
@bp.route('/index')
def index():
    user = {"username": "Ewan"}
    return render_template("index.html", title="Home", user=user)

@bp.route('/api')
def api():
    return "Hello world!" 

