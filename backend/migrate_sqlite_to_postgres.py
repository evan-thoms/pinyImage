#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to PostgreSQL
Run this after setting up PostgreSQL database
"""

import sqlite3
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, User, Card
from config import config

load_dotenv()

def migrate_sqlite_to_postgres():
    """Migrate data from SQLite to PostgreSQL"""
    print("🚀 Starting SQLite to PostgreSQL migration...")
    
    # Initialize database
    app_config = config['production'] if os.getenv('FLASK_ENV') == 'production' else config['development']
    db.init_app(None)  # We'll set the app later
    
    # Create tables
    print("📋 Creating PostgreSQL tables...")
    with db.engine.connect() as conn:
        db.metadata.create_all(conn)
    
    # Connect to SQLite
    sqlite_path = 'database.db'
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite database not found at {sqlite_path}")
        return False
    
    print("📖 Reading SQLite data...")
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        # Create default user
        print("👤 Creating default user...")
        default_user = User(
            username='default_user',
            email='default@pinyimage.com',
            password_hash='migrated_user_no_password'
        )
        db.session.add(default_user)
        db.session.commit()
        
        # Migrate cards
        print("🃏 Migrating cards...")
        sqlite_cursor.execute('SELECT title, pinyin, meaning, con, created FROM cards')
        cards_data = sqlite_cursor.fetchall()
        
        migrated_count = 0
        for card_data in cards_data:
            try:
                # Parse created date
                created_date = None
                if card_data[4]:  # created field
                    try:
                        created_date = datetime.fromisoformat(card_data[4])
                    except:
                        created_date = datetime.utcnow()
                
                card = Card(
                    user_id=default_user.id,
                    title=card_data[0],  # title
                    pinyin=card_data[1],  # pinyin
                    meaning=card_data[2],  # meaning
                    con=card_data[3],      # con
                    created_at=created_date or datetime.utcnow()
                )
                db.session.add(card)
                migrated_count += 1
                
            except Exception as e:
                print(f"⚠️  Error migrating card {card_data[0]}: {e}")
                continue
        
        db.session.commit()
        print(f"✅ Successfully migrated {migrated_count} cards")
        
        # Verify migration
        total_cards = Card.query.count()
        print(f"📊 Total cards in PostgreSQL: {total_cards}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.session.rollback()
        return False
        
    finally:
        sqlite_conn.close()

def verify_migration():
    """Verify that migration was successful"""
    print("🔍 Verifying migration...")
    
    try:
        # Check user count
        user_count = User.query.count()
        print(f"👥 Users: {user_count}")
        
        # Check card count
        card_count = Card.query.count()
        print(f"🃏 Cards: {card_count}")
        
        # Show sample cards
        sample_cards = Card.query.limit(3).all()
        print("📝 Sample cards:")
        for card in sample_cards:
            print(f"  - {card.title} ({card.pinyin}): {card.meaning[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == '__main__':
    print("🔄 PinyImage Database Migration Tool")
    print("=" * 40)
    
    # Check environment
    env = os.getenv('FLASK_ENV', 'development')
    print(f"🌍 Environment: {env}")
    
    # Run migration
    success = migrate_sqlite_to_postgres()
    
    if success:
        print("\n✅ Migration completed successfully!")
        verify_migration()
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
