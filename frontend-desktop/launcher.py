#!/usr/bin/env python3
"""
Chemical Equipment Visualizer - Desktop Application Launcher
This script checks dependencies and provides helpful error messages
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)

def check_venv():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("\n" + "="*60)
        print("WARNING: Not running in a virtual environment!")
        print("="*60)
        print("\nIt's recommended to use a virtual environment.")
        print("\nTo create one:")
        print("1. python -m venv venv")
        print("2. venv\\Scripts\\activate (Windows)")
        print("3. pip install -r requirements.txt")
        print("="*60 + "\n")
        
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

def check_backend_running():
    """Check if backend server is accessible"""
    try:
        import requests
        response = requests.get('http://localhost:8000/api/', timeout=2)
        return True
    except:
        return False

def main():
    """Main launcher function"""
    print("\n" + "="*60)
    print("Chemical Equipment Visualizer - Desktop Application")
    print("="*60 + "\n")
    
    # Check Python version
    check_python_version()
    
    # Check virtual environment
    check_venv()
    
    # Check if backend is running
    if not check_backend_running():
        print("WARNING: Backend server is not running!")
        print("\nPlease start the Django backend first:")
        print("1. Open a new terminal")
        print("2. Navigate to 'backend' folder")
        print("3. Run: python manage.py runserver")
        print("\nOr use the batch file: run_backend.bat")
        print("\n" + "="*60 + "\n")
        
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Launch the main application
    print("Starting application...\n")
    try:
        import main
        main.main()
    except KeyboardInterrupt:
        print("\n\nApplication closed by user.")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        print("\nIf you see import errors, please run:")
        print("pip install -r requirements.txt")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
