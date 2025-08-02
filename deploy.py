#!/usr/bin/env python3
"""
Deployment script for SQL Optimizer Pro
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_git():
    """Check if git is installed and initialized"""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git():
    """Initialize git repository if not already done"""
    if not Path('.git').exists():
        print("📁 Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git repository initialized")
    else:
        print("ℹ️  Git repository already exists")

def create_heroku_app(app_name):
    """Create Heroku app"""
    try:
        print(f"🚀 Creating Heroku app: {app_name}")
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        # Set environment variables
        print("🔧 Setting environment variables...")
        subprocess.run(['heroku', 'config:set', 'SECRET_KEY=your-super-secret-key-here'], check=True)
        subprocess.run(['heroku', 'config:set', 'FLASK_ENV=production'], check=True)
        
        print("✅ Heroku app created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create Heroku app: {e}")
        return False

def deploy_to_heroku():
    """Deploy to Heroku"""
    try:
        print("🚀 Deploying to Heroku...")
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        print("✅ Deployment successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def open_heroku_app():
    """Open the deployed app"""
    try:
        print("🌐 Opening your app...")
        subprocess.run(['heroku', 'open'], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Could not open app automatically")
        print("💡 You can open it manually with: heroku open")

def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    try:
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """Main deployment function"""
    print("🚀 SQL Optimizer Pro - Deployment Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_git():
        print("❌ Git is not installed. Please install git first.")
        print("   Download from: https://git-scm.com/")
        return False
    
    if not check_heroku_cli():
        print("❌ Heroku CLI is not installed.")
        print("   Install with: winget install --id=Heroku.HerokuCLI")
        print("   Or download from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Get app name
    app_name = input("Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    if not app_name:
        app_name = "sql-optimizer-pro"
    
    # Initialize git
    init_git()
    
    # Create Heroku app
    if not create_heroku_app(app_name):
        return False
    
    # Deploy
    if not deploy_to_heroku():
        return False
    
    # Open app
    open_heroku_app()
    
    print("\n" + "=" * 50)
    print("🎉 Deployment completed successfully!")
    print(f"🌐 Your app is live at: https://{app_name}.herokuapp.com")
    print("\n💡 Next steps:")
    print("   1. Test your application")
    print("   2. Share the URL with others")
    print("   3. Consider adding a custom domain")
    print("   4. Set up monitoring and analytics")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 