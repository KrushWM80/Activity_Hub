/**
 * BigQuery Connection Test
 * Tests connection to wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep
 */

class BigQueryTester {
    constructor() {
        this.projectId = 'wmt-assetprotection-prod';
        this.dataset = 'Store_Support_Dev';
        this.table = 'AMP_Data_Prep';
        this.testResults = {};
    }

    /**
     * Run comprehensive BigQuery connection test
     */
    async runFullTest() {
        console.log('🧪 Starting BigQuery Connection Test...');
        console.log(`📊 Target: ${this.projectId}.${this.dataset}.${this.table}`);
        
        const results = {
            timestamp: new Date().toISOString(),
            tests: []
        };

        // Test 1: Authentication Check
        results.tests.push(await this.testAuthentication());
        
        // Test 2: Project Access
        results.tests.push(await this.testProjectAccess());
        
        // Test 3: Dataset Access
        results.tests.push(await this.testDatasetAccess());
        
        // Test 4: Table Schema
        results.tests.push(await this.testTableSchema());
        
        // Test 5: Sample Data Query
        results.tests.push(await this.testSampleQuery());
        
        // Test 6: Full Dashboard Query
        results.tests.push(await this.testDashboardQuery());
        
        this.displayResults(results);
        return results;
    }

    /**
     * Test 1: Authentication
     */
    async testAuthentication() {
        const test = {
            name: 'Authentication Test',
            status: 'running',
            details: []
        };

        try {
            // Check if Google APIs are loaded
            if (typeof gapi === 'undefined') {
                test.details.push('❌ Google API not loaded');
                test.status = 'failed';
                return test;
            }

            // Check authentication status
            if (gapi.auth2) {
                const authInstance = gapi.auth2.getAuthInstance();
                if (authInstance && authInstance.isSignedIn.get()) {
                    test.details.push('✅ User authenticated with Google');
                    const user = authInstance.currentUser.get();
                    const profile = user.getBasicProfile();
                    test.details.push(`👤 User: ${profile.getEmail()}`);
                    
                    const authResponse = user.getAuthResponse();
                    test.details.push(`🔑 Access token available: ${authResponse.access_token ? 'Yes' : 'No'}`);
                    test.status = 'passed';
                } else {
                    test.details.push('❌ User not authenticated');
                    test.status = 'failed';
                }
            } else {
                test.details.push('❌ Google Auth2 not initialized');
                test.status = 'failed';
            }
        } catch (error) {
            test.details.push(`❌ Authentication error: ${error.message}`);
            test.status = 'failed';
        }

        return test;
    }

    /**
     * Test 2: Project Access
     */
    async testProjectAccess() {
        const test = {
            name: 'Project Access Test',
            status: 'running',
            details: []
        };

        try {
            const token = await this.getAccessToken();
            const response = await fetch(`https://bigquery.googleapis.com/bigquery/v2/projects/${this.projectId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const projectInfo = await response.json();
                test.details.push(`✅ Project access confirmed: ${projectInfo.friendlyName || this.projectId}`);
                test.details.push(`📍 Location: ${projectInfo.defaultLocation || 'Not specified'}`);
                test.status = 'passed';
            } else {
                const error = await response.text();
                test.details.push(`❌ Project access denied: ${response.status} - ${error}`);
                test.status = 'failed';
            }
        } catch (error) {
            test.details.push(`❌ Project access error: ${error.message}`);
            test.status = 'failed';
        }

        return test;
    }

    /**
     * Test 3: Dataset Access
     */
    async testDatasetAccess() {
        const test = {
            name: 'Dataset Access Test',
            status: 'running',
            details: []
        };

        try {
            const token = await this.getAccessToken();
            const response = await fetch(`https://bigquery.googleapis.com/bigquery/v2/projects/${this.projectId}/datasets/${this.dataset}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const datasetInfo = await response.json();
                test.details.push(`✅ Dataset access confirmed: ${datasetInfo.friendlyName || this.dataset}`);
                test.details.push(`🏷️ Dataset ID: ${datasetInfo.id}`);
                test.details.push(`📅 Created: ${new Date(parseInt(datasetInfo.creationTime)).toLocaleDateString()}`);
                test.status = 'passed';
            } else {
                const error = await response.text();
                test.details.push(`❌ Dataset access denied: ${response.status} - ${error}`);
                test.status = 'failed';
            }
        } catch (error) {
            test.details.push(`❌ Dataset access error: ${error.message}`);
            test.status = 'failed';
        }

        return test;
    }

