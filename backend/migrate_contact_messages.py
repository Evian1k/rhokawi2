#!/usr/bin/env python3
"""
Migration script to add user_id field to contact_messages table.
This script safely adds the missing user_id column to existing contact_messages.
"""

import sqlite3
import os
from pathlib import Path

def migrate_contact_messages():
    """Add user_id column to contact_messages table if it doesn't exist."""
    
    # Get the database path
    db_path = Path(__file__).parent / 'instance' / 'rhokawi.db'
    
    # Create instance directory if it doesn't exist
    db_path.parent.mkdir(exist_ok=True)
    
    try:
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if user_id column exists
        cursor.execute("PRAGMA table_info(contact_messages)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("Adding user_id column to contact_messages table...")
            cursor.execute("""
                ALTER TABLE contact_messages 
                ADD COLUMN user_id INTEGER REFERENCES users(id)
            """)
            print("✅ user_id column added successfully!")
        else:
            print("✅ user_id column already exists in contact_messages table")
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting contact_messages table migration...")
    success = migrate_contact_messages()
    
    if success:
        print("🎉 Migration completed successfully!")
    else:
        print("💥 Migration failed!")
        exit(1)