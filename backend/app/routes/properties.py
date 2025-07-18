"""
Property management routes for real estate listings.
"""

import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, or_
from app import db
from app.models import Property, User
from app.schemas import (
    property_schema, properties_schema, property_create_schema, 
    property_update_schema, property_search_schema
)
from app.utils import (
    validate_json, success_response, handle_error, 
    paginate_query, agent_or_admin_required, create_property_search_query
)

properties_bp = Blueprint('properties', __name__)


@properties_bp.route('', methods=['GET'])
def get_properties():
    """
    Get all properties (with pagination and basic filtering).
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - status: Filter by status (available, sold, pending)
    - agent_id: Filter by agent ID
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', 'available')
        agent_id = request.args.get('agent_id', type=int)
        
        # Build query
        query = Property.query.filter_by(status=status)
        
        if agent_id:
            query = query.filter_by(agent_id=agent_id)
        
        query = query.order_by(Property.created_at.desc())
        
        # Execute paginated query
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Properties retrieved successfully',
            data={
                'properties': properties_schema.dump(result['items']),
                'pagination': result['pagination']
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve properties', 500)


@properties_bp.route('/search', methods=['GET'])
def search_properties():
    """
    Search properties with advanced filters.
    
    Query Parameters:
    - location: Location search (partial match)
    - property_type: Type of property
    - min_price: Minimum price
    - max_price: Maximum price
    - bedrooms: Minimum number of bedrooms
    - status: Property status (default: available)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    """
    try:
        # Validate search parameters
        search_params = property_search_schema.load(request.args)
        
        # Build search query
        query = create_property_search_query(search_params)
        
        # Execute paginated query
        result = paginate_query(
            query, 
            search_params.get('page', 1), 
            search_params.get('per_page', 20)
        )
        
        return success_response(
            message='Property search completed',
            data={
                'properties': properties_schema.dump(result['items']),
                'pagination': result['pagination'],
                'search_params': search_params
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to search properties', 500)


@properties_bp.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """
    Get a specific property by ID.
    """
    try:
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        return success_response(
            message='Property retrieved successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve property', 500)


@properties_bp.route('', methods=['POST'])
@agent_or_admin_required
@validate_json(property_create_schema)
def create_property(validated_data):
    """
    Create a new property (agent or admin only).
    
    Expected JSON:
    {
        "title": "string",
        "description": "string",
        "property_type": "house|apartment|condo|townhouse|land|commercial",
        "location": "string",
        "address": "string",
        "price": decimal,
        "bedrooms": integer,
        "bathrooms": integer,
        "square_feet": integer,
        "lot_size": "string",
        "year_built": integer,
        "features": ["feature1", "feature2"]
    }
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Create new property
        property = Property(
            title=validated_data['title'],
            description=validated_data.get('description'),
            property_type=validated_data['property_type'],
            location=validated_data['location'],
            address=validated_data.get('address'),
            price=validated_data['price'],
            bedrooms=validated_data.get('bedrooms'),
            bathrooms=validated_data.get('bathrooms'),
            square_feet=validated_data.get('square_feet'),
            lot_size=validated_data.get('lot_size'),
            year_built=validated_data.get('year_built'),
            features=json.dumps(validated_data.get('features', [])),
            agent_id=current_user_id
        )
        
        # Save property to database
        db.session.add(property)
        db.session.commit()
        
        return success_response(
            message='Property created successfully',
            data=property_schema.dump(property),
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to create property', 500)


@properties_bp.route('/<int:property_id>', methods=['PUT'])
@agent_or_admin_required
@validate_json(property_update_schema)
def update_property(property_id, validated_data):
    """
    Update an existing property (agent or admin only).
    Agent can only update their own properties, admin can update any.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get the property
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        # Check permissions (agents can only update their own properties)
        if not current_user.is_admin and property.agent_id != current_user_id:
            return handle_error(
                Exception('Forbidden'),
                'You can only update your own properties',
                403
            )
        
        # Update property fields
        for field, value in validated_data.items():
            if field == 'features' and value is not None:
                setattr(property, field, json.dumps(value))
            elif value is not None:
                setattr(property, field, value)
        
        db.session.commit()
        
        return success_response(
            message='Property updated successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to update property', 500)


@properties_bp.route('/<int:property_id>', methods=['DELETE'])
@agent_or_admin_required
def delete_property(property_id):
    """
    Delete a property (agent or admin only).
    Agent can only delete their own properties, admin can delete any.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get the property
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        # Check permissions (agents can only delete their own properties)
        if not current_user.is_admin and property.agent_id != current_user_id:
            return handle_error(
                Exception('Forbidden'),
                'You can only delete your own properties',
                403
            )
        
        db.session.delete(property)
        db.session.commit()
        
        return success_response(
            message='Property deleted successfully',
            status_code=204
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete property', 500)


@properties_bp.route('/agent/<int:agent_id>', methods=['GET'])
def get_agent_properties(agent_id):
    """
    Get all properties by a specific agent.
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - status: Filter by status
    """
    try:
        # Check if agent exists
        agent = User.query.get(agent_id)
        if not agent or not agent.can_manage_properties():
            return handle_error(
                Exception('Agent not found'),
                f'Agent with ID {agent_id} not found',
                404
            )
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', 'available')
        
        # Query agent's properties
        query = Property.query.filter_by(agent_id=agent_id, status=status).order_by(Property.created_at.desc())
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message=f'Properties by {agent.username} retrieved successfully',
            data={
                'properties': properties_schema.dump(result['items']),
                'pagination': result['pagination'],
                'agent': {
                    'id': agent.id,
                    'username': agent.username,
                    'role': agent.role
                }
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve agent properties', 500)


@properties_bp.route('/<int:property_id>/images', methods=['POST'])
@agent_or_admin_required
def add_property_images(property_id):
    """
    Add images to a property.
    Images should be uploaded via the /upload endpoint first.
    
    Expected JSON:
    {
        "image_urls": ["url1", "url2", ...]
    }
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get the property
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                f'Property with ID {property_id} not found',
                404
            )
        
        # Check permissions
        if not current_user.is_admin and property.agent_id != current_user_id:
            return handle_error(
                Exception('Forbidden'),
                'You can only update your own properties',
                403
            )
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data or 'image_urls' not in json_data:
            return handle_error(
                Exception('Bad Request'),
                'image_urls array is required',
                400
            )
        
        # Get existing images
        existing_images = json.loads(property.images) if property.images else []
        
        # Add new images
        new_images = json_data['image_urls']
        all_images = existing_images + new_images
        
        # Update property
        property.images = json.dumps(all_images)
        db.session.commit()
        
        return success_response(
            message='Images added successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to add images', 500)