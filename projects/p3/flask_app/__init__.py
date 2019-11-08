from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = b'`\x14\xdc\x1ao\xa8{3\x1b\xae\xb8\xf1^\xd7\r\x15'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

from flask_app import routes
from flask_app.models import *