// Global state
let isReady = false;
let currentScreenshot = null;

// DOM elements
const commandInput = document.getElementById('command-input');
const sendBtn = document.getElementById('send-btn');
const quickButtons = document.getElementById('quick-buttons');
const screenshotContainer = document.getElementById('screenshot-container');
const logContainer = document.getElementById('log-container');
const deviceInfo = document.getElementById('device-info');
const loadingOverlay = document.getElementById('loading-overlay');
const modelStatus = document.getElementById('model-status');
const androidStatus = document.getElementById('android-status');
const modelText = document.getElementById('model-text');
const androidText = document.getElementById('android-text');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadQuickCommands();
    
    // Start status polling
    setInterval(updateStatus, 3000);
    updateStatus(); // Initial status check
});

function initializeApp() {
    console.log('Initializing Gemma3 Android Controller...');
    loadDeviceInfo();
}

function setupEventListeners() {
    // Send command on button click
    sendBtn.addEventListener('click', sendCommand);
    
    // Send command on Enter key
    commandInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendCommand();
        }
    });
    
    // Auto-resize input
    commandInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
}

async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();
        
        // Update model status
        updateStatusIndicator(modelStatus, modelText, status.model);
        
        // Update Android status
        updateStatusIndicator(androidStatus, androidText, status.android);
        
        // Update global ready state
        isReady = status.ready;
        
        // Enable/disable send button
        sendBtn.disabled = !isReady;
        
    } catch (error) {
        console.error('Error updating status:', error);
        updateStatusIndicator(modelStatus, modelText, {loaded: false, loading: false, error: 'Connection failed'});
        updateStatusIndicator(androidStatus, androidText, {success: false, error: 'Connection failed'});
    }
}

function updateStatusIndicator(statusElement, textElement, statusData) {
    // Remove existing status classes
    statusElement.classList.remove('connected', 'disconnected', 'loading');
    
    if (statusData.loading) {
        statusElement.classList.add('loading');
        textElement.textContent = 'Loading...';
    } else if (statusData.loaded || statusData.success) {
        statusElement.classList.add('connected');
        textElement.textContent = statusData.loaded ? 'Ready' : 'Connected';
    } else {
        statusElement.classList.add('disconnected');
        textElement.textContent = statusData.error || 'Disconnected';
    }
}

async function loadQuickCommands() {
    try {
        const response = await fetch('/api/quick_commands');
        const commands = await response.json();
        
        quickButtons.innerHTML = '';
        commands.forEach(cmd => {
            const button = document.createElement('button');
            button.className = 'quick-btn';
            button.textContent = cmd.name;
            button.onclick = () => executeQuickCommand(cmd.command);
            quickButtons.appendChild(button);
        });
    } catch (error) {
        console.error('Error loading quick commands:', error);
    }
}

async function loadDeviceInfo() {
    try {
        const response = await fetch('/api/device_info');
        const info = await response.json();
        
        if (info.error) {
            deviceInfo.innerHTML = `
                <div class="info-placeholder">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>${info.error}</p>
                </div>
            `;
            return;
        }
        
        deviceInfo.innerHTML = `
            <div class="info-item">
                <div class="info-label">Device ID</div>
                <div class="info-value">${info.device_id || 'Unknown'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Model</div>
                <div class="info-value">${info.model || 'Unknown'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Android Version</div>
                <div class="info-value">${info.android_version || 'Unknown'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">API Level</div>
                <div class="info-value">${info.api_level || 'Unknown'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Screen Size</div>
                <div class="info-value">${info.screen_size ? `${info.screen_size[0]}x${info.screen_size[1]}` : 'Unknown'}</div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading device info:', error);
        deviceInfo.innerHTML = `
            <div class="info-placeholder">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error loading device information</p>
            </div>
        `;
    }
}

async function sendCommand() {
    const command = commandInput.value.trim();
    if (!command) return;
    
    if (!isReady) {
        addLogEntry('System not ready', 'Please wait for model and device to be ready', 'error');
        return;
    }
    
    // Show loading
    showLoading(true);
    sendBtn.disabled = true;
    
    try {
        const response = await fetch('/api/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            addLogEntry(command, result.result.message || 'Command executed successfully', 'success');
            
            // If it was a screenshot command, update the screenshot
            if (result.parsed_command.action === 'screenshot' && result.result.screenshot) {
                updateScreenshot(result.result.screenshot);
            }
        } else {
            addLogEntry(command, result.error || 'Command failed', 'error');
        }
        
        // Clear input
        commandInput.value = '';
        
    } catch (error) {
        console.error('Error sending command:', error);
        addLogEntry(command, 'Network error: ' + error.message, 'error');
    } finally {
        showLoading(false);
        sendBtn.disabled = !isReady;
    }
}

async function executeQuickCommand(command) {
    commandInput.value = command;
    await sendCommand();
}

async function takeScreenshot() {
    showLoading(true);
    
    try {
        const response = await fetch('/api/screenshot');
        const result = await response.json();
        
        if (result.success && result.screenshot) {
            updateScreenshot(result.screenshot);
            addLogEntry('Screenshot', 'Screenshot captured successfully', 'success');
        } else {
            addLogEntry('Screenshot', result.error || 'Screenshot failed', 'error');
        }
    } catch (error) {
        console.error('Error taking screenshot:', error);
        addLogEntry('Screenshot', 'Network error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function updateScreenshot(base64Image) {
    currentScreenshot = base64Image;
    screenshotContainer.innerHTML = `
        <img src="data:image/png;base64,${base64Image}" 
             alt="Device Screenshot" 
             class="screenshot-image"
             onclick="openScreenshotModal()" />
    `;
    screenshotContainer.classList.add('has-image');
}

function openScreenshotModal() {
    if (!currentScreenshot) return;
    
    // Create modal
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
        cursor: pointer;
    `;
    
    const img = document.createElement('img');
    img.src = `data:image/png;base64,${currentScreenshot}`;
    img.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        border-radius: 10px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    `;
    
    modal.appendChild(img);
    modal.onclick = () => document.body.removeChild(modal);
    
    document.body.appendChild(modal);
}

function addLogEntry(command, result, type = 'success') {
    // Remove placeholder if it exists
    const placeholder = logContainer.querySelector('.log-placeholder');
    if (placeholder) {
        placeholder.remove();
    }
    
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    
    const timestamp = new Date().toLocaleTimeString();
    
    entry.innerHTML = `
        <div class="log-timestamp">${timestamp}</div>
        <div class="log-command">${escapeHtml(command)}</div>
        <div class="log-result">${escapeHtml(result)}</div>
    `;
    
    logContainer.insertBefore(entry, logContainer.firstChild);
    
    // Limit log entries to 50
    const entries = logContainer.querySelectorAll('.log-entry');
    if (entries.length > 50) {
        entries[entries.length - 1].remove();
    }
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('show');
    } else {
        loadingOverlay.classList.remove('show');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Utility functions for debugging
window.debugFunctions = {
    getStatus: () => fetch('/api/status').then(r => r.json()),
    getDeviceInfo: () => fetch('/api/device_info').then(r => r.json()),
    takeScreenshot: () => fetch('/api/screenshot').then(r => r.json()),
    sendCommand: (cmd) => fetch('/api/command', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({command: cmd})
    }).then(r => r.json())
};

console.log('Gemma3 Android Controller loaded. Debug functions available in window.debugFunctions'); 