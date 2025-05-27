import ollama
import json
import re
from typing import Dict, List, Optional

class GemmaController:
    def __init__(self, model_name: str = "gemma3:latest"):
        """
        Initialize the Gemma controller with Ollama.
        
        Args:
            model_name: The Ollama model identifier (e.g., "gemma3:latest", "gemma2:2b")
        """
        self.model_name = model_name
        self.client = ollama.Client()
        self.model_loaded = False
        print(f"Using Ollama model: {self.model_name}")
        
    def load_model(self):
        """Check if the Ollama model is available."""
        try:
            print(f"Checking Ollama model: {self.model_name}...")
            
            # List available models
            models = self.client.list()
            available_models = [model.model for model in models.models]
            
            if self.model_name in available_models:
                print(f"✅ Model {self.model_name} is available!")
                self.model_loaded = True
                return True
            else:
                print(f"❌ Model {self.model_name} not found.")
                print(f"Available models: {available_models}")
                return False
                
        except Exception as e:
            print(f"Error checking Ollama model: {e}")
            return False
    
    def parse_command(self, user_input: str, screenshot_available: bool = False) -> Dict:
        """
        Parse user input and convert it to Android control commands using Ollama.
        
        Args:
            user_input: Natural language command from user
            screenshot_available: Whether a screenshot is available for context
            
        Returns:
            Dictionary containing parsed command information
        """
        if not self.model_loaded:
            return {"error": "Model not loaded"}
        
        # Create a structured prompt for command parsing
        system_prompt = """You are an Android device controller. Convert natural language commands into structured JSON actions.

Available actions:
- tap: {"action": "tap", "x": int, "y": int}
- long_press: {"action": "long_press", "x": int, "y": int, "duration": int}
- double_tap: {"action": "double_tap", "x": int, "y": int}
- swipe: {"action": "swipe", "start_x": int, "start_y": int, "end_x": int, "end_y": int, "duration": int}
- pinch: {"action": "pinch", "x": int, "y": int, "scale": float}
- zoom: {"action": "zoom", "x": int, "y": int, "scale": float}
- type: {"action": "type", "text": "string"}
- clear_text: {"action": "clear_text"}
- paste: {"action": "paste"}
- copy: {"action": "copy"}
- cut: {"action": "cut"}
- key: {"action": "key", "keycode": "BACK|HOME|MENU|POWER|VOLUME_UP|VOLUME_DOWN|ENTER|DELETE|TAB|SPACE|SEARCH|CAMERA|CALL|ENDCALL"}
- app: {"action": "app", "package": "com.example.app"}
- app_info: {"action": "app_info", "package": "com.example.app"}
- force_stop: {"action": "force_stop", "package": "com.example.app"}
- uninstall: {"action": "uninstall", "package": "com.example.app"}
- install: {"action": "install", "apk_path": "/path/to/app.apk"}
- screenshot: {"action": "screenshot"}
- screen_record: {"action": "screen_record", "duration": int}
- scroll: {"action": "scroll", "direction": "up|down|left|right", "distance": int}
- fling: {"action": "fling", "direction": "up|down|left|right", "velocity": int}
- drag: {"action": "drag", "start_x": int, "start_y": int, "end_x": int, "end_y": int, "duration": int}
- rotate: {"action": "rotate", "orientation": "portrait|landscape|reverse_portrait|reverse_landscape"}
- brightness: {"action": "brightness", "level": int}
- volume: {"action": "volume", "level": int, "stream": "music|ring|alarm|notification"}
- wifi: {"action": "wifi", "enabled": bool}
- bluetooth: {"action": "bluetooth", "enabled": bool}
- airplane_mode: {"action": "airplane_mode", "enabled": bool}
- location: {"action": "location", "enabled": bool}
- notification_panel: {"action": "notification_panel", "expand": bool}
- quick_settings: {"action": "quick_settings"}
- recent_apps: {"action": "recent_apps"}
- split_screen: {"action": "split_screen", "app1": "package1", "app2": "package2"}
- picture_in_picture: {"action": "picture_in_picture"}
- accessibility: {"action": "accessibility", "service": "talkback|magnification", "enabled": bool}
- developer_options: {"action": "developer_options", "option": "usb_debugging|show_touches|pointer_location", "enabled": bool}
- system_ui: {"action": "system_ui", "component": "status_bar|navigation_bar", "visible": bool}
- input_method: {"action": "input_method", "ime": "keyboard_package"}
- language: {"action": "language", "locale": "en_US|es_ES|fr_FR|de_DE|ja_JP|ko_KR|zh_CN"}
- timezone: {"action": "timezone", "zone": "America/New_York|Europe/London|Asia/Tokyo"}
- auto_rotate: {"action": "auto_rotate", "enabled": bool}
- sleep_timeout: {"action": "sleep_timeout", "seconds": int}
- font_size: {"action": "font_size", "scale": float}
- display_size: {"action": "display_size", "scale": float}
- dark_mode: {"action": "dark_mode", "enabled": bool}
- do_not_disturb: {"action": "do_not_disturb", "enabled": bool}
- battery_saver: {"action": "battery_saver", "enabled": bool}
- data_saver: {"action": "data_saver", "enabled": bool}
- hotspot: {"action": "hotspot", "enabled": bool}
- nfc: {"action": "nfc", "enabled": bool}
- cast_screen: {"action": "cast_screen", "device": "device_name"}
- backup: {"action": "backup", "type": "full|app_data"}
- factory_reset: {"action": "factory_reset", "confirm": bool}
- reboot: {"action": "reboot", "mode": "normal|recovery|bootloader"}
- shutdown: {"action": "shutdown"}
- wake_up: {"action": "wake_up"}
- lock_screen: {"action": "lock_screen"}
- unlock_screen: {"action": "unlock_screen", "method": "swipe|pin|pattern|fingerprint", "credential": "string"}
- emergency_call: {"action": "emergency_call"}
- flashlight: {"action": "flashlight", "enabled": bool}
- camera_flash: {"action": "camera_flash", "mode": "on|off|auto|torch"}
- vibrate: {"action": "vibrate", "pattern": [int], "amplitude": int}
- play_sound: {"action": "play_sound", "file": "/path/to/sound.mp3", "volume": float}
- tts: {"action": "tts", "text": "string", "language": "en|es|fr|de|ja|ko|zh"}
- ocr: {"action": "ocr", "region": {"x": int, "y": int, "width": int, "height": int}}
- find_element: {"action": "find_element", "method": "text|id|class|xpath", "value": "string"}
- wait_for_element: {"action": "wait_for_element", "method": "text|id|class|xpath", "value": "string", "timeout": int}
- assert_element: {"action": "assert_element", "method": "text|id|class|xpath", "value": "string", "exists": bool}
- get_element_bounds: {"action": "get_element_bounds", "method": "text|id|class|xpath", "value": "string"}
- get_screen_info: {"action": "get_screen_info"}
- get_device_info: {"action": "get_device_info"}
- get_battery_info: {"action": "get_battery_info"}
- get_network_info: {"action": "get_network_info"}
- get_storage_info: {"action": "get_storage_info"}
- get_running_apps: {"action": "get_running_apps"}
- get_installed_apps: {"action": "get_installed_apps"}
- get_system_settings: {"action": "get_system_settings", "namespace": "system|secure|global"}
- set_system_setting: {"action": "set_system_setting", "namespace": "system|secure|global", "key": "string", "value": "string"}
- shell_command: {"action": "shell_command", "command": "string"}
- file_operation: {"action": "file_operation", "operation": "copy|move|delete|create|read", "source": "/path", "destination": "/path"}
- permission: {"action": "permission", "package": "com.example.app", "permission": "android.permission.CAMERA", "grant": bool}
- intent: {"action": "intent", "action": "android.intent.action.VIEW", "data": "content://", "extras": {}}
- broadcast: {"action": "broadcast", "action": "com.example.CUSTOM_ACTION", "extras": {}}
- service: {"action": "service", "operation": "start|stop", "component": "com.example/.MyService"}
- activity: {"action": "activity", "operation": "start|finish", "component": "com.example/.MainActivity"}
- monkey_test: {"action": "monkey_test", "package": "com.example.app", "events": int, "seed": int}
- stress_test: {"action": "stress_test", "type": "cpu|memory|storage|network", "duration": int}
- performance_test: {"action": "performance_test", "package": "com.example.app", "duration": int}
- memory_dump: {"action": "memory_dump", "package": "com.example.app", "output": "/path/to/dump"}
- cpu_profile: {"action": "cpu_profile", "package": "com.example.app", "duration": int}
- network_monitor: {"action": "network_monitor", "package": "com.example.app", "duration": int}
- log_capture: {"action": "log_capture", "level": "verbose|debug|info|warn|error", "tag": "string", "duration": int}
- crash_report: {"action": "crash_report", "package": "com.example.app"}
- anr_report: {"action": "anr_report", "package": "com.example.app"}
- security_scan: {"action": "security_scan", "package": "com.example.app"}
- accessibility_scan: {"action": "accessibility_scan"}
- ui_hierarchy: {"action": "ui_hierarchy", "format": "xml|json"}
- element_screenshot: {"action": "element_screenshot", "method": "text|id|class|xpath", "value": "string"}
- compare_screenshots: {"action": "compare_screenshots", "image1": "/path1", "image2": "/path2", "threshold": float}
- visual_test: {"action": "visual_test", "baseline": "/path/to/baseline.png", "threshold": float}
- gesture_record: {"action": "gesture_record", "name": "gesture_name", "duration": int}
- gesture_play: {"action": "gesture_play", "name": "gesture_name"}
- macro_record: {"action": "macro_record", "name": "macro_name"}
- macro_play: {"action": "macro_play", "name": "macro_name"}
- conditional: {"action": "conditional", "condition": {"method": "text|id|class|xpath", "value": "string", "exists": bool}, "then": {}, "else": {}}
- loop: {"action": "loop", "count": int, "actions": [{}]}
- wait: {"action": "wait", "seconds": int}
- random_action: {"action": "random_action", "actions": ["tap|swipe|scroll"], "count": int}

Examples:
User: "Take a screenshot"
Response: {"action": "screenshot"}

User: "Record screen for 30 seconds"
Response: {"action": "screen_record", "duration": 30}

User: "Go back"
Response: {"action": "key", "keycode": "BACK"}

User: "Open camera"
Response: {"action": "app", "package": "com.android.camera"}

User: "Type hello world"
Response: {"action": "type", "text": "hello world"}

User: "Scroll down"
Response: {"action": "scroll", "direction": "down"}

User: "Long press in the center"
Response: {"action": "long_press", "x": 540, "y": 960, "duration": 1000}

User: "Turn on WiFi"
Response: {"action": "wifi", "enabled": true}

User: "Set brightness to 50%"
Response: {"action": "brightness", "level": 128}

User: "Rotate to landscape"
Response: {"action": "rotate", "orientation": "landscape"}

User: "Enable dark mode"
Response: {"action": "dark_mode", "enabled": true}

User: "Get device info"
Response: {"action": "get_device_info"}

User: "Find element with text Login"
Response: {"action": "find_element", "method": "text", "value": "Login"}

User: "Swipe from left to right"
Response: {"action": "swipe", "start_x": 100, "start_y": 960, "end_x": 980, "end_y": 960, "duration": 300}

User: "Pinch to zoom out"
Response: {"action": "pinch", "x": 540, "y": 960, "scale": 0.5}

User: "Open notification panel"
Response: {"action": "notification_panel", "expand": true}

User: "Turn on flashlight"
Response: {"action": "flashlight", "enabled": true}

User: "Reboot device"
Response: {"action": "reboot", "mode": "normal"}

User: "Wait 3 seconds"
Response: {"action": "wait", "seconds": 3}

IMPORTANT: Respond ONLY with valid JSON. No explanations or additional text.

Convert this command: "{user_input}"
"""

        try:
            # Send request to Ollama
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user', 
                        'content': f'Convert this command: "{user_input}"'
                    }
                ],
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'num_predict': 100
                }
            )
            
            # Extract the response
            response_text = response['message']['content'].strip()
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^}]*\}', response_text)
            if json_match:
                try:
                    command_json = json.loads(json_match.group())
                    return self._validate_command(command_json)
                except json.JSONDecodeError:
                    pass
            
            # Fallback: parse common commands manually
            return self._fallback_parse(user_input)
            
        except Exception as e:
            print(f"Error parsing command with Ollama: {e}")
            return self._fallback_parse(user_input)
    
    def _validate_command(self, command: Dict) -> Dict:
        """Validate and sanitize the parsed command."""
        if "action" not in command:
            return {"error": "No action specified"}
        
        action = command["action"]
        
        # Validate required parameters for each action
        if action == "tap":
            if "x" not in command or "y" not in command:
                return {"error": "Tap action requires x and y coordinates"}
            command["x"] = max(0, min(1080, int(command["x"])))
            command["y"] = max(0, min(1920, int(command["y"])))
            
        elif action == "long_press":
            if "x" not in command or "y" not in command:
                return {"error": "Long press action requires x and y coordinates"}
            command["x"] = max(0, min(1080, int(command["x"])))
            command["y"] = max(0, min(1920, int(command["y"])))
            command["duration"] = max(500, min(10000, int(command.get("duration", 1000))))
            
        elif action == "double_tap":
            if "x" not in command or "y" not in command:
                return {"error": "Double tap action requires x and y coordinates"}
            command["x"] = max(0, min(1080, int(command["x"])))
            command["y"] = max(0, min(1920, int(command["y"])))
            
        elif action == "swipe":
            required = ["start_x", "start_y", "end_x", "end_y"]
            if not all(param in command for param in required):
                return {"error": "Swipe action requires start_x, start_y, end_x, end_y"}
            for param in required:
                command[param] = max(0, min(1080 if "x" in param else 1920, int(command[param])))
            command["duration"] = max(100, min(5000, int(command.get("duration", 300))))
            
        elif action in ["pinch", "zoom"]:
            if "x" not in command or "y" not in command or "scale" not in command:
                return {"error": f"{action} action requires x, y coordinates and scale"}
            command["x"] = max(0, min(1080, int(command["x"])))
            command["y"] = max(0, min(1920, int(command["y"])))
            command["scale"] = max(0.1, min(10.0, float(command["scale"])))
            
        elif action == "drag":
            required = ["start_x", "start_y", "end_x", "end_y"]
            if not all(param in command for param in required):
                return {"error": "Drag action requires start_x, start_y, end_x, end_y"}
            for param in required:
                command[param] = max(0, min(1080 if "x" in param else 1920, int(command[param])))
            command["duration"] = max(100, min(5000, int(command.get("duration", 1000))))
                
        elif action == "type":
            if "text" not in command:
                return {"error": "Type action requires text"}
            command["text"] = str(command["text"])[:1000]
            
        elif action == "key":
            valid_keys = ["BACK", "HOME", "MENU", "POWER", "VOLUME_UP", "VOLUME_DOWN", 
                         "ENTER", "DELETE", "TAB", "SPACE", "SEARCH", "CAMERA", "CALL", "ENDCALL"]
            if "keycode" not in command or command["keycode"] not in valid_keys:
                return {"error": f"Key action requires valid keycode: {valid_keys}"}
                
        elif action in ["app", "app_info", "force_stop", "uninstall"]:
            if "package" not in command:
                return {"error": f"{action} action requires package name"}
                
        elif action == "install":
            if "apk_path" not in command:
                return {"error": "Install action requires apk_path"}
                
        elif action == "screen_record":
            command["duration"] = max(1, min(300, int(command.get("duration", 30))))
            
        elif action == "scroll":
            valid_directions = ["up", "down", "left", "right"]
            if "direction" not in command or command["direction"] not in valid_directions:
                return {"error": f"Scroll action requires valid direction: {valid_directions}"}
            command["distance"] = max(100, min(2000, int(command.get("distance", 500))))
            
        elif action == "fling":
            valid_directions = ["up", "down", "left", "right"]
            if "direction" not in command or command["direction"] not in valid_directions:
                return {"error": f"Fling action requires valid direction: {valid_directions}"}
            command["velocity"] = max(100, min(5000, int(command.get("velocity", 1000))))
            
        elif action == "rotate":
            valid_orientations = ["portrait", "landscape", "reverse_portrait", "reverse_landscape"]
            if "orientation" not in command or command["orientation"] not in valid_orientations:
                return {"error": f"Rotate action requires valid orientation: {valid_orientations}"}
                
        elif action == "brightness":
            if "level" not in command:
                return {"error": "Brightness action requires level (0-255)"}
            command["level"] = max(0, min(255, int(command["level"])))
            
        elif action == "volume":
            if "level" not in command:
                return {"error": "Volume action requires level (0-100)"}
            command["level"] = max(0, min(100, int(command["level"])))
            valid_streams = ["music", "ring", "alarm", "notification"]
            if "stream" in command and command["stream"] not in valid_streams:
                return {"error": f"Volume stream must be one of: {valid_streams}"}
            command["stream"] = command.get("stream", "music")
            
        elif action in ["wifi", "bluetooth", "airplane_mode", "location", "auto_rotate", 
                       "dark_mode", "do_not_disturb", "battery_saver", "data_saver", 
                       "hotspot", "nfc", "flashlight"]:
            if "enabled" not in command:
                return {"error": f"{action} action requires enabled (true/false)"}
            command["enabled"] = bool(command["enabled"])
            
        elif action == "notification_panel":
            if "expand" not in command:
                return {"error": "Notification panel action requires expand (true/false)"}
            command["expand"] = bool(command["expand"])
            
        elif action == "split_screen":
            if "app1" not in command or "app2" not in command:
                return {"error": "Split screen action requires app1 and app2 package names"}
                
        elif action == "accessibility":
            valid_services = ["talkback", "magnification"]
            if "service" not in command or command["service"] not in valid_services:
                return {"error": f"Accessibility action requires valid service: {valid_services}"}
            if "enabled" not in command:
                return {"error": "Accessibility action requires enabled (true/false)"}
            command["enabled"] = bool(command["enabled"])
            
        elif action == "developer_options":
            valid_options = ["usb_debugging", "show_touches", "pointer_location"]
            if "option" not in command or command["option"] not in valid_options:
                return {"error": f"Developer options action requires valid option: {valid_options}"}
            if "enabled" not in command:
                return {"error": "Developer options action requires enabled (true/false)"}
            command["enabled"] = bool(command["enabled"])
            
        elif action == "system_ui":
            valid_components = ["status_bar", "navigation_bar"]
            if "component" not in command or command["component"] not in valid_components:
                return {"error": f"System UI action requires valid component: {valid_components}"}
            if "visible" not in command:
                return {"error": "System UI action requires visible (true/false)"}
            command["visible"] = bool(command["visible"])
            
        elif action == "input_method":
            if "ime" not in command:
                return {"error": "Input method action requires ime package"}
                
        elif action == "language":
            valid_locales = ["en_US", "es_ES", "fr_FR", "de_DE", "ja_JP", "ko_KR", "zh_CN"]
            if "locale" not in command or command["locale"] not in valid_locales:
                return {"error": f"Language action requires valid locale: {valid_locales}"}
                
        elif action == "timezone":
            valid_zones = ["America/New_York", "Europe/London", "Asia/Tokyo"]
            if "zone" not in command or command["zone"] not in valid_zones:
                return {"error": f"Timezone action requires valid zone: {valid_zones}"}
                
        elif action == "sleep_timeout":
            if "seconds" not in command:
                return {"error": "Sleep timeout action requires seconds"}
            command["seconds"] = max(15, min(1800, int(command["seconds"])))
            
        elif action in ["font_size", "display_size"]:
            if "scale" not in command:
                return {"error": f"{action} action requires scale (0.5-2.0)"}
            command["scale"] = max(0.5, min(2.0, float(command["scale"])))
            
        elif action == "unlock_screen":
            valid_methods = ["swipe", "pin", "pattern", "fingerprint"]
            if "method" not in command or command["method"] not in valid_methods:
                return {"error": f"Unlock screen action requires valid method: {valid_methods}"}
            if command["method"] in ["pin", "pattern"] and "credential" not in command:
                return {"error": f"Unlock method {command['method']} requires credential"}
                
        elif action == "camera_flash":
            valid_modes = ["on", "off", "auto", "torch"]
            if "mode" not in command or command["mode"] not in valid_modes:
                return {"error": f"Camera flash action requires valid mode: {valid_modes}"}
                
        elif action == "vibrate":
            if "pattern" in command and not isinstance(command["pattern"], list):
                return {"error": "Vibrate pattern must be a list of integers"}
            command["amplitude"] = max(1, min(255, int(command.get("amplitude", 128))))
            
        elif action == "play_sound":
            if "file" not in command:
                return {"error": "Play sound action requires file path"}
            command["volume"] = max(0.0, min(1.0, float(command.get("volume", 1.0))))
            
        elif action == "tts":
            if "text" not in command:
                return {"error": "TTS action requires text"}
            valid_languages = ["en", "es", "fr", "de", "ja", "ko", "zh"]
            command["language"] = command.get("language", "en")
            if command["language"] not in valid_languages:
                return {"error": f"TTS language must be one of: {valid_languages}"}
                
        elif action in ["find_element", "wait_for_element", "assert_element", "get_element_bounds", "element_screenshot"]:
            valid_methods = ["text", "id", "class", "xpath"]
            if "method" not in command or command["method"] not in valid_methods:
                return {"error": f"{action} requires valid method: {valid_methods}"}
            if "value" not in command:
                return {"error": f"{action} requires value"}
            if action == "wait_for_element":
                command["timeout"] = max(1, min(60, int(command.get("timeout", 10))))
            if action == "assert_element" and "exists" not in command:
                return {"error": "Assert element action requires exists (true/false)"}
                
        elif action == "ocr":
            if "region" in command:
                region = command["region"]
                if not all(key in region for key in ["x", "y", "width", "height"]):
                    return {"error": "OCR region requires x, y, width, height"}
                    
        elif action == "shell_command":
            if "command" not in command:
                return {"error": "Shell command action requires command"}
                
        elif action == "file_operation":
            valid_operations = ["copy", "move", "delete", "create", "read"]
            if "operation" not in command or command["operation"] not in valid_operations:
                return {"error": f"File operation requires valid operation: {valid_operations}"}
            if command["operation"] in ["copy", "move"] and "destination" not in command:
                return {"error": f"File {command['operation']} requires destination"}
            if "source" not in command:
                return {"error": "File operation requires source path"}
                
        elif action == "permission":
            if not all(key in command for key in ["package", "permission", "grant"]):
                return {"error": "Permission action requires package, permission, and grant"}
            command["grant"] = bool(command["grant"])
            
        elif action in ["monkey_test", "performance_test"]:
            if "package" not in command:
                return {"error": f"{action} requires package name"}
            if action == "monkey_test":
                command["events"] = max(1, min(10000, int(command.get("events", 100))))
                command["seed"] = int(command.get("seed", 1))
            else:
                command["duration"] = max(1, min(300, int(command.get("duration", 60))))
                
        elif action == "stress_test":
            valid_types = ["cpu", "memory", "storage", "network"]
            if "type" not in command or command["type"] not in valid_types:
                return {"error": f"Stress test requires valid type: {valid_types}"}
            command["duration"] = max(1, min(300, int(command.get("duration", 60))))
            
        elif action == "ui_hierarchy":
            valid_formats = ["xml", "json"]
            command["format"] = command.get("format", "xml")
            if command["format"] not in valid_formats:
                return {"error": f"UI hierarchy format must be one of: {valid_formats}"}
                
        elif action == "compare_screenshots":
            if not all(key in command for key in ["image1", "image2"]):
                return {"error": "Compare screenshots requires image1 and image2 paths"}
            command["threshold"] = max(0.0, min(1.0, float(command.get("threshold", 0.9))))
            
        elif action == "visual_test":
            if "baseline" not in command:
                return {"error": "Visual test requires baseline image path"}
            command["threshold"] = max(0.0, min(1.0, float(command.get("threshold", 0.9))))
            
        elif action in ["gesture_record", "macro_record"]:
            if "name" not in command:
                return {"error": f"{action} requires name"}
            if action == "gesture_record":
                command["duration"] = max(1, min(60, int(command.get("duration", 10))))
                
        elif action in ["gesture_play", "macro_play"]:
            if "name" not in command:
                return {"error": f"{action} requires name"}
                
        elif action == "conditional":
            if "condition" not in command or "then" not in command:
                return {"error": "Conditional action requires condition and then"}
                
        elif action == "loop":
            if "count" not in command or "actions" not in command:
                return {"error": "Loop action requires count and actions"}
            command["count"] = max(1, min(100, int(command["count"])))
            
        elif action == "wait":
            if "seconds" not in command:
                return {"error": "Wait action requires seconds"}
            command["seconds"] = max(0.1, min(60.0, float(command["seconds"])))
            
        elif action == "random_action":
            valid_actions = ["tap", "swipe", "scroll"]
            if "actions" not in command:
                command["actions"] = valid_actions
            command["count"] = max(1, min(50, int(command.get("count", 5))))
        
        return command
    
    def _fallback_parse(self, user_input: str) -> Dict:
        """Fallback parser for common commands when AI parsing fails."""
        user_input = user_input.lower().strip()
        
        # Screenshot and recording commands
        if any(word in user_input for word in ["screenshot", "capture", "screen"]):
            if "record" in user_input:
                return {"action": "screen_record", "duration": 30}
            return {"action": "screenshot"}
        
        # Navigation commands
        if any(word in user_input for word in ["back", "return"]):
            return {"action": "key", "keycode": "BACK"}
        
        if any(word in user_input for word in ["home", "launcher"]):
            return {"action": "key", "keycode": "HOME"}
        
        if "recent apps" in user_input or "task switcher" in user_input:
            return {"action": "recent_apps"}
        
        # Scroll and swipe commands
        if "scroll down" in user_input or "swipe up" in user_input:
            return {"action": "scroll", "direction": "down"}
        
        if "scroll up" in user_input or "swipe down" in user_input:
            return {"action": "scroll", "direction": "up"}
        
        if "scroll left" in user_input:
            return {"action": "scroll", "direction": "left"}
        
        if "scroll right" in user_input:
            return {"action": "scroll", "direction": "right"}
        
        # Gesture commands
        if "long press" in user_input or "hold" in user_input:
            return {"action": "long_press", "x": 540, "y": 960, "duration": 1000}
        
        if "double tap" in user_input or "double click" in user_input:
            return {"action": "double_tap", "x": 540, "y": 960}
        
        if "pinch" in user_input:
            return {"action": "pinch", "x": 540, "y": 960, "scale": 0.5}
        
        if "zoom" in user_input:
            return {"action": "zoom", "x": 540, "y": 960, "scale": 2.0}
        
        # Text input commands
        if user_input.startswith("type "):
            text = user_input[5:].strip()
            return {"action": "type", "text": text}
        
        if "paste" in user_input:
            return {"action": "paste"}
        
        if "copy" in user_input:
            return {"action": "copy"}
        
        if "clear text" in user_input:
            return {"action": "clear_text"}
        
        # System settings
        if "wifi on" in user_input or "enable wifi" in user_input:
            return {"action": "wifi", "enabled": True}
        
        if "wifi off" in user_input or "disable wifi" in user_input:
            return {"action": "wifi", "enabled": False}
        
        if "bluetooth on" in user_input or "enable bluetooth" in user_input:
            return {"action": "bluetooth", "enabled": True}
        
        if "bluetooth off" in user_input or "disable bluetooth" in user_input:
            return {"action": "bluetooth", "enabled": False}
        
        if "airplane mode on" in user_input:
            return {"action": "airplane_mode", "enabled": True}
        
        if "airplane mode off" in user_input:
            return {"action": "airplane_mode", "enabled": False}
        
        if "flashlight on" in user_input or "turn on flashlight" in user_input:
            return {"action": "flashlight", "enabled": True}
        
        if "flashlight off" in user_input or "turn off flashlight" in user_input:
            return {"action": "flashlight", "enabled": False}
        
        if "dark mode on" in user_input or "enable dark mode" in user_input:
            return {"action": "dark_mode", "enabled": True}
        
        if "dark mode off" in user_input or "disable dark mode" in user_input:
            return {"action": "dark_mode", "enabled": False}
        
        # Volume and brightness
        if "volume up" in user_input:
            return {"action": "key", "keycode": "VOLUME_UP"}
        
        if "volume down" in user_input:
            return {"action": "key", "keycode": "VOLUME_DOWN"}
        
        if "brightness" in user_input:
            if "max" in user_input or "100" in user_input:
                return {"action": "brightness", "level": 255}
            elif "min" in user_input or "0" in user_input:
                return {"action": "brightness", "level": 0}
            else:
                return {"action": "brightness", "level": 128}
        
        # Screen orientation
        if "rotate" in user_input:
            if "landscape" in user_input:
                return {"action": "rotate", "orientation": "landscape"}
            elif "portrait" in user_input:
                return {"action": "rotate", "orientation": "portrait"}
        
        # Notifications
        if "notification" in user_input:
            if "expand" in user_input or "open" in user_input:
                return {"action": "notification_panel", "expand": True}
            elif "close" in user_input or "collapse" in user_input:
                return {"action": "notification_panel", "expand": False}
        
        if "quick settings" in user_input:
            return {"action": "quick_settings"}
        
        # Lock screen
        if "lock" in user_input and "screen" in user_input:
            return {"action": "lock_screen"}
        
        if "unlock" in user_input and "screen" in user_input:
            return {"action": "unlock_screen", "method": "swipe"}
        
        if "wake up" in user_input or "wake" in user_input:
            return {"action": "wake_up"}
        
        # Power actions
        if "reboot" in user_input or "restart" in user_input:
            return {"action": "reboot", "mode": "normal"}
        
        if "shutdown" in user_input or "power off" in user_input:
            return {"action": "shutdown"}
        
        # App management
        if "open" in user_input:
            if "camera" in user_input:
                return {"action": "app", "package": "com.android.camera"}
            elif "settings" in user_input:
                return {"action": "app", "package": "com.android.settings"}
            elif "browser" in user_input or "chrome" in user_input:
                return {"action": "app", "package": "com.android.chrome"}
            elif "gallery" in user_input or "photos" in user_input:
                return {"action": "app", "package": "com.google.android.apps.photos"}
            elif "calculator" in user_input:
                return {"action": "app", "package": "com.android.calculator2"}
            elif "contacts" in user_input:
                return {"action": "app", "package": "com.android.contacts"}
            elif "phone" in user_input or "dialer" in user_input:
                return {"action": "app", "package": "com.android.dialer"}
            elif "messages" in user_input or "sms" in user_input:
                return {"action": "app", "package": "com.android.mms"}
            elif "clock" in user_input or "alarm" in user_input:
                return {"action": "app", "package": "com.android.deskclock"}
            elif "calendar" in user_input:
                return {"action": "app", "package": "com.android.calendar"}
            elif "maps" in user_input:
                return {"action": "app", "package": "com.google.android.apps.maps"}
            elif "youtube" in user_input:
                return {"action": "app", "package": "com.google.android.youtube"}
            elif "play store" in user_input:
                return {"action": "app", "package": "com.android.vending"}
        
        # Device info
        if "device info" in user_input or "phone info" in user_input:
            return {"action": "get_device_info"}
        
        if "battery" in user_input and "info" in user_input:
            return {"action": "get_battery_info"}
        
        if "storage" in user_input and "info" in user_input:
            return {"action": "get_storage_info"}
        
        if "network" in user_input and "info" in user_input:
            return {"action": "get_network_info"}
        
        if "running apps" in user_input:
            return {"action": "get_running_apps"}
        
        if "installed apps" in user_input:
            return {"action": "get_installed_apps"}
        
        # Testing commands
        if "ui hierarchy" in user_input or "dump ui" in user_input:
            return {"action": "ui_hierarchy", "format": "xml"}
        
        if "monkey test" in user_input:
            return {"action": "monkey_test", "package": "com.android.launcher", "events": 100}
        
        # Wait command
        if user_input.startswith("wait "):
            try:
                seconds = float(user_input[5:].strip())
                return {"action": "wait", "seconds": seconds}
            except ValueError:
                return {"action": "wait", "seconds": 1.0}
        
        # Default tap in center
        if any(word in user_input for word in ["tap", "click", "touch"]):
            return {"action": "tap", "x": 540, "y": 960}
        
        return {"error": f"Could not parse command: {user_input}"}
    
    def get_model_info(self) -> Dict:
        """Get information about the Ollama model."""
        try:
            models = self.client.list()
            available_models = [model.model for model in models.models]
            
            return {
                "model_name": self.model_name,
                "backend": "ollama",
                "loaded": self.model_loaded,
                "available_models": available_models,
                "ollama_running": True
            }
        except Exception as e:
            return {
                "model_name": self.model_name,
                "backend": "ollama",
                "loaded": False,
                "available_models": [],
                "ollama_running": False,
                "error": str(e)
            } 