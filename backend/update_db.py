#!/usr/bin/env python3
"""
Database update script to add phone field to contact_messages table.
"""

from app import create_app, db
from sqlalchemy import text

def update_database():
    """Update database schema to add phone field to contact_messages."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if phone column already exists
            result = db.session.execute(text("""
                SELECT COUNT(*) 
                FROM pragma_table_info('contact_messages') 
                WHERE name = 'phone'
            """)).scalar()
            
            if result == 0:
                print("Adding phone column to contact_messages table...")
                db.session.execute(text("""
                    ALTER TABLE contact_messages 
                    ADD COLUMN phone VARCHAR(20)
                """))
                db.session.commit()
                print("✅ Phone column added successfully!")
            else:
                print("✅ Phone column already exists.")
                
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    update_database()