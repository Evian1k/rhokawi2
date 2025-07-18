"""
Property management routes for real estate listings.
"""

import json
import os
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
    paginate_query, admin_required, create_property_search_query
)

properties_bp = Blueprint('properties', __name__)


@properties_bp.route('', methods=['GET'])
def get_properties():
    """
    Get all properties (public endpoint - shows verified properties to public).
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - status: Filter by status (available, sold, pending)
    - show_all: If authenticated admin, can see all properties
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', 'available')
        show_all = request.args.get('show_all', 'false').lower() == 'true'
        
        # Build query - for public, only show verified properties
        query = Property.query.filter_by(status=status)
        
        # Check if this is an admin request for all properties
        is_admin = False
        try:
            from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            if current_user_id:
                current_user = User.query.get(current_user_id)
                is_admin = current_user and current_user.is_admin
        except:
            pass
        
        # If not admin or not requesting all, only show verified properties
        if not (is_admin and show_all):
            query = query.filter_by(is_verified=True)
        
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
        return handle_error(e, 'Failed to get properties', 500)


@properties_bp.route('/search', methods=['GET'])
def search_properties():
    """
    Search properties with advanced filtering (public endpoint - only verified properties).
    """
    try:
        # Get search parameters from query string
        search_params = request.args.to_dict()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build search query
        query = create_property_search_query(search_params)
        
        # Only show verified properties to public
        query = query.filter_by(is_verified=True)
        
        query = query.order_by(Property.created_at.desc())
        
        # Execute paginated query
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Properties search completed',
            data={
                'properties': properties_schema.dump(result['items']),
                'pagination': result['pagination'],
                'search_criteria': search_params
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Property search failed', 500)


@properties_bp.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """
    Get a specific property by ID (public endpoint).
    """
    try:
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                'Property not found',
                404
            )
        
        # Check if admin is requesting or if property is verified
        is_admin = False
        try:
            from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            if current_user_id:
                current_user = User.query.get(current_user_id)
                is_admin = current_user and current_user.is_admin
        except:
            pass
        
        # If not admin and property not verified, deny access
        if not is_admin and not property.is_verified:
            return handle_error(
                Exception('Property not found'),
                'Property not found',
                404
            )
        
        return success_response(
            message='Property retrieved successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to get property', 500)


@properties_bp.route('', methods=['POST'])
@jwt_required()
@validate_json(property_create_schema)
def create_property(validated_data):
    """
    Create a new property (admin only).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return handle_error(
                Exception('Unauthorized'),
                'Only admins can create properties',
                403
            )
        
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
            status=validated_data.get('status', 'available'),
            features=json.dumps(validated_data.get('features', [])),
            images=json.dumps(validated_data.get('images', [])),
            admin_id=current_user.id,
            is_verified=True  # Auto-verify admin-created properties
        )
        
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
@jwt_required()
@validate_json(property_update_schema)
def update_property(property_id, validated_data):
    """
    Update a property (admin only).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return handle_error(
                Exception('Unauthorized'),
                'Only admins can update properties',
                403
            )
        
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                'Property not found',
                404
            )
        
        # Update property fields
        for field, value in validated_data.items():
            if field in ['features', 'images'] and value is not None:
                setattr(property, field, json.dumps(value))
            elif value is not None:
                setattr(property, field, value)
        
        # Mark as unverified if content changed (except for admin updating verification)
        if 'is_verified' not in validated_data:
            property.is_verified = False
        
        db.session.commit()
        
        return success_response(
            message='Property updated successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to update property', 500)


@properties_bp.route('/<int:property_id>', methods=['DELETE'])
@jwt_required()
def delete_property(property_id):
    """
    Delete a property (admin only). This removes it from public view immediately.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return handle_error(
                Exception('Unauthorized'),
                'Only admins can delete properties',
                403
            )
        
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                'Property not found',
                404
            )
        
        # Delete associated images from filesystem if any
        if property.images:
            try:
                images = json.loads(property.images)
                for image_url in images:
                    # Clean up image files (implement based on your storage)
                    pass
            except:
                pass
        
        db.session.delete(property)
        db.session.commit()
        
        return success_response(
            message='Property deleted successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete property', 500)


@properties_bp.route('/<int:property_id>/verify', methods=['PUT'])
@jwt_required()
def verify_property(property_id):
    """
    Verify/unverify a property for public display (admin only).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return handle_error(
                Exception('Unauthorized'),
                'Only admins can verify properties',
                403
            )
        
        data = request.get_json()
        is_verified = data.get('is_verified', False)
        verification_notes = data.get('verification_notes', '')
        
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                'Property not found',
                404
            )
        
        property.is_verified = is_verified
        property.verification_notes = verification_notes
        
        db.session.commit()
        
        return success_response(
            message=f'Property {"verified" if is_verified else "unverified"} successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to verify property', 500)


@properties_bp.route('/<int:property_id>/images', methods=['POST'])
@jwt_required()
def add_property_images(property_id):
    """
    Add images to a property (admin only).
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return handle_error(
                Exception('Unauthorized'),
                'Only admins can add property images',
                403
            )
        
        property = Property.query.get(property_id)
        
        if not property:
            return handle_error(
                Exception('Property not found'),
                'Property not found',
                404
            )
        
        data = request.get_json()
        new_image_urls = data.get('image_urls', [])
        
        # Get existing images
        try:
            existing_images = json.loads(property.images) if property.images else []
        except:
            existing_images = []
        
        # Add new images
        all_images = existing_images + new_image_urls
        property.images = json.dumps(all_images)
        
        # Mark as unverified when images change
        property.is_verified = False
        
        db.session.commit()
        
        return success_response(
            message='Images added to property successfully',
            data=property_schema.dump(property)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to add property images', 500)