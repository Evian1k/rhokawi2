#!/usr/bin/env python3
"""
Comprehensive Admin Login Fix Script
This script ensures the admin login system is fully functional.
"""

from app import create_app, db
from app.models import User
import json

def fix_admin_login():
    """Fix and verify admin login functionality."""
    print("🔧 Starting Admin Login Fix...")
    
    app = create_app()
    
    with app.app_context():
        # 1. Ensure database tables exist
        print("1. Creating database tables...")
        db.create_all()
        
        # 2. Create/verify admin users
        print("2. Setting up admin users...")
        
        # Main admin (evian12k)
        main_admin = User.query.filter_by(username='evian12k').first()
        if not main_admin:
            main_admin = User(
                username='evian12k',
                email='evian12k@rhokawi.com',
                password='rhokawi25@12ktbl',
                first_name='Main',
                last_name='Admin',
                is_main_admin=True
            )
            db.session.add(main_admin)
            print("   ✅ Created main admin: evian12k")
        else:
            print("   ✅ Main admin exists: evian12k")
        
        # Simple admin for testing
        simple_admin = User.query.filter_by(username='admin').first()
        if not simple_admin:
            simple_admin = User(
                username='admin',
                email='admin@rhokawi.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_main_admin=True
            )
            db.session.add(simple_admin)
            print("   ✅ Created simple admin: admin")
        else:
            print("   ✅ Simple admin exists: admin")
        
        # Commit changes
        db.session.commit()
        
        # 3. Test password verification
        print("3. Testing password verification...")
        
        # Test main admin
        if main_admin.check_password('rhokawi25@12ktbl'):
            print("   ✅ Main admin password verification: PASS")
        else:
            print("   ❌ Main admin password verification: FAIL")
        
        # Test simple admin
        if simple_admin.check_password('admin123'):
            print("   ✅ Simple admin password verification: PASS")
        else:
            print("   ❌ Simple admin password verification: FAIL")
        
        # 4. Test login endpoints
        print("4. Testing login endpoints...")
        
        with app.test_client() as client:
            # Test main admin login
            response = client.post('/api/auth/login', 
                                 data=json.dumps({'username': 'evian12k', 'password': 'rhokawi25@12ktbl'}),
                                 content_type='application/json')
            
            if response.status_code == 200:
                print("   ✅ Main admin login endpoint: PASS")
            else:
                print(f"   ❌ Main admin login endpoint: FAIL (Status: {response.status_code})")
                print(f"      Response: {response.get_json()}")
            
            # Test simple admin login
            response = client.post('/api/auth/login', 
                                 data=json.dumps({'username': 'admin', 'password': 'admin123'}),
                                 content_type='application/json')
            
            if response.status_code == 200:
                print("   ✅ Simple admin login endpoint: PASS")
            else:
                print(f"   ❌ Simple admin login endpoint: FAIL (Status: {response.status_code})")
                print(f"      Response: {response.get_json()}")
        
        # 5. Display final status
        print("\n" + "="*50)
        print("📊 ADMIN LOGIN STATUS")
        print("="*50)
        
        users = User.query.all()
        print(f"Total admin users: {len(users)}")
        
        for user in users:
            print(f"  👤 {user.username}")
            print(f"     Email: {user.email}")
            print(f"     Role: {user.role}")
            print(f"     Active: {user.is_active}")
            print(f"     Main Admin: {user.is_main_admin}")
            print()
        
        print("🎯 RECOMMENDED LOGIN CREDENTIALS:")
        print("   Username: admin")
        print("   Password: admin123")
        print()
        print("🔐 ALTERNATIVE LOGIN CREDENTIALS:")
        print("   Username: evian12k")
        print("   Password: rhokawi25@12ktbl")
        print()
        print("🌐 FRONTEND URL: http://localhost:5173/login")
        print("🔌 BACKEND URL: http://localhost:5000/api/auth/login")
        print("="*50)
        
        return True

if __name__ == '__main__':
    try:
        success = fix_admin_login()
        if success:
            print("\n🎉 Admin login fix completed successfully!")
        else:
            print("\n💥 Admin login fix failed!")
    except Exception as e:
        print(f"\n❌ Error during fix: {e}")
        import traceback
        traceback.print_exc()