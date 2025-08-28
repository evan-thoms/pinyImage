# Database Migration Plan: SQLite → PostgreSQL

## Current Issues
- SQLite file gets reset on every deployment
- No user separation
- No data persistence
- Not suitable for production

## Migration Steps

### 1. Add PostgreSQL Dependencies
```bash
# Add to requirements.txt
psycopg2-binary==2.9.7
alembic==1.12.0
```

### 2. Create Database Models
```python
# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    cards = relationship("Card", back_populates="user")

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(10), nullable=False)  # Chinese character
    pinyin = Column(String(50), nullable=False)
    meaning = Column(Text, nullable=False)
    con = Column(Text, nullable=False)  # mnemonic connection
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime)
    review_count = Column(Integer, default=0)
    difficulty = Column(Integer, default=1)  # 1-5 scale
    user = relationship("User", back_populates="cards")
```

### 3. Environment Variables
```bash
# Add to Render environment variables
DATABASE_URL=postgresql://user:password@host:port/database
```

### 4. Migration Script
```python
# migrate_data.py
import sqlite3
import psycopg2
from sqlalchemy import create_engine
from models import Base, User, Card

def migrate_sqlite_to_postgres():
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('database.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    engine = create_engine(os.getenv('DATABASE_URL'))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create default user
    default_user = User(username='default', email='default@example.com', password_hash='dummy')
    session.add(default_user)
    session.commit()
    
    # Migrate cards
    sqlite_cursor.execute('SELECT * FROM cards')
    for row in sqlite_cursor.fetchall():
        card = Card(
            user_id=default_user.id,
            title=row[2],  # title
            pinyin=row[3],  # pinyin
            meaning=row[4],  # meaning
            con=row[5]      # con
        )
        session.add(card)
    
    session.commit()
    session.close()
    sqlite_conn.close()
```

## Benefits After Migration
- ✅ Data persistence across deployments
- ✅ User-specific data
- ✅ Better performance
- ✅ Scalability
- ✅ Backup capabilities
- ✅ Connection pooling

## Resume Impact
- Database management skills
- Migration experience
- Production-ready thinking
- User data handling
