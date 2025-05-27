#!/usr/bin/env python3
"""
Demo script for Gemma3 Android Controller
Tests the core functionality without the web interface
"""

import time
import json
from gemma_controller import GemmaController
from android_controller import AndroidController

def print_separator(title):
    """Print a formatted separator."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def test_android_connection():
    """Test Android device connection."""
    print_separator("Testing Android Connection")
    
    android = AndroidController()
    result = android.check_adb_connection()
    
    if "error" in result:
        print(f"❌ Android connection failed: {result['error']}")
        return False
    else:
        print(f"✅ Android device connected: {result['device_id']}")
        
        # Get device info
        device_info = android.get_device_info()
        if "error" not in device_info:
            print(f"📱 Model: {device_info.get('model', 'Unknown')}")
            print(f"🤖 Android: {device_info.get('android_version', 'Unknown')}")
            print(f"📏 Screen: {device_info.get('screen_size', 'Unknown')}")
        
        return True

def test_gemma_model():
    """Test Gemma model loading and parsing."""
    print_separator("Testing Gemma Model")
    
    gemma = GemmaController()
    
    print("🔄 Loading Gemma model (this may take a while)...")
    success = gemma.load_model()
    
    if not success:
        print("❌ Failed to load Gemma model")
        return False, None
    
    print("✅ Gemma model loaded successfully")
    
    # Test command parsing
    test_commands = [
        "take a screenshot",
        "go back",
        "scroll down",
        "open camera",
        "type hello world",
        "tap in the center"
    ]
    
    print("\n🧪 Testing command parsing:")
    for cmd in test_commands:
        parsed = gemma.parse_command(cmd)
        print(f"  '{cmd}' -> {json.dumps(parsed, indent=2)}")
    
    return True, gemma

def run_interactive_demo(gemma, android):
    """Run an interactive demo."""
    print_separator("Interactive Demo")
    print("🎮 Enter natural language commands to control your Android device")
    print("💡 Examples: 'take screenshot', 'go home', 'scroll down', 'open camera'")
    print("⏹️  Type 'quit' to exit")
    
    while True:
        try:
            command = input("\n🤖 Enter command: ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                break
            
            if not command:
                continue
            
            # Parse command
            print(f"🔍 Parsing: {command}")
            parsed = gemma.parse_command(command)
            
            if "error" in parsed:
                print(f"❌ Parse error: {parsed['error']}")
                continue
            
            print(f"📋 Parsed: {json.dumps(parsed, indent=2)}")
            
            # Execute command
            print("⚡ Executing...")
            result = android.execute_command(parsed)
            
            if "error" in result:
                print(f"❌ Execution error: {result['error']}")
            elif result.get("success"):
                print(f"✅ Success: {result.get('message', 'Command executed')}")
                
                # If screenshot, save it
                if parsed.get("action") == "screenshot" and result.get("screenshot"):
                    import base64
                    screenshot_data = base64.b64decode(result["screenshot"])
                    with open("demo_screenshot.png", "wb") as f:
                        f.write(screenshot_data)
                    print("📸 Screenshot saved as demo_screenshot.png")
            else:
                print(f"⚠️  Unexpected result: {result}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Demo ended")

def main():
    """Main demo function."""
    print("🤖 Gemma3 Android Controller Demo")
    print("This script tests the core functionality without the web interface")
    
    # Test Android connection
    if not test_android_connection():
        print("\n❌ Cannot proceed without Android device connection")
        print("📋 Please ensure:")
        print("   1. ADB is installed and in PATH")
        print("   2. Android device is connected via USB")
        print("   3. USB debugging is enabled")
        print("   4. Device is authorized for debugging")
        return
    
    # Test Gemma model
    success, gemma = test_gemma_model()
    if not success:
        print("\n❌ Cannot proceed without Gemma model")
        print("📋 Please ensure:")
        print("   1. All dependencies are installed (pip install -r requirements.txt)")
        print("   2. Sufficient RAM/VRAM for model loading")
        print("   3. Internet connection for model download (first time)")
        return
    
    # Create Android controller
    android = AndroidController()
    
    # Run interactive demo
    try:
        run_interactive_demo(gemma, android)
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    
    print("\n🎉 Demo completed!")
    print("💡 To run the full web interface, use: python app.py")

if __name__ == "__main__":
    main() 