from flask import render_template, request, session
from . import main


@main.route('/')
def index():
    if session['email'] is not None:
        return render_template("home.html")
    return render_template("index.html")
