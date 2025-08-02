#!/usr/bin/env python3
"""
Setup script for SQL Optimizer Pro
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = ['uploads', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"ℹ️  Directory already exists: {directory}")

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_modules = [
        'flask',
        'sqlparse',
        'sqlalchemy',
        'jinja2',
        'werkzeug'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def main():
    """Main setup function"""
    print("🚀 SQL Optimizer Pro - Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return False
    
    # Create directories
    create_directories()
    
    # Test imports
    if not test_imports():
        print("❌ Setup failed during import testing")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Run tests: python test_app.py")
    print("   2. Start server: python run.py")
    print("   3. Open browser: http://localhost:5000")
    print("=" * 40)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 