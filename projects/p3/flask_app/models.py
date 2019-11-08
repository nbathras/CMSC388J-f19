from flask_app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name  = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)

    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return "Name: " + str(self.name) + ", Email: " + str(self.email)

class Post(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    title   = db.Column(db.String(128),  nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    date    = db.Column(db.DateTime,     nullable=False)

    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return "Author: " + str(self.user.name) + ", Title: " + str(self.title) + ", Date: " + str(self.date) + ", Content: " + str(self.content)

class Comment(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    post_id    = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    author  = db.Column(db.String(128),  nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    date    = db.Column(db.DateTime,     nullable=False)

    def __repr__(self):
        return "Author: " + str(self.author) + ", Date: " + str(self.date) + ", Content: " + str(self.content)