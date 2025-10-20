# loopu/db.py
from flask import current_app, g
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

DB_CLIENT_KEY = "_mongo_client"
DB_NAME = "loopu"

def get_client() -> MongoClient:
    """Return a cached MongoClient bound to the current app context."""
    if DB_CLIENT_KEY not in g:
        uri = current_app.config.get("MONGO_URI")
        g._mongo_client = MongoClient(uri)
    return g._mongo_client

def get_db():
    """Return a Database object. If URI has no default DB, fall back to DB_NAME."""
    client = get_client()
    try:
        db = client.get_default_database()
    except ConfigurationError:
        db = None
    if db is None:
        db = client[DB_NAME]
    return db

def init_db(app):
    """Register teardown hook to close MongoClient when app context ends."""
    @app.teardown_appcontext
    def close_connection(_exc):
        client = g.pop(DB_CLIENT_KEY, None)
        if client is not None:
            client.close()
