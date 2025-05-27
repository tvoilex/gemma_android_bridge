#!/bin/bash
# Activation script for Gemma3 Android Controller virtual environment

echo "🚀 Activating Gemma3 Android Controller environment..."
source gemma_android_env/bin/activate

echo "✅ Virtual environment activated!"
echo "📋 Available commands:"
echo "   python start.py          - Start the web application"
echo "   python demo.py           - Run the command-line demo"
echo "   python app.py            - Start with debug mode"
echo "   deactivate               - Exit virtual environment"
echo ""
echo "🌐 Web interface will be available at: http://localhost:5001"
echo "📱 Make sure your Android device is connected with USB debugging enabled" 