#!/usr/bin/env node

/**
 * BigQuery Connection Test - Command Line Version
 * Run: node bigquery-cli-test.js
 */

const https = require('https');
const fs = require('fs');

class BigQueryCLITester {
    constructor() {
        this.projectId = 'wmt-assetprotection-prod';
        this.dataset = 'Store_Support_Dev';
        this.table = 'AMP_Data_Prep';
    }

    async testConnection() {
        console.log('🧪 BigQuery Connection Test - CLI Version');
        console.log('=' .repeat(50));
        console.log(`📊 Target: ${this.projectId}.${this.dataset}.${this.table}`);
        console.log('');

        // Test 1: Check if running in Google Cloud environment
        await this.testGoogleCloudEnvironment();

        // Test 2: Test with curl command
        await this.generateCurlTest();

        // Test 3: Generate test queries
        await this.generateTestQueries();

        console.log('\n' + '='.repeat(50));
        console.log('🏁 Test Complete');
    }

    async testGoogleCloudEnvironment() {
        console.log('1. 🏠 Environment Check');
        
        // Check for Google Cloud CLI
        const { exec } = require('child_process');
        
        return new Promise((resolve) => {
            exec('gcloud --version', (error, stdout, stderr) => {
                if (error) {
                    console.log('   ❌ Google Cloud CLI not installed');
                    console.log('   💡 Install: https://cloud.google.com/sdk/docs/install');
                } else {
                    console.log('   ✅ Google Cloud CLI found');
                    console.log(`   📋 Version: ${stdout.split('\n')[0]}`);
                    
                    // Check authentication
                    exec('gcloud auth list --filter=status:ACTIVE --format="value(account)"', (error2, stdout2) => {
                        if (stdout2.trim()) {
                            console.log(`   ✅ Authenticated as: ${stdout2.trim()}`);
                        } else {
                            console.log('   ❌ Not authenticated with gcloud');
                            console.log('   💡 Run: gcloud auth login');
                        }
                    });
                }
                resolve();
            });
        });
    }

    async generateCurlTest() {
        console.log('\n2. 🌐 cURL Test Command');
        
        const curlCommand = `curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \\
  -H "Content-Type: application/json" \\
  --data '{
    "query":"SELECT COUNT(*) as total_rows FROM \`${this.projectId}.${this.dataset}.${this.table}\` LIMIT 1",
    "useLegacySql":false
  }' \\
  "https://bigquery.googleapis.com/bigquery/v2/projects/${this.projectId}/queries"`;

        console.log('   📋 Run this command to test connection:');
        console.log('   ' + '-'.repeat(60));
        console.log(curlCommand);
        console.log('   ' + '-'.repeat(60));
        
        // Save to file
        fs.writeFileSync('bigquery-test.sh', `#!/bin/bash\n# BigQuery Connection Test\n\n${curlCommand}\n`);
        console.log('   💾 Saved as: bigquery-test.sh');
    }

    async generateTestQueries() {
        console.log('\n3. 📝 Test Queries');
        
        const queries = [
            {
                name: 'Table Info',
                query: `SELECT 
  COUNT(*) as total_rows,
  COUNT(DISTINCT actv_title_home_ofc_nm) as unique_activities,
  MIN(create_ts) as earliest_date,
  MAX(create_ts) as latest_date
FROM \`${this.projectId}.${this.dataset}.${this.table}\``
            },
            {
                name: 'Sample Data',
                query: `SELECT 
  actv_title_home_ofc_nm,
  location,
  division,
  activity_type,
  status,
  create_ts
FROM \`${this.projectId}.${this.dataset}.${this.table}\`
ORDER BY create_ts DESC
LIMIT 5`
            },
            {
                name: 'Dashboard Query',
                query: `SELECT 
  EXTRACT(WEEK FROM create_ts) as week_number,
  actv_title_home_ofc_nm as activity_title,
  location,
  COUNT(*) as total_count,
  division,
  activity_type,
  status
FROM \`${this.projectId}.${this.dataset}.${this.table}\`
WHERE published = true
GROUP BY week_number, activity_title, location, division, activity_type, status
ORDER BY week_number DESC
LIMIT 10`
            }
        ];

        queries.forEach((q, index) => {
            console.log(`   ${index + 1}. ${q.name}:`);
            console.log('      ' + '-'.repeat(50));
            console.log('      ' + q.query.replace(/\n/g, '\n      '));
            console.log('');
        });

        // Save queries to file
        const queryFile = queries.map(q => `-- ${q.name}\n${q.query};\n`).join('\n');
        fs.writeFileSync('bigquery-test-queries.sql', queryFile);
        console.log('   💾 Saved queries as: bigquery-test-queries.sql');
    }
}

// Run the test
if (require.main === module) {
    const tester = new BigQueryCLITester();
    tester.testConnection().catch(console.error);
}

module.exports = BigQueryCLITester;