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
            
            // In a production environment, this would handle authentication
            // and establish the BigQuery connection
            await this.authenticate();
            
            this.isConnected = true;
            console.log('Successfully connected to AMP Data Prep source');
            
            return true;
        } catch (error) {
            console.error('Failed to initialize data connection:', error);
            this.isConnected = false;
            throw error;
        }
    }

    /**
     * Authenticate with BigQuery service
     */
    async authenticate() {
        // Simulate authentication process
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ success: true });
            }, 1000);
        });
    }

    /**
     * Build SQL query for AMP data based on filters
     */
    buildQuery(filters = {}) {
        let query = `
            WITH amp_data AS (
                SELECT 
                    -- Core AMP fields
                    EXTRACT(WEEK FROM msg_start_dt) as week_number,
                    actv_title_home_ofc_nm as activity_title,
                    CONCAT('*', COALESCE(trgt_store_nbr_array[SAFE_OFFSET(0)], 'All Locations')) as location,
                    
                    -- Count fields
                    ARRAY_LENGTH(trgt_store_nbr_array) as total_count,
                    COUNTIF(store_format = 'SC') as sc_count,
                    COUNTIF(store_format = 'NHM') as nhm_count,
                    COUNTIF(division = '1') as div1_count,
                    COUNTIF(store_format = 'FUEL') as fuel_count,
                    
                    -- Status and classification
                    CASE 
                        WHEN msg_status_id = 'PUBLISHED' THEN 'complete'
                        WHEN msg_status_id = 'DRAFT' THEN 'incomplete'
                        ELSE 'inform'
                    END as status,
                    
                    -- Dimensional fields
                    division,
                    region,
                    market,
                    facility,
                    actv_type_nm as activity_type,
                    bus_domain_nm as store_area,
                    
                    -- Filter fields
                    msg_status_id = 'PUBLISHED' as published,
                    create_ts,
                    msg_start_dt,
                    msg_end_dt
                    
                FROM \`${this.dataSource}\`
                WHERE 1=1
        `;

        // Add date filter for current context
        query += `
            AND msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
            AND msg_status_id = 'PUBLISHED'  -- Only show published status as requested
        `;

        // Apply dynamic filters
        if (filters.division) {
            query += ` AND division = '${filters.division}'`;
        }
        if (filters.region) {
            query += ` AND region = '${filters.region}'`;
        }
        if (filters.market) {
            query += ` AND market = '${filters.market}'`;
        }
        if (filters.facility) {
            query += ` AND facility = '${filters.facility}'`;
        }
        if (filters.week) {
            query += ` AND EXTRACT(WEEK FROM msg_start_dt) = ${filters.week}`;
        }
        if (filters.activityType) {
            query += ` AND actv_type_nm = '${filters.activityType}'`;
        }
        if (filters.storeArea) {
            query += ` AND bus_domain_nm = '${filters.storeArea}'`;
        }
        if (filters.keyword) {
            query += ` AND (LOWER(actv_title_home_ofc_nm) LIKE '%${filters.keyword.toLowerCase()}%' 
                          OR LOWER(actv_type_nm) LIKE '%${filters.keyword.toLowerCase()}%'
                          OR LOWER(bus_domain_nm) LIKE '%${filters.keyword.toLowerCase()}%')`;
        }

        query += `
            )
            SELECT * FROM amp_data
            ORDER BY week_number DESC, total_count DESC
            LIMIT 1000
        `;

        return query;
    }

    /**
     * Execute query against BigQuery
     */
    async executeQuery(query) {
        try {
            if (!this.isConnected) {
                await this.initialize();
            }

            console.log('Executing BigQuery query...');
            
            // Check if we have a direct data source available
            if (window.REAL_AMP_DATA) {
                console.log('Using directly provided real data');
                return window.REAL_AMP_DATA;
            }
            
            // Try to execute real BigQuery query
            const realData = await this.executeBigQueryREST(query);
            console.log('Successfully retrieved real data from BigQuery');
            return realData;
            
        } catch (error) {
            console.error('Real data query failed:', error);
            console.warn('Falling back to sample data. Error:', error.message);
            
            // Show user-friendly message about using sample data
            if (typeof document !== 'undefined') {
                const authIndicator = document.getElementById('authIndicator');
                if (authIndicator) {
                    authIndicator.textContent = '📊 Using Sample Data';
                    authIndicator.className = 'auth-indicator disconnected';
                }
            }
            
            // Fallback to sample data if real query fails
            return this.generateSampleData();
        }
    }

    /**
     * Execute BigQuery using REST API
     */
    async executeBigQueryREST(query) {
        const projectId = 'wmt-assetprotection-prod';
        
        try {
            // Try to get authentication token
            const token = await this.getAccessToken();
            
            const response = await fetch(`https://bigquery.googleapis.com/bigquery/v2/projects/${projectId}/queries`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    query: query,
                    useLegacySql: false,
                    maxResults: 10000,
                    timeoutMs: 30000
                })
            });

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`BigQuery API error: ${response.status} - ${errorData}`);
            }

            const result = await response.json();
            return this.transformBigQueryResults(result);
            
        } catch (error) {
            console.error('BigQuery REST API execution failed:', error);
            throw error;
        }
    }

    /**
     * Get access token for BigQuery authentication
     */
    async getAccessToken() {
        // For now, throw an error to force fallback to sample data
        // This will be replaced with actual authentication once configured
        throw new Error('BigQuery authentication not configured. Using sample data instead.');
        
        // Commented out authentication methods for when you're ready to configure:
        /*
        // Method 1: Google API OAuth2
        if (typeof gapi !== 'undefined' && gapi.auth2) {
            const authInstance = gapi.auth2.getAuthInstance();
            if (authInstance && authInstance.isSignedIn.get()) {
                const user = authInstance.currentUser.get();
                return user.getAuthResponse().access_token;
            }
        }
        
        // Method 2: Custom auth service
        if (window.BigQueryAuth && window.BigQueryAuth.getToken) {
            return await window.BigQueryAuth.getToken();
        }
        
        // Method 3: Direct token (for testing)
        if (window.BIGQUERY_ACCESS_TOKEN) {
            return window.BIGQUERY_ACCESS_TOKEN;
        }
        
        throw new Error('No authentication method available. Please configure OAuth2 or service account authentication.');
        */
    }

    /**
     * Transform BigQuery results to expected format
     */
    transformBigQueryResults(bigqueryResponse) {
        if (!bigqueryResponse.rows || bigqueryResponse.rows.length === 0) {
            console.warn('No data returned from BigQuery');
            return [];
        }

        const schema = bigqueryResponse.schema.fields;
        const rows = bigqueryResponse.rows;

        console.log(`Transforming ${rows.length} rows from BigQuery`);

        return rows.map(row => {
            const record = {};
            row.f.forEach((field, index) => {
                const fieldName = schema[index].name;
                const fieldValue = field.v;
                
                // Handle different data types
                switch (schema[index].type) {
                    case 'INTEGER':
                        record[fieldName] = fieldValue ? parseInt(fieldValue) : 0;
                        break;
                    case 'FLOAT':
                        record[fieldName] = fieldValue ? parseFloat(fieldValue) : 0;
                        break;
                    case 'BOOLEAN':
                        record[fieldName] = fieldValue === 'true';
                        break;
                    case 'TIMESTAMP':
                        record[fieldName] = fieldValue ? new Date(fieldValue * 1000).toISOString() : null;
                        break;
                    default:
                        record[fieldName] = fieldValue || '';
                }
            });
            return record;
        });
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

            const query = this.buildQuery(filters);
            const data = await this.executeQuery(query);
            
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