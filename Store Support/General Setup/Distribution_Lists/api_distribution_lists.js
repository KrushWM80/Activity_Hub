/**
 * Code Puppy Pages API Endpoint
 * Queries BigQuery for distribution lists
 * 
 * Deploy this to Code Puppy Pages as: /api/distribution-lists
 */

const { BigQuery } = require('@google-cloud/bigquery');

// Initialize BigQuery client
const bigquery = new BigQuery({
    projectId: 'wmt-assetprotection-prod'
});

/**
 * GET /api/distribution-lists
 * Returns all distribution lists from BigQuery
 */
async function getDistributionLists(req, res) {
    try {
        const query = `
            SELECT 
                email,
                name,
                display_name,
                description,
                member_count,
                category
            FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
            ORDER BY name
        `;
        
        console.log('Executing BigQuery query...');
        const [rows] = await bigquery.query({
            query: query,
            location: 'US'
        });
        
        console.log(`Retrieved ${rows.length} distribution lists`);
        
        res.status(200).json(rows);
        
    } catch (error) {
        console.error('Error querying BigQuery:', error);
        res.status(500).json({
            error: 'Failed to load distribution lists',
            message: error.message
        });
    }
}

/**
 * GET /api/distribution-lists/search?q=searchTerm
 * Search distribution lists by keyword
 */
async function searchDistributionLists(req, res) {
    try {
        const searchTerm = req.query.q || '';
        
        const query = `
            SELECT 
                email,
                name,
                display_name,
                description,
                member_count,
                category
            FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
            WHERE LOWER(email) LIKE @searchTerm
               OR LOWER(name) LIKE @searchTerm
               OR LOWER(description) LIKE @searchTerm
            ORDER BY name
            LIMIT 100
        `;
        
        const options = {
            query: query,
            location: 'US',
            params: { searchTerm: `%${searchTerm.toLowerCase()}%` }
        };
        
        const [rows] = await bigquery.query(options);
        
        res.status(200).json(rows);
        
    } catch (error) {
        console.error('Error searching BigQuery:', error);
        res.status(500).json({
            error: 'Failed to search distribution lists',
            message: error.message
        });
    }
}

/**
 * GET /api/distribution-lists/category/:category
 * Get distribution lists by category
 */
async function getDistributionListsByCategory(req, res) {
    try {
        const category = req.params.category;
        
        const query = `
            SELECT 
                email,
                name,
                display_name,
                description,
                member_count,
                category
            FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
            WHERE category = @category
            ORDER BY name
        `;
        
        const options = {
            query: query,
            location: 'US',
            params: { category: category }
        };
        
        const [rows] = await bigquery.query(options);
        
        res.status(200).json(rows);
        
    } catch (error) {
        console.error('Error querying BigQuery:', error);
        res.status(500).json({
            error: 'Failed to load distribution lists',
            message: error.message
        });
    }
}

/**
 * GET /api/distribution-lists/stats
 * Get statistics about distribution lists
 */
async function getDistributionListStats(req, res) {
    try {
        const query = `
            SELECT 
                category,
                COUNT(*) as count,
                SUM(member_count) as total_members,
                AVG(member_count) as avg_members
            FROM \`wmt-assetprotection-prod.Store_Support_Dev.dl_catalog\`
            GROUP BY category
            ORDER BY count DESC
        `;
        
        const [rows] = await bigquery.query({
            query: query,
            location: 'US'
        });
        
        res.status(200).json(rows);
        
    } catch (error) {
        console.error('Error querying BigQuery:', error);
        res.status(500).json({
            error: 'Failed to load statistics',
            message: error.message
        });
    }
}

// Export for Code Puppy Pages
module.exports = {
    getDistributionLists,
    searchDistributionLists,
    getDistributionListsByCategory,
    getDistributionListStats
};
