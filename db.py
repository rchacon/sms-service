import os

from flask import g
from pymongo import MongoClient


class Mongo(object):
    def __init__(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        mongo = getattr(g, '_database', None)
        if mongo is not None:
            mongo.close()

    def get_db(self):
        uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/sms')
        mongo = g._database = MongoClient(uri)
        db = mongo.get_default_database()
        return db

    @property
    def db(self):
        mongo = getattr(g, '_database', None)
        if mongo is None:
            return self.get_db()
        db = mongo.get_default_database()
        return db
