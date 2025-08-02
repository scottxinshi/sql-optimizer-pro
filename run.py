#!/usr/bin/env python3
"""
SQL Optimizer Pro - Run Script
"""

import os
import sys
from app import app

def main():
    """Main function to run the SQL Optimizer Pro application"""
    
    print("🚀 Starting SQL Optimizer Pro...")
    print("=" * 50)
    print("📊 SQL Query Analysis & Optimization Tool")
    print("=" * 50)
    
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # Run the application
    try:
        print("🌐 Starting web server...")
        print("📍 Local URL: http://localhost:5000")
        print("🌍 Network URL: http://0.0.0.0:5000")
        print("=" * 50)
        print("💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 