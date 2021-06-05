import os

from flask import Flask
from flask_pymongo import PyMongo

# https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/

mongo_db = None

def create_app(test_config=None):
    """
    Application factory function
    """
    # create and configure the app
    # __name__ is the name of current Python module
    # instance_relative_config=True means config file located at relative to instance folder (flask-tutorial)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # should be random value
        # location of SQLite database file
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # will overide default config from config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        # map to config instance
        app.config.from_mapping(test_config)

    # setting up MongoDB
    app.config["MONGO_URI"] = "mongodb+srv://admin:0KwfxU628CQ6uA66@cluster0.pibyp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    global mongo_db
    mongo_db = PyMongo(app).db

    # ensure the instance folder exists
    try:
        # check folder existence
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        db = mongo_db
        todo = db.todos.find_one()
        print(todo)
        return 'Hello, World!'

    # initialize app and register functions in db.py
    from . import db
    db.init_app(app)

    # register blueprint
    from . import api
    from . import view
    app.register_blueprint(api.bp)
    app.register_blueprint(view.bp)

    # secure session data
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

    return app


if __name__ == "__main__":
    """
    Run manually
    """
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
