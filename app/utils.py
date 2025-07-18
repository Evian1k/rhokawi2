"""
Utility functions for the Flask application.
"""

import os
import secrets
import string
from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models import User
from app.schemas import error_schema


def validate_json(schema):
    """
    Decorator to validate JSON request data against a Marshmallow schema.
    
    Args:
        schema: Marshmallow schema instance to validate against
    
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get JSON data from request
                json_data = request.get_json()
                if not json_data:
                    return jsonify(error_schema.dump({
                        'error': 'Bad Request',
                        'message': 'No JSON data provided',
                        'status_code': 400
                    })), 400
                
                # Validate data against schema
                validated_data = schema.load(json_data)
                
                # Pass validated data to the route function
                return f(validated_data, *args, **kwargs)
                
            except ValidationError as e:
                return jsonify(error_schema.dump({
                    'error': 'Validation Error',
                    'message': str(e.messages),
                    'status_code': 400
                })), 400
            except Exception as e:
                return jsonify(error_schema.dump({
                    'error': 'Internal Server Error',
                    'message': 'An unexpected error occurred',
                    'status_code': 500
                })), 500
        
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorator to require admin privileges for a route.
    
    Args:
        f: Function to decorate
    
    Returns:
        Decorated function
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify(error_schema.dump({
                'error': 'Forbidden',
                'message': 'Admin privileges required',
                'status_code': 403
            })), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user():
    """
    Get the current authenticated user.
    
    Returns:
        User: Current user instance or None
    """
    try:
        current_user_id = get_jwt_identity()
        if current_user_id:
            return User.query.get(current_user_id)
    except Exception:
        pass
    return None


def generate_random_string(length=32):
    """
    Generate a random string of specified length.
    
    Args:
        length (int): Length of the string to generate
    
    Returns:
        str: Random string
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def safe_filename(filename):
    """
    Generate a safe filename by removing/replacing unsafe characters.
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Safe filename
    """
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Ensure filename is not empty
    if not filename:
        filename = 'file'
    
    return filename


def paginate_query(query, page=1, per_page=20, max_per_page=100):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page (int): Page number (1-based)
        per_page (int): Items per page
        max_per_page (int): Maximum items per page
    
    Returns:
        dict: Pagination data with items and metadata
    """
    # Validate parameters
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    
    # Execute paginated query
    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': paginated.items,
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_prev': paginated.has_prev,
            'has_next': paginated.has_next
        }
    }


def handle_error(error, message=None, status_code=500):
    """
    Handle and format error responses.
    
    Args:
        error: Exception or error object
        message (str): Custom error message
        status_code (int): HTTP status code
    
    Returns:
        tuple: JSON response and status code
    """
    error_message = message or str(error) or 'An unexpected error occurred'
    
    # Log error if in development
    if current_app.debug:
        current_app.logger.error(f'Error: {error_message}')
    
    return jsonify(error_schema.dump({
        'error': error.__class__.__name__ if hasattr(error, '__class__') else 'Error',
        'message': error_message,
        'status_code': status_code
    })), status_code


def success_response(message, data=None, status_code=200):
    """
    Create a standardized success response.
    
    Args:
        message (str): Success message
        data: Response data
        status_code (int): HTTP status code
    
    Returns:
        tuple: JSON response and status code
    """
    response_data = {'message': message}
    if data is not None:
        response_data['data'] = data
    
    return jsonify(response_data), status_code