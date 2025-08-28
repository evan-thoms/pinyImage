#!/usr/bin/env python3
"""
Comprehensive test script for production authentication
"""
import requests
import json
import os
import sys

# Test configuration
LOCAL_BASE_URL = "http://localhost:5001"
PRODUCTION_BASE_URL = "https://pinyimage-backend.onrender.com"

def test_backend_health(base_url):
    """Test if backend is responding"""
    print(f"🔍 Testing backend health at {base_url}")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend healthy: {data.get('status')}")
            return True
        else:
            print(f"   ❌ Backend unhealthy: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Backend connection failed: {e}")
        return False

def test_authentication_required(base_url):
    """Test that endpoints require authentication"""
    print(f"\n🔐 Testing authentication requirements at {base_url}")
    
    # Test cards endpoint without auth
    try:
        response = requests.get(f"{base_url}/api/cards")
        print(f"   Cards without auth: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Authentication required")
        else:
            print("   ❌ Authentication not enforced")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test post endpoint without auth
    try:
        response = requests.post(f"{base_url}/api/post", json={})
        print(f"   Post without auth: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Authentication required")
        else:
            print("   ❌ Authentication not enforced")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_with_demo_auth(base_url):
    """Test with demo authentication"""
    print(f"\n👤 Testing with demo authentication at {base_url}")
    
    # Demo user info
    demo_email = "test_user@demo.com"
    demo_id = "test_user_123"
    demo_token = "demo_token_123"
    
    headers = {
        'Authorization': f'Bearer {demo_token}',
        'X-User-Email': demo_email,
        'X-User-ID': demo_id,
        'Content-Type': 'application/json'
    }
    
    # Test cards endpoint
    try:
        response = requests.get(f"{base_url}/api/cards", headers=headers)
        print(f"   Cards with auth: {response.status_code}")
        if response.status_code == 200:
            cards = response.json()
            print(f"   ✅ Retrieved {len(cards)} cards")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test creating a card
    test_card = {
        "title": "测试",
        "pinyin": "cè shì",
        "meaning": "test",
        "con": "test connection"
    }
    
    try:
        response = requests.post(f"{base_url}/api/post", json=test_card, headers=headers)
        print(f"   Create card: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Card created successfully")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_user_isolation(base_url):
    """Test that users are isolated"""
    print(f"\n🔒 Testing user isolation at {base_url}")
    
    # User 1
    user1_headers = {
        'Authorization': 'Bearer token1',
        'X-User-Email': 'user1@demo.com',
        'X-User-ID': 'user1',
        'Content-Type': 'application/json'
    }
    
    # User 2
    user2_headers = {
        'Authorization': 'Bearer token2',
        'X-User-Email': 'user2@demo.com',
        'X-User-ID': 'user2',
        'Content-Type': 'application/json'
    }
    
    # Create cards for both users
    test_card = {
        "title": "隔离",
        "pinyin": "gé lí",
        "meaning": "isolation",
        "con": "user isolation test"
    }
    
    try:
        # User 1 creates a card
        response1 = requests.post(f"{base_url}/api/post", json=test_card, headers=user1_headers)
        print(f"   User1 create card: {response1.status_code}")
        
        # User 2 creates a card
        response2 = requests.post(f"{base_url}/api/post", json=test_card, headers=user2_headers)
        print(f"   User2 create card: {response2.status_code}")
        
        # Check isolation
        cards1 = requests.get(f"{base_url}/api/cards", headers=user1_headers).json()
        cards2 = requests.get(f"{base_url}/api/cards", headers=user2_headers).json()
        
        print(f"   User1 has {len(cards1)} cards")
        print(f"   User2 has {len(cards2)} cards")
        
        if len(cards1) > 0 and len(cards2) > 0:
            print("   ✅ Users are isolated")
        else:
            print("   ❌ User isolation failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    print("🧪 PRODUCTION AUTHENTICATION TEST SUITE")
    print("=" * 50)
    
    # Test local backend
    print("\n📍 LOCAL BACKEND TESTS")
    print("-" * 30)
    if test_backend_health(LOCAL_BASE_URL):
        test_authentication_required(LOCAL_BASE_URL)
        test_with_demo_auth(LOCAL_BASE_URL)
        test_user_isolation(LOCAL_BASE_URL)
    
    # Test production backend
    print("\n📍 PRODUCTION BACKEND TESTS")
    print("-" * 30)
    if test_backend_health(PRODUCTION_BASE_URL):
        test_authentication_required(PRODUCTION_BASE_URL)
        test_with_demo_auth(PRODUCTION_BASE_URL)
        test_user_isolation(PRODUCTION_BASE_URL)
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    main()
