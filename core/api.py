import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, app, Flask, jsonify
)
from flask.wrappers import Response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS, cross_origin
from core.db import get_db
from core import view, mongo_db
from core.algorithm.SentimentAnalysis import SentimentAnalysis
from bson import json_util
import json
from core.algorithm.travelInfo import GoogleDirectionsRouting

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
    print(request.json)

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
    # print(request.json)
    source = request.json.get('start')
    destination = request.json.get('end')
    if source is None or destination is None:
        error = 'Source or destination address is empty'
        return error, 400

    newRoute = GoogleDirectionsRouting(source, destination)
    result = newRoute.get_sorted_routes()
    # print(json.dumps(result, indent = 4))

    if len(result.get('routes')) == 0:
        error = 'Source or destination address not found'
        return error, 400

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

@bp.route('/hello')
def hello():
    # db = mongo_db
    # todo = db.todos.find_one()
    # print(todo)
    # return json.loads(json.dumps(todo, default=json_util.default))
    data_list = SentimentAnalysis.retrieve_all()
    re_data = {
        'data':data_list
    }
    return re_data

@bp.route('/getAnalysis', methods=(['GET']))
def getAllAnalysis():
    '''Retrun json results of all sentiment analysis'''
    db = mongo_db
    cursor = db.analysis.find({})
    data_list = []
    for document in cursor:
        data = document
        del data['_id']
        del data['last_retrieve']
        data_list.append(data)
    return json.loads(json.dumps({"result":data_list}, default=json_util.default))
