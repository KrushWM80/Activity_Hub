// AMP Data Connection Module
// Handles connection to wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep

class AMPDataConnector {
    constructor() {
        this.dataSource = 'wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep';
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
        this.isConnected = false;
    }

    /**
     * Initialize connection to BigQuery data source
     */
    async initialize() {
        try {
            console.log(`Initializing connection to ${this.dataSource}`);
            console.log('Using backend server at http://localhost:5000');
            
            // Test backend connection
            const response = await fetch('http://localhost:5000/health');
            const health = await response.json();
            
            this.isConnected = health.bigquery_connected;
            
            if (this.isConnected) {
                console.log('✅ Successfully connected to AMP Backend Server');
                console.log('Backend is connected to BigQuery:', health.project);
            } else {
                console.warn('⚠️ Backend server is running but BigQuery is not connected');
                console.log('This may happen if gcloud credentials are not configured');
            }
            
            return true;
        } catch (error) {
            console.error('Failed to initialize data connection:', error);
            console.warn('Backend server may not be running. Start it with: python amp_backend_server.py');
            this.isConnected = false;
            // Don't throw - allow fallback to sample data
            return false;
        }
    }

    /**
     * Execute query against backend API instead of BigQuery directly
     */
    async executeQuery(query, filters = {}) {
        try {
            if (!this.isConnected) {
                await this.initialize();
            }

            console.log('Fetching data from backend server...');
            
            // Build query string with filters
            const queryParams = new URLSearchParams();
            
            if (filters.division) queryParams.append('division', filters.division);
            if (filters.region) queryParams.append('region', filters.region);
            if (filters.market) queryParams.append('market', filters.market);
            if (filters.facility) queryParams.append('facility', filters.facility);
            if (filters.week) queryParams.append('week', filters.week);
            if (filters.activityType) queryParams.append('activity_type', filters.activityType);
            if (filters.storeArea) queryParams.append('store_area', filters.storeArea);
            if (filters.keyword) queryParams.append('keyword', filters.keyword);
            
            const url = `http://localhost:5000/api/amp-data?${queryParams.toString()}`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`Backend error: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error || 'Unknown backend error');
            }
            
            console.log(`✅ Successfully retrieved ${result.count} records from backend`);
            return result.data;
            
        } catch (error) {
            console.error('Real data query failed:', error);
            console.warn('Falling back to sample data. Error:', error.message);
            
            // Show user-friendly message about using sample data
            if (typeof document !== 'undefined') {
                const authIndicator = document.getElementById('authIndicator');
                if (authIndicator) {
                    authIndicator.textContent = '📊 Using Sample Data (Backend not available)';
                    authIndicator.className = 'auth-indicator disconnected';
                }
            }
            
            // Fallback to sample data if real query fails
            return this.generateSampleData();
        }
    }

    /**
     * Transform backend API response to expected format
     */
    transformBigQueryResults(backendData) {
        if (!Array.isArray(backendData)) {
            console.warn('Invalid data format from backend');
            return [];
        }
        return backendData;
    }

    /**
     * Get AMP data with filters applied
     */
    async getData(filters = {}) {
        try {
            const cacheKey = JSON.stringify(filters);
            
            // Check cache first
            if (this.cache.has(cacheKey)) {
                const cached = this.cache.get(cacheKey);
                if (Date.now() - cached.timestamp < this.cacheTimeout) {
                    console.log('Returning cached data');
                    return cached.data;
                }
            }

            // Query backend API with filters
            const data = await this.executeQuery(null, filters);
            
            // Cache the results
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });

            return data;
            
        } catch (error) {
            console.error('Failed to get AMP data:', error);
            // Return fallback data to keep dashboard functional
            return this.generateFallbackData();
        }
    }

    /**
     * Get summary metrics for dashboard
     */
    async getMetrics(filters = {}) {
        try {
            const data = await this.getData(filters);
            
            const totalActivities = data.length;
            const completedActivities = data.filter(item => item.status === 'complete').length;
            const inProgressActivities = data.filter(item => item.status === 'incomplete').length;
            const informOnlyActivities = data.filter(item => item.status === 'inform').length;
            
            const currentWeek = Math.max(...data.map(item => item.week_number || 0));
            const thisWeekActivities = data.filter(item => item.week_number === currentWeek).length;
            
            const completionRate = totalActivities > 0 ? Math.round((completedActivities / totalActivities) * 100) : 0;
            const totalStoreImpact = data.reduce((sum, item) => sum + (item.total_count || 0), 0);

            return {
                totalActivities,
                completedActivities,
                inProgressActivities,
                informOnlyActivities,
                thisWeekActivities,
                completionRate,
                totalStoreImpact,
                currentWeek
            };
            
        } catch (error) {
            console.error('Failed to get metrics:', error);
            return {
                totalActivities: 0,
                completedActivities: 0,
                inProgressActivities: 0,
                informOnlyActivities: 0,
                thisWeekActivities: 0,
                completionRate: 0,
                totalStoreImpact: 0,
                currentWeek: 0
            };
        }
    }

    /**
     * Get unique filter values for dropdowns
     */
    async getFilterOptions() {
        try {
            const data = await this.getData();
            
            return {
                divisions: [...new Set(data.map(item => item.division).filter(Boolean))].sort(),
                regions: [...new Set(data.map(item => item.region).filter(Boolean))].sort(),
                markets: [...new Set(data.map(item => item.market).filter(Boolean))].sort(),
                sites: [...new Set(data.map(item => item.site).filter(Boolean))].sort(),
                weeks: [...new Set(data.map(item => item.week_number).filter(Boolean))].sort((a, b) => b - a),
                activityTypes: [...new Set(data.map(item => item.activity_type).filter(Boolean))].sort(),
                storeAreas: [...new Set(data.map(item => item.store_area).filter(Boolean))].sort(),
                titles: [...new Set(data.map(item => item.activity_title).filter(Boolean))].sort()
            };
            
        } catch (error) {
            console.error('Failed to get filter options:', error);
            return {
                divisions: [],
                regions: [],
                markets: [],
                facilities: [],
                weeks: [],
                activityTypes: [],
                storeAreas: [],
                titles: []
            };
        }
    }

    /**
     * Generate enhanced sample data matching BigQuery schema
     */
    generateSampleData() {
        const currentWeek = 43; // Current week number
        const activities = [
            "Action Required! Arkansas: Dispensing Medications for Gender Affirming Care to Minors",
            "Update! Refrigerated and Reconstituted Pharmacy Delivery",
            "ACC: Applying Road Hazard Credit for Dotcom Tires",
            "ACTION REQUIRED: Optional Return Authorized for RDC Assembly Overstocked Merchandise",
            "Alcohol Delivery Coming to Your Store!",
            "Antone's Sandwiches Coming to Your Store – Week 38",
            "AP High Service Project",
            "Arizona: Eligibility Under State-Issued COVID Standing Order",
            "Associate Feedback: New Spill Station Cabinet Test",
            "Bakery Mod Update Timing Alert",
            "Colorado Law on New Hire Associates",
            "Coming Soon! Roofing Project",
            "Coupon Fraud at SCOs Involving Gift Cards",
            "COVID Vaccine Manual Ordering",
            "Delivery is Coming in Two Weeks",
            "Dept. 5: Upcoming 'Superman' Release",
            "Dept. 9: Tennessee Wildlife Resources Agency SSN and DL Exemption Details"
        ];

        const activityTypes = ["Verification", "Inform"];
        const storeAreas = ["Pharmacy", "Auto", "General Merchandise", "Grocery", "Bakery", "Entertainment"];
        const divisions = ["WEST", "NORTH", "NHM", "SOUTHWEST", "EAST", "SOUTHEAST"];
        const regions = ["Region 1", "Region 2", "Region 3", "Region 4"];
        const markets = ["Market 1", "Market 2", "Market 3", "Market 4", "Market 5"];
        
        return activities.map((title, index) => {
            const activityType = activityTypes[index % activityTypes.length];
            const isVerification = activityType === 'Verification';
            
            return {
                week_number: currentWeek - (index % 4),
                activity_title: title,
                location: "*Location",
                total_count: index % 3 === 0 ? Math.floor(Math.random() * 2000) + 2000 : Math.floor(Math.random() * 1500) + 100, // Mix of majority (>=2000) and others
                sc_count: Math.floor(Math.random() * 3000) + 50,
                nhm_count: Math.floor(Math.random() * 1000) + 10,
                div1_count: Math.floor(Math.random() * 500) + 5,
                fuel_count: index === 0 ? 1 : 0, // Only one fuel center (7368)
                status: index % 3 === 0 ? 'incomplete' : (index % 3 === 1 ? 'complete' : 'inform'),
                division: divisions[index % divisions.length],
                region: `${(index % 4) + 1}`,
                market: `${(index % 5) + 1}`,
                site: `${(index % 10) + 1}`,
                activity_type: activityType,
                store_area: storeAreas[index % storeAreas.length],
                published: true,
                alignment: index % 4 === 0 ? 'H&W' : 'Store',
                // Add verification counts for verification activities
                ...(isVerification && {
                    complete_count: Math.floor(Math.random() * 800) + 100,
                    incomplete_count: Math.floor(Math.random() * 400) + 50
                }),
                // Add preview link for all activities
                preview_link: `https://walmart.sharepoint.com/sites/ActivityHub/Pages/Preview.aspx?id=${index + 1000}`,
                create_ts: new Date(Date.now() - (index * 24 * 60 * 60 * 1000)).toISOString(),
                msg_start_dt: new Date(Date.now() - (index * 24 * 60 * 60 * 1000)).toISOString(),
                msg_end_dt: new Date(Date.now() + ((7 - index) * 24 * 60 * 60 * 1000)).toISOString()
            };
        });
    }

    /**
     * Generate fallback data in case of connection issues
     */
    generateFallbackData() {
        console.warn('Using fallback data due to connection issues');
        return this.generateSampleData().slice(0, 5); // Return limited fallback data
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
        console.log('Data cache cleared');
    }

    /**
     * Get connection status
     */
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            dataSource: this.dataSource,
            cacheSize: this.cache.size,
            lastUpdate: new Date().toISOString()
        };
    }
}

// Export for use in main dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AMPDataConnector;
} else {
    window.AMPDataConnector = AMPDataConnector;
}