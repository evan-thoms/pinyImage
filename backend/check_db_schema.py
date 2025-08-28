#!/usr/bin/env python3
"""
Check and fix database schema issues
"""
import os
import sys
from sqlalchemy import text, inspect

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_schema():
    """Check the actual database schema"""
    print("🔍 Checking Database Schema")
    print("=" * 40)
    
    # Set environment variables
    os.environ['DATABASE_URL'] = 'sqlite:///database.db'
    os.environ['FLASK_ENV'] = 'development'
    
    # Import the app and models
    from main import app
    from models import db, User, Card
    
    with app.app_context():
        # Get database inspector
        inspector = inspect(db.engine)
        
        # Check users table
        print("\n📋 Users Table Schema:")
        print("-" * 20)
        if inspector.has_table('users'):
            columns = inspector.get_columns('users')
            for column in columns:
                print(f"  {column['name']}: {column['type']}")
        else:
            print("  ❌ Users table does not exist!")
        
        # Check cards table
        print("\n📋 Cards Table Schema:")
        print("-" * 20)
        if inspector.has_table('cards'):
            columns = inspector.get_columns('cards')
            for column in columns:
                print(f"  {column['name']}: {column['type']}")
        else:
            print("  ❌ Cards table does not exist!")
        
        # Test User model
        print("\n🧪 Testing User Model:")
        print("-" * 20)
        try:
            # Try to query users
            users = User.query.all()
            print(f"  ✅ User query successful: {len(users)} users found")
            
            # Try to create a test user
            test_user = User(
                username='test_user',
                email='test@example.com',
                password_hash='test_hash'
            )
            db.session.add(test_user)
            db.session.commit()
            print("  ✅ User creation successful")
            
            # Clean up
            db.session.delete(test_user)
            db.session.commit()
            print("  ✅ User deletion successful")
            
        except Exception as e:
            print(f"  ❌ User model error: {e}")
        
        # Test Card model
        print("\n🧪 Testing Card Model:")
        print("-" * 20)
        try:
            # Try to query cards
            cards = Card.query.all()
            print(f"  ✅ Card query successful: {len(cards)} cards found")
            
            # Try to create a test card
            test_user = User.query.first()
            if test_user:
                test_card = Card(
                    user_id=test_user.id,
                    title='测试',
                    pinyin='cè shì',
                    meaning='test',
                    con='test connection'
                )
                db.session.add(test_card)
                db.session.commit()
                print("  ✅ Card creation successful")
                
                # Clean up
                db.session.delete(test_card)
                db.session.commit()
                print("  ✅ Card deletion successful")
            else:
                print("  ⚠️ No users found to test card creation")
                
        except Exception as e:
            print(f"  ❌ Card model error: {e}")

def fix_database_schema():
    """Fix database schema by recreating tables"""
    print("\n🔧 Fixing Database Schema")
    print("=" * 40)
    
    # Set environment variables
    os.environ['DATABASE_URL'] = 'sqlite:///database.db'
    os.environ['FLASK_ENV'] = 'development'
    
    # Import the app and models
    from main import app
    from models import db, User, Card
    
    with app.app_context():
        try:
            # Drop all tables
            print("  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("  Creating new tables...")
            db.create_all()
            
            print("  ✅ Database schema fixed!")
            
            # Verify
            inspector = inspect(db.engine)
            print(f"  Users table exists: {inspector.has_table('users')}")
            print(f"  Cards table exists: {inspector.has_table('cards')}")
            
        except Exception as e:
            print(f"  ❌ Error fixing schema: {e}")

if __name__ == "__main__":
    check_database_schema()
    
    # Ask if user wants to fix schema
    response = input("\nDo you want to fix the database schema? (y/n): ")
    if response.lower() == 'y':
        fix_database_schema()
    else:
        print("Schema not modified.")
