# WSGI configuration file for SQL Optimizer Pro
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/sql_optimizer'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secret-key-here'

# Import your Flask app
from app import app as application

# For debugging
if __name__ == "__main__":
    application.run()
