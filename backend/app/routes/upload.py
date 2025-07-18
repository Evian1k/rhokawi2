"""
File upload routes for handling image uploads.
"""

import os
from flask import Blueprint, request, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from app.utils import success_response, handle_error, save_uploaded_file, allowed_file

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('', methods=['POST'])
@jwt_required()
def upload_file():
    """
    Upload a file (image).
    
    Expected: multipart/form-data with 'file' field
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return handle_error(
                Exception('No file provided'),
                'No file field in request',
                400
            )
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return handle_error(
                Exception('No file selected'),
                'No file selected for upload',
                400
            )
        
        # Check file type
        if not allowed_file(file.filename):
            return handle_error(
                Exception('Invalid file type'),
                'File type not allowed. Only PNG, JPG, JPEG, GIF, and WEBP files are allowed.',
                400
            )
        
        # Check file size (16MB max)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > 16 * 1024 * 1024:  # 16MB
            return handle_error(
                Exception('File too large'),
                'File size exceeds 16MB limit',
                400
            )
        
        # Save file
        file_url = save_uploaded_file(file)
        
        if not file_url:
            return handle_error(
                Exception('Upload failed'),
                'Failed to save uploaded file',
                500
            )
        
        return success_response(
            message='File uploaded successfully',
            data={
                'file_url': file_url,
                'filename': file.filename,
                'size': file_size
            },
            status_code=201
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to upload file', 500)


@upload_bp.route('/multiple', methods=['POST'])
@jwt_required()
def upload_multiple_files():
    """
    Upload multiple files (images).
    
    Expected: multipart/form-data with multiple 'files' fields
    """
    try:
        # Check if files are in request
        if 'files' not in request.files:
            return handle_error(
                Exception('No files provided'),
                'No files field in request',
                400
            )
        
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return handle_error(
                Exception('No files selected'),
                'No files selected for upload',
                400
            )
        
        # Limit number of files
        if len(files) > 10:
            return handle_error(
                Exception('Too many files'),
                'Maximum 10 files allowed per upload',
                400
            )
        
        uploaded_files = []
        total_size = 0
        
        for file in files:
            # Skip empty files
            if file.filename == '':
                continue
            
            # Check file type
            if not allowed_file(file.filename):
                return handle_error(
                    Exception('Invalid file type'),
                    f'File {file.filename} type not allowed. Only PNG, JPG, JPEG, GIF, and WEBP files are allowed.',
                    400
                )
            
            # Check individual file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset file pointer
            
            if file_size > 16 * 1024 * 1024:  # 16MB per file
                return handle_error(
                    Exception('File too large'),
                    f'File {file.filename} exceeds 16MB limit',
                    400
                )
            
            total_size += file_size
            
            # Check total upload size (100MB max)
            if total_size > 100 * 1024 * 1024:
                return handle_error(
                    Exception('Total size too large'),
                    'Total upload size exceeds 100MB limit',
                    400
                )
            
            # Save file
            file_url = save_uploaded_file(file)
            
            if file_url:
                uploaded_files.append({
                    'file_url': file_url,
                    'filename': file.filename,
                    'size': file_size
                })
            else:
                return handle_error(
                    Exception('Upload failed'),
                    f'Failed to save file {file.filename}',
                    500
                )
        
        if not uploaded_files:
            return handle_error(
                Exception('No valid files'),
                'No valid files were uploaded',
                400
            )
        
        return success_response(
            message=f'{len(uploaded_files)} files uploaded successfully',
            data={
                'files': uploaded_files,
                'total_files': len(uploaded_files),
                'total_size': total_size
            },
            status_code=201
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to upload files', 500)


@upload_bp.route('/<path:filename>')
def serve_file(filename):
    """
    Serve uploaded files.
    """
    try:
        upload_path = os.path.join(current_app.root_path, '..', 'uploads')
        return send_from_directory(upload_path, filename)
    except Exception as e:
        return handle_error(e, 'File not found', 404)