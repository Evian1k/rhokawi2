"""
Routes package initialization.
"""

from flask import Blueprint
from .auth import auth_bp
from .users import users_bp
from .posts import posts_bp
from .main import main_bp


def register_routes(app):
    """
    Register all blueprints with the Flask application.
    
    Args:
        app: Flask application instance
    """
    # Register main blueprint
    app.register_blueprint(main_bp)
    
    # Register API blueprints with URL prefix
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')