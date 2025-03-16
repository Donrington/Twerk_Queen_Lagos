from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"


class Contestant(db.Model):
    __tablename__ = 'contestants'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    state_of_origin = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_photo = db.Column(db.String(200))  # Store file path
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    finalist = db.Column(db.Boolean, default=False)  # New field to mark finalists

    # Relationship to Votes with cascade delete
    votes = db.relationship("Vote", backref="contestant", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Contestant {self.first_name} {self.last_name} (Finalist: {self.finalist})>"



class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    contestant_id = db.Column(db.Integer, db.ForeignKey('contestants.id'), nullable=False)
    vote_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Vote for Contestant ID {self.contestant_id}>"


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Admin')
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(300))  # URL to the featured image
    def __repr__(self):
        return f"<BlogPost {self.title}>"


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_resolved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<ContactMessage from {self.name}>"
