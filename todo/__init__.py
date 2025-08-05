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

    # Set default configuration that can be overridden by instance/config.py
    app.config.from_mapping(
        # A default secret key for development.
        # This SHOULD be overridden with a random value in instance/config.py
        SECRET_KEY="dev",
        # Default to a simple SQLite database.
        # This WILL be overridden by the PostgreSQL URI in instance/config.py
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'todo.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # This will override the defaults set above.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore[assignment]

    with app.app_context():
        db.create_all()

    # Register blueprints
    from . import auth, views

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)

    return app
