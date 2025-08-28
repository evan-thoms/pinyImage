#!/usr/bin/env python3
"""
Simple test for backend without authentication
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_backend():
    print("🧪 Testing Backend (No Auth)")
    print("=" * 40)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is healthy!")
        else:
            print("❌ Health check failed")
            return
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return
    
    # Test 2: Cards endpoint
    print("\n2. Testing cards endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/cards")
        print(f"Cards status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Cards endpoint working!")
        else:
            print(f"❌ Cards endpoint failed: {response.text}")
    except Exception as e:
        print(f"❌ Cards error: {e}")
    
    print("\n🎉 Backend tests completed!")

if __name__ == "__main__":
    test_backend()
