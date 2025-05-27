#!/usr/bin/env python3
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from app import app

if __name__ == '__main__':
    print("🚀 Starting Gemma3 Android Controller...")
    print("📱 Make sure your Android device is connected with USB debugging enabled")
    print("🌐 Open http://localhost:5002 in your browser")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    app.run(debug=False, host='0.0.0.0', port=5002, threaded=True)
