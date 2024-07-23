from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secreate_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://default:aO3tn5ACpvfD@ep-wispy-art-a1doin49.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['LOGIN_URL'] = '/login'

# File-based cache configuration
app.config["CACHE_TYPE"] = "FileSystemCache"
app.config["CACHE_DIR"] = "/tmp/cache_directory"  # Use a temporary directory

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
cache = Cache(app)
