from flask import Flask

from app.config import Config


def create_app():
    """Create and configure the Flask application."""

    application = Flask(
        __name__
    )

    application.config["SECRET_KEY"] = Config.SECRET_KEY

    application.config["DEBUG"] = Config.DEBUG

    application.config["DATABASE_PATH"] = str(
        Config.DATABASE_PATH
    )

    from app.routes import routes

    application.register_blueprint(
        routes
    )

    return application
