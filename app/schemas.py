"""
Marshmallow schemas for request/response validation and serialization.
"""

from marshmallow import Schema, fields, validate, post_load
from marshmallow.validate import Length, Email


class UserSchema(Schema):
    """Schema for User model serialization/deserialization."""
    
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=Length(min=3, max=80))
    email = fields.Email(required=True, validate=Email())
    password = fields.String(required=True, load_only=True, validate=Length(min=6))
    first_name = fields.String(allow_none=True, validate=Length(max=50))
    last_name = fields.String(allow_none=True, validate=Length(max=50))
    is_active = fields.Boolean(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    """Schema for user login validation."""
    
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class PostSchema(Schema):
    """Schema for Post model serialization/deserialization."""
    
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=Length(min=1, max=200))
    content = fields.String(required=True, validate=Length(min=1))
    author_id = fields.Integer(required=True)
    author = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PostCreateSchema(Schema):
    """Schema for creating new posts."""
    
    title = fields.String(required=True, validate=Length(min=1, max=200))
    content = fields.String(required=True, validate=Length(min=1))


class PostUpdateSchema(Schema):
    """Schema for updating existing posts."""
    
    title = fields.String(validate=Length(min=1, max=200))
    content = fields.String(validate=Length(min=1))


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
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
post_create_schema = PostCreateSchema()
post_update_schema = PostUpdateSchema()
error_schema = ErrorSchema()
success_schema = SuccessSchema()
paginated_response_schema = PaginatedResponseSchema()