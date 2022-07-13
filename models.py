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
    posts=db.relationship('Post', backref="user")



    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}, id {self.id}>"

class Post(db.Model):
    '''Post'''

    __tablename__="posts"
    
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer,
                       db.ForeignKey("users.id"),
                       nullable=False)    
    post_title=db.Column(db.Text, nullable=False)
    post_content=db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Post {self.id} {self.post_title}, user_id: {self.user_id}>"

class PostTag(db.Model):
    '''Joins together a Post and Tag'''
    
    __tablename__="post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id=db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    


class Tag(db.Model):
    '''Tag'''

    __tablename__="tags"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False, unique=True)

    posts=db.relationship('Post', secondary="post_tags", cascade="delete", backref="tags")


    
