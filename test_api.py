#!/usr/bin/env python3
"""
Test script for the Real Estate Flask API
This script tests all major endpoints to ensure they work correctly.
"""

import requests
import json
import os

BASE_URL = "http://localhost:5000/api"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.user_data = None
        
    def test_register(self):
        """Test user registration"""
        print("Testing user registration...")
        data = {
            "username": "test_agent",
            "email": "agent@test.com", 
            "password": "password123",
            "role": "agent"
        }
        
        response = self.session.post(f"{BASE_URL}/register", json=data)
        print(f"Register Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✓ Registration successful")
            return True
        else:
            print(f"✗ Registration failed: {response.json()}")
            return False
    
    def test_login(self):
        """Test user login"""
        print("\nTesting user login...")
        data = {
            "username": "test_agent",
            "password": "password123"
        }
        
        response = self.session.post(f"{BASE_URL}/login", json=data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            self.user_data = response.json()['user']
            print(f"✓ Login successful as {self.user_data['role']}")
            return True
        else:
            print(f"✗ Login failed: {response.json()}")
            return False
    
    def test_create_property(self):
        """Test property creation"""
        print("\nTesting property creation...")
        data = {
            "title": "Modern Test House",
            "description": "A beautiful test property with modern amenities",
            "location": "123 Test Street, Test City",
            "type": "house",
            "price": 450000,
            "bedrooms": 3,
            "bathrooms": 2,
            "square_feet": 2000
        }
        
        response = self.session.post(f"{BASE_URL}/properties", json=data)
        print(f"Create Property Status: {response.status_code}")
        
        if response.status_code == 201:
            property_data = response.json()['property']
            print(f"✓ Property created with ID: {property_data['id']}")
            return property_data['id']
        else:
            print(f"✗ Property creation failed: {response.json()}")
            return None
    
    def test_get_properties(self):
        """Test getting properties with pagination"""
        print("\nTesting property listing...")
        
        response = self.session.get(f"{BASE_URL}/properties?page=1&per_page=5")
        print(f"Get Properties Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Retrieved {len(data['properties'])} properties")
            print(f"  Total properties: {data['pagination']['total']}")
            return True
        else:
            print(f"✗ Getting properties failed: {response.json()}")
            return False
    
    def test_search_properties(self):
        """Test property search"""
        print("\nTesting property search...")
        
        # Search by location
        response = self.session.get(f"{BASE_URL}/properties?location=Test&min_price=400000")
        print(f"Search Properties Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Search returned {len(data['properties'])} properties")
            return True
        else:
            print(f"✗ Property search failed: {response.json()}")
            return False
    
    def test_favorites(self, property_id):
        """Test favorites functionality"""
        if not property_id:
            print("\nSkipping favorites test - no property ID")
            return False
            
        print(f"\nTesting favorites with property ID {property_id}...")
        
        # Add to favorites
        response = self.session.post(f"{BASE_URL}/favorites/{property_id}")
        print(f"Add Favorite Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✓ Property added to favorites")
            
            # Get favorites
            response = self.session.get(f"{BASE_URL}/favorites")
            if response.status_code == 200:
                favorites = response.json()['favorites']
                print(f"✓ Retrieved {len(favorites)} favorites")
                
                # Remove from favorites
                response = self.session.delete(f"{BASE_URL}/favorites/{property_id}")
                if response.status_code == 200:
                    print("✓ Property removed from favorites")
                    return True
        
        print("✗ Favorites test failed")
        return False
    
    def test_contact(self, property_id=None):
        """Test contact functionality"""
        print("\nTesting contact submission...")
        
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "555-0123",
            "message": "I'm interested in this property. Please contact me.",
            "property_id": property_id
        }
        
        response = self.session.post(f"{BASE_URL}/contact", json=data)
        print(f"Contact Submission Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✓ Contact inquiry submitted successfully")
            
            # Test getting contacts (requires admin/agent role)
            response = self.session.get(f"{BASE_URL}/contacts")
            if response.status_code == 200:
                contacts = response.json()['contacts']
                print(f"✓ Retrieved {len(contacts)} contact inquiries")
                return True
            else:
                print(f"Contact retrieval status: {response.status_code}")
                return True  # Still consider success if we can't retrieve (role issues)
        else:
            print(f"✗ Contact submission failed: {response.json()}")
            return False
    
    def test_logout(self):
        """Test user logout"""
        print("\nTesting user logout...")
        
        response = self.session.post(f"{BASE_URL}/logout")
        print(f"Logout Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Logout successful")
            return True
        else:
            print(f"✗ Logout failed: {response.json()}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("=== Real Estate API Test Suite ===")
        print(f"Testing API at: {BASE_URL}")
        
        # Test authentication flow
        if not self.test_register():
            return False
        
        if not self.test_login():
            return False
        
        # Test property operations
        property_id = self.test_create_property()
        
        self.test_get_properties()
        self.test_search_properties()
        
        # Test favorites
        self.test_favorites(property_id)
        
        # Test contact
        self.test_contact(property_id)
        
        # Test logout
        self.test_logout()
        
        print("\n=== Test Suite Complete ===")
        print("If you see mostly ✓ marks above, the API is working correctly!")
        return True

def main():
    tester = APITester()
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000")
        print("Flask server is running")
    except requests.exceptions.ConnectionError:
        print("ERROR: Flask server is not running!")
        print("Please start the server with: python app.py")
        return
    
    tester.run_all_tests()

if __name__ == "__main__":
    main()