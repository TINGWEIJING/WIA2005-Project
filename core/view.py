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

@bp.route('/cityLinkMap.html', methods=(['GET']))
def getCityLinkMap():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('cityLinkMap.html')

@bp.route('/posLajuMap.html', methods=(['GET']))
def getPosLajuMap():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('posLajuMap.html')

@bp.route('/gdexMap.html', methods=(['GET']))
def getGdexMap():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('gdexMap.html')

@bp.route('/jAndTMap.html', methods=(['GET']))
def getJAndTMap():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('jAndTMap.html')

@bp.route('/dhlMap.html', methods=(['GET']))
def getDHLMap():
    """Send data"""
    # pass in the file path, default starting with "/templates/" path
    return render_template('dhlMap.html')
