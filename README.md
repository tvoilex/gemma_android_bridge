# 🤖 Greedex - AI-Powered Android Controller

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
2. **Android Debug Bridge (ADB)**
   - Install Android SDK Platform Tools
   - Enable USB Debugging on your Android device
3. **GPU Support** (recommended for Gemma3)
   - CUDA-compatible GPU for faster inference

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv gemma_android_env
   source gemma_android_env/bin/activate  # On Windows: gemma_android_env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or run the automated setup:
   ```bash
   python setup.py
   ```

3. **Enable USB Debugging on your Android device:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings > Developer Options
   - Enable "USB Debugging"

4. **Connect your Android device:**
   ```bash
   adb devices
   ```
   You should see your device listed.

5. **Run the application:**
   ```bash
   python start.py
   ```
   
   Or for development with debug mode:
   ```bash
   python app.py
   ```

6. **Open your browser:**
   Navigate to `http://localhost:5002`

## Usage Examples

- "Take a screenshot"
- "Open the camera app"
- "Scroll down on the current page"
- "Tap the search button"
- "Type 'hello world' in the text field"
- "Go back to the home screen"
- "Open settings and navigate to WiFi"

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

1. **Device not found**: Ensure USB debugging is enabled and device is connected
2. **Permission denied**: Check ADB permissions and device authorization
3. **Model loading issues**: Ensure sufficient RAM/VRAM for Gemma3
4. **Slow responses**: Consider using a smaller model variant or GPU acceleration

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

- 📋 **Issues**: [GitHub Issues](https://github.com/greedex/greedex/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/greedex/greedex/discussions)
- 📖 **Documentation**: [Project Overview](PROJECT_OVERVIEW.md)

---

**⚠️ Disclaimer**: This tool is designed for development and testing purposes. Always ensure your Android device is trusted and secure when enabling USB debugging. 