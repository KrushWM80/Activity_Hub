/**
 * Data Connections Manager
 * Handles connections to external data sources
 */

const DataConnections = {
    currentConnection: null,

    /**
     * Test BigQuery connection
     */
    async testBigQueryConnection(config) {
        // In production, this would call a backend API
        // For demo, we simulate the connection test
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (config.projectId && config.dataset && config.table) {
                    resolve({
                        success: true,
                        message: 'Connection successful',
                        metadata: {
                            projectId: config.projectId,
                            dataset: config.dataset,
                            table: config.table,
                            rowCount: '~10,000 rows',
                            lastModified: new Date().toISOString()
                        }
                    });
                } else {
                    reject(new Error('Missing required fields'));
                }
            }, 1500);
        });
    },

    /**
     * Fetch sample data from BigQuery
     */
    async fetchBigQuerySample(config, limit = 100) {
        // In production, this would fetch actual data from BigQuery
        // For demo purposes, we'll generate sample data
        return new Promise((resolve) => {
            setTimeout(() => {
                // Sample columns that might come from BigQuery
                const sampleColumns = [
                    'IH_Project_ID', 'IH_Title', 'IH_Status', 'IH_Store_Number',
                    'IH_Market', 'IH_Region', 'IH_Start_Date', 'IH_End_Date',
                    'IH_Owner', 'IH_Department', 'IH_Budget', 'IH_Priority'
                ];

                const records = [];
                for (let i = 0; i < Math.min(limit, 10); i++) {
                    const record = {};
                    sampleColumns.forEach(col => {
                        record[col] = `Sample ${col.replace('IH_', '')} ${i + 1}`;
                    });
                    records.push(record);
                }

                resolve({
                    columns: sampleColumns,
                    records,
                    totalRows: limit
                });
            }, 1000);
        });
    },

    /**
     * Test API connection
     */
    async testApiConnection(config) {
        // For demo, simulate API test
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (config.endpoint) {
                    resolve({
                        success: true,
                        message: 'API endpoint reachable',
                        metadata: {
                            endpoint: config.endpoint,
                            method: config.method || 'GET',
                            authType: config.authType || 'None'
                        }
                    });
                } else {
                    reject(new Error('Endpoint URL is required'));
                }
            }, 1000);
        });
    },

    /**
     * Fetch data from API
     */
    async fetchApiData(config) {
        // In production, this would make actual API calls
        return new Promise((resolve) => {
            setTimeout(() => {
                // Sample API response structure
                const sampleColumns = [
                    'id', 'name', 'status', 'location', 'startDate',
                    'endDate', 'owner', 'category', 'priority'
                ];

                const records = [];
                for (let i = 0; i < 10; i++) {
                    const record = {};
                    sampleColumns.forEach(col => {
                        record[col] = `API ${col} ${i + 1}`;
                    });
                    records.push(record);
                }

                resolve({
                    columns: sampleColumns,
                    records,
                    totalRows: 10
                });
            }, 1200);
        });
    },

    /**
     * Save connection configuration
     */
    async saveConnection(name, type, config) {
        const connection = {
            id: `conn_${Date.now()}`,
            name,
            type,
            config,
            createdAt: new Date().toISOString(),
            lastUsed: null
        };

        // Use LocalStorage module if available
        if (typeof LocalStorage !== 'undefined') {
            await LocalStorage.saveConnection(connection);
        } else {
            // Fallback to direct localStorage
            const connections = this.getSavedConnections();
            connections.push(connection);
            localStorage.setItem('activity_hub_connections', JSON.stringify(connections));
        }

        return connection;
    },

    /**
     * Get all saved connections
     */
    getSavedConnections() {
        if (typeof LocalStorageManager !== 'undefined') {
            return LocalStorageManager.getConnections();
        }
        const saved = localStorage.getItem('activityhub_connections');
        return saved ? JSON.parse(saved) : [];
    },

    /**
     * Delete a saved connection
     */
    async deleteConnection(connectionId) {
        if (typeof LocalStorage !== 'undefined') {
            return await LocalStorage.deleteConnection(connectionId);
        }
        const connections = this.getSavedConnections().filter(c => c.id !== connectionId);
        localStorage.setItem('activity_hub_connections', JSON.stringify(connections));
    },

    /**
     * Render saved connections list
     */
    renderSavedConnections() {
        const container = document.getElementById('saved-connections-list');
        if (!container) return;

        const connections = this.getSavedConnections();

        if (connections.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No saved connections found</p>
                    <p class="hint">Connections are saved after completing an import</p>
                </div>
            `;
            return;
        }

        container.innerHTML = connections.map(conn => `
            <div class="saved-connection-card" data-id="${conn.connection_id || conn.id}">
                <div class="connection-icon">${this.getTypeIcon(conn.type)}</div>
                <div class="connection-info">
                    <h4>${conn.name}</h4>
                    <p>${conn.type === 'bigquery' ? `${conn.config.projectId}.${conn.config.dataset}.${conn.config.table}` : conn.config.endpoint || conn.type}</p>
                    <small>Last used: ${conn.last_used ? new Date(conn.last_used).toLocaleDateString() : 'Never'}</small>
                </div>
                <button class="btn btn-primary btn-small use-connection-btn" data-id="${conn.connection_id || conn.id}">
                    Use Connection
                </button>
            </div>
        `).join('');

        // Bind use buttons
        container.querySelectorAll('.use-connection-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.useConnection(btn.dataset.id);
            });
        });
    },

    /**
     * Get icon for connection type
     */
    getTypeIcon(type) {
        const icons = {
            'bigquery': '🗄️',
            'api': '🔌',
            'file': '📄'
        };
        return icons[type] || '🔗';
    },

    /**
     * Use a saved connection
     */
    async useConnection(connectionId) {
        const connections = this.getSavedConnections();
        const connection = connections.find(c => (c.connection_id || c.id) === connectionId);

        if (!connection) {
            alert('Connection not found');
            return;
        }

        this.currentConnection = connection;

        // Update last used
        connection.last_used = new Date().toISOString();
        localStorage.setItem('activityhub_connections', JSON.stringify(connections));

        // Navigate to appropriate step based on connection type
        if (typeof UploadWizard !== 'undefined') {
            UploadWizard.setConnection(connection);
            // For BigQuery, need to fetch sample data first
            if (connection.type === 'bigquery') {
                await this.fetchBigQueryDataForWizard(connection);
            }
            UploadWizard.goToStep(3); // Go to mapping step
        }
    },

    /**
     * Fetch BigQuery sample data for wizard
     */
    async fetchBigQueryDataForWizard(connection) {
        try {
            const result = await this.fetchBigQuerySample(connection.config);
            UploadWizard.sourceData = result;
            UploadWizard.sourceType = 'bigquery';
        } catch (error) {
            console.error('Failed to fetch BigQuery data:', error);
            alert('Failed to fetch data from BigQuery');
        }
    },

    /**
     * Setup API sync configuration
     */
    setupApiSync(config) {
        const syncConfig = {
            enabled: true,
            direction: config.direction || 'bidirectional', // 'pull', 'push', 'bidirectional'
            frequency: config.frequency || 'manual', // 'realtime', 'hourly', 'daily', 'manual'
            endpoint: {
                pull: config.pullEndpoint || config.endpoint,
                push: config.pushEndpoint || config.endpoint
            },
            authentication: config.authentication,
            lastSync: null,
            conflictResolution: config.conflictResolution || 'source_wins' // 'source_wins', 'activity_hub_wins', 'manual'
        };

        return syncConfig;
    },

    /**
     * Render BigQuery configuration form
     */
    renderBigQueryForm() {
        const container = document.getElementById('bigquery-config');
        if (!container) return;

        container.innerHTML = `
            <div class="form-group">
                <label>GCP Project ID</label>
                <input type="text" id="bq-project-id" placeholder="your-project-id" class="form-control">
            </div>
            <div class="form-group">
                <label>Dataset</label>
                <input type="text" id="bq-dataset" placeholder="your_dataset" class="form-control">
            </div>
            <div class="form-group">
                <label>Table</label>
                <input type="text" id="bq-table" placeholder="your_table" class="form-control">
            </div>
            <div class="form-group">
                <label>Service Account Key (JSON)</label>
                <textarea id="bq-service-key" placeholder="Paste service account JSON key" class="form-control" rows="4"></textarea>
            </div>
            <button class="btn btn-primary" id="test-bq-connection">Test Connection</button>
            <div id="bq-connection-status" class="connection-status"></div>
        `;

        // Bind test button
        document.getElementById('test-bq-connection').addEventListener('click', async () => {
            const config = this.getBigQueryConfig();
            const statusEl = document.getElementById('bq-connection-status');

            statusEl.innerHTML = '<span class="loading">Testing connection...</span>';

            try {
                const result = await this.testBigQueryConnection(config);
                statusEl.innerHTML = `<span class="success">✅ ${result.message}</span>`;
                this.currentConnection = { type: 'bigquery', config };
            } catch (error) {
                statusEl.innerHTML = `<span class="error">❌ ${error.message}</span>`;
            }
        });
    },

    /**
     * Get BigQuery configuration from form
     */
    getBigQueryConfig() {
        return {
            projectId: document.getElementById('bq-project-id')?.value || '',
            dataset: document.getElementById('bq-dataset')?.value || '',
            table: document.getElementById('bq-table')?.value || '',
            serviceKey: document.getElementById('bq-service-key')?.value || ''
        };
    },

    /**
     * Render API configuration form
     */
    renderApiForm() {
        const container = document.getElementById('api-config');
        if (!container) return;

        container.innerHTML = `
            <div class="form-group">
                <label>API Endpoint URL</label>
                <input type="url" id="api-endpoint" placeholder="https://api.example.com/data" class="form-control">
            </div>
            <div class="form-group">
                <label>HTTP Method</label>
                <select id="api-method" class="form-control">
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                </select>
            </div>
            <div class="form-group">
                <label>Authentication Type</label>
                <select id="api-auth-type" class="form-control">
                    <option value="none">None</option>
                    <option value="api_key">API Key</option>
                    <option value="bearer">Bearer Token</option>
                    <option value="basic">Basic Auth</option>
                </select>
            </div>
            <div id="api-auth-fields"></div>
            <button class="btn btn-primary" id="test-api-connection">Test Connection</button>
            <div id="api-connection-status" class="connection-status"></div>
        `;

        // Handle auth type change
        document.getElementById('api-auth-type').addEventListener('change', (e) => {
            this.renderApiAuthFields(e.target.value);
        });

        // Bind test button
        document.getElementById('test-api-connection').addEventListener('click', async () => {
            const config = this.getApiConfig();
            const statusEl = document.getElementById('api-connection-status');

            statusEl.innerHTML = '<span class="loading">Testing connection...</span>';

            try {
                const result = await this.testApiConnection(config);
                statusEl.innerHTML = `<span class="success">✅ ${result.message}</span>`;
                this.currentConnection = { type: 'api', config };
            } catch (error) {
                statusEl.innerHTML = `<span class="error">❌ ${error.message}</span>`;
            }
        });
    },

    /**
     * Render API authentication fields based on type
     */
    renderApiAuthFields(authType) {
        const container = document.getElementById('api-auth-fields');
        if (!container) return;

        switch (authType) {
            case 'api_key':
                container.innerHTML = `
                    <div class="form-group">
                        <label>API Key Header Name</label>
                        <input type="text" id="api-key-header" value="X-API-Key" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>API Key Value</label>
                        <input type="password" id="api-key-value" placeholder="Your API key" class="form-control">
                    </div>
                `;
                break;

            case 'bearer':
                container.innerHTML = `
                    <div class="form-group">
                        <label>Bearer Token</label>
                        <input type="password" id="api-bearer-token" placeholder="Your bearer token" class="form-control">
                    </div>
                `;
                break;

            case 'basic':
                container.innerHTML = `
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" id="api-basic-username" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="api-basic-password" class="form-control">
                    </div>
                `;
                break;

            default:
                container.innerHTML = '';
        }
    },

    /**
     * Get API configuration from form
     */
    getApiConfig() {
        const authType = document.getElementById('api-auth-type')?.value || 'none';
        const config = {
            endpoint: document.getElementById('api-endpoint')?.value || '',
            method: document.getElementById('api-method')?.value || 'GET',
            authType
        };

        // Add auth-specific config
        switch (authType) {
            case 'api_key':
                config.apiKeyHeader = document.getElementById('api-key-header')?.value;
                config.apiKeyValue = document.getElementById('api-key-value')?.value;
                break;
            case 'bearer':
                config.bearerToken = document.getElementById('api-bearer-token')?.value;
                break;
            case 'basic':
                config.basicUsername = document.getElementById('api-basic-username')?.value;
                config.basicPassword = document.getElementById('api-basic-password')?.value;
                break;
        }

        return config;
    }
};
