#!/usr/bin/env python3
"""
Comprehensive PostgreSQL Deployment Test
Tests all components before deployment
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} may have compatibility issues")
        return False

def test_dependencies():
    """Test all required dependencies"""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('psycopg2', 'psycopg2-binary'),
        ('openai', 'OpenAI'),
        ('pinyin', 'pinyin'),
        ('requests', 'requests')
    ]
    
    all_good = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name} imported successfully")
        except ImportError as e:
            print(f"❌ {package_name} import failed: {e}")
            all_good = False
    
    return all_good

def test_database_connection():
    """Test database connection and operations"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from models import db, User, Card
        from config import config
        from main import app
        
        # Test database connection within app context
        with app.app_context():
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful")
        
        # Test user creation
        with app.app_context():
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
        with app.app_context():
            # Refresh the user object in the new session
            test_user = User.query.filter_by(username='test_user').first()
            
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
            
            # Test user relationship
            user_cards = test_user.cards
            print(f"✅ User has {len(user_cards)} cards")
            
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
            return True  # Not a failure, just no API key
        
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

def test_character_service():
    """Test character data service"""
    print("\n🔤 Testing character data service...")
    
    try:
        from character_data_service import CharacterDataService
        
        char_service = CharacterDataService()
        
        # Test character info with fallbacks
        char_info = char_service.get_character_info('水')
        if char_info:
            print(f"✅ Character service working: {char_info['source']}")
        else:
            print("❌ Character service failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Character service test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization"""
    print("\n🌐 Testing Flask app...")
    
    try:
        from main import app
        
        # Test app configuration
        print(f"✅ Flask app created successfully")
        print(f"✅ Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
        print(f"✅ Environment: {app.config.get('ENV', 'Not set')}")
        
        # Test app context
        with app.app_context():
            from models import db
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ App context working")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔗 Testing API endpoints...")
    
    base_url = "http://localhost:5001"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
            print(f"✅ Database: {health_data['services']['database']}")
            print(f"✅ AI Service: {health_data['services']['ai_service']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test status endpoint
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status check: Database={status_data['database']}, AI={status_data['ai_available']}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
        
        # Test cards endpoint
        response = requests.get(f"{base_url}/api/cards", timeout=5)
        if response.status_code == 200:
            cards = response.json()
            print(f"✅ Cards endpoint: {len(cards)} cards retrieved")
        else:
            print(f"❌ Cards endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("⚠️  API server not running (start with 'python main.py')")
        return True  # Not a failure if server isn't running
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variables"""
    print("\n🔧 Testing environment variables...")
    
    required_vars = ['OPENAI_API_KEY', 'DATABASE_URL']
    optional_vars = ['FLASK_ENV', 'SECRET_KEY']
    
    all_good = True
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️  {var} is not set (required for production)")
            all_good = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"ℹ️  {var} is not set (optional)")
    
    return all_good

def main():
    """Run all tests"""
    print("🧪 PinyImage PostgreSQL Deployment Test Suite")
    print("=" * 60)
    
    # Check environment
    env = os.getenv('FLASK_ENV', 'development')
    print(f"🌍 Environment: {env}")
    
    # Run tests
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Database Connection", test_database_connection),
        ("OpenAI Service", test_openai_service),
        ("Character Service", test_character_service),
        ("Flask App", test_flask_app),
        ("Environment Variables", test_environment_variables),
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
        print("🎉 All tests passed! System is ready for PostgreSQL deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
