from flask import render_template
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    return render_template("error.html", number=403, message='Forbidden'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("error.html", number=404, message='Not Found'), 400


@main.app_errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', number=405, message='Method not allowed'), 405


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", number=500, message='Internal Server Error'), 500
