# Contributing to GAB

Thank you for your interest in contributing to Greedex! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Operating system and version
   - Python version
   - Android device model and OS version
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Error messages or logs

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Describe the use case** and why the feature would be valuable
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity** and maintenance burden

### Code Contributions

#### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/tvoilex/gemma_android_bridge.git
   cd gemma_android_bridge
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv gemma_android_env
   source gemma_android_env/bin/activate  # On Windows: gemma_android_env\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style
- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Keep line length under **88 characters** (Black formatter standard)
- Use **meaningful variable and function names**

##### Code Quality
- **Write tests** for new functionality
- **Ensure existing tests pass** before submitting
- **Add error handling** for edge cases
- **Log important events** using Python's logging module
- **Validate user inputs** and provide helpful error messages

##### Documentation
- **Update README.md** if adding new features
- **Add docstrings** to new functions and classes
- **Include usage examples** for new functionality
- **Update PROJECT_OVERVIEW.md** for architectural changes

#### Testing

1. **Run the test suite**:
   ```bash
   python -m pytest tests/
   ```
2. **Test with real Android device**:
   ```bash
   python demo.py
   ```
3. **Test web interface**:
   ```bash
   python app.py
   # Open http://localhost:5002 and test functionality
   ```

#### Submitting Changes

1. **Commit your changes** with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add voice command support"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Create a Pull Request** on GitHub with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/videos for UI changes
   - Test results

## 📋 Development Setup

### Prerequisites

- **Python 3.8+**
- **Android SDK Platform Tools** (for ADB)
- **Android device** with USB debugging enabled
- **Git** for version control

### Optional Tools

- **Ollama** for local AI model hosting
- **CUDA-compatible GPU** for faster AI inference
- **VS Code** or **PyCharm** for development

### Environment Variables

Create a `.env.local` file for local development:
```bash
FLASK_ENV=development
FLASK_DEBUG=true
OLLAMA_HOST=http://localhost:11434
ADB_PATH=/path/to/adb
```

## 🏗️ Project Structure

```
greedex/
├── 🤖 Core Components
│   ├── gemma_controller.py      # AI model integration
│   ├── android_controller.py    # Android device control
│   └── app.py                   # Flask web application
│
├── 🌐 Web Interface
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
│
├── 🛠️ Scripts & Tools
│   ├── setup.py                # Automated setup
│   ├── demo.py                 # CLI testing
│   └── *.sh                    # Shell scripts
│
├── 📚 Documentation
│   ├── README.md               # Main documentation
│   ├── PROJECT_OVERVIEW.md     # Technical overview
│   └── CONTRIBUTING.md         # This file
│
└── 🧪 Tests
    └── tests/                  # Test suite
```

## 🎯 Areas for Contribution

### High Priority
- **Error handling improvements**
- **Test coverage expansion**
- **Performance optimizations**
- **Documentation updates**
- **Cross-platform compatibility**

### Medium Priority
- **New AI model integrations**
- **Advanced Android automation features**
- **Web UI enhancements**
- **Voice command support**
- **Multi-device control**

### Low Priority
- **Code refactoring**
- **Additional utility scripts**
- **Example applications**
- **Integration with other tools**

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**:
   - OS: macOS/Windows/Linux version
   - Python version: `python --version`
   - Package versions: `pip freeze`

2. **Device information**:
   - Android device model
   - Android OS version
   - ADB version: `adb --version`

3. **Reproduction steps**:
   - Exact commands run
   - Input provided
   - Expected behavior
   - Actual behavior

4. **Logs and errors**:
   - Console output
   - Error messages
   - Stack traces

## 📝 Commit Message Guidelines

Use conventional commit format:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance tasks

Examples:
```
feat: add voice command recognition
fix: resolve ADB connection timeout issue
docs: update installation instructions
style: format code with Black
refactor: simplify command parsing logic
test: add unit tests for Android controller
chore: update dependencies
```

## 🔒 Security

- **Never commit sensitive information** (API keys, passwords, etc.)
- **Use environment variables** for configuration
- **Validate all user inputs** to prevent injection attacks
- **Follow secure coding practices** for Android automation
- **Report security vulnerabilities** privately to maintainers

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check README.md and PROJECT_OVERVIEW.md
- **Code Examples**: See demo.py for usage examples

## 📄 License

By contributing to Greedex, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Greedex! 🚀 
