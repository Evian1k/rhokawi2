#!/usr/bin/env python3
"""
Test script to check admin login functionality.
"""

from app import create_app, db
from app.models import User
import json

def test_admin_login():
    """Test admin login functionality."""
    app = create_app()
    
    with app.app_context():
        # Check if admin user exists
        admin_user = User.query.filter_by(username='evian12k').first()
        
        if not admin_user:
            print("❌ Admin user 'evian12k' not found in database")
            return False
            
        print(f"✅ Admin user found: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Role: {admin_user.role}")
        print(f"   Is Main Admin: {admin_user.is_main_admin}")
        print(f"   Is Active: {admin_user.is_active}")
        
        # Test password verification
        test_password = "rhokawi25@12ktbl"
        password_valid = admin_user.check_password(test_password)
        
        if password_valid:
            print(f"✅ Password verification successful")
        else:
            print(f"❌ Password verification failed")
            return False
            
        # Test with client
        with app.test_client() as client:
            # Test login endpoint
            login_data = {
                "username": "evian12k",
                "password": "rhokawi25@12ktbl"
            }
            
            response = client.post('/api/auth/login', 
                                 data=json.dumps(login_data),
                                 content_type='application/json')
            
            print(f"Login response status: {response.status_code}")
            print(f"Login response data: {response.get_json()}")
            
            if response.status_code == 200:
                print("✅ Admin login test successful!")
                return True
            else:
                print("❌ Admin login test failed!")
                return False

if __name__ == '__main__':
    success = test_admin_login()
    if success:
        print("\n🎉 All tests passed! Admin login is working correctly.")
    else:
        print("\n💥 Tests failed! There's an issue with admin login.")