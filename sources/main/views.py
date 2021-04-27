from flask import render_template, request, session
from . import main


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/<str:id>')
def main_page(id):
    if id == session['email']:
        return render_template("home.html")
    else:
        return render_template("error.html", number=403, message='Something went wrong')
