from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import flash , Flask ,render_template,redirect,request,url_for
import time
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from models import User, program


app = Flask(__name__)

app.secret_key = "secreate_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)