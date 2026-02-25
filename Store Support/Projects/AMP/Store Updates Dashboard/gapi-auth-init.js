/**
 * Google API Authentication Initialization
 * Handles OAuth2 sign-in for BigQuery access in AMP Dashboard
 */

// Configuration - TODO: Replace with your Google OAuth2 client ID
const GOOGLE_CLIENT_ID = '<YOUR_GOOGLE_CLIENT_ID>'; // Get from Google Cloud Console
const GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/bigquery',
    'https://www.googleapis.com/auth/cloud-platform'
];

/**
 * Initialize Google API client and set up authentication flow
 */
function initializeGoogleAuth() {
    console.log('Initializing Google Authentication...');
    
    if (typeof gapi === 'undefined') {
        console.error('Google API client library not loaded');
        updateAuthStatus('Error: Google API not loaded', 'error');
        return;
    }

    // Load auth2 library
    gapi.load('auth2', () => {
        try {
            const auth2 = gapi.auth2.init({
                client_id: GOOGLE_CLIENT_ID,
                scope: GOOGLE_SCOPES.join(' ')
            });

            // Set up sign-in button click handler
            const signInBtn = document.getElementById('google-signin-btn');
            if (signInBtn) {
                signInBtn.addEventListener('click', () => {
                    signInWithGoogle(auth2);
                });
            }

            // Check if already signed in
            if (auth2.isSignedIn.get()) {
                onSignInSuccess(auth2.currentUser.get());
            } else {
                updateAuthStatus('Not signed in', 'warning');
            }

            // Listen for sign-in state changes
            auth2.isSignedIn.listen((isSignedIn) => {
                if (isSignedIn) {
                    onSignInSuccess(auth2.currentUser.get());
                } else {
                    updateAuthStatus('Not signed in', 'warning');
                }
            });

        } catch (error) {
            console.error('Failed to initialize auth2:', error);
            updateAuthStatus('Failed to initialize authentication', 'error');
        }
    });
}

/**
 * Handle sign-in button click
 */
function signInWithGoogle(auth2) {
    console.log('Initiating Google sign-in...');
    
    auth2.signIn().then(
        (user) => {
            onSignInSuccess(user);
        },
        (error) => {
            console.error('Sign-in failed:', error);
            updateAuthStatus('Sign-in failed: ' + error.error, 'error');
        }
    );
}

/**
 * Callback when sign-in succeeds
 */
function onSignInSuccess(user) {
    const profile = user.getBasicProfile();
    const authResponse = user.getAuthResponse(true);
    
    console.log('✅ Successfully signed in as:', profile.getName());
    console.log('Email:', profile.getEmail());
    
    // Update UI
    const signInBtn = document.getElementById('google-signin-btn');
    if (signInBtn) {
        signInBtn.textContent = `Signed in as ${profile.getGivenName()}`;
        signInBtn.disabled = true;
        signInBtn.style.background = '#38A169'; // Green for success
    }
    
    updateAuthStatus(`✅ Authenticated as ${profile.getName()}`, 'success');
    
    // Store token globally for dashboard to use
    window.ampAuthToken = authResponse.id_token || authResponse.access_token;
    window.ampAuthTokenExpiry = new Date(authResponse.expires_at);
    window.ampAuthUser = {
        name: profile.getName(),
        email: profile.getEmail(),
        picture: profile.getImageUrl()
    };
    
    console.log('Token valid until:', window.ampAuthTokenExpiry);
    
    // Refresh dashboard data after auth
    setTimeout(() => {
        if (typeof dataConnector !== 'undefined') {
            console.log('Refreshing dashboard with live BigQuery data...');
            // Trigger data refresh in dashboard
            if (window.location.hash.includes('#')) {
                // Trigger filter/load event if dashboard is loaded
                const event = new CustomEvent('authenticationSuccess');
                document.dispatchEvent(event);
            }
        }
    }, 500);
}

/**
 * Update authentication status display
 */
function updateAuthStatus(message, status = 'info') {
    const statusElement = document.getElementById('auth-status');
    if (!statusElement) return;
    
    statusElement.textContent = message;
    statusElement.style.color = getStatusColor(status);
    
    console.log(`[${status.toUpperCase()}] ${message}`);
}

/**
 * Get color for status indicator
 */
function getStatusColor(status) {
    const colors = {
        success: '#38A169',  // Green
        warning: '#D69E2E',  // Orange
        error: '#E53E3E',    // Red
        info: '#3182CE'      // Blue
    };
    return colors[status] || colors.info;
}

/**
 * Sign out the user
 */
function signOutUser() {
    if (typeof gapi !== 'undefined' && gapi.auth2) {
        const auth2 = gapi.auth2.getAuthInstance();
        if (auth2) {
            auth2.signOut().then(() => {
                console.log('Signed out successfully');
                updateAuthStatus('Signed out', 'warning');
                
                // Reset UI
                const signInBtn = document.getElementById('google-signin-btn');
                if (signInBtn) {
                    signInBtn.textContent = 'Sign in with Google';
                    signInBtn.disabled = false;
                    signInBtn.style.background = '#1E3A8A';
                }
                
                // Clear stored token
                window.ampAuthToken = null;
                window.ampAuthTokenExpiry = null;
                window.ampAuthUser = null;
            });
        }
    }
}

/**
 * Get current authentication status
 */
function getAuthStatus() {
    return {
        isAuthenticated: !!window.ampAuthToken,
        user: window.ampAuthUser || null,
        tokenExpiry: window.ampAuthTokenExpiry || null,
        hasValidToken: window.ampAuthToken && new Date() < (window.ampAuthTokenExpiry || new Date())
    };
}

/**
 * Initialize authentication on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing Google authentication...');
    
    // Check if client ID is configured
    if (GOOGLE_CLIENT_ID === '<YOUR_GOOGLE_CLIENT_ID>') {
        console.warn('⚠️ WARNING: Google OAuth2 client ID not configured!');
        updateAuthStatus('⚠️ Authentication not configured. See console for setup instructions.', 'error');
        console.log('\n📋 SETUP INSTRUCTIONS:');
        console.log('1. Go to: https://console.cloud.google.com/');
        console.log('2. Select project: wmt-assetprotection-prod');
        console.log('3. Create OAuth2 credentials (Web application)');
        console.log('4. Add authorized JavaScript origins:');
        console.log('   - http://localhost:8080');
        console.log('   - http://localhost:3000');
        console.log('5. Copy the Client ID and replace <YOUR_GOOGLE_CLIENT_ID> in gapi-auth-init.js');
        return;
    }
    
    initializeGoogleAuth();
});

// Export functions for external use
window.GoogleAuthModule = {
    initializeGoogleAuth,
    signInWithGoogle,
    signOutUser,
    getAuthStatus,
    updateAuthStatus
};
