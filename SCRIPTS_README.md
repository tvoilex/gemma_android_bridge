# Separate Scripts for Gemma 3 and Flask

This project now includes two separate scripts to run Gemma 3 and the Flask application independently, so you don't have to wait for model loading each time you restart your app.

## Scripts Overview

### 1. `run_gemma.sh` - Gemma 3 Model Service
This script starts the Ollama service and ensures the Gemma 3 model is available.

**Features:**
- Checks if Ollama is installed
- Starts Ollama service if not running
- Downloads Gemma 3 model if not available
- Keeps the service running in the background
- Properly handles shutdown signals (Ctrl+C)
- Provides status updates and helpful messages

### 2. `run_flask.sh` - Flask Web Application
This script starts the Flask web application for Android device control.

**Features:**
- Activates virtual environment if available
- Checks if Ollama service is running
- Verifies Gemma 3 model availability
- Checks Android device connection
- Installs/verifies dependencies
- Starts the Flask web server

### 3. `stop_gemma.sh` - Stop Gemma 3 Service
This script properly stops all Ollama processes and cleans up.

**Features:**
- Finds all running Ollama processes
- Attempts graceful shutdown first
- Forces shutdown if needed
- Cleans up temporary files
- Provides clear status feedback

## Usage Instructions

### First Time Setup

1. **Start Gemma 3 service** (in Terminal 1):
   ```bash
   ./run_gemma.sh
   ```
   This will:
   - Install/start Ollama if needed
   - Download Gemma 3 model if not present
   - Keep the service running

2. **Start Flask application** (in Terminal 2):
   ```bash
   ./run_flask.sh
   ```
   This will:
   - Check all dependencies
   - Start the web application on http://localhost:5002

### Daily Usage

Once Gemma 3 is downloaded and Ollama is set up:

1. **Keep Gemma 3 running** (Terminal 1):
   ```bash
   ./run_gemma.sh
   ```
   Leave this running in the background.

2. **Restart Flask as needed** (Terminal 2):
   ```bash
   ./run_flask.sh
   ```
   You can stop and restart this anytime without affecting Gemma 3.

## Benefits

- **Faster Development**: No need to wait for model loading when restarting Flask
- **Independent Services**: Gemma 3 runs separately from Flask
- **Better Resource Management**: Keep model loaded while developing
- **Easy Debugging**: Restart Flask without losing model state

## Troubleshooting

### If `run_gemma.sh` fails:
- Ensure Ollama is installed: `curl -fsSL https://ollama.ai/install.sh | sh`
- Check available disk space (Gemma 3 model is several GB)
- Verify internet connection for model download

### If `run_flask.sh` fails:
- Make sure `run_gemma.sh` is running first
- Check if Android device is connected with USB debugging enabled
- Verify virtual environment is set up: `python -m venv gemma_android_env`
- Install dependencies: `pip install -r requirements.txt`

## Port Information

- **Ollama API**: http://localhost:11434
- **Flask Web App**: http://localhost:5002

## Stopping Services

- **Flask**: Press `Ctrl+C` in the Flask terminal
- **Gemma 3**: Press `Ctrl+C` in the Ollama terminal, or use `./stop_gemma.sh`

### Complete Shutdown
To stop all services completely:
```bash
./stop_gemma.sh  # Stops Ollama/Gemma 3 service
# Flask stops automatically when you press Ctrl+C
```

The Flask app can be restarted quickly while keeping Gemma 3 running for faster development cycles. 