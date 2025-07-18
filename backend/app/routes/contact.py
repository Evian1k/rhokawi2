"""
Contact message routes for user inquiries and communication.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import ContactMessage, Property, User
from app.schemas import contact_message_schema, contact_messages_schema
from app.utils import validate_json, success_response, handle_error, paginate_query, admin_required

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('', methods=['POST'])
@validate_json(contact_message_schema)
def send_message(validated_data):
    """
    Send a contact message.
    Can be sent by authenticated users or anonymous visitors.
    
    Expected JSON:
    {
        "name": "string",
        "email": "string",
        "message": "string",
        "property_id": integer (optional)
    }
    """
    try:
        # Get current user if authenticated (optional)
        current_user_id = None
        try:
            # Check if there's a valid JWT token
            if get_jwt():
                current_user_id = get_jwt_identity()
        except:
            # No token or invalid token - that's fine for contact messages
            pass
        
        # Validate property if specified
        property_id = validated_data.get('property_id')
        if property_id:
            property = Property.query.get(property_id)
            if not property:
                return handle_error(
                    Exception('Property not found'),
                    f'Property with ID {property_id} not found',
                    404
                )
        
        # Create contact message
        message = ContactMessage(
            name=validated_data['name'],
            email=validated_data['email'],
            message=validated_data['message'],
            property_id=property_id,
            user_id=current_user_id
        )
        
        # Save message to database
        db.session.add(message)
        db.session.commit()
        
        return success_response(
            message='Contact message sent successfully',
            data=contact_message_schema.dump(message),
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to send contact message', 500)


@contact_bp.route('', methods=['GET'])
@admin_required
def get_messages():
    """
    Get all contact messages (admin only).
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - status: Filter by status (unread, read, replied)
    - property_id: Filter by property ID
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        property_id = request.args.get('property_id', type=int)
        
        # Build query
        query = ContactMessage.query
        
        if status:
            query = query.filter_by(status=status)
        
        if property_id:
            query = query.filter_by(property_id=property_id)
        
        query = query.order_by(ContactMessage.created_at.desc())
        
        # Execute paginated query
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Contact messages retrieved successfully',
            data={
                'messages': contact_messages_schema.dump(result['items']),
                'pagination': result['pagination']
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve contact messages', 500)


@contact_bp.route('/<int:message_id>', methods=['GET'])
@admin_required
def get_message(message_id):
    """
    Get a specific contact message (admin only).
    """
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return handle_error(
                Exception('Message not found'),
                f'Contact message with ID {message_id} not found',
                404
            )
        
        return success_response(
            message='Contact message retrieved successfully',
            data=contact_message_schema.dump(message)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve contact message', 500)


@contact_bp.route('/<int:message_id>/status', methods=['PUT'])
@admin_required
def update_message_status(message_id):
    """
    Update contact message status (admin only).
    
    Expected JSON:
    {
        "status": "unread|read|replied"
    }
    """
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return handle_error(
                Exception('Message not found'),
                f'Contact message with ID {message_id} not found',
                404
            )
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data or 'status' not in json_data:
            return handle_error(
                Exception('Bad Request'),
                'status is required',
                400
            )
        
        status = json_data['status']
        if status not in ['unread', 'read', 'replied']:
            return handle_error(
                Exception('Invalid status'),
                'Status must be unread, read, or replied',
                400
            )
        
        # Update status
        message.status = status
        db.session.commit()
        
        return success_response(
            message='Message status updated successfully',
            data=contact_message_schema.dump(message)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to update message status', 500)


@contact_bp.route('/<int:message_id>', methods=['DELETE'])
@admin_required
def delete_message(message_id):
    """
    Delete a contact message (admin only).
    """
    try:
        message = ContactMessage.query.get(message_id)
        
        if not message:
            return handle_error(
                Exception('Message not found'),
                f'Contact message with ID {message_id} not found',
                404
            )
        
        db.session.delete(message)
        db.session.commit()
        
        return success_response(
            message='Contact message deleted successfully',
            status_code=204
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete contact message', 500)


@contact_bp.route('/my-messages', methods=['GET'])
@jwt_required()
def get_user_messages():
    """
    Get contact messages from the current authenticated user.
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query user's messages
        query = ContactMessage.query.filter_by(user_id=current_user_id).order_by(ContactMessage.created_at.desc())
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Your contact messages retrieved successfully',
            data={
                'messages': contact_messages_schema.dump(result['items']),
                'pagination': result['pagination']
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve your contact messages', 500)