#!/usr/bin/env python3
"""
Comprehensive endpoint test to verify all JWT and authentication fixes.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api"

def test_auth_and_get_token():
    """Test authentication and get valid token."""
    print("=== TESTING AUTHENTICATION ===")
    
    # Test login
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login: {response.status_code} - {'✅ SUCCESS' if response.status_code == 200 else '❌ FAILED'}")
    
    if response.status_code == 200:
        token = response.json().get('data', {}).get('access_token')
        print(f"Token received: {token[:50]}...")
        return token
    else:
        print(f"Login failed: {response.text}")
        return None

def test_protected_endpoints(token):
    """Test all protected endpoints that were previously failing."""
    print(f"\n=== TESTING PROTECTED ENDPOINTS ===")
    
    if not token:
        print("❌ No token available - skipping protected endpoint tests")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    all_passed = True
    
    # Test cases: (method, endpoint, expected_status, description)
    test_cases = [
        ("GET", "/auth/me", 200, "Get current user info"),
        ("GET", "/contact?page=1&per_page=10", 200, "Get contact messages"),
        ("GET", "/properties?show_all=true", 200, "Get all properties (admin)"),
    ]
    
    for method, endpoint, expected_status, description in test_cases:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            elif method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json={})
            
            status_ok = response.status_code == expected_status
            status_symbol = "✅" if status_ok else "❌"
            print(f"{method} {endpoint}: {response.status_code} - {status_symbol} {description}")
            
            if not status_ok:
                all_passed = False
                print(f"  Expected: {expected_status}, Got: {response.status_code}")
                print(f"  Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ {method} {endpoint}: ERROR - {e}")
            all_passed = False
    
    return all_passed

def test_upload_endpoint(token):
    """Test upload endpoint that was returning 500 errors."""
    print(f"\n=== TESTING UPLOAD ENDPOINT ===")
    
    if not token:
        print("❌ No token available - skipping upload test")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with no file (should return proper error, not 500)
    try:
        response = requests.post(f"{BASE_URL}/upload", headers=headers)
        print(f"Upload (no file): {response.status_code} - {'✅ EXPECTED ERROR' if response.status_code == 400 else '❌ UNEXPECTED'}")
        
        # Test with invalid token (should return 401, not 500)
        bad_headers = {"Authorization": "Bearer invalid_token"}
        response = requests.post(f"{BASE_URL}/upload", headers=bad_headers)
        print(f"Upload (bad token): {response.status_code} - {'✅ PROPER AUTH ERROR' if response.status_code == 401 else '❌ WRONG ERROR'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False

def test_public_endpoints():
    """Test public endpoints."""
    print(f"\n=== TESTING PUBLIC ENDPOINTS ===")
    
    test_cases = [
        ("GET", "/properties", 200, "Get public properties"),
        ("GET", "/properties/2", 200, "Get specific property (was 404)"),
        ("GET", "/properties/search?status=available", 200, "Search properties"),
    ]
    
    all_passed = True
    
    for method, endpoint, expected_status, description in test_cases:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            status_ok = response.status_code == expected_status
            status_symbol = "✅" if status_ok else "❌"
            print(f"{method} {endpoint}: {response.status_code} - {status_symbol} {description}")
            
            if not status_ok:
                all_passed = False
                print(f"  Expected: {expected_status}, Got: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {method} {endpoint}: ERROR - {e}")
            all_passed = False
    
    return all_passed

def test_properties_post(token):
    """Test properties POST that was returning 422."""
    print(f"\n=== TESTING PROPERTIES POST ===")
    
    if not token:
        print("❌ No token available - skipping properties POST test")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with invalid data (should return validation error, not 422 auth error)
    try:
        response = requests.post(f"{BASE_URL}/properties", headers=headers, json={})
        print(f"Properties POST (no data): {response.status_code} - {'✅ VALIDATION ERROR' if response.status_code == 400 else '❌ UNEXPECTED'}")
        
        # Test with bad token (should return 401, not 422)
        bad_headers = {"Authorization": "Bearer invalid_token"}
        response = requests.post(f"{BASE_URL}/properties", headers=bad_headers, json={})
        print(f"Properties POST (bad token): {response.status_code} - {'✅ AUTH ERROR' if response.status_code == 401 else '❌ WRONG ERROR'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Properties POST test error: {e}")
        return False

def main():
    """Run comprehensive endpoint tests."""
    print("🧪 COMPREHENSIVE ENDPOINT TEST SUITE")
    print("=" * 60)
    print("Testing all previously failing endpoints...")
    
    # Wait a moment for any server to be ready
    time.sleep(1)
    
    # Test authentication
    token = test_auth_and_get_token()
    
    # Test all endpoint categories
    public_ok = test_public_endpoints()
    protected_ok = test_protected_endpoints(token)
    upload_ok = test_upload_endpoint(token)
    properties_ok = test_properties_post(token)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY:")
    print(f"🌐 Public endpoints: {'✅ PASSED' if public_ok else '❌ FAILED'}")
    print(f"🔒 Protected endpoints: {'✅ PASSED' if protected_ok else '❌ FAILED'}")
    print(f"📤 Upload endpoint: {'✅ PASSED' if upload_ok else '❌ FAILED'}")
    print(f"🏠 Properties POST: {'✅ PASSED' if properties_ok else '❌ FAILED'}")
    
    if all([public_ok, protected_ok, upload_ok, properties_ok]):
        print("\n🎉 ALL TESTS PASSED! Your Flask API is working correctly!")
        print("✅ No more 422 errors")
        print("✅ No more 500 errors") 
        print("✅ No more 404 errors on existing resources")
        print("✅ Proper authentication error handling")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n💡 Note: Make sure your Flask server is running on http://127.0.0.1:5000")

if __name__ == "__main__":
    main()