"""
File upload routes for handling image uploads.
"""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.utils import success_response, handle_error

upload_bp = Blueprint('upload', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# Maximum file size (16MB)
MAX_FILE_SIZE = 16 * 1024 * 1024

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    """Create upload folder if it doesn't exist."""
    upload_folder = os.path.join(os.getcwd(), 'uploads', 'images')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder

@upload_bp.route('', methods=['POST'])
def upload_file():
    """
    Upload a single image file (admin only).
    
    Returns:
    {
        "data": {
            "url": "uploads/images/filename.jpg",
            "filename": "original_filename.jpg",
            "size": 12345
        }
    }
    """
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Check if user exists and is active
        if not current_user or not current_user.is_active:
            from app.schemas import error_schema
            return jsonify(error_schema.dump({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status_code': 401
            })), 401
        
        # Check if file is present
        if 'file' not in request.files:
            return handle_error(
                Exception('No file provided'),
                'No file provided in request',
                400
            )
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return handle_error(
                Exception('No file selected'),
                'No file selected',
                400
            )
        
        # Check file size
        if len(file.read()) > MAX_FILE_SIZE:
            return handle_error(
                Exception('File too large'),
                f'File size exceeds {MAX_FILE_SIZE / (1024*1024)}MB limit',
                400
            )
        
        # Reset file pointer
        file.seek(0)
        
        # Validate file type
        if not allowed_file(file.filename):
            return handle_error(
                Exception('Invalid file type'),
                'Only image files (PNG, JPG, JPEG, GIF, WebP) are allowed',
                400
            )
        
        # Create upload folder
        upload_folder = create_upload_folder()
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Save file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Create URL path (relative to static serving)
        file_url = f"uploads/images/{unique_filename}"
        
        return success_response(
            message='File uploaded successfully',
            data={
                'url': file_url,
                'filename': file.filename,
                'size': os.path.getsize(file_path)
            }
        )
        
    except Exception as e:
        # Check if it's a JWT validation error
        if "verify_jwt_in_request" in str(e) or "JWT" in str(e):
            from app.schemas import error_schema
            return jsonify(error_schema.dump({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token',
                'status_code': 401
            })), 401
        return handle_error(e, 'Failed to upload file', 500)


@upload_bp.route('/multiple', methods=['POST'])
def upload_multiple_files():
    """
    Upload multiple image files (admin only).
    
    Returns:
    {
        "data": {
            "files": [
                {
                    "url": "uploads/images/filename1.jpg",
                    "filename": "original1.jpg",
                    "size": 12345
                },
                ...
            ]
        }
    }
    """
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Check if user exists and is active
        if not current_user or not current_user.is_active:
            from app.schemas import error_schema
            return jsonify(error_schema.dump({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status_code': 401
            })), 401
        
        # Check if files are present
        if 'files' not in request.files:
            return handle_error(
                Exception('No files provided'),
                'No files provided in request',
                400
            )
        
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return handle_error(
                Exception('No files selected'),
                'No files selected',
                400
            )
        
        # Create upload folder
        upload_folder = create_upload_folder()
        
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                continue
            
            # Check file size
            file_content = file.read()
            if len(file_content) > MAX_FILE_SIZE:
                continue  # Skip files that are too large
            
            # Reset file pointer
            file.seek(0)
            
            # Validate file type
            if not allowed_file(file.filename):
                continue  # Skip invalid file types
            
            # Generate unique filename
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            
            # Save file
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # Add to results
            uploaded_files.append({
                'url': f"uploads/images/{unique_filename}",
                'filename': file.filename,
                'size': os.path.getsize(file_path)
            })
        
        if not uploaded_files:
            return handle_error(
                Exception('No valid files'),
                'No valid image files were uploaded',
                400
            )
        
        return success_response(
            message=f'{len(uploaded_files)} file(s) uploaded successfully',
            data={
                'files': uploaded_files
            }
        )
        
    except Exception as e:
        # Check if it's a JWT validation error
        if "verify_jwt_in_request" in str(e) or "JWT" in str(e):
            from app.schemas import error_schema
            return jsonify(error_schema.dump({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token',
                'status_code': 401
            })), 401
        return handle_error(e, 'Failed to upload files', 500)


@upload_bp.route('/delete', methods=['POST'])
def delete_file():
    """
    Delete an uploaded file (admin only).
    
    Expected JSON:
    {
        "url": "uploads/images/filename.jpg"
    }
    """
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_active:
            from app.schemas import error_schema
            return jsonify(error_schema.dump({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status_code': 401
            })), 401
        
        data = request.get_json()
        if not data or 'url' not in data:
            return handle_error(
                Exception('Missing URL'),
                'File URL is required',
                400
            )
        
        file_url = data['url']
        
        # Extract filename from URL
        if file_url.startswith('uploads/images/'):
            filename = file_url.replace('uploads/images/', '')
            file_path = os.path.join(os.getcwd(), 'uploads', 'images', filename)
            
            # Check if file exists and delete it
            if os.path.exists(file_path):
                os.remove(file_path)
                return success_response(
                    message='File deleted successfully'
                )
            else:
                return handle_error(
                    Exception('File not found'),
                    'File not found on server',
                    404
                )
        else:
            return handle_error(
                Exception('Invalid URL'),
                'Invalid file URL format',
                400
            )
        
    except Exception as e:
        # Check if it's a JWT validation error
        if "verify_jwt_in_request" in str(e) or "JWT" in str(e):
            from app.schemas import error_schema
            return jsonify(error_schema.dump({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token',
                'status_code': 401
            })), 401
        return handle_error(e, 'Failed to delete file', 500)