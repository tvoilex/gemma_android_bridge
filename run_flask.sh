#!/bin/bash

# Script to run Flask application
# This script starts the Flask web application for Android control

echo "🌐 Starting Flask Application..."
echo "================================"

# Check if we're in the correct directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the project directory."
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d "gemma_android_env" ]; then
    echo "🐍 Activating virtual environment..."
    source gemma_android_env/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Using system Python."
    echo "💡 Consider creating a virtual environment with: python -m venv gemma_android_env"
fi

# Check if Ollama service is running
echo "🔍 Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama service is not running!"
    echo "💡 Please start Gemma 3 first with: ./run_gemma.sh"
    echo "   Or start Ollama manually with: ollama serve"
    exit 1
else
    echo "✅ Ollama service is running"
fi

# Check if Gemma 3 model is available
echo "🤖 Checking Gemma 3 model..."
if curl -s http://localhost:11434/api/tags | grep -q "gemma3"; then
    echo "✅ Gemma 3 model is available"
else
    echo "❌ Gemma 3 model not found!"
    echo "💡 Please ensure Gemma 3 is downloaded with: ollama pull gemma3:latest"
    exit 1
fi

# Install/check dependencies
echo "📦 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies are satisfied"
    else
        echo "⚠️  Some dependencies might be missing. Installing..."
        pip install -r requirements.txt
    fi
else
    echo "⚠️  requirements.txt not found"
fi

# Check Android connection
echo "📱 Checking Android connection..."
if command -v adb &> /dev/null; then
    if adb devices | grep -q "device$"; then
        echo "✅ Android device connected"
    else
        echo "⚠️  No Android device detected"
        echo "💡 Make sure USB debugging is enabled and device is connected"
    fi
else
    echo "⚠️  ADB not found. Please install Android SDK platform-tools"
fi

echo ""
echo "🚀 Starting Flask Application..."
echo "================================"
echo "📱 Make sure your Android device is connected with USB debugging enabled"
echo "🌐 Open http://localhost:5002 in your browser"
echo "⏹️  Press Ctrl+C to stop"
echo ""

# Set environment variables for production
export FLASK_ENV=production
export FLASK_DEBUG=false

# Start the Flask application
python app.py 