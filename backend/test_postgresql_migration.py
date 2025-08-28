#!/usr/bin/env python3
"""
Test script for PostgreSQL migration and OpenAI integration
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def test_database_connection():
    """Test database connection and basic operations"""
    print("🔍 Testing database connection...")
    
    try:
        from models import db, User, Card
        from config import config
        
        # Test database connection
        db.session.execute('SELECT 1')
        print("✅ Database connection successful")
        
        # Test user creation
        test_user = User.query.filter_by(username='test_user').first()
        if not test_user:
            test_user = User(
                username='test_user',
                email='test@pinyimage.com',
                password_hash='test_hash'
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully")
        else:
            print("✅ Test user already exists")
        
        # Test card creation
        test_card = Card(
            user_id=test_user.id,
            title='测试',
            pinyin='cè shì',
            meaning='test',
            con='This is a test connection'
        )
        db.session.add(test_card)
        db.session.commit()
        print("✅ Test card created successfully")
        
        # Test card retrieval
        cards = Card.query.all()
        print(f"✅ Retrieved {len(cards)} cards from database")
        
        # Clean up test data
        db.session.delete(test_card)
        db.session.commit()
        print("✅ Test cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_openai_service():
    """Test OpenAI service functionality"""
    print("\n🤖 Testing OpenAI service...")
    
    try:
        from openai_service import OpenAIService
        
        openai_service = OpenAIService()
        
        if not openai_service.is_available():
            print("⚠️  OpenAI service not available (no API key)")
            return False
        
        # Test character info
        char_info = openai_service.get_character_info('水')
        if char_info:
            print(f"✅ Character info retrieved: {char_info['pinyin']} - {char_info['meaning']}")
        else:
            print("❌ Character info retrieval failed")
            return False
        
        # Test mnemonic generation
        mnemonic = openai_service.generate_mnemonic('水', 'shuǐ', 'water')
        if mnemonic:
            print(f"✅ Mnemonic generated: {mnemonic[:50]}...")
        else:
            print("❌ Mnemonic generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI service test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test status endpoint
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status check: Database={status_data['database']}, AI={status_data['ai_available']}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
        
        # Test cards endpoint
        response = requests.get(f"{base_url}/api/cards")
        if response.status_code == 200:
            cards = response.json()
            print(f"✅ Cards endpoint: {len(cards)} cards retrieved")
        else:
            print(f"❌ Cards endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("⚠️  API server not running (start with 'python main.py')")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 PinyImage PostgreSQL Migration & OpenAI Integration Test")
    print("=" * 60)
    
    # Check environment
    env = os.getenv('FLASK_ENV', 'development')
    print(f"🌍 Environment: {env}")
    
    # Run tests
    tests = [
        ("Database Connection", test_database_connection),
        ("OpenAI Service", test_openai_service),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! System is ready for production.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == len(results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
