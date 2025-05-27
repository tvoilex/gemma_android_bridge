#!/bin/bash

# Script to stop Gemma 3 / Ollama service
# This script properly stops all Ollama processes

echo "🛑 Stopping Gemma 3 Model Service..."
echo "===================================="

# Find and stop Ollama processes
OLLAMA_PIDS=$(pgrep -f "ollama")

if [ -z "$OLLAMA_PIDS" ]; then
    echo "✅ No Ollama processes found running"
else
    echo "🔍 Found Ollama processes: $OLLAMA_PIDS"
    
    # Try graceful shutdown first
    echo "🔄 Attempting graceful shutdown..."
    pkill -TERM ollama
    
    # Wait a few seconds for graceful shutdown
    sleep 3
    
    # Check if processes are still running
    REMAINING_PIDS=$(pgrep -f "ollama")
    
    if [ -z "$REMAINING_PIDS" ]; then
        echo "✅ Ollama service stopped successfully"
    else
        echo "⚠️  Some processes still running, forcing shutdown..."
        pkill -KILL ollama
        sleep 1
        
        # Final check
        FINAL_CHECK=$(pgrep -f "ollama")
        if [ -z "$FINAL_CHECK" ]; then
            echo "✅ All Ollama processes stopped"
        else
            echo "❌ Some processes may still be running: $FINAL_CHECK"
            echo "💡 You may need to restart your terminal or system"
        fi
    fi
fi

# Clean up any leftover socket files (if any)
if [ -S "/tmp/ollama.sock" ]; then
    rm -f /tmp/ollama.sock
    echo "🧹 Cleaned up socket file"
fi

echo ""
echo "🎉 Gemma 3 service shutdown complete!"
echo "💡 You can restart it anytime with: ./run_gemma.sh"