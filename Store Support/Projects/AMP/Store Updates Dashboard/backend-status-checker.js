/**
 * Backend Connection Status Checker
 * Monitors connection to Python backend server and displays status
 */

const BACKEND_URL = 'http://localhost:5000';
let backendConnected = false;

/**
 * Check backend connection status
 */
async function checkBackendStatus() {
    try {
        const response = await fetch(`${BACKEND_URL}/health`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            const health = await response.json();
            
            if (health.bigquery_connected) {
                updateStatus('✅ Connected to BigQuery', 'success');
                backendConnected = true;
                console.log('✅ Backend connected to BigQuery:', health.project);
            } else {
                updateStatus('⚠️ Backend running but BigQuery not connected', 'warning');
                console.warn('Backend is running but BigQuery authentication may be missing');
            }
        } else {
            updateStatus('❌ Backend error (HTTP ' + response.status + ')', 'error');
        }
    } catch (error) {
        updateStatus('❌ Backend not running (start with: python amp_backend_server.py)', 'error');
        console.error('Backend connection failed:', error.message);
        console.log('Start the backend with: python amp_backend_server.py');
    }
}

/**
 * Update status display in UI
 */
function updateStatus(message, status = 'info') {
    const statusElement = document.getElementById('auth-status');
    const indicator = document.getElementById('status-indicator');
    
    if (!statusElement || !indicator) return;
    
    statusElement.textContent = message;
    
    // Update indicator color
    const colors = {
        success: '#38A169',  // Green
        warning: '#D69E2E',  // Orange
        error: '#E53E3E',    // Red
        info: '#3182CE'      // Blue
    };
    
    indicator.style.background = colors[status] || colors.info;
    
    // Stop pulse animation if connected
    if (status === 'success') {
        indicator.style.animation = 'none';
        indicator.style.opacity = '1';
    }
    
    console.log(`[${status.toUpperCase()}] ${message}`);
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Checking backend connection...');
    console.log('Backend URL:', BACKEND_URL);
    
    // Check immediately
    checkBackendStatus();
    
    // Check every 30 seconds
    setInterval(checkBackendStatus, 30000);
});

// Export for use in other scripts
window.BackendStatus = {
    checkStatus: checkBackendStatus,
    isConnected: () => backendConnected,
    updateStatus: updateStatus
};
