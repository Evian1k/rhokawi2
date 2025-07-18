"""
Authentication routes for user login, registration, and token management.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.schemas import user_schema, user_login_schema, error_schema
from app.utils import validate_json, success_response, handle_error

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@validate_json(user_schema)
def register(validated_data):
    """
    Register a new user.
    
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
        # Create new user
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        
        # Set role (defaults to 'client' if not specified)
        user.role = validated_data.get('role', 'client')
        
        # Save user to database
        db.session.add(user)
        db.session.commit()
        
        # Create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return success_response(
            message='User registered successfully',
            data={
                'user': user_schema.dump(user),
                'access_token': access_token,
                'refresh_token': refresh_token
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
        return handle_error(e, 'Failed to register user', 500)


@auth_bp.route('/login', methods=['POST'])
@validate_json(user_login_schema)
def login(validated_data):
    """
    Login user and return access tokens.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    """
    try:
        username = validated_data['username']
        password = validated_data['password']
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        # Validate user and password
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
                'Your account has been disabled',
                403
            )
        
        # Create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return success_response(
            message='Login successful',
            data={
                'user': user_schema.dump(user),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Login failed', 500)


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
                'User not found or inactive',
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
    Get current user information.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return handle_error(
                Exception('User not found'),
                'User not found',
                404
            )
        
        return success_response(
            message='User information retrieved successfully',
            data=user_schema.dump(user)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to get user information', 500)