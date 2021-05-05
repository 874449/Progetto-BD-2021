from flask import render_template, request, session
from flask_login import login_required
from . import main


@main.route('/')
def index():
    if session['email'] is not None:
        return render_template("home.html")
    return render_template("index.html")


@main.route('/secret')
@login_required
def secret():
    return '<h1>Shhhh!</1><p>It\'s a secret</p>'
