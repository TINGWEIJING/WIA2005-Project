import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, app, Flask, jsonify
)
from flask.wrappers import Response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS, cross_origin
from core.db import get_db
from core import view

bp = Blueprint('api', __name__, url_prefix='/api')
CORS(bp)

@bp.route('/get', methods=(['GET']))
def sampleGetRequest():
    """A sample GET API function"""
    error = None

    if error is not None:
        app.logger.error(error)
        return Response(status=500)

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

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

# The client and the server communication via json
@bp.route('/getroutes', methods=(['POST']))
def obtainRoutesRequest():
    """Get all routes from src and dest"""
    error = None
    # request.form
    # request.json
    # print(request.form)
    print(request.json)
    # for eachData in request.data:
    #     print(eachData)
    # srcLat = request.form.get('srcLat')
    # srcLong = request.form.get('srcLong')
    # destLat = request.form.get('destLat')
    # destLong = request.form.get('destLong')
    # try:
        # print(float(srcLat))
        # print(float(srcLong))
        # print(float(destLat))
        # print(float(destLong))
    # except ValueError:
    #     return "Unsuccessful", 501

    result = {
        "routes": [
            {
                "hub": "City-link Express",
                "distance": 10,
                "legs": [
                    {
                        "point": [1, 2]
                    },
                    {
                        "point": [3, 4]
                    },
                    {
                        "point": [3, 4]
                    },
                ]
            },
            {
                "hub": "Pos Laju",
                "distance": 9,
                "legs": [
                    {
                        "point": [1, 2]
                    },
                    {
                        "point": [3, 4]
                    }
                ]
            },
            {
                "hub": "GDEX",
                "distance": 8,
                "legs": [
                    {
                        "point": [1, 2]
                    },
                    {
                        "point": [3, 4]
                    }
                ]
            },
            {
                "hub": "J&T",
                "distance": 7,
                "legs": [
                    {
                        "point": [1, 2]
                    },
                    {
                        "point": [3, 4]
                    }
                ]
            },
            {
                "hub": "DHL",
                "distance": 6,
                "legs": [
                    {
                        "point": [1, 2]
                    },
                    {
                        "point": [3, 4]
                    }
                ]
            }
        ]
    }

    return result, 200

# http://127.0.0.1:5000/api/analyse
@bp.route('/analyse', methods=(['POST']))
def analyseRequest():
    """Get all routes from src and dest"""
    error = None
    # request.form
    # request.json
    print(request.json)
    url = request.json.get('url')
    text = request.json.get('text')

    result = {
        "pos_words":10,
        "neg_words":5,
        "neu_words":1,
    }

    return result, 200