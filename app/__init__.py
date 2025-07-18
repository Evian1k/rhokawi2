"""
Flask application factory.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """
    Create and configure the Flask application.
    
    Args:
        config_name (str): Configuration name to use ('development', 'testing', 'production')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.routes import register_routes
    register_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app