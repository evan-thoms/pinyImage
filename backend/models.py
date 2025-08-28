from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    cards = db.relationship('Card', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Card(db.Model):
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(10), nullable=False)  # Chinese character
    pinyin = db.Column(db.String(50), nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    con = db.Column(db.Text, nullable=False)  # mnemonic connection
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Learning progress fields
    last_reviewed = db.Column(db.DateTime)
    review_count = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.Integer, default=1)  # 1-5 scale
    next_review = db.Column(db.DateTime)
    mastered = db.Column(db.Boolean, default=False)
    
    # Relationship
    user = db.relationship('User', back_populates='cards')
    
    def __repr__(self):
        return f'<Card {self.title} for user {self.user_id}>'
    
    def to_dict(self):
        """Convert card to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'pinyin': self.pinyin,
            'meaning': self.meaning,
            'con': self.con,
            'created': self.created_at.isoformat() if self.created_at else None,
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None,
            'review_count': self.review_count,
            'difficulty': self.difficulty,
            'mastered': self.mastered
        }
