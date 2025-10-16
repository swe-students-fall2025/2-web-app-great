from flask import Flask
from .db import init_db

def create_app(config_obj) -> Flask:
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_object(config_obj)

    init_db(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
