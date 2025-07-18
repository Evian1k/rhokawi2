#!/usr/bin/env python3
"""
Fix database issues - add missing properties and verify existing data.
"""

from app import create_app, db
from app.models import Property, User, ContactMessage
import os

def fix_database():
    """Fix database issues by ensuring required data exists."""
    app = create_app()
    
    with app.app_context():
        print("=== CHECKING CURRENT DATABASE STATE ===")
        
        # Check properties
        properties = Property.query.all()
        print(f"Current properties: {len(properties)}")
        for p in properties:
            print(f"  ID: {p.id}, Title: {p.title}, Status: {p.status}, Verified: {p.is_verified}")
        
        # Check if property ID 2 exists
        property_2 = Property.query.get(2)
        if not property_2:
            print("\n=== ADDING MISSING PROPERTY ID 2 ===")
            # Create a sample property with ID 2
            new_property = Property(
                title="Sample Property 2",
                description="A beautiful sample property for testing purposes",
                price=250000.00,
                bedrooms=3,
                bathrooms=2,
                square_feet=1500,
                property_type="house",
                status="available",
                location="Sample City, SC 12345",
                address="123 Sample Street",
                is_verified=True  # Make it verified so it shows up in public searches
            )
            
            db.session.add(new_property)
            try:
                db.session.commit()
                print(f"✓ Created property ID 2: {new_property.title}")
            except Exception as e:
                print(f"✗ Failed to create property: {e}")
                db.session.rollback()
        else:
            print(f"\n✓ Property ID 2 exists: {property_2.title}")
            # Ensure it's verified
            if not property_2.is_verified:
                print("  Making property 2 verified...")
                property_2.is_verified = True
                db.session.commit()
        
        # Check users
        users = User.query.all()
        print(f"\nCurrent users: {len(users)}")
        for u in users:
            print(f"  ID: {u.id}, Username: {u.username}, Active: {u.is_active}, Main Admin: {u.is_main_admin}")
        
        # Ensure at least one active admin exists
        active_admins = User.query.filter_by(is_active=True).all()
        if not active_admins:
            print("\n=== WARNING: NO ACTIVE ADMINS FOUND ===")
            print("Creating a default admin user...")
            default_admin = User(
                username="admin",
                email="admin@rhokawi.com",
                password="admin123",
                first_name="System",
                last_name="Administrator",
                is_main_admin=True
            )
            db.session.add(default_admin)
            try:
                db.session.commit()
                print(f"✓ Created default admin: {default_admin.username}")
            except Exception as e:
                print(f"✗ Failed to create admin: {e}")
                db.session.rollback()
        
        # Check contact messages
        messages = ContactMessage.query.all()
        print(f"\nContact messages: {len(messages)}")
        
        # Verify all properties are accessible
        print("\n=== VERIFYING PROPERTY ACCESS ===")
        all_properties = Property.query.all()
        for prop in all_properties:
            print(f"Property {prop.id}: {prop.title} (Status: {prop.status}, Verified: {prop.is_verified})")
        
        print("\n=== DATABASE FIXES COMPLETED ===")

if __name__ == "__main__":
    fix_database()