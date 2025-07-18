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
                Exception('Missing fields'),
                'Username, email, and password are required',
                400
            )
        
        # Create new admin user (not main admin)
        new_admin = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_main_admin=False  # Added admins are never main admin
        )
        
        # Save user to database
        db.session.add(new_admin)
        db.session.commit()
        
        return success_response(
            message='Admin user added successfully',
            data={
                'user': user_schema.dump(new_admin)
            },
            status_code=201
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
        return handle_error(e, 'Failed to add admin user', 500)


@auth_bp.route('/admins', methods=['GET'])
@jwt_required()
def get_admins():
    """
    Get list of all admin users (only main admin can access).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.can_add_admins():
            return handle_error(
                Exception('Unauthorized'),
                'Only the main admin can view admin list',
                403
            )
        
        admins = User.query.all()
        
        return success_response(
            message='Admin users retrieved successfully',
            data={
                'admins': [user_schema.dump(admin) for admin in admins]
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to get admin users', 500)


@auth_bp.route('/admins/<int:admin_id>', methods=['DELETE'])
@jwt_required()
def delete_admin(admin_id):
    """
    Delete an admin user (only main admin can do this, cannot delete main admin).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.can_add_admins():
            return handle_error(
                Exception('Unauthorized'),
                'Only the main admin can delete admin users',
                403
            )
        
        admin_to_delete = User.query.get(admin_id)
        
        if not admin_to_delete:
            return handle_error(
                Exception('Not found'),
                'Admin user not found',
                404
            )
        
        if admin_to_delete.is_main_admin:
            return handle_error(
                Exception('Cannot delete main admin'),
                'The main admin cannot be deleted',
                403
            )
        
        if admin_to_delete.id == current_user.id:
            return handle_error(
                Exception('Cannot delete self'),
                'You cannot delete your own account',
                403
            )
        
        db.session.delete(admin_to_delete)
        db.session.commit()
        
        return success_response(
            message='Admin user deleted successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete admin user', 500)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return handle_error(
                Exception('Invalid user'),
                'Admin user not found or inactive',
                404
            )
        
        # Create new access token
        access_token = create_access_token(identity=user.id)
        
        return success_response(
            message='Token refreshed successfully',
            data={
                'access_token': access_token
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Token refresh failed', 500)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current admin user information.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return handle_error(
                Exception('User not found'),
                'Admin user not found',
                404
            )
        
        return success_response(
            message='Admin user information retrieved successfully',
            data=user_schema.dump(user)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to get admin user information', 500)