#!/usr/bin/env python3
"""
Test script to verify API fixes are working correctly.
"""

import requests
import json
import sys
import os

BASE_URL = "http://127.0.0.1:5000/api"

def test_login_and_get_token():
    """Test login and get JWT token."""
    print("=== Testing Login ===")
    login_url = f"{BASE_URL}/auth/login"
    
    # Try with default admin credentials
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('access_token')
            if token:
                print(f"✓ Login successful, got token: {token[:50]}...")
                return token
            else:
                print("✗ Login successful but no token received")
        else:
            print(f"✗ Login failed: {response.text}")
            
    except Exception as e:
        print(f"✗ Login error: {e}")
    
    return None

def test_properties_endpoint():
    """Test properties endpoints."""
    print("\n=== Testing Properties ===")
    
    # Test get all properties
    try:
        response = requests.get(f"{BASE_URL}/properties")
        print(f"GET /properties Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            properties = data.get('data', {}).get('properties', [])
            print(f"✓ Found {len(properties)} properties")
            for prop in properties:
                print(f"  - Property {prop['id']}: {prop['title']}")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test specific property (ID 2)
    try:
        response = requests.get(f"{BASE_URL}/properties/2")
        print(f"GET /properties/2 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            prop = data.get('data')
            print(f"✓ Property 2: {prop['title']}")
        elif response.status_code == 404:
            print("✗ Property 2 not found - need to run fix_database_issues.py")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_contact_endpoints(token):
    """Test contact endpoints."""
    print("\n=== Testing Contact Endpoints ===")
    
    if not token:
        print("✗ No token available, skipping authenticated tests")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET contact messages (admin only)
    try:
        response = requests.get(f"{BASE_URL}/contact?page=1&per_page=10", headers=headers)
        print(f"GET /contact Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            messages = data.get('data', {}).get('messages', [])
            print(f"✓ Found {len(messages)} contact messages")
        elif response.status_code == 401:
            print("✗ Authentication failed - token may be invalid")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test POST contact message (public endpoint)
    try:
        contact_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message"
        }
        response = requests.post(f"{BASE_URL}/contact", json=contact_data)
        print(f"POST /contact Status: {response.status_code}")
        if response.status_code == 201:
            print("✓ Contact message sent successfully")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_upload_endpoint(token):
    """Test upload endpoint."""
    print("\n=== Testing Upload Endpoint ===")
    
    if not token:
        print("✗ No token available, skipping upload test")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test file
    test_file_content = b"fake image content for testing"
    files = {"file": ("test.jpg", test_file_content, "image/jpeg")}
    
    try:
        response = requests.post(f"{BASE_URL}/upload", files=files, headers=headers)
        print(f"POST /upload Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            file_info = data.get('data')
            print(f"✓ File uploaded: {file_info['filename']}")
        elif response.status_code == 401:
            print("✗ Authentication failed - token may be invalid")
        elif response.status_code == 400:
            print("✗ Bad request - may be file validation issue")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Run all tests."""
    print("API FIXES TEST SUITE")
    print("=" * 50)
    
    # Test basic endpoints first
    test_properties_endpoint()
    
    # Test authentication and protected endpoints
    token = test_login_and_get_token()
    test_contact_endpoints(token)
    test_upload_endpoint(token)
    
    print("\n" + "=" * 50)
    print("TEST SUITE COMPLETED")
    print("\nIf you see 422 or 404 errors, run:")
    print("  python fix_database_issues.py")
    print("\nThen restart the Flask server and run this test again.")

if __name__ == "__main__":
    main()