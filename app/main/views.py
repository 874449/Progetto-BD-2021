from flask import render_template, request, session
from flask_login import login_required, current_user
from .. models import *
from .. import db
from . import main
import datetime


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template("index.html")


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        nuovo = Questionario('Nuovo', datetime.datetime)
    return render_template('dashboard.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')