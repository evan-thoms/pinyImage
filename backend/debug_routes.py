#!/usr/bin/env python3
"""
Debug script to check Flask routes
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['DATABASE_URL'] = 'sqlite:///database.db'
os.environ['FLASK_ENV'] = 'development'

# Import the app
from main import app

print("🔍 Flask App Routes:")
print("=" * 50)

for rule in app.url_map.iter_rules():
    print(f"Route: {rule.rule}")
    print(f"  Methods: {rule.methods}")
    print(f"  Endpoint: {rule.endpoint}")
    print("-" * 30)

print("\n🎯 Testing specific routes:")
print("=" * 50)

# Test if /api/register route exists
register_rule = None
for rule in app.url_map.iter_rules():
    if rule.rule == '/api/register':
        register_rule = rule
        break

if register_rule:
    print(f"✅ /api/register route found!")
    print(f"   Methods: {register_rule.methods}")
    print(f"   Endpoint: {register_rule.endpoint}")
else:
    print("❌ /api/register route NOT found!")

# Test if any route matches /api/register
print("\n🔍 Routes that might match /api/register:")
for rule in app.url_map.iter_rules():
    if '/api/register' in rule.rule or rule.rule.endswith('<path:path>'):
        print(f"   {rule.rule} -> {rule.methods}")
