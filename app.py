from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import threading
import time
import os
from gemma_controller import GemmaController
from android_controller import AndroidController

app = Flask(__name__)
CORS(app)

# Global instances
# Replace with your local Gemma model path
# gemma = GemmaController("/path/to/your/local/gemma/model")
gemma = GemmaController()  # Will use default model
android = AndroidController()
model_loaded = False
loading_model = False

def load_model_async():
    """Load the Gemma model asynchronously."""
    global model_loaded, loading_model
    loading_model = True
    try:
        success = gemma.load_model()
        model_loaded = success
        print(f"Model loading {'successful' if success else 'failed'}")
    except Exception as e:
        print(f"Error loading model: {e}")
        model_loaded = False
    finally:
        loading_model = False

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get the current status of the system."""
    # Check Android connection
    android_status = android.check_adb_connection()
    
    # Get model info
    model_info = gemma.get_model_info()
    
    return jsonify({
        "model": {
            "loaded": model_loaded,
            "loading": loading_model,
            "info": model_info
        },
        "android": android_status,
        "ready": model_loaded and android_status.get("success", False)
    })

@app.route('/api/command', methods=['POST'])
def execute_command():
    """Execute a natural language command."""
    try:
        data = request.get_json()
        user_command = data.get('command', '').strip()
        
        if not user_command:
            return jsonify({"error": "No command provided"}), 400
        
        if not model_loaded:
            return jsonify({"error": "Gemma model not loaded"}), 503
        
        # Check Android connection
        android_status = android.check_adb_connection()
        if "error" in android_status:
            return jsonify({"error": f"Android connection failed: {android_status['error']}"}), 503
        
        # Parse command with Gemma
        print(f"Parsing command: {user_command}")
        parsed_command = gemma.parse_command(user_command)
        
        if "error" in parsed_command:
            return jsonify({
                "error": f"Command parsing failed: {parsed_command['error']}",
                "original_command": user_command
            }), 400
        
        print(f"Parsed command: {parsed_command}")
        
        # Execute command on Android device
        result = android.execute_command(parsed_command)
        
        return jsonify({
            "success": True,
            "original_command": user_command,
            "parsed_command": parsed_command,
            "result": result
        })
        
    except Exception as e:
        return jsonify({"error": f"Command execution failed: {str(e)}"}), 500

@app.route('/api/screenshot')
def take_screenshot():
    """Take a screenshot of the Android device."""
    try:
        # Check Android connection
        android_status = android.check_adb_connection()
        if "error" in android_status:
            return jsonify({"error": f"Android connection failed: {android_status['error']}"}), 503
        
        result = android.execute_command({"action": "screenshot"})
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Screenshot failed: {str(e)}"}), 500

@app.route('/api/device_info')
def get_device_info():
    """Get information about the connected Android device."""
    try:
        device_info = android.get_device_info()
        return jsonify(device_info)
        
    except Exception as e:
        return jsonify({"error": f"Could not get device info: {str(e)}"}), 500

@app.route('/api/apps')
def list_apps():
    """Get a list of installed apps on the device."""
    try:
        apps = android.list_installed_apps()
        return jsonify(apps)
        
    except Exception as e:
        return jsonify({"error": f"Could not list apps: {str(e)}"}), 500

@app.route('/api/load_model', methods=['POST'])
def load_model():
    """Manually trigger model loading."""
    global loading_model, model_loaded
    
    if model_loaded:
        return jsonify({"message": "Model already loaded"})
    
    if loading_model:
        return jsonify({"message": "Model is currently loading"})
    
    # Start loading in background
    thread = threading.Thread(target=load_model_async)
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Model loading started"})

@app.route('/api/quick_commands')
def get_quick_commands():
    """Get a list of quick commands for the UI."""
    commands = [
        {"name": "Take Screenshot", "command": "take a screenshot"},
        {"name": "Go Home", "command": "go to home screen"},
        {"name": "Go Back", "command": "go back"},
        {"name": "Scroll Down", "command": "scroll down"},
        {"name": "Scroll Up", "command": "scroll up"},
        {"name": "Open Camera", "command": "open camera app"},
        {"name": "Open Settings", "command": "open settings"},
        {"name": "Tap Center", "command": "tap in the center"},
        {"name": "Volume Up", "command": "press volume up"},
        {"name": "Volume Down", "command": "press volume down"}
    ]
    return jsonify(commands)

if __name__ == '__main__':
    # Create templates and static directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Starting Gemma3 Android Controller...")
    print("Loading model in background...")
    
    # Start loading model in background
    thread = threading.Thread(target=load_model_async)
    thread.daemon = True
    thread.start()
    
    # Check Android connection
    print("Checking Android connection...")
    android_status = android.check_adb_connection()
    if "error" in android_status:
        print(f"Warning: {android_status['error']}")
    else:
        print(f"Android device connected: {android_status.get('device_id', 'Unknown')}")
    
    print("\nStarting web server...")
    print("Open http://localhost:5002 in your browser")
    
    app.run(debug=True, host='0.0.0.0', port=5002, threaded=True) 