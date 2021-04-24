import os

from flask import Flask

# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/


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

    # ensure the instance folder exists
    try:
        # check folder existence
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # initialize app and register functions in db.py
    # from . import db
    # db.init_app(app)

    # register blueprint
    from . import api
    from . import view
    app.register_blueprint(api.bp)
    app.register_blueprint(view.bp)

    return app


if __name__ == "__main__":
    """
    Run manually
    """
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
