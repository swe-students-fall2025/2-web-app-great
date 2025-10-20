from flask import Flask
from .db import init_db
from .routes import bp as main_bp
from .auth import bp as auth_bp, login_manager
def create_app(config_obj):
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_object(config_obj)
    init_db(app)
    login_manager.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app
