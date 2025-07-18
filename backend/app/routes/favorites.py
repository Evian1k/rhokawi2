"""
Favorites routes for users to save and manage favorite properties.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Property, User
from app.schemas import properties_schema
from app.utils import success_response, handle_error, paginate_query

favorites_bp = Blueprint('favorites', __name__)


@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    """
    Get user's favorite properties (with pagination).
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
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
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query user's favorite properties
        from app.models import user_favorites
        query = Property.query.join(user_favorites).filter(
            user_favorites.c.user_id == current_user_id
        ).order_by(Property.created_at.desc())
        
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Favorite properties retrieved successfully',
            data={
                'properties': properties_schema.dump(result['items']),
                'pagination': result['pagination']
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve favorite properties', 500)


@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    """
    Add a property to user's favorites.
    
    Expected JSON:
    {
        "property_id": integer
    }
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
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data or 'property_id' not in json_data:
            return handle_error(
                Exception('Bad Request'),
                'property_id is required',
                400
            )
        
        property_id = json_data['property_id']
        
        # Check if property exists
        property = Property.query.get(property_id)
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        # Check if already favorited
        if property in user.favorite_properties:
            return handle_error(
                Exception('Already favorited'),
                'Property is already in favorites',
                409
            )
        
        # Add to favorites
        user.favorite_properties.append(property)
        db.session.commit()
        
        return success_response(
            message='Property added to favorites',
            data={
                'property_id': property_id,
                'property_title': property.title
            },
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to add property to favorites', 500)


@favorites_bp.route('/<int:property_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(property_id):
    """
    Remove a property from user's favorites.
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
        
        # Check if property exists
        property = Property.query.get(property_id)
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        # Check if property is in favorites
        if property not in user.favorite_properties:
            return handle_error(
                Exception('Not in favorites'),
                'Property is not in favorites',
                404
            )
        
        # Remove from favorites
        user.favorite_properties.remove(property)
        db.session.commit()
        
        return success_response(
            message='Property removed from favorites',
            status_code=204
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to remove property from favorites', 500)


@favorites_bp.route('/<int:property_id>/check', methods=['GET'])
@jwt_required()
def check_favorite(property_id):
    """
    Check if a property is in user's favorites.
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
        
        # Check if property exists
        property = Property.query.get(property_id)
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        is_favorite = property in user.favorite_properties
        
        return success_response(
            message='Favorite status checked',
            data={
                'property_id': property_id,
                'is_favorite': is_favorite
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to check favorite status', 500)