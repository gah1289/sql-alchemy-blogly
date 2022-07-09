"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint

db = SQLAlchemy()

def connect_db(app):
    '''Connect to database'''
    db.app=app
    db.init_app(app)

class User(db.Model):
    '''User'''

    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.Text, nullable=False, default="/static/images/no-user-image-icon-3.jpg") 
    # Default image isn't working?
    post=db.relationship('Post')

class Post(db.Model):
    '''Post'''

    __tablename__="posts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    
    user_id = db.Column(db.Integer,
                       db.ForeignKey("users.id"),
                       primary_key=True)


    post_title=db.Column(db.String(50), nullable=False)
    post_content=db.Column(db.Text)





    
