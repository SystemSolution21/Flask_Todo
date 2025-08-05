import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# It's good practice to initialize extensions here
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # --- Configuration Loading ---
    # 1. Set default configuration
    app.config.from_mapping(
        # A default secret key for development, overridden by environment
        SECRET_KEY="dev",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 2. Load configuration from environment variables (preferred)
    # This will override the defaults and is perfect for containers.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", app.config["SECRET_KEY"])
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore

    # Import models to ensure they're registered
    from . import models

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Create tables
    with app.app_context():
        db.create_all()

    # Import and register the blueprints
    from . import auth, views

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)

    return app
