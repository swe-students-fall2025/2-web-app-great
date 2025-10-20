from flask import current_app, g
from pymongo import MongoClient
def init_db(app):
    @app.teardown_appcontext
    def close_client(exception=None):
        client = g.pop('mongo_client', None)
        if client is not None:
            client.close()
def get_db():
    if 'mongo_client' not in g:
        g.mongo_client = MongoClient(current_app.config['MONGO_URI'])
    return g.mongo_client.get_database('loopu')
