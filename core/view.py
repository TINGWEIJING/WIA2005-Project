import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.wrappers import Response
from werkzeug.security import check_password_hash, generate_password_hash

from core.db import get_db

# A Blueprint is a way to organize a group of related views and other code
# Blueprint name 'view', __name__ is passed so that this object knows where it is defined
# remember to register this blueprint
bp = Blueprint('view', __name__)

@bp.route('/')
def loadMainPage():
    """Render html file"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('index.html')


@bp.route('/redirect')
def redirectPage() -> Response:
    """A sample redirect function which will redirect user to another URL"""
    # pass in the function name
    return redirect(url_for('view.loadMainPage'))

@bp.route('/send', methods=(['GET']))
def sendData():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('send_data.html')

@bp.route('/sentimentAnalysis.html', methods=(['GET']))
def getCityLinkMap():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('sentimentAnalysis.html')