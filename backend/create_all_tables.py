#!/usr/bin/env python3
"""
Create all database tables including contact_messages with user_id field.
"""

import os
import sys
from flask import Flask
from app import create_app, db
from app.models import User, Property, ContactMessage

def create_all_tables():
    """Create all database tables."""
    
    try:
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            # Create all tables
            print("Creating all database tables...")
            db.create_all()
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {tables}")
            
            # Verify contact_messages has user_id column
            if 'contact_messages' in tables:
                columns = [col['name'] for col in inspector.get_columns('contact_messages')]
                print(f"contact_messages columns: {columns}")
                
                if 'user_id' in columns:
                    print("✅ contact_messages table has user_id column!")
                else:
                    print("❌ contact_messages table missing user_id column!")
                    return False
            
            print("✅ All tables created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Creating all database tables...")
    success = create_all_tables()
    
    if success:
        print("🎉 Database setup completed successfully!")
    else:
        print("💥 Database setup failed!")
        sys.exit(1)