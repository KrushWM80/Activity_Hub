/**
 * Local Storage Manager
 * Handles IndexedDB for project data and localStorage for connections/settings
 */

const LocalStorageManager = {
    DB_NAME: 'ActivityHubProjects',
    DB_VERSION: 1,
    STORES: {
        PROJECTS: 'projects',
        UPLOADS: 'uploads',
        MAPPINGS: 'mappings'
    },
    db: null,

    /**
     * Initialize IndexedDB
     */
    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.DB_NAME, this.DB_VERSION);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // Projects store
                if (!db.objectStoreNames.contains(this.STORES.PROJECTS)) {
                    const projectStore = db.createObjectStore(this.STORES.PROJECTS, { keyPath: 'id', autoIncrement: true });
                    projectStore.createIndex('project_id', 'project_id', { unique: false });
                    projectStore.createIndex('upload_id', 'upload_id', { unique: false });
                    projectStore.createIndex('status', 'status', { unique: false });
                    projectStore.createIndex('source_type', 'source_type', { unique: false });
                }

                // Uploads store (tracks import history)
                if (!db.objectStoreNames.contains(this.STORES.UPLOADS)) {
                    const uploadStore = db.createObjectStore(this.STORES.UPLOADS, { keyPath: 'upload_id' });
                    uploadStore.createIndex('created_date', 'created_date', { unique: false });
                    uploadStore.createIndex('connection_id', 'connection_id', { unique: false });
                }

                // Mappings store (saved column mappings)
                if (!db.objectStoreNames.contains(this.STORES.MAPPINGS)) {
                    const mappingStore = db.createObjectStore(this.STORES.MAPPINGS, { keyPath: 'mapping_id' });
                    mappingStore.createIndex('source_name', 'source_name', { unique: false });
                }
            };
        });
    },

    /**
     * Seed default connections if they don't exist
     */
    seedDefaultConnections() {
        const connections = this.getConnections();
        
        // Check if Intake Hub connection exists
        const hasIntakeHub = connections.some(c => c.connection_id === 'conn-intake-hub-bq');
        
        if (!hasIntakeHub) {
            const intakeHubConnection = {
                connection_id: 'conn-intake-hub-bq',
                name: 'Intake Hub Data',
                type: 'bigquery',
                config: {
                    projectId: 'wmt-assetprotection-prod',
                    dataset: 'Store_Support_Dev',
                    table: 'IH_Intake_Data',
                    description: 'Intake Hub project data from BigQuery'
                },
                created_date: '2025-01-15T00:00:00.000Z',
                last_used: null
            };
            
            connections.push(intakeHubConnection);
            localStorage.setItem('activityhub_connections', JSON.stringify(connections));
            console.log('Seeded Intake Hub default connection');
        }
    },

    /**
     * Generate unique ID
     */
    generateId(prefix = '') {
        const timestamp = Date.now().toString(36);
        const random = Math.random().toString(36).substr(2, 9);
        return `${prefix}${timestamp}-${random}`;
    },

    // ==========================================
    // Projects CRUD
    // ==========================================

    /**
     * Add projects in batch
     */
    async addProjects(projects, uploadId) {
        if (!this.db) await this.init();
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.PROJECTS], 'readwrite');
            const store = transaction.objectStore(this.STORES.PROJECTS);
            let addedCount = 0;

            projects.forEach(project => {
                const record = {
                    ...project,
                    upload_id: uploadId,
                    _created: new Date().toISOString(),
                    _updated: new Date().toISOString()
                };
                const request = store.add(record);
                request.onsuccess = () => addedCount++;
            });

            transaction.oncomplete = () => resolve(addedCount);
            transaction.onerror = () => reject(transaction.error);
        });
    },

    /**
     * Get all projects
     */
    async getAllProjects() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.PROJECTS], 'readonly');
            const store = transaction.objectStore(this.STORES.PROJECTS);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get projects by upload ID
     */
    async getProjectsByUpload(uploadId) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.PROJECTS], 'readonly');
            const store = transaction.objectStore(this.STORES.PROJECTS);
            const index = store.index('upload_id');
            const request = index.getAll(uploadId);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Update a project
     */
    async updateProject(id, updates) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.PROJECTS], 'readwrite');
            const store = transaction.objectStore(this.STORES.PROJECTS);
            const getRequest = store.get(id);

            getRequest.onsuccess = () => {
                const record = getRequest.result;
                if (record) {
                    const updated = {
                        ...record,
                        ...updates,
                        _updated: new Date().toISOString()
                    };
                    store.put(updated);
                    resolve(updated);
                } else {
                    reject(new Error('Project not found'));
                }
            };
            getRequest.onerror = () => reject(getRequest.error);
        });
    },

    /**
     * Delete projects by upload ID
     */
    async deleteProjectsByUpload(uploadId) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.PROJECTS], 'readwrite');
            const store = transaction.objectStore(this.STORES.PROJECTS);
            const index = store.index('upload_id');
            const request = index.openCursor(IDBKeyRange.only(uploadId));
            let deletedCount = 0;

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    store.delete(cursor.primaryKey);
                    deletedCount++;
                    cursor.continue();
                }
            };

            transaction.oncomplete = () => resolve(deletedCount);
            transaction.onerror = () => reject(transaction.error);
        });
    },

    // ==========================================
    // Uploads History
    // ==========================================

    /**
     * Create upload record
     */
    async createUpload(uploadData) {
        if (!this.db) await this.init();

        const upload = {
            upload_id: this.generateId('upload-'),
            created_date: new Date().toISOString(),
            ...uploadData
        };

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.UPLOADS], 'readwrite');
            const store = transaction.objectStore(this.STORES.UPLOADS);
            const request = store.add(upload);

            request.onsuccess = () => resolve(upload);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get all uploads
     */
    async getAllUploads() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.UPLOADS], 'readonly');
            const store = transaction.objectStore(this.STORES.UPLOADS);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Update upload record
     */
    async updateUpload(uploadId, updates) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.UPLOADS], 'readwrite');
            const store = transaction.objectStore(this.STORES.UPLOADS);
            const getRequest = store.get(uploadId);

            getRequest.onsuccess = () => {
                const record = getRequest.result;
                if (record) {
                    const updated = { ...record, ...updates };
                    store.put(updated);
                    resolve(updated);
                } else {
                    reject(new Error('Upload not found'));
                }
            };
            getRequest.onerror = () => reject(getRequest.error);
        });
    },

    // ==========================================
    // Saved Mappings
    // ==========================================

    /**
     * Save a column mapping
     */
    async saveMapping(mappingData) {
        if (!this.db) await this.init();

        const mapping = {
            mapping_id: this.generateId('mapping-'),
            created_date: new Date().toISOString(),
            ...mappingData
        };

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.MAPPINGS], 'readwrite');
            const store = transaction.objectStore(this.STORES.MAPPINGS);
            const request = store.put(mapping);

            request.onsuccess = () => resolve(mapping);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get all mappings
     */
    async getAllMappings() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.STORES.MAPPINGS], 'readonly');
            const store = transaction.objectStore(this.STORES.MAPPINGS);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    // ==========================================
    // Connections (localStorage)
    // ==========================================

    /**
     * Save a connection configuration
     */
    saveConnection(connection) {
        const connections = this.getConnections();
        const existing = connections.findIndex(c => c.connection_id === connection.connection_id);
        
        if (existing >= 0) {
            connections[existing] = { ...connections[existing], ...connection };
        } else {
            connection.connection_id = connection.connection_id || this.generateId('conn-');
            connection.created_date = connection.created_date || new Date().toISOString();
            connections.push(connection);
        }

        localStorage.setItem('activityhub_connections', JSON.stringify(connections));
        return connection;
    },

    /**
     * Get all connections
     */
    getConnections() {
        const data = localStorage.getItem('activityhub_connections');
        return data ? JSON.parse(data) : [];
    },

    /**
     * Get connection by ID
     */
    getConnection(connectionId) {
        const connections = this.getConnections();
        return connections.find(c => c.connection_id === connectionId);
    },

    /**
     * Delete a connection
     */
    deleteConnection(connectionId) {
        const connections = this.getConnections();
        const filtered = connections.filter(c => c.connection_id !== connectionId);
        localStorage.setItem('activityhub_connections', JSON.stringify(filtered));
    },

    // ==========================================
    // Settings
    // ==========================================

    /**
     * Get setting
     */
    getSetting(key, defaultValue = null) {
        const data = localStorage.getItem(`activityhub_setting_${key}`);
        return data ? JSON.parse(data) : defaultValue;
    },

    /**
     * Set setting
     */
    setSetting(key, value) {
        localStorage.setItem(`activityhub_setting_${key}`, JSON.stringify(value));
    },

    /**
     * Check if sync warning should be shown
     */
    shouldShowSyncWarning() {
        return !this.getSetting('hide_sync_warning', false);
    },

    /**
     * Hide sync warning
     */
    hideSyncWarning() {
        this.setSetting('hide_sync_warning', true);
    }
};

// Initialize on load
LocalStorageManager.init().then(() => {
    LocalStorageManager.seedDefaultConnections();
}).catch(console.error);
