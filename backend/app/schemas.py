"""
Marshmallow schemas for request/response validation and serialization.
"""

from marshmallow import Schema, fields, validate, post_load
from marshmallow.validate import Length, Email, OneOf


class UserSchema(Schema):
    """Schema for User model serialization/deserialization."""
    
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=Length(min=3, max=80))
    email = fields.Email(required=True, validate=Email())
    password = fields.String(required=True, load_only=True, validate=Length(min=6))
    first_name = fields.String(allow_none=True, validate=Length(max=50))
    last_name = fields.String(allow_none=True, validate=Length(max=50))
    role = fields.String(validate=OneOf(['client', 'agent', 'admin']), load_default='client')
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    """Schema for user login validation."""
    
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PropertySchema(Schema):
    """Schema for Property model serialization/deserialization."""
    
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=Length(min=1, max=200))
    description = fields.String(allow_none=True)
    property_type = fields.String(required=True, validate=OneOf(['house', 'apartment', 'condo', 'townhouse', 'land', 'commercial']))
    location = fields.String(required=True, validate=Length(min=1, max=200))
    address = fields.String(allow_none=True, validate=Length(max=300))
    price = fields.Decimal(required=True, places=2)
    bedrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    bathrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    square_feet = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    lot_size = fields.String(allow_none=True, validate=Length(max=50))
    year_built = fields.Integer(allow_none=True, validate=validate.Range(min=1800, max=2030))
    status = fields.String(validate=OneOf(['available', 'sold', 'pending']), load_default='available')
    features = fields.List(fields.String(), load_default=[])
    images = fields.List(fields.String(), load_default=[])
    agent_id = fields.Integer(allow_none=True)
    agent = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PropertyCreateSchema(Schema):
    """Schema for creating new properties."""
    
    title = fields.String(required=True, validate=Length(min=1, max=200))
    description = fields.String(allow_none=True)
    property_type = fields.String(required=True, validate=OneOf(['house', 'apartment', 'condo', 'townhouse', 'land', 'commercial']))
    location = fields.String(required=True, validate=Length(min=1, max=200))
    address = fields.String(allow_none=True, validate=Length(max=300))
    price = fields.Decimal(required=True, places=2)
    bedrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    bathrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    square_feet = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    lot_size = fields.String(allow_none=True, validate=Length(max=50))
    year_built = fields.Integer(allow_none=True, validate=validate.Range(min=1800, max=2030))
    features = fields.List(fields.String(), load_default=[])


class PropertyUpdateSchema(Schema):
    """Schema for updating existing properties."""
    
    title = fields.String(validate=Length(min=1, max=200))
    description = fields.String(allow_none=True)
    property_type = fields.String(validate=OneOf(['house', 'apartment', 'condo', 'townhouse', 'land', 'commercial']))
    location = fields.String(validate=Length(min=1, max=200))
    address = fields.String(allow_none=True, validate=Length(max=300))
    price = fields.Decimal(places=2)
    bedrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    bathrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    square_feet = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    lot_size = fields.String(allow_none=True, validate=Length(max=50))
    year_built = fields.Integer(allow_none=True, validate=validate.Range(min=1800, max=2030))
    status = fields.String(validate=OneOf(['available', 'sold', 'pending']))
    features = fields.List(fields.String())


class PropertySearchSchema(Schema):
    """Schema for property search parameters."""
    
    location = fields.String(allow_none=True)
    property_type = fields.String(allow_none=True, validate=OneOf(['house', 'apartment', 'condo', 'townhouse', 'land', 'commercial']))
    min_price = fields.Decimal(allow_none=True, places=2, validate=validate.Range(min=0))
    max_price = fields.Decimal(allow_none=True, places=2, validate=validate.Range(min=0))
    bedrooms = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    status = fields.String(allow_none=True, validate=OneOf(['available', 'sold', 'pending']))
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=20, validate=validate.Range(min=1, max=100))


class ContactMessageSchema(Schema):
    """Schema for ContactMessage model serialization/deserialization."""
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=Length(min=1, max=100))
    email = fields.Email(required=True, validate=Email())
    phone = fields.String(allow_none=True, validate=Length(max=20))
    subject = fields.String(allow_none=True, validate=Length(max=200))
    message = fields.String(required=True, validate=Length(min=1))
    property_id = fields.Integer(allow_none=True)
    property_title = fields.String(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class FileUploadSchema(Schema):
    """Schema for file upload validation."""
    
    file = fields.Raw(required=True)


class ErrorSchema(Schema):
    """Schema for error responses."""
    
    error = fields.String(required=True)
    message = fields.String(required=True)
    status_code = fields.Integer(required=True)


class SuccessSchema(Schema):
    """Schema for success responses."""
    
    message = fields.String(required=True)
    data = fields.Raw()


class PaginationSchema(Schema):
    """Schema for pagination metadata."""
    
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)
    total = fields.Integer(required=True)
    pages = fields.Integer(required=True)
    has_prev = fields.Boolean(required=True)
    has_next = fields.Boolean(required=True)


class PaginatedResponseSchema(Schema):
    """Schema for paginated responses."""
    
    data = fields.List(fields.Raw(), required=True)
    pagination = fields.Nested(PaginationSchema, required=True)


# Schema instances for reuse
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_login_schema = UserLoginSchema()
property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
property_create_schema = PropertyCreateSchema()
property_update_schema = PropertyUpdateSchema()
property_search_schema = PropertySearchSchema()
contact_message_schema = ContactMessageSchema()
contact_messages_schema = ContactMessageSchema(many=True)
file_upload_schema = FileUploadSchema()
error_schema = ErrorSchema()
success_schema = SuccessSchema()
paginated_response_schema = PaginatedResponseSchema()