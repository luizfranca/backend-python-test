from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
salt = 's0mRIdlKvI'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/alayatodo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

import alayatodo.views

def hashpasswords():
    from alayatodo.models.users import Users 
    
    users = Users.query.all()
    for user in users:
        user.password = bcrypt.generate_password_hash(user.password + salt)
    
    db.session.commit()