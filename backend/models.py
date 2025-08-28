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
    
    # Learning progress fields
    total_study_time = db.Column(db.Integer, default=0)  # in minutes
    streak_days = db.Column(db.Integer, default=0)
    last_study_date = db.Column(db.DateTime)
    study_goal = db.Column(db.Integer, default=10)  # daily goal in minutes
    
    # Authentication fields
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Relationship
    cards = db.relationship('Card', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash password and store it"""
        import bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if password matches hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_study_time': self.total_study_time,
            'streak_days': self.streak_days,
            'study_goal': self.study_goal,
            'last_study_date': self.last_study_date.isoformat() if self.last_study_date else None
        }

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
