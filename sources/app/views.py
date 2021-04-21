from flask import Blueprint, render_template
from . import main


@main.route('/')
def home():
    return render_template("index.html")
