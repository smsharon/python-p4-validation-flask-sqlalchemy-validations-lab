from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author name is required.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone number must be a 10-digit number')
        return value


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary is not None and len(summary) >= 250:
            raise ValueError('Summary must be at most 250 characters long')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ('Fiction', 'Non-Fiction'):
            raise ValueError('Category must be "Fiction" or "Non-Fiction"')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Title must contain at least one clickbait phrase')
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
