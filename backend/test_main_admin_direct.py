#!/usr/bin/env python3
"""
Direct test script for main admin system.
Tests the admin system without needing the server running.
"""

from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

def test_main_admin_system():
    """Test the main admin system directly."""
    print("🚀 Testing Main Admin System (Direct Database Test)")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # Test 1: Check database state
        print("\n🔍 Test 1: Database State")
        print("-" * 30)
        
        users = User.query.all()
        print(f"Total users in database: {len(users)}")
        
        if len(users) == 1:
            user = users[0]
            print(f"Single user: {user.username}")
            print(f"Is main admin: {user.is_main_admin}")
            print(f"Is active: {user.is_active}")
            print(f"Email: {user.email}")
            
            if user.username == 'evian12k' and user.is_main_admin:
                print("✅ Database state correct: Only evian12k exists as main admin")
                db_test = True
            else:
                print("❌ Database state incorrect")
                db_test = False
        else:
            print("❌ Database should have exactly 1 user")
            for user in users:
                print(f"  - {user.username} (Main Admin: {user.is_main_admin})")
            db_test = False
        
        # Test 2: Password verification
        print("\n🔐 Test 2: Password Verification")
        print("-" * 30)
        
        main_admin = User.query.filter_by(username='evian12k').first()
        if main_admin:
            correct_password = main_admin.check_password('rhokawi25@12ktbl')
            wrong_password = main_admin.check_password('wrong_password')
            
            if correct_password and not wrong_password:
                print("✅ Password verification working correctly")
                print(f"✅ Main admin can login with: evian12k / rhokawi25@12ktbl")
                password_test = True
            else:
                print("❌ Password verification failed")
                password_test = False
        else:
            print("❌ Main admin user not found")
            password_test = False
        
        # Test 3: Admin privileges
        print("\n👑 Test 3: Admin Privileges")
        print("-" * 30)
        
        if main_admin:
            can_add_admins = main_admin.can_add_admins()
            can_change_password = main_admin.can_change_password()
            can_manage_properties = main_admin.can_manage_properties()
            
            print(f"Can add admins: {can_add_admins}")
            print(f"Can change password: {can_change_password}")
            print(f"Can manage properties: {can_manage_properties}")
            
            if can_add_admins and can_change_password and can_manage_properties:
                print("✅ Main admin has all required privileges")
                privileges_test = True
            else:
                print("❌ Main admin missing some privileges")
                privileges_test = False
        else:
            privileges_test = False
        
        # Test 4: Create and test non-main admin
        print("\n🚫 Test 4: Non-Main Admin Restrictions")
        print("-" * 30)
        
        # Create a test admin
        test_admin = User(
            username='test_admin',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Admin',
            is_main_admin=False
        )
        
        db.session.add(test_admin)
        db.session.commit()
        
        # Test non-main admin privileges
        can_add_admins = test_admin.can_add_admins()
        can_change_password = test_admin.can_change_password()
        can_manage_properties = test_admin.can_manage_properties()
        
        print(f"Test admin can add admins: {can_add_admins}")
        print(f"Test admin can change password: {can_change_password}")
        print(f"Test admin can manage properties: {can_manage_properties}")
        
        if not can_add_admins and not can_change_password and can_manage_properties:
            print("✅ Non-main admin has correct restricted privileges")
            restrictions_test = True
        else:
            print("❌ Non-main admin restrictions not working correctly")
            restrictions_test = False
        
        # Clean up test admin
        db.session.delete(test_admin)
        db.session.commit()
        print("✅ Test admin cleaned up")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        tests = [
            ("Database State", db_test),
            ("Password Verification", password_test),
            ("Main Admin Privileges", privileges_test),
            ("Non-Main Admin Restrictions", restrictions_test)
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        for test_name, result in tests:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! Main admin system is working correctly.")
            print("🔐 Main Admin Details:")
            print(f"   Username: evian12k")
            print(f"   Password: rhokawi25@12ktbl")
            print(f"   Email: {main_admin.email}")
            print(f"   Can add other admins: YES")
            print(f"   Can change own password: YES")
            print(f"   Can manage properties: YES")
            print("\n✨ System is ready for use!")
        else:
            print("\n⚠️ Some tests failed. Please check the system configuration.")
        
        return passed == total

if __name__ == '__main__':
    success = test_main_admin_system()
    exit(0 if success else 1)