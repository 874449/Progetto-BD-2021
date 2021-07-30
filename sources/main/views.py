from flask import render_template, request, session
from flask_login import login_required
from . import main


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/secret')
@login_required
def secret():
    return '<h1>Shhhh!</1><p>It\'s a secret</p>'


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')