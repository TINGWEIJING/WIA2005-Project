import sqlite3
from flask import Flask
from flask_pymongo import PyMongo
import click
# g is a namespace object that can store data during an application context
# read: https://flask.palletsprojects.com/en/1.1.x/appcontext/
from flask import current_app, g
from flask.cli import with_appcontext
from core import mongo_db
from core.algorithm.SentimentAnalysis import SentimentAnalysis

def init_app(app: Flask):
    """Initialize app for registering functions"""
    # call that function when cleaning up after returning the response
    # app.teardown_appcontext(close_db)
    # new command that can be called with the flask command
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        # mongo = PyMongo(current_app)
        # g.db = mongo.db
        g.db = mongo_db

    # return the connection of db which is stored in g
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize database"""
    db = get_db()
    # insert some data
    data_list = SentimentAnalysis.retrieve_all()
    db.analysis.remove({})
    for data in data_list:
        filter = {
            "courier":data['courier'],
            "url":data['url']
        }
        db.analysis.update_one(filter=filter, update={"$set":data}, upsert=True)



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
