from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Create Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Initialize migrations
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Import routes
from app import views
