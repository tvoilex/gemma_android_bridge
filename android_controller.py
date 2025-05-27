import subprocess
import time
import base64
import io
from PIL import Image
# import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple

class AndroidController:
    def __init__(self):
        """Initialize the Android controller."""
        self.device_id = None
        self.screen_size = None
        
    def check_adb_connection(self) -> Dict:
        """Check if ADB is available and devices are connected."""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if result.returncode != 0:
                return {"error": "ADB not found. Please install Android SDK Platform Tools."}
            
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = []
            
            for line in lines:
                if line.strip() and '\t' in line:
                    device_id, status = line.split('\t')
                    devices.append({"id": device_id, "status": status})
            
            if not devices:
                return {"error": "No devices connected. Please connect an Android device with USB debugging enabled."}
            
            # Use the first available device
            for device in devices:
                if device["status"] == "device":
                    self.device_id = device["id"]
                    self._get_screen_size()
                    return {"success": True, "device_id": self.device_id, "devices": devices}
            
            return {"error": "No authorized devices found. Please check USB debugging authorization."}
            
        except FileNotFoundError:
            return {"error": "ADB not found. Please install Android SDK Platform Tools."}
        except Exception as e:
            return {"error": f"Error checking ADB connection: {str(e)}"}
    
    def _get_screen_size(self):
        """Get the screen size of the connected device."""
        try:
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'wm', 'size'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse output like "Physical size: 1080x1920"
                size_line = result.stdout.strip()
                if 'x' in size_line:
                    size_part = size_line.split(':')[-1].strip()
                    width, height = map(int, size_part.split('x'))
                    self.screen_size = (width, height)
                    print(f"Screen size: {width}x{height}")
        except Exception as e:
            print(f"Could not get screen size: {e}")
            self.screen_size = (1080, 1920)  # Default fallback
    
    def execute_command(self, command: Dict) -> Dict:
        """Execute a parsed command on the Android device."""
        if not self.device_id:
            connection_result = self.check_adb_connection()
            if "error" in connection_result:
                return connection_result
        
        action = command.get("action")
        
        try:
            if action == "screenshot":
                return self._take_screenshot()
            elif action == "tap":
                return self._tap(command["x"], command["y"])
            elif action == "swipe":
                return self._swipe(command["start_x"], command["start_y"], 
                                 command["end_x"], command["end_y"])
            elif action == "type":
                return self._type_text(command["text"])
            elif action == "key":
                return self._press_key(command["keycode"])
            elif action == "app":
                return self._open_app(command["package"])
            elif action == "scroll":
                return self._scroll(command["direction"])
            else:
                return {"error": f"Unknown action: {action}"}
                
        except Exception as e:
            return {"error": f"Error executing command: {str(e)}"}
    
    def _take_screenshot(self) -> Dict:
        """Take a screenshot of the device."""
        try:
            # Take screenshot and save to device
            subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'screencap', '/sdcard/screenshot.png'
            ], check=True)
            
            # Pull screenshot to local machine
            result = subprocess.run([
                'adb', '-s', self.device_id, 'exec-out', 'cat', '/sdcard/screenshot.png'
            ], capture_output=True)
            
            if result.returncode == 0:
                # Convert to base64 for web display
                screenshot_b64 = base64.b64encode(result.stdout).decode('utf-8')
                
                # Clean up device storage
                subprocess.run([
                    'adb', '-s', self.device_id, 'shell', 'rm', '/sdcard/screenshot.png'
                ], capture_output=True)
                
                return {
                    "success": True,
                    "screenshot": screenshot_b64,
                    "message": "Screenshot captured successfully"
                }
            else:
                return {"error": "Failed to capture screenshot"}
                
        except Exception as e:
            return {"error": f"Screenshot failed: {str(e)}"}
    
    def _tap(self, x: int, y: int) -> Dict:
        """Tap at the specified coordinates."""
        try:
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'input', 'tap', str(x), str(y)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": f"Tapped at ({x}, {y})"}
            else:
                return {"error": f"Tap failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Tap failed: {str(e)}"}
    
    def _swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 300) -> Dict:
        """Swipe from start coordinates to end coordinates."""
        try:
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'input', 'swipe',
                str(start_x), str(start_y), str(end_x), str(end_y), str(duration)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})"}
            else:
                return {"error": f"Swipe failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Swipe failed: {str(e)}"}
    
    def _type_text(self, text: str) -> Dict:
        """Type text on the device."""
        try:
            # Escape special characters for shell
            escaped_text = text.replace(' ', '%s').replace('&', '\\&').replace('"', '\\"')
            
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'input', 'text', escaped_text
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": f"Typed: {text}"}
            else:
                return {"error": f"Type failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Type failed: {str(e)}"}
    
    def _press_key(self, keycode: str) -> Dict:
        """Press a key on the device."""
        try:
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'input', 'keyevent', f'KEYCODE_{keycode}'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": f"Pressed {keycode} key"}
            else:
                return {"error": f"Key press failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Key press failed: {str(e)}"}
    
    def _open_app(self, package_name: str) -> Dict:
        """Open an app by package name."""
        try:
            # First try to start the main activity
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'monkey', '-p', package_name, '1'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": f"Opened app: {package_name}"}
            else:
                # Fallback: try to launch with am start
                result2 = subprocess.run([
                    'adb', '-s', self.device_id, 'shell', 'am', 'start', 
                    '-n', f'{package_name}/.MainActivity'
                ], capture_output=True, text=True)
                
                if result2.returncode == 0:
                    return {"success": True, "message": f"Opened app: {package_name}"}
                else:
                    return {"error": f"Could not open app {package_name}. App may not be installed."}
                
        except Exception as e:
            return {"error": f"App launch failed: {str(e)}"}
    
    def _scroll(self, direction: str) -> Dict:
        """Scroll in the specified direction."""
        if not self.screen_size:
            self.screen_size = (1080, 1920)  # Default fallback
        
        width, height = self.screen_size
        center_x = width // 2
        center_y = height // 2
        
        # Define scroll distances (about 1/3 of screen)
        scroll_distance = min(width, height) // 3
        
        try:
            if direction == "down":
                # Swipe up to scroll down
                start_y = center_y + scroll_distance // 2
                end_y = center_y - scroll_distance // 2
                return self._swipe(center_x, start_y, center_x, end_y)
            elif direction == "up":
                # Swipe down to scroll up
                start_y = center_y - scroll_distance // 2
                end_y = center_y + scroll_distance // 2
                return self._swipe(center_x, start_y, center_x, end_y)
            elif direction == "left":
                # Swipe right to scroll left
                start_x = center_x + scroll_distance // 2
                end_x = center_x - scroll_distance // 2
                return self._swipe(start_x, center_y, end_x, center_y)
            elif direction == "right":
                # Swipe left to scroll right
                start_x = center_x - scroll_distance // 2
                end_x = center_x + scroll_distance // 2
                return self._swipe(start_x, center_y, end_x, center_y)
            else:
                return {"error": f"Invalid scroll direction: {direction}"}
                
        except Exception as e:
            return {"error": f"Scroll failed: {str(e)}"}
    
    def get_device_info(self) -> Dict:
        """Get information about the connected device."""
        if not self.device_id:
            return {"error": "No device connected"}
        
        try:
            # Get device model
            model_result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'getprop', 'ro.product.model'
            ], capture_output=True, text=True)
            
            # Get Android version
            version_result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'getprop', 'ro.build.version.release'
            ], capture_output=True, text=True)
            
            # Get API level
            api_result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'getprop', 'ro.build.version.sdk'
            ], capture_output=True, text=True)
            
            return {
                "device_id": self.device_id,
                "model": model_result.stdout.strip() if model_result.returncode == 0 else "Unknown",
                "android_version": version_result.stdout.strip() if version_result.returncode == 0 else "Unknown",
                "api_level": api_result.stdout.strip() if api_result.returncode == 0 else "Unknown",
                "screen_size": self.screen_size
            }
            
        except Exception as e:
            return {"error": f"Could not get device info: {str(e)}"}
    
    def list_installed_apps(self) -> Dict:
        """Get a list of installed apps on the device."""
        try:
            result = subprocess.run([
                'adb', '-s', self.device_id, 'shell', 'pm', 'list', 'packages'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                packages = []
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('package:'):
                        package_name = line.replace('package:', '')
                        packages.append(package_name)
                
                return {"success": True, "packages": packages[:50]}  # Limit to first 50
            else:
                return {"error": "Could not list packages"}
                
        except Exception as e:
            return {"error": f"Package listing failed: {str(e)}"} 