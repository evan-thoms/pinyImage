#!/usr/bin/env python3
"""
Test character analysis and datetime formatting
"""
import requests
import json
import os
import sys

# Test configuration
LOCAL_BASE_URL = "http://localhost:5001"
PRODUCTION_BASE_URL = "https://pinyimage-backend.onrender.com"

def test_character_analysis(base_url):
    """Test character analysis with actual meanings and radicals"""
    print(f"🔍 Testing character analysis at {base_url}")
    
    test_characters = ['水', '火', '人', '大', '小']
    
    for char in test_characters:
        print(f"\n  Testing character: {char}")
        try:
            response = requests.post(f"{base_url}/api/result", 
                                   json={"user_input": char},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                meaning = data.get('meaning', '')
                result = data.get('result', '')
                
                print(f"    Status: ✅ 200")
                print(f"    Meaning: {meaning}")
                print(f"    Has radical info: {'radical' in result.lower()}")
                
                # Check if meaning is not just "character"
                if meaning != 'character':
                    print(f"    ✅ Real meaning found: {meaning}")
                else:
                    print(f"    ⚠️ Fallback meaning: {meaning}")
                    
            else:
                print(f"    Status: ❌ {response.status_code}")
                print(f"    Error: {response.text}")
                
        except Exception as e:
            print(f"    Error: {e}")

def test_datetime_formatting(base_url):
    """Test datetime formatting in card responses"""
    print(f"\n📅 Testing datetime formatting at {base_url}")
    
    try:
        # Test cards endpoint to see datetime format
        response = requests.get(f"{base_url}/api/cards", timeout=10)
        
        if response.status_code == 200:
            cards = response.json()
            print(f"  Status: ✅ 200")
            print(f"  Cards found: {len(cards)}")
            
            if cards:
                card = cards[0]
                created = card.get('created')
                created_display = card.get('created_display')
                
                print(f"  ISO date: {created}")
                print(f"  Display date: {created_display}")
                
                if created_display and len(created_display) < len(created):
                    print(f"  ✅ Date formatting working")
                else:
                    print(f"  ⚠️ Date formatting may need improvement")
            else:
                print(f"  ℹ️ No cards to test datetime formatting")
        else:
            print(f"  Status: ❌ {response.status_code}")
            
    except Exception as e:
        print(f"  Error: {e}")

def test_card_creation_with_meaning(base_url):
    """Test creating a card with proper meaning"""
    print(f"\n➕ Testing card creation with meaning at {base_url}")
    
    test_card = {
        "title": "测试",
        "pinyin": "cè shì",
        "meaning": "test",
        "con": "test connection"
    }
    
    try:
        response = requests.post(f"{base_url}/api/post", 
                               json=test_card,
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: ✅ 200")
            print(f"  Response: {data}")
        else:
            print(f"  Status: ❌ {response.status_code}")
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"  Error: {e}")

def main():
    """Run all tests"""
    print("🧪 CHARACTER ANALYSIS AND DATETIME TEST SUITE")
    print("=" * 60)
    
    # Test local backend
    print("\n📍 LOCAL BACKEND TESTS")
    print("-" * 40)
    test_character_analysis(LOCAL_BASE_URL)
    test_datetime_formatting(LOCAL_BASE_URL)
    test_card_creation_with_meaning(LOCAL_BASE_URL)
    
    # Test production backend
    print("\n📍 PRODUCTION BACKEND TESTS")
    print("-" * 40)
    test_character_analysis(PRODUCTION_BASE_URL)
    test_datetime_formatting(PRODUCTION_BASE_URL)
    test_card_creation_with_meaning(PRODUCTION_BASE_URL)
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    main()
