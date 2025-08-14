#!/usr/bin/env python3
"""
Royal Restaurant Billing System - Startup Script
This script handles the initialization and startup of the restaurant billing system.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Your Python version: {sys.version}")
        print("Please install Python 3.7+ and try again")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    requirements = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "plotly>=5.15.0"
    ]
    
    for package in requirements:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True, text=True)
            print(f"✅ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            print("Please install manually using: pip install", package)
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['db', 'data', 'pages', 'utils', '.streamlit']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def check_database():
    """Check if database exists and is accessible"""
    db_path = 'db/restaurant.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️  Database exists but no tables found - will be initialized on first run")
        else:
            print(f"✅ Database verified with {len(tables)} tables")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"⚠️  Database will be created on first run: {e}")
        return True

def start_application():
    """Start the Streamlit application"""
    print("\n🚀 Starting Royal Restaurant Billing System...")
    print("📱 The application will open in your default web browser")
    print("🌐 URL: http://localhost:5000")
    print("\n⚠️  Important:")
    print("   - Keep this terminal window open while using the application")
    print("   - Press Ctrl+C to stop the application")
    print("   - The application works completely offline")
    print("\n" + "="*60)
    
    try:
        # Start streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "5000",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        print("Thank you for using Royal Restaurant Billing System!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("Please check the error above and try again")

def main():
    """Main startup function"""
    print("🍽️  Royal Restaurant Billing System - Startup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Installation failed. Please resolve package installation issues.")
        return
    
    # Check database
    check_database()
    
    print("\n✅ System initialization complete!")
    print("🎉 Ready to start the application!")
    
    # Ask user if they want to start
    response = input("\nWould you like to start the application now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        start_application()
    else:
        print("\n📝 To start the application later, run:")
        print("   python run_restaurant.py")
        print("   OR")
        print("   streamlit run app.py --server.port 5000")

if __name__ == "__main__":
    main()