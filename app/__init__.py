from flask import Flask

from flask_cors import CORS


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="db.sqlite",
    )
    CORS(app)

    from . import db

    db.init_app(app)

    from .task.views import bp as task_bp

    app.register_blueprint(task_bp)

    return app
