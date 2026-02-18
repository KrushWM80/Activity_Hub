/**
 * BigQuery Authentication Module
 * Handles authentication for BigQuery data access
 */

class BigQueryAuth {
    constructor() {
        this.clientId = null; // Set your OAuth2 client ID here
        this.apiKey = null;   // Set your API key here
        this.scopes = ['https://www.googleapis.com/auth/bigquery.readonly'];
        this.isAuthenticated = false;
        this.authInstance = null;
    }

    /**
     * Initialize Google API and authentication
     */
    async initialize(clientId, apiKey) {
        this.clientId = clientId;
        this.apiKey = apiKey;

        return new Promise((resolve, reject) => {
            // Load Google API
            if (typeof gapi === 'undefined') {
                const script = document.createElement('script');
                script.src = 'https://apis.google.com/js/api.js';
                script.onload = async () => {
                    try {
                        await this.loadGoogleAuth();
                        resolve();
                    } catch (error) {
                        reject(error);
                    }
                };
                script.onerror = () => reject(new Error('Failed to load Google API'));
                document.head.appendChild(script);
            } else {
                this.loadGoogleAuth().then(resolve).catch(reject);
            }
        });
    }

    /**
     * Load and initialize Google Auth
     */
    async loadGoogleAuth() {
        return new Promise((resolve, reject) => {
            gapi.load('auth2', async () => {
                try {
                    await gapi.auth2.init({
                        client_id: this.clientId,
                        scope: this.scopes.join(' ')
                    });
                    
                    this.authInstance = gapi.auth2.getAuthInstance();
                    this.isAuthenticated = this.authInstance.isSignedIn.get();
                    
                    console.log('Google Auth initialized. Signed in:', this.isAuthenticated);
                    resolve();
                } catch (error) {
                    reject(error);
                }
            });
        });
    }

    /**
     * Sign in user
     */
    async signIn() {
        if (!this.authInstance) {
            throw new Error('Auth not initialized. Call initialize() first.');
        }

        try {
            if (!this.isAuthenticated) {
                await this.authInstance.signIn();
                this.isAuthenticated = true;
            }
            return this.getToken();
        } catch (error) {
            console.error('Sign in failed:', error);
            throw error;
        }
    }

    /**
     * Get current access token
     */
    async getToken() {
        if (!this.authInstance) {
            throw new Error('Auth not initialized');
        }

        if (!this.isAuthenticated) {
            await this.signIn();
        }

        const user = this.authInstance.currentUser.get();
        const authResponse = user.getAuthResponse();
        
        if (!authResponse.access_token) {
            throw new Error('No access token available');
        }

        return authResponse.access_token;
    }

    /**
     * Sign out user
     */
    async signOut() {
        if (this.authInstance) {
            await this.authInstance.signOut();
            this.isAuthenticated = false;
        }
    }

    /**
     * Check if user is signed in
     */
    isSignedIn() {
        return this.isAuthenticated && this.authInstance && this.authInstance.isSignedIn.get();
    }
}

// Make BigQueryAuth available globally
window.BigQueryAuth = new BigQueryAuth();

// Service Account Authentication (Alternative method)
class ServiceAccountAuth {
    constructor(serviceAccountKey) {
        this.serviceAccountKey = serviceAccountKey;
        this.token = null;
        this.tokenExpiry = null;
    }

    /**
     * Get token using service account (requires server-side proxy)
     */
    async getToken() {
        if (this.token && this.tokenExpiry && Date.now() < this.tokenExpiry) {
            return this.token;
        }

        // In a real implementation, this would call your backend service
        // that handles service account authentication
        const response = await fetch('/api/bigquery-token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                serviceAccount: this.serviceAccountKey
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get service account token');
        }

        const data = await response.json();
        this.token = data.access_token;
        this.tokenExpiry = Date.now() + (data.expires_in * 1000);
        
        return this.token;
    }
}

// Instructions for setup
console.log(`
BigQuery Authentication Setup Instructions:

1. OAuth2 Method (Recommended for development):
   - Go to Google Cloud Console
   - Enable BigQuery API
   - Create OAuth2 credentials
   - Add your domain to authorized origins
   - Initialize with: window.BigQueryAuth.initialize('YOUR_CLIENT_ID', 'YOUR_API_KEY')

2. Service Account Method (For production):
   - Create a service account in Google Cloud Console
   - Grant BigQuery Data Viewer permissions
   - Set up a backend service to handle authentication
   - Use ServiceAccountAuth class

3. Test authentication:
   - Call window.BigQueryAuth.signIn() to authenticate
   - Check window.BigQueryAuth.isSignedIn() for status
`);