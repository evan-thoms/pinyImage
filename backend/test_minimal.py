#!/usr/bin/env python3
"""
Minimal test for authentication
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_minimal():
    print("🧪 Minimal Authentication Test")
    print("=" * 40)
    
    # Test 1: Check if backend is running
    print("\n1. Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend health check failed")
            return
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return
    
    # Test 2: Test register endpoint with curl-like request
    print("\n2. Testing register endpoint...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/register", 
            json=register_data,
            headers=headers
        )
        print(f"Register status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text[:200]}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            data = response.json()
            print(f"Token: {data.get('access_token', 'No token')[:20]}...")
        elif response.status_code == 405:
            print("❌ Method not allowed - route conflict detected")
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Registration error: {e}")

if __name__ == "__main__":
    test_minimal()
