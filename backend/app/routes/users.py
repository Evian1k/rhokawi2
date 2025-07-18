"""
User management routes for CRUD operations.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.schemas import user_schema, users_schema, error_schema
from app.utils import validate_json, success_response, handle_error, admin_required, paginate_query

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get all users (with pagination).
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query users
        query = User.query.order_by(User.created_at.desc())
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Users retrieved successfully',
            data={
                'users': users_schema.dump(result['items']),
                'pagination': result['pagination']
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve users', 500)


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Get a specific user by ID.
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return handle_error(
                Exception('User not found'),
                f'User with ID {user_id} not found',
                404
            )
        
        return success_response(
            message='User retrieved successfully',
            data=user_schema.dump(user)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve user', 500)


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update a user's information.
    Current user can only update their own information, unless they are admin.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return handle_error(
                Exception('User not found'),
                f'User with ID {user_id} not found',
                404
            )
        
        # Check permissions
        if current_user_id != user_id and not current_user.is_admin:
            return handle_error(
                Exception('Forbidden'),
                'You can only update your own information',
                403
            )
        
        # Get and validate request data
        json_data = request.get_json()
        if not json_data:
            return handle_error(
                Exception('Bad Request'),
                'No JSON data provided',
                400
            )
        
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'email']
        if current_user.is_admin:
            allowed_fields.extend(['username', 'is_active', 'is_admin'])
        
        for field in allowed_fields:
            if field in json_data:
                setattr(user, field, json_data[field])
        
        # Update password if provided
        if 'password' in json_data:
            user.set_password(json_data['password'])
        
        db.session.commit()
        
        return success_response(
            message='User updated successfully',
            data=user_schema.dump(user)
        )
        
    except IntegrityError as e:
        db.session.rollback()
        if 'username' in str(e):
            message = 'Username already exists'
        elif 'email' in str(e):
            message = 'Email already exists'
        else:
            message = 'User with this information already exists'
        
        return handle_error(e, message, 409)
    
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to update user', 500)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
    Delete a user (admin only).
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return handle_error(
                Exception('User not found'),
                f'User with ID {user_id} not found',
                404
            )
        
        # Prevent deleting the last admin
        if user.is_admin:
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count <= 1:
                return handle_error(
                    Exception('Forbidden'),
                    'Cannot delete the last admin user',
                    403
                )
        
        db.session.delete(user)
        db.session.commit()
        
        return success_response(
            message='User deleted successfully',
            status_code=204
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete user', 500)


@users_bp.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    """
    Search users by username or email.
    
    Query Parameters:
    - q: Search query
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    """
    try:
        search_query = request.args.get('q', '').strip()
        
        if not search_query:
            return handle_error(
                Exception('Bad Request'),
                'Search query parameter "q" is required',
                400
            )
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Search users
        query = User.query.filter(
            (User.username.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%')) |
            (User.first_name.ilike(f'%{search_query}%')) |
            (User.last_name.ilike(f'%{search_query}%'))
        ).order_by(User.created_at.desc())
        
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Users found successfully',
            data={
                'users': users_schema.dump(result['items']),
                'pagination': result['pagination'],
                'query': search_query
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to search users', 500)