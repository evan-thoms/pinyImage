#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""

import requests
import json

# Test locally first
BASE_URL = "http://localhost:5001"

def test_authentication():
    print("🧪 Testing Authentication Endpoints")
    print("=" * 40)
    
    # Test 1: Register new user
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=register_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"Token: {data['access_token'][:20]}...")
            token = data['access_token']
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data['access_token'][:20]}...")
            token = data['access_token']
        else:
            print(f"❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 3: Get Profile (Protected Route)
    print("\n3. Testing Protected Profile Route...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Profile access successful!")
            print(f"Username: {data['user']['username']}")
            print(f"Email: {data['user']['email']}")
        else:
            print(f"❌ Profile access failed: {response.text}")
    except Exception as e:
        print(f"❌ Profile error: {e}")
    
    print("\n🎉 Authentication tests completed!")

if __name__ == "__main__":
    test_authentication()
