from flask import Flask, request, jsonify, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')  # admin, agent, client
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    properties = db.relationship('Property', backref='owner', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='user', lazy=True)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    location = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # house, apartment, condo, etc.
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    square_feet = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    favorites = db.relationship('Favorite', backref='property', lazy=True, cascade='all, delete-orphan')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'property_id', name='unique_user_property'),)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Authentication helpers
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# Utility functions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def serialize_property(property_obj, include_favorites=False):
    result = {
        'id': property_obj.id,
        'title': property_obj.title,
        'description': property_obj.description,
        'image_url': property_obj.image_url,
        'location': property_obj.location,
        'type': property_obj.type,
        'price': property_obj.price,
        'bedrooms': property_obj.bedrooms,
        'bathrooms': property_obj.bathrooms,
        'square_feet': property_obj.square_feet,
        'created_at': property_obj.created_at.isoformat(),
        'updated_at': property_obj.updated_at.isoformat(),
        'owner': {
            'id': property_obj.owner.id,
            'username': property_obj.owner.username,
            'role': property_obj.owner.role
        }
    }
    
    if include_favorites:
        current_user = get_current_user()
        if current_user:
            favorite = Favorite.query.filter_by(
                user_id=current_user.id, 
                property_id=property_obj.id
            ).first()
            result['is_favorited'] = favorite is not None
        else:
            result['is_favorited'] = False
    
    return result

# Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    role = data.get('role', 'client')
    
    # Only admins can create admin/agent accounts
    current_user = get_current_user()
    if role in ['admin', 'agent'] and (not current_user or current_user.role != 'admin'):
        role = 'client'
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role=role
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user_info():
    user = get_current_user()
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

# Property Routes
@app.route('/api/properties', methods=['GET'])
def get_properties():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Search filters
    location = request.args.get('location', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    bedrooms = request.args.get('bedrooms', type=int)
    
    query = Property.query
    
    # Apply filters
    if location:
        query = query.filter(Property.location.ilike(f'%{location}%'))
    
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    
    if bedrooms is not None:
        query = query.filter(Property.bedrooms == bedrooms)
    
    # Order by creation date (newest first)
    query = query.order_by(Property.created_at.desc())
    
    # Paginate
    pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    properties = [serialize_property(prop, include_favorites=True) for prop in pagination.items]
    
    return jsonify({
        'properties': properties,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    property_obj = Property.query.get_or_404(property_id)
    return jsonify({'property': serialize_property(property_obj, include_favorites=True)}), 200

@app.route('/api/properties', methods=['POST'])
@role_required('admin', 'agent')
def create_property():
    data = request.get_json()
    
    required_fields = ['title', 'description', 'location', 'type', 'price', 'bedrooms', 'bathrooms', 'square_feet']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    current_user = get_current_user()
    
    property_obj = Property(
        title=data['title'],
        description=data['description'],
        image_url=data.get('image_url'),
        location=data['location'],
        type=data['type'],
        price=data['price'],
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        square_feet=data['square_feet'],
        owner_id=current_user.id
    )
    
    db.session.add(property_obj)
    db.session.commit()
    
    return jsonify({
        'message': 'Property created successfully',
        'property': serialize_property(property_obj)
    }), 201

@app.route('/api/properties/<int:property_id>', methods=['PUT'])
@role_required('admin', 'agent')
def update_property(property_id):
    property_obj = Property.query.get_or_404(property_id)
    current_user = get_current_user()
    
    # Only the owner or admin can update
    if current_user.role != 'admin' and property_obj.owner_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    updatable_fields = ['title', 'description', 'image_url', 'location', 'type', 'price', 'bedrooms', 'bathrooms', 'square_feet']
    for field in updatable_fields:
        if field in data:
            setattr(property_obj, field, data[field])
    
    property_obj.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Property updated successfully',
        'property': serialize_property(property_obj)
    }), 200

@app.route('/api/properties/<int:property_id>', methods=['DELETE'])
@role_required('admin', 'agent')
def delete_property(property_id):
    property_obj = Property.query.get_or_404(property_id)
    current_user = get_current_user()
    
    # Only the owner or admin can delete
    if current_user.role != 'admin' and property_obj.owner_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    db.session.delete(property_obj)
    db.session.commit()
    
    return jsonify({'message': 'Property deleted successfully'}), 200

# Image Upload Route
@app.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Return URL
        file_url = f'/uploads/{filename}'
        return jsonify({
            'message': 'File uploaded successfully',
            'url': file_url
        }), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

# Favorites Routes
@app.route('/api/favorites', methods=['GET'])
@login_required
def get_favorites():
    current_user = get_current_user()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = db.session.query(Property).join(Favorite).filter(
        Favorite.user_id == current_user.id
    ).order_by(Favorite.created_at.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    properties = [serialize_property(prop, include_favorites=True) for prop in pagination.items]
    
    return jsonify({
        'favorites': properties,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@app.route('/api/favorites/<int:property_id>', methods=['POST'])
@login_required
def add_favorite(property_id):
    current_user = get_current_user()
    property_obj = Property.query.get_or_404(property_id)
    
    # Check if already favorited
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        property_id=property_id
    ).first()
    
    if existing_favorite:
        return jsonify({'error': 'Property already in favorites'}), 400
    
    favorite = Favorite(user_id=current_user.id, property_id=property_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Property added to favorites'}), 201

@app.route('/api/favorites/<int:property_id>', methods=['DELETE'])
@login_required
def remove_favorite(property_id):
    current_user = get_current_user()
    
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        property_id=property_id
    ).first_or_404()
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Property removed from favorites'}), 200

# Contact Route
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    
    required_fields = ['name', 'email', 'message']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    current_user = get_current_user()
    
    contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        message=data['message'],
        property_id=data.get('property_id'),
        user_id=current_user.id if current_user else None
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({
        'message': 'Contact inquiry submitted successfully',
        'contact_id': contact.id
    }), 201

@app.route('/api/contacts', methods=['GET'])
@role_required('admin', 'agent')
def get_contacts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Contact.query.order_by(Contact.created_at.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    contacts = []
    for contact in pagination.items:
        contact_data = {
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'message': contact.message,
            'property_id': contact.property_id,
            'created_at': contact.created_at.isoformat()
        }
        
        if contact.property_id:
            property_obj = Property.query.get(contact.property_id)
            if property_obj:
                contact_data['property'] = {
                    'id': property_obj.id,
                    'title': property_obj.title,
                    'location': property_obj.location
                }
        
        contacts.append(contact_data)
    
    return jsonify({
        'contacts': contacts,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

# Static file serving for uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(
                username='admin',
                email='admin@realestate.com',
                password_hash=admin_password,
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: username=admin, password=admin123")

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)