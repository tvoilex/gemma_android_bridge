# 🤖 GAB - AI-Powered Android Controller

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)

An intelligent Android device controller that uses Google's Gemma3 language model to interpret natural language commands and automate Android devices through ADB (Android Debug Bridge).

## Features

- 🤖 **AI-Powered Control**: Use Gemma3 to interpret natural language commands
- 📱 **Android Integration**: Control Android devices via ADB (Android Debug Bridge)
- 🌐 **Web Interface**: Simple web UI for sending commands and viewing responses
- 📸 **Screen Capture**: Take screenshots and analyze device state
- 🎯 **Smart Actions**: Tap, swipe, type, and navigate based on AI understanding

## Prerequisites

1. **Python 3.8+**
2. **Ollama** (for running Gemma3 model locally)
   - Install from [ollama.ai](https://ollama.ai) or use: `curl -fsSL https://ollama.ai/install.sh | sh`
3. **Android Debug Bridge (ADB)**
   - Install Android SDK Platform Tools
   - Enable USB Debugging on your Android device
4. **GPU Support** (recommended for Gemma3)
   - CUDA-compatible GPU for faster inference

## Setup

### Quick Setup (Automated)
```bash
python setup.py
```
This will handle most of the setup automatically.

### Manual Setup

1. **Install Ollama and Gemma3 model:**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # In a new terminal, pull Gemma3 model
   ollama pull gemma3:latest
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv gemma_android_env
   source gemma_android_env/bin/activate  # On Windows: gemma_android_env\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Enable USB Debugging on your Android device:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings > Developer Options
   - Enable "USB Debugging"

5. **Connect your Android device:**
   ```bash
   adb devices
   ```
   You should see your device listed.

6. **Start the services:**
   
   **Option A: Using separate scripts (recommended for development)**
   ```bash
   # Terminal 1: Start Gemma3 service
   ./run_gemma.sh
   
   # Terminal 2: Start Flask application
   ./run_flask.sh
   ```
   
   **Option B: All-in-one launcher**
   ```bash
   python start.py
   ```

7. **Open your browser:**
   Navigate to `http://localhost:5002`

## Usage Examples

- "Take a screenshot"
- "Open the camera app"
- "Scroll down on the current page"
- "Tap the search button"
- "Type 'hello world' in the text field"
- "Go back to the home screen"
- "Open settings and navigate to WiFi"
  ![image](https://github.com/user-attachments/assets/767e156a-9098-45c1-8b8c-d02b41c631ad)


## Project Structure

```
├── app.py                 # Main Flask application
├── gemma_controller.py    # Gemma3 model integration
├── android_controller.py  # Android device control via ADB
├── static/               # Web UI assets
│   ├── style.css
│   └── script.js
├── templates/            # HTML templates
│   └── index.html
└── requirements.txt      # Python dependencies
```

## API Endpoints

- `POST /api/command` - Send natural language command
- `GET /api/screenshot` - Get current device screenshot
- `GET /api/device_info` - Get connected device information
- `GET /api/status` - Get system status
- `GET /api/apps` - Get installed applications
- `POST /api/load_model` - Load AI model
- `GET /api/quick_commands` - Get quick command suggestions

## Security Notes

- This application is designed for development/testing purposes
- Ensure your Android device is trusted
- ADB connection should be over USB for security

## Troubleshooting

### Ollama/Gemma Issues
1. **Ollama not found**: 
   - Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
   - Restart your terminal after installation
2. **Gemma model not found**: 
   - Pull the model: `ollama pull gemma2:2b`
   - Check available models: `ollama list`
3. **Ollama service not running**: 
   - Start service: `ollama serve`
   - Check if running: `curl http://localhost:11434/api/tags`
4. **Model loading slow**: 
   - First download takes time (model is ~1.5GB)
   - Subsequent loads are faster
   - Use GPU if available for better performance

### Android Device Issues
5. **Device not found**: Ensure USB debugging is enabled and device is connected
6. **Permission denied**: Check ADB permissions and device authorization
7. **ADB not found**: Install Android SDK Platform Tools

### Application Issues
8. **Port already in use**: Change port in `app.py` or kill existing process
9. **Dependencies missing**: Run `pip install -r requirements.txt`
10. **Virtual environment issues**: Recreate with `python -m venv gemma_android_env`

## 🚀 Future Enhancements

- 🎤 Voice command support
- 📱 Multi-device control
- 👁️ Advanced computer vision for UI element detection
- 🔄 Custom action sequences and macros
- 🧠 Integration with other AI models
- 🐳 Docker containerization
- ☁️ Cloud deployment options

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Report bugs and request features
- Submit code improvements
- Add new functionality
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google for the Gemma3 language model
- The Ollama team for local AI model hosting
- The Android development community
- All contributors and users of this project

## 📞 Support
- 📖 **Documentation**: [Project Overview](PROJECT_OVERVIEW.md)

---

**⚠️ Disclaimer**: This tool is designed for development and testing purposes. Always ensure your Android device is trusted and secure when enabling USB debugging. 
