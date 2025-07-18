#!/usr/bin/env python3
"""
Clean admin setup script.
Ensures only evian12k is the main admin and removes any other admin users.
"""

from app import create_app, db
from app.models import User
import json

def clean_admin_setup():
    """Clean up admin setup - only evian12k should be the main admin."""
    app = create_app()
    
    with app.app_context():
        # Get all users
        all_users = User.query.all()
        print(f"Found {len(all_users)} users:")
        for user in all_users:
            print(f"  - {user.username} (Main Admin: {user.is_main_admin})")
        
        # Delete all users except evian12k
        users_to_delete = User.query.filter(User.username != 'evian12k').all()
        
        if users_to_delete:
            print(f"\nDeleting {len(users_to_delete)} non-main admin users:")
            for user in users_to_delete:
                print(f"  - Deleting: {user.username}")
                db.session.delete(user)
        
        # Ensure evian12k exists and is the main admin
        main_admin = User.query.filter_by(username='evian12k').first()
        
        if not main_admin:
            print("\nCreating main admin user: evian12k")
            main_admin = User(
                username='evian12k',
                email='evian12k@rhokawi.com',
                password='rhokawi25@12ktbl',
                first_name='Main',
                last_name='Admin',
                is_main_admin=True
            )
            db.session.add(main_admin)
        else:
            print("\nEnsuring evian12k is the main admin")
            main_admin.is_main_admin = True
            main_admin.is_active = True
            # Update password to ensure it's correct
            main_admin.set_password('rhokawi25@12ktbl')
        
        # Commit changes
        db.session.commit()
        
        # Verify final state
        final_users = User.query.all()
        print(f"\nFinal admin setup:")
        print(f"Total users: {len(final_users)}")
        for user in final_users:
            print(f"  - {user.username} (Main Admin: {user.is_main_admin})")
        
        print(f"\n✅ Admin setup cleaned successfully!")
        print(f"Main Admin credentials: evian12k / rhokawi25@12ktbl")
        print(f"Only the main admin can add other admins and change their own password.")

if __name__ == '__main__':
    clean_admin_setup()