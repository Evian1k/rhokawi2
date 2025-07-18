"""
Post management routes for CRUD operations.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Post, User
from app.schemas import post_schema, posts_schema, post_create_schema, post_update_schema
from app.utils import validate_json, success_response, handle_error, paginate_query

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    """
    Get all posts (with pagination).
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - author_id: Filter by author ID
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        author_id = request.args.get('author_id', type=int)
        
        # Build query
        query = Post.query
        
        if author_id:
            query = query.filter_by(author_id=author_id)
        
        query = query.order_by(Post.created_at.desc())
        
        # Execute paginated query
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Posts retrieved successfully',
            data={
                'posts': posts_schema.dump(result['items']),
                'pagination': result['pagination']
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve posts', 500)


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get a specific post by ID.
    """
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return handle_error(
                Exception('Post not found'),
                f'Post with ID {post_id} not found',
                404
            )
        
        return success_response(
            message='Post retrieved successfully',
            data=post_schema.dump(post)
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve post', 500)


@posts_bp.route('', methods=['POST'])
@jwt_required()
@validate_json(post_create_schema)
def create_post(validated_data):
    """
    Create a new post.
    
    Expected JSON:
    {
        "title": "string",
        "content": "string"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Create new post
        post = Post(
            title=validated_data['title'],
            content=validated_data['content'],
            author_id=current_user_id
        )
        
        # Save post to database
        db.session.add(post)
        db.session.commit()
        
        return success_response(
            message='Post created successfully',
            data=post_schema.dump(post),
            status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to create post', 500)


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
@validate_json(post_update_schema)
def update_post(post_id, validated_data):
    """
    Update an existing post.
    Users can only update their own posts unless they are admin.
    
    Expected JSON:
    {
        "title": "string" (optional),
        "content": "string" (optional)
    }
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get the post
        post = Post.query.get(post_id)
        
        if not post:
            return handle_error(
                Exception('Post not found'),
                f'Post with ID {post_id} not found',
                404
            )
        
        # Check permissions
        if post.author_id != current_user_id and not current_user.is_admin:
            return handle_error(
                Exception('Forbidden'),
                'You can only update your own posts',
                403
            )
        
        # Update post fields
        if 'title' in validated_data:
            post.title = validated_data['title']
        
        if 'content' in validated_data:
            post.content = validated_data['content']
        
        db.session.commit()
        
        return success_response(
            message='Post updated successfully',
            data=post_schema.dump(post)
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to update post', 500)


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """
    Delete a post.
    Users can only delete their own posts unless they are admin.
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get the post
        post = Post.query.get(post_id)
        
        if not post:
            return handle_error(
                Exception('Post not found'),
                f'Post with ID {post_id} not found',
                404
            )
        
        # Check permissions
        if post.author_id != current_user_id and not current_user.is_admin:
            return handle_error(
                Exception('Forbidden'),
                'You can only delete your own posts',
                403
            )
        
        db.session.delete(post)
        db.session.commit()
        
        return success_response(
            message='Post deleted successfully',
            status_code=204
        )
        
    except Exception as e:
        db.session.rollback()
        return handle_error(e, 'Failed to delete post', 500)


@posts_bp.route('/search', methods=['GET'])
def search_posts():
    """
    Search posts by title or content.
    
    Query Parameters:
    - q: Search query
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    """
    try:
        search_query = request.args.get('q', '').strip()
        
        if not search_query:
            return handle_error(
                Exception('Bad Request'),
                'Search query parameter "q" is required',
                400
            )
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Search posts
        query = Post.query.filter(
            (Post.title.ilike(f'%{search_query}%')) |
            (Post.content.ilike(f'%{search_query}%'))
        ).order_by(Post.created_at.desc())
        
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message='Posts found successfully',
            data={
                'posts': posts_schema.dump(result['items']),
                'pagination': result['pagination'],
                'query': search_query
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to search posts', 500)


@posts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    """
    Get all posts by a specific user.
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    """
    try:
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return handle_error(
                Exception('User not found'),
                f'User with ID {user_id} not found',
                404
            )
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query user's posts
        query = Post.query.filter_by(author_id=user_id).order_by(Post.created_at.desc())
        result = paginate_query(query, page, per_page)
        
        return success_response(
            message=f'Posts by {user.username} retrieved successfully',
            data={
                'posts': posts_schema.dump(result['items']),
                'pagination': result['pagination'],
                'author': {
                    'id': user.id,
                    'username': user.username
                }
            }
        )
        
    except Exception as e:
        return handle_error(e, 'Failed to retrieve user posts', 500)