from flask import Blueprint, render_template
from sources import app as app

main = Blueprint('main', __name__)

from . import views, auth, errors
