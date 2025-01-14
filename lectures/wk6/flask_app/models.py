<<<<<<< HEAD
from flask_app import db, login_manager
from flask_login import UserMixin

from datetime import datetime

@login_manager.user_loader
def load_user_with_id(id):
    user = User.query.get(id)
    return user

# Use db.Text to allow unlimited length, if needed

class User(db.Model, Mixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return 'User: %s' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    writer_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

    def __repr__(self):
        return self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    writer_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

    def __repr__(self):
        return 'Comment id: %s by User with email: %s' % (self.id, self.writer_email)
=======
from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User('%s', '%s')" % (self.username, self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post: '%s'" % self.title
>>>>>>> afa158b78cafcfb689bf752b992e49d83dcbb0f3
