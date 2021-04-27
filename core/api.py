import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, app
)
from flask.wrappers import Response
from werkzeug.security import check_password_hash, generate_password_hash

from core.db import get_db
from core import view

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/get', methods=(['GET']))
def sampleGetRequest():
    """A sample GET API function"""
    error = None

    if error is not None:
        app.logger.error(error)
        return Response(status=500)

    error = None

    results = {}
    results['Text'] = 'A'
    results['Value'] = 1
    # return the python dict, will auto jsonify
    return results


@bp.route('/send', methods=(['POST']))
def samplePostRequest():
    """A sample POST API function"""
    error = None
    print(request.form)

    if error is not None:
        flash(error)

    # return "Success", 200
    return redirect(url_for('view.loadMainPage'))
