#!/usr/bin/env python3
"""
Setup script for Gemma3 Android Controller MVP
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_adb():
    """Check if ADB is available."""
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ADB is available")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ ADB not found")
    print("📋 Please install Android SDK Platform Tools:")
    
    system = platform.system().lower()
    if system == "darwin":  # macOS
        print("   brew install android-platform-tools")
    elif system == "linux":
        print("   sudo apt-get install android-tools-adb  # Ubuntu/Debian")
        print("   sudo yum install android-tools         # CentOS/RHEL")
    elif system == "windows":
        print("   Download from: https://developer.android.com/studio/releases/platform-tools")
    
    return False

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def check_device_connection():
    """Check if Android device is connected."""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = [line for line in lines if line.strip() and '\t' in line]
            
            if devices:
                print(f"✅ Found {len(devices)} connected device(s):")
                for device in devices:
                    device_id, status = device.split('\t')
                    print(f"   📱 {device_id} ({status})")
                return True
            else:
                print("⚠️  No devices connected")
                print("📋 To connect your Android device:")
                print("   1. Enable Developer Options (tap Build Number 7 times)")
                print("   2. Enable USB Debugging in Developer Options")
                print("   3. Connect device via USB")
                print("   4. Authorize the computer when prompted")
                return False
    except FileNotFoundError:
        return False

def check_gpu_support():
    """Check for GPU support."""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
            print(f"✅ CUDA GPU detected: {gpu_name}")
            print(f"   💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️  No CUDA GPU detected - will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet - GPU check will be done after installation")
        return False

def create_launch_script():
    """Create a launch script for easy startup."""
    script_content = f"""#!/usr/bin/env python3
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
"""
    
    with open('start.py', 'w') as f:
        f.write(script_content)
    
    # Make executable on Unix systems
    if platform.system() != 'Windows':
        os.chmod('start.py', 0o755)
    
    print("✅ Created start.py launcher script")

def main():
    """Main setup function."""
    print("🤖 Gemma3 Android Controller MVP Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check ADB
    adb_available = check_adb()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check GPU support (after PyTorch installation)
    print("\n🔍 Checking GPU support...")
    check_gpu_support()
    
    # Check device connection
    if adb_available:
        print("\n📱 Checking device connection...")
        check_device_connection()
    
    # Create launch script
    print("\n📝 Creating launch script...")
    create_launch_script()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("   1. Connect your Android device with USB debugging enabled")
    print("   2. Run: python start.py")
    print("   3. Open http://localhost:5002 in your browser")
    print("   4. Wait for the Gemma model to load (first time may take a while)")
    print("   5. Start controlling your device with natural language!")
    
    if not adb_available:
        print("\n⚠️  Remember to install ADB before running the application")
    
    print("\n💡 Example commands to try:")
    print("   • 'Take a screenshot'")
    print("   • 'Open the camera app'")
    print("   • 'Scroll down'")
    print("   • 'Go back to home screen'")
    print("   • 'Type hello world'")

if __name__ == "__main__":
    main() 