#!/bin/bash

# Script to run Gemma 3 model via Ollama
# This script starts the Ollama service and ensures Gemma 3 model is available

echo "🤖 Starting Gemma 3 Model Service..."
echo "=================================="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it first:"
    echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Start Ollama service in the background if not already running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama service..."
    ollama serve &
    OLLAMA_PID=$!
    echo "📝 Ollama service started with PID: $OLLAMA_PID"
    
    # Wait a moment for the service to start
    sleep 3
else
    echo "✅ Ollama service is already running"
fi

# Check if Gemma 3 model is available
echo "🔍 Checking for Gemma 3 model..."
if ollama list | grep -q "gemma3"; then
    echo "✅ Gemma 3 model is available"
else
    echo "📥 Gemma 3 model not found. Downloading..."
    echo "⚠️  This may take a while depending on your internet connection..."
    ollama pull gemma3:latest
    
    if [ $? -eq 0 ]; then
        echo "✅ Gemma 3 model downloaded successfully"
    else
        echo "❌ Failed to download Gemma 3 model"
        exit 1
    fi
fi

echo ""
echo "🎉 Gemma 3 Model Service is ready!"
echo "📡 Ollama API is running on http://localhost:11434"
echo "🤖 Gemma 3 model is loaded and ready to use"
echo ""
echo "💡 You can now start the Flask application with: ./run_flask.sh"
echo "⏹️  Press Ctrl+C to stop the Ollama service"

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Ollama service..."
    if [ ! -z "$OLLAMA_PID" ]; then
        # Kill the Ollama process we started
        kill $OLLAMA_PID 2>/dev/null
        wait $OLLAMA_PID 2>/dev/null
        echo "✅ Ollama service stopped"
    else
        # If Ollama was already running, ask user if they want to stop it
        echo "⚠️  Ollama was already running when script started."
        echo "💡 Use './stop_gemma.sh' to stop the service completely"
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep the script running to maintain the service
if [ ! -z "$OLLAMA_PID" ]; then
    # Wait for the Ollama process we started
    echo "🔄 Ollama service running (PID: $OLLAMA_PID). Press Ctrl+C to stop..."
    wait $OLLAMA_PID
else
    # If Ollama was already running, just monitor it
    echo "🔄 Monitoring existing Ollama service... (Press Ctrl+C to exit)"
    echo "💡 Note: This will not stop the existing Ollama service"
    while true; do
        if ! pgrep -x "ollama" > /dev/null; then
            echo "❌ Ollama service stopped unexpectedly"
            break
        fi
        sleep 5
    done
fi 