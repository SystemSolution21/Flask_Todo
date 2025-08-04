import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Load the instance config, if it exists
    app.config.from_pyfile("config.py", silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore

    with app.app_context():
        db.create_all()

    # Register blueprints
    from . import auth, views

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)

    return app
