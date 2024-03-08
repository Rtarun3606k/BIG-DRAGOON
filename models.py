from config import db
from flask import flash , Flask ,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    # todos = db.relationship('program', backref='user', lazy=True)
    todos = db.relationship('program', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_question = db.Column(db.Text(),nullable=False )
    program_solution = db.Column(db.Text(),nullable=False )
    date_created = db.Column(db.String(300), default=datetime.utcnow)
    program_id = db.Column(db.Text(),nullable=False )


    def __repr__(self) -> str:
        return f"status {self.program_question} - task {self.program_solution}- "
