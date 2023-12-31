from flask import Flask, request, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codelab.db'
app.config['SECRET_KEY'] = 'secret'



login_manager = LoginManager(app)
db = SQLAlchemy(app)
