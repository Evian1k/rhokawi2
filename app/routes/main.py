"""
Main routes for basic endpoints and health checks.
"""

from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Root endpoint."""
    return jsonify({
        'message': 'Flask API is running',
        'version': '1.0.0',
        'status': 'healthy'
    })


@main_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running properly'
    })


@main_bp.route('/api')
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'Real Estate API',
        'version': '1.0.0',
        'description': 'A comprehensive real estate platform API',
        'endpoints': {
            'auth': '/api/auth',
            'users': '/api/users',
            'properties': '/api/properties',
            'favorites': '/api/favorites',
            'contact': '/api/contact',
            'upload': '/api/upload'
        },
        'features': [
            'JWT Authentication',
            'Role-based access control',
            'Property management',
            'Property search and filtering',
            'User favorites',
            'Contact messages',
            'File uploads'
        ]
    })