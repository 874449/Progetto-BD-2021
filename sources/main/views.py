from flask import render_template, request, session
from . import main


@main.route('/')
def index():
    return render_template("index.html")