    /**
     * Test 4: Table Schema
     */
    async testTableSchema() {
        const test = {
            name: 'Table Schema Test',
            status: 'running',
            details: []
        };

        try {
            const token = await this.getAccessToken();
            const response = await fetch(`https://bigquery.googleapis.com/bigquery/v2/projects/${this.projectId}/datasets/${this.dataset}/tables/${this.table}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const tableInfo = await response.json();
                test.details.push(`✅ Table found: ${tableInfo.friendlyName || this.table}`);
                test.details.push(`📊 Rows: ${tableInfo.numRows ? parseInt(tableInfo.numRows).toLocaleString() : 'Unknown'}`);
                test.details.push(`💾 Size: ${tableInfo.numBytes ? (parseInt(tableInfo.numBytes) / 1024 / 1024).toFixed(2) + ' MB' : 'Unknown'}`);
                
                if (tableInfo.schema && tableInfo.schema.fields) {
                    test.details.push(`🏛️ Columns: ${tableInfo.schema.fields.length}`);
                    test.details.push(`📋 Key fields: ${tableInfo.schema.fields.slice(0, 5).map(f => f.name).join(', ')}...`);
                }
                
                test.status = 'passed';
            } else {
                const error = await response.text();
                test.details.push(`❌ Table access denied: ${response.status} - ${error}`);
                test.status = 'failed';
            }
        } catch (error) {
            test.details.push(`❌ Table schema error: ${error.message}`);
            test.status = 'failed';
        }

        return test;
    }

    /**
     * Test 5: Sample Query
     */
    async testSampleQuery() {
        const test = {
            name: 'Sample Data Query Test',
            status: 'running',
            details: []
        };

        const sampleQuery = `
            SELECT 
                COUNT(*) as total_rows,
                COUNT(DISTINCT actv_title_home_ofc_nm) as unique_activities,
                MIN(create_ts) as earliest_date,
                MAX(create_ts) as latest_date
            FROM \`${this.projectId}.${this.dataset}.${this.table}\`
            LIMIT 1
        `;

        try {
            const result = await this.executeQuery(sampleQuery);
            
            if (result && result.length > 0) {
                const stats = result[0];
                test.details.push(`✅ Query executed successfully`);
                test.details.push(`📊 Total rows: ${parseInt(stats.total_rows).toLocaleString()}`);
                test.details.push(`🎯 Unique activities: ${stats.unique_activities}`);
                test.details.push(`📅 Date range: ${stats.earliest_date} to ${stats.latest_date}`);
                test.status = 'passed';
            } else {
                test.details.push(`❌ Query returned no results`);
                test.status = 'failed';
            }
        } catch (error) {
            test.details.push(`❌ Sample query error: ${error.message}`);
            test.status = 'failed';
        }

        return test;
    }

    /**
     * Test 6: Dashboard Query
     */
    async testDashboardQuery() {
        const test = {
            name: 'Dashboard Query Test',
            status: 'running',
            details: []
        };

        const dashboardQuery = `
            SELECT 
                EXTRACT(WEEK FROM create_ts) as week_number,
                actv_title_home_ofc_nm as activity_title,
                location,
                COUNT(*) as total_count,
                SUM(CASE WHEN store_type = 'SC' THEN 1 ELSE 0 END) as sc_count,
                SUM(CASE WHEN store_type = 'NHM' THEN 1 ELSE 0 END) as nhm_count,
                division,
                activity_type,
                status
            FROM \`${this.projectId}.${this.dataset}.${this.table}\`
            WHERE published = true
            GROUP BY week_number, activity_title, location, division, activity_type, status
            ORDER BY week_number DESC, activity_title
            LIMIT 10
        `;

        try {
            const result = await this.executeQuery(dashboardQuery);
            
            if (result && result.length > 0) {
                test.details.push(`✅ Dashboard query executed successfully`);
                test.details.push(`📊 Sample records: ${result.length}`);
                test.details.push(`🎯 First activity: ${result[0].activity_title}`);
                test.details.push(`📅 Latest week: ${result[0].week_number}`);
                
                // Save sample data for dashboard use
                window.BIGQUERY_TEST_DATA = result;
                test.details.push(`💾 Sample data saved to window.BIGQUERY_TEST_DATA`);
                
                test.status = 'passed';
            } else {
                test.details.push(`❌ Dashboard query returned no results`);
                test.status = 'failed';
            }
        } catch (error) {
            test.details.push(`❌ Dashboard query error: ${error.message}`);
            test.status = 'failed';
        }

        return test;
    }

    /**
     * Execute BigQuery query
     */
    async executeQuery(query) {
        const token = await this.getAccessToken();
        
        const response = await fetch(`https://bigquery.googleapis.com/bigquery/v2/projects/${this.projectId}/queries`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                useLegacySql: false,
                maxResults: 1000,
                timeoutMs: 30000
            })
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(`Query failed: ${response.status} - ${error}`);
        }

        const result = await response.json();
        
        if (!result.rows) {
            return [];
        }

        // Transform results
        const schema = result.schema.fields;
        return result.rows.map(row => {
            const record = {};
            row.f.forEach((field, index) => {
                record[schema[index].name] = field.v;
            });
            return record;
        });
    }

