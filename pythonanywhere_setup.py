#!/usr/bin/env python3
"""
PythonAnywhere Free Deployment Setup
"""

import os
import sys

def create_wsgi_file():
    """Create WSGI configuration file for PythonAnywhere"""
    wsgi_content = '''# WSGI configuration file for SQL Optimizer Pro
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
'''
    
    with open('passenger_wsgi.py', 'w') as f:
        f.write(wsgi_content)
    
    print("✅ Created passenger_wsgi.py for PythonAnywhere")

def create_setup_instructions():
    """Create setup instructions for PythonAnywhere"""
    instructions = """
# PythonAnywhere Free Deployment Instructions

## Step 1: Sign up for PythonAnywhere
1. Go to https://www.pythonanywhere.com
2. Click "Create a Beginner account" (FREE)
3. Choose a username and password

## Step 2: Upload Your Files
1. Go to the "Files" tab
2. Create a new directory: sql_optimizer
3. Upload all your project files to this directory

## Step 3: Set up Virtual Environment
1. Go to the "Consoles" tab
2. Start a new Bash console
3. Run these commands:

```bash
cd sql_optimizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Create Web App
1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Select Python 3.8 or higher
5. Set the source code directory to: /home/yourusername/sql_optimizer

## Step 5: Configure WSGI File
1. Click on the WSGI configuration file
2. Replace the content with the passenger_wsgi.py content
3. Update the path to match your username

## Step 6: Reload Web App
1. Click "Reload" button
2. Your app will be available at: https://yourusername.pythonanywhere.com

## Free Tier Limitations:
- 512 MB storage
- 1 web app
- 1 CPU core
- 512 MB RAM
- Perfect for this application!

## Cost: $0/month
"""
    
    with open('PYTHONANYWHERE_SETUP.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created PythonAnywhere setup instructions")

def main():
    """Main setup function"""
    print("🐍 PythonAnywhere Free Setup")
    print("=" * 40)
    
    create_wsgi_file()
    create_setup_instructions()
    
    print("\n🎉 Setup files created!")
    print("📖 Read PYTHONANYWHERE_SETUP.md for detailed instructions")
    print("💰 Total cost: $0/month")

if __name__ == "__main__":
    main() 