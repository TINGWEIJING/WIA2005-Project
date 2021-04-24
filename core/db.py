import sqlite3
from flask import Flask

import click
# g is a namespace object that can store data during an application context
# read: https://flask.palletsprojects.com/en/1.1.x/appcontext/
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app: Flask):
    """Initialize app for registering functions"""
    # call that function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # new command that can be called with the flask command
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # db path
            # parse the declared type for each column it returns
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # return tuple as row data

    # return the connection of db which is stored in g
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize database"""
    db = get_db()

    # Search for schema.sql file in flaskr
    with current_app.open_resource('schema.sql') as f:
        # run the sql file
        db.executescript(f.read().decode('utf8'))



@click.command('init-db')
# https://click.palletsprojects.com/en/7.x/api/#click.command
# defines a command line command called init-db that calls the init_db function
@with_appcontext
# https://flask.palletsprojects.com/en/1.1.x/api/#flask.cli.with_appcontext
# guaranteed to be executed with the script’s application context
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