    /**
     * Get access token
     */
    async getAccessToken() {
        if (typeof gapi !== 'undefined' && gapi.auth2) {
            const authInstance = gapi.auth2.getAuthInstance();
            if (authInstance && authInstance.isSignedIn.get()) {
                const user = authInstance.currentUser.get();
                return user.getAuthResponse().access_token;
            }
        }
        throw new Error('Not authenticated with Google');
    }

    /**
     * Display test results
     */
    displayResults(results) {
        console.log('\n🧪 BIGQUERY CONNECTION TEST RESULTS');
        console.log('=' .repeat(50));
        
        let passedTests = 0;
        let totalTests = results.tests.length;
        
        results.tests.forEach((test, index) => {
            console.log(`\n${index + 1}. ${test.name}`);
            console.log(`Status: ${test.status.toUpperCase()}`);
            
            if (test.status === 'passed') passedTests++;
            
            test.details.forEach(detail => {
                console.log(`   ${detail}`);
            });
        });
        
        console.log('\n' + '='.repeat(50));
        console.log(`📊 SUMMARY: ${passedTests}/${totalTests} tests passed`);
        
        if (passedTests === totalTests) {
            console.log('🎉 All tests passed! BigQuery connection is working.');
            console.log('💡 You can now use real data in your dashboard.');
        } else {
            console.log('⚠️  Some tests failed. Check authentication and permissions.');
            console.log('📋 Falling back to sample data for dashboard.');
        }
    }
}

// Initialize tester and make available globally
window.BigQueryTester = BigQueryTester;

// Auto-run basic connectivity test
console.log('🔧 BigQuery tester loaded. Available commands:');
console.log('- new BigQueryTester().runFullTest() - Run complete test suite');
console.log('- testBigQueryConnection() - Quick connection test');

// Quick test function
async function testBigQueryConnection() {
    const tester = new BigQueryTester();
    try {
        console.log('🚀 Running quick BigQuery connection test...');
        const authTest = await tester.testAuthentication();
        
        if (authTest.status === 'passed') {
            console.log('✅ Authentication successful, running sample query...');
            const queryTest = await tester.testSampleQuery();
            
            if (queryTest.status === 'passed') {
                console.log('🎉 BigQuery connection successful!');
            } else {
                console.log('❌ Query test failed - check table permissions');
            }
        } else {
            console.log('❌ Authentication failed - please sign in first');
        }
    } catch (error) {
        console.error('🚨 Test error:', error);
    }
}

window.testBigQueryConnection = testBigQueryConnection;