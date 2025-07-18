"""
Database models for the Flask application.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Many-to-many relationship table for user favorites
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'), primary_key=True)
)


class User(db.Model):
    """User model for admin authentication and management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20), default='admin', nullable=False)  # Only admin role
    is_main_admin = db.Column(db.Boolean, default=False, nullable=False)  # Main admin flag
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, username, email, password, first_name=None, last_name=None, is_main_admin=False):
        """Initialize User instance."""
        self.username = username
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = 'admin'  # Always admin
        self.is_main_admin = is_main_admin
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches user's password."""
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        """Check if user is admin (always true now)."""
        return True
    
    def can_add_admins(self):
        """Check if user can add other admins (only main admin)."""
        return self.is_main_admin
    
    def can_manage_properties(self):
        """Check if user can create/update/delete properties (all admins can)."""
        return True
    
    def to_dict(self):
        """Convert user instance to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_main_admin': self.is_main_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of User."""
        main_status = " (Main)" if self.is_main_admin else ""
        return f'<User {self.username} (Admin{main_status})>'


class Property(db.Model):
    """Property model for real estate listings."""
    
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    property_type = db.Column(db.String(50), nullable=False)  # house, apartment, condo, etc.
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    square_feet = db.Column(db.Integer, nullable=True)
    lot_size = db.Column(db.String(50), nullable=True)
    year_built = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='available', nullable=False)  # available, sold, pending
    features = db.Column(db.Text, nullable=True)  # JSON string of features
    images = db.Column(db.Text, nullable=True)  # JSON string of image URLs
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Changed from agent_id
    is_verified = db.Column(db.Boolean, default=False, nullable=False)  # Property accuracy verification
    verification_notes = db.Column(db.Text, nullable=True)  # Notes about property verification
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    admin = db.relationship('User', backref=db.backref('properties', lazy=True))
    
    def to_dict(self):
        """Convert property instance to dictionary."""
        import json
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'property_type': self.property_type,
            'location': self.location,
            'address': self.address,
            'price': float(self.price) if self.price else None,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'square_feet': self.square_feet,
            'lot_size': self.lot_size,
            'year_built': self.year_built,
            'status': self.status,
            'features': json.loads(self.features) if self.features and self.features != 'null' else [],
            'images': json.loads(self.images) if self.images and self.images != 'null' else [],
            'admin_id': self.admin_id,
            'admin': {
                'id': self.admin.id,
                'username': self.admin.username,
                'name': f"{self.admin.first_name} {self.admin.last_name}".strip()
            } if self.admin else None,
            'is_verified': self.is_verified,
            'verification_notes': self.verification_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of Property."""
        return f'<Property {self.title}>'


class ContactMessage(db.Model):
    """Contact message model."""
    
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=True)
    status = db.Column(db.String(20), default='unread', nullable=False)  # unread, read, replied
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    property = db.relationship('Property', backref=db.backref('inquiries', lazy=True))
    
    def to_dict(self):
        """Convert contact message instance to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'property_id': self.property_id,
            'property_title': self.property.title if self.property else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """String representation of ContactMessage."""
        return f'<ContactMessage from {self.name}>'