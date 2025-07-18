#!/usr/bin/env python3
"""
Database initialization script.
Creates tables and adds the main admin user.
"""

from app import create_app, db
from app.models import User, Property, ContactMessage
import json

def init_database():
    """Initialize database with tables and main admin user."""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate to ensure clean schema
        db.drop_all()
        db.create_all()
        
        # Create main admin user (evian12k)
        main_admin = User(
            username='evian12k',
            email='evian12k@rhokawi.com',
            password='rhokawi25@12ktbl',
            first_name='Main',
            last_name='Admin',
            is_main_admin=True
        )
        db.session.add(main_admin)
        
        # Commit the main admin
        db.session.commit()
        
        print("Database initialized successfully!")
        print(f"Main Admin user: evian12k / rhokawi25@12ktbl")
        print("This is the only admin user that can add other admins.")

if __name__ == '__main__':
    init_database()