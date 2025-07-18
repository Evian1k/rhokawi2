"""
Authentication routes for admin login and admin management.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.schemas import user_schema, user_login_schema, error_schema
from app.utils import validate_json, success_response, handle_error

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET'])
def login_info():
    """
    Login endpoint info for GET requests.
    """
    return jsonify({
        'message': 'Login endpoint requires POST method',
        'method': 'POST',
        'endpoint': '/api/auth/login',
        'expected_data': {
            'username': 'string',
            'password': 'string'
        },
        'example': {
            'username': 'admin',
            'password': 'admin123'
        }
    }), 405


@auth_bp.route('/login', methods=['POST'])
@validate_json(user_login_schema)
def login(validated_data):
    """
    Admin login endpoint.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    """
    try:
        username = validated_data['username']
        password = validated_data['password']
        
        # Find admin user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        # Validate user and password (only admins exist now)
        if not user or not user.check_password(password):
            return handle_error(
                Exception('Invalid credentials'),
                'Invalid username or password',
                401
            )
        
        # Check if user is active
        if not user.is_active:
            return handle_error(
                Exception('Account disabled'),
                'Your admin account has been disabled',
                403
            )
        
        # Create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return success_response(
            message='Admin login successful',
            data={
                'user': user_schema.dump(user),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Login failed', 500)


@auth_bp.route('/add-admin', methods=['POST'])
@jwt_required()
def add_admin():
    """
    Add a new admin user (only main admin can do this).
    
    Expected JSON:
    {
        "username": "string",
        "email": "string", 
        "password": "string",
        "first_name": "string" (optional),
        "last_name": "string" (optional)
    }
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.can_add_admins():
            return handle_error(
                Exception('Unauthorized'),
                'Only the main admin can add other admins',
                403
            )
        
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return handle_error(
                Exception('Missing required fields'),
                'Username, email, and password are required',
                400
            )
        
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return handle_error(
                Exception('User already exists'),
                'Username or email already exists',
                409
            )
        
        # Create new admin user
        new_admin = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_main_admin=False  # New admins are not main admins
        )
        
        db.session.add(new_admin)
        db.session.commit()
        
        return success_response(
            message='Admin user created successfully',
            data={
                'user': user_schema.dump(new_admin)
            }
        )
        
    except IntegrityError:
        db.session.rollback()
        return handle_error(
            Exception('Database integrity error'),
            'Username or email already exists',
            409
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to create admin user', 500)


@auth_bp.route('/admins', methods=['GET'])
@jwt_required()
def get_admins():
    """
    Get all admin users (only main admin can do this).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.can_add_admins():
            return handle_error(
                Exception('Unauthorized'),
                'Only the main admin can view all admins',
                403
            )
        
        admins = User.query.all()
        
        return success_response(
            message='Admin users retrieved successfully',
            data={
                'admins': user_schema.dump(admins, many=True)
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve admin users', 500)


@auth_bp.route('/admins/<int:admin_id>', methods=['DELETE'])
@jwt_required()
def delete_admin(admin_id):
    """
    Delete an admin user (only main admin can do this).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.can_add_admins():
            return handle_error(
                Exception('Unauthorized'),
                'Only the main admin can delete other admins',
                403
            )
        
        # Prevent deleting self
        if current_user_id == admin_id:
            return handle_error(
                Exception('Cannot delete self'),
                'You cannot delete your own admin account',
                400
            )
        
        admin_to_delete = User.query.get(admin_id)
        
        if not admin_to_delete:
            return handle_error(
                Exception('Admin not found'),
                'Admin user not found',
                404
            )
        
        # Prevent deleting other main admins
        if admin_to_delete.is_main_admin:
            return handle_error(
                Exception('Cannot delete main admin'),
                'Cannot delete main admin accounts',
                400
            )
        
        db.session.delete(admin_to_delete)
        db.session.commit()
        
        return success_response(
            message='Admin user deleted successfully',
            data={
                'deleted_admin': user_schema.dump(admin_to_delete)
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete admin user', 500)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return handle_error(
                Exception('User not found'),
                'Current user not found',
                404
            )
        
        return success_response(
            message='Current user retrieved successfully',
            data=user_schema.dump(current_user)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve current user', 500)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh access token using refresh token.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_active:
            return handle_error(
                Exception('Invalid user'),
                'User not found or inactive',
                401
            )
        
        new_access_token = create_access_token(identity=current_user_id)
        
        return success_response(
            message='Token refreshed successfully',
            data={
                'access_token': new_access_token
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to refresh token', 500)


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change password endpoint (only main admin can change their own password).
    
    Expected JSON:
    {
        "current_password": "string",
        "new_password": "string"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return handle_error(
                Exception('User not found'),
                'Current user not found',
                404
            )
        
        # Only main admin can change their own password
        if not current_user.is_main_admin:
            return handle_error(
                Exception('Unauthorized'),
                'Only the main admin can change their password',
                403
            )
        
        data = request.get_json()
        
        if not data or not data.get('current_password') or not data.get('new_password'):
            return handle_error(
                Exception('Missing required fields'),
                'Current password and new password are required',
                400
            )
        
        # Verify current password
        if not current_user.check_password(data['current_password']):
            return handle_error(
                Exception('Invalid current password'),
                'Current password is incorrect',
                401
            )
        
        # Update password
        current_user.set_password(data['new_password'])
        db.session.commit()
        
        return success_response(
            message='Password changed successfully',
            data={}
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to change password', 500)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout endpoint (token invalidation handled on frontend).
    """
    return success_response(
        message='Logout successful',
        data={}
    )