#!/usr/bin/env python3
"""
Check Flask configuration
"""
import os
import sys

# Set environment variables
os.environ['DATABASE_URL'] = 'sqlite:///database.db'
os.environ['FLASK_ENV'] = 'development'

print("🔍 Environment Variables:")
print("=" * 40)
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
print(f"SECRET_KEY: {os.environ.get('SECRET_KEY', 'Not set')}")

# Import the app
from main import app

print("\n🔍 Flask App Configuration:")
print("=" * 40)
print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
print(f"FLASK_ENV: {app.config.get('FLASK_ENV')}")
print(f"DEBUG: {app.config.get('DEBUG')}")
print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")

print("\n🔍 Database Connection Test:")
print("=" * 40)
try:
    with app.app_context():
        from models import db
        # Test database connection
        db.session.execute('SELECT 1')
        print("✅ Database connection successful!")
        
        # Check if tables exist
        from models import User, Card
        print("✅ Models imported successfully!")
        
except Exception as e:
    print(f"❌ Database error: {e}")

print("\n🔍 Route Registration:")
print("=" * 40)
for rule in app.url_map.iter_rules():
    if 'api' in rule.rule:
        print(f"  {rule.rule} -> {rule.methods}")
