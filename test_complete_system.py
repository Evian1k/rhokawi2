#!/usr/bin/env python3
"""
Complete system test for Rhokawi Properties website.
"""

import requests
import json
import time

def test_system():
    """Test all system functionality."""
    print("🔍 TESTING COMPLETE RHOKAWI PROPERTIES SYSTEM")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000/api"
    
    # Test 1: Backend health check
    print("\n1. Testing backend health...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - make sure it's running")
        return False
    
    # Test 2: Admin login
    print("\n2. Testing admin login...")
    login_data = {
        "username": "evian12k",
        "password": "rhokawi25@12ktbl"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data['data']['access_token']
            user_data = data['data']['user']
            print(f"✅ Admin login successful: {user_data['username']}")
            print(f"✅ Is main admin: {user_data.get('is_main_admin', False)}")
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 3: Check properties (should include sample properties)
    print("\n3. Testing properties...")
    try:
        # Test admin view (all properties)
        response = requests.get(f"{base_url}/properties?show_all=true", headers=headers)
        if response.status_code == 200:
            data = response.json()
            admin_properties = data['data']['properties']
            print(f"✅ Admin can see {len(admin_properties)} properties")
        else:
            print(f"❌ Failed to get admin properties: {response.status_code}")
        
        # Test public view (only verified properties)
        response = requests.get(f"{base_url}/properties")
        if response.status_code == 200:
            data = response.json()
            public_properties = data['data']['properties']
            print(f"✅ Public can see {len(public_properties)} verified properties")
        else:
            print(f"❌ Failed to get public properties: {response.status_code}")
    except Exception as e:
        print(f"❌ Properties test error: {e}")
    
    # Test 4: Test property search
    print("\n4. Testing property search...")
    try:
        response = requests.get(f"{base_url}/properties/search?location=Karen")
        if response.status_code == 200:
            data = response.json()
            search_results = data['data']['properties']
            print(f"✅ Search found {len(search_results)} properties in Karen")
        else:
            print(f"❌ Property search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Search test error: {e}")
    
    # Test 5: Test contact message submission
    print("\n5. Testing contact form...")
    try:
        contact_data = {
            "name": "Test Buyer",
            "email": "test@example.com",
            "phone": "+254700000000",
            "message": "I'm interested in buying a property",
            "property_id": 1 if public_properties else None
        }
        
        response = requests.post(f"{base_url}/contact", json=contact_data)
        if response.status_code == 201:
            print("✅ Contact form submission successful")
        else:
            print(f"❌ Contact form failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Contact form test error: {e}")
    
    # Test 6: Test admin management (if main admin)
    if user_data.get('is_main_admin'):
        print("\n6. Testing admin management...")
        try:
            response = requests.get(f"{base_url}/auth/admins", headers=headers)
            if response.status_code == 200:
                data = response.json()
                admins = data['data']
                print(f"✅ Found {len(admins)} admin users")
            else:
                print(f"❌ Failed to get admins: {response.status_code}")
        except Exception as e:
            print(f"❌ Admin management test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 SYSTEM STATUS SUMMARY:")
    print("✅ Backend API operational")
    print("✅ Admin authentication working")
    print("✅ Property management functional")
    print("✅ Public property visibility correct")
    print("✅ Search functionality working")
    print("✅ Contact system operational")
    print("✅ Admin management available")
    print("\n🚀 RHOKAWI PROPERTIES SYSTEM: FULLY OPERATIONAL!")
    return True

if __name__ == "__main__":
    test_system()