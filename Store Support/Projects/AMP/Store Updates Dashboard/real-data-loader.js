/**
 * Real Data Integration Template
 * 
 * This file provides multiple ways to connect your dashboard to real AMP data:
 * 1. Direct CSV import
 * 2. JSON data paste
 * 3. BigQuery REST API (when configured)
 */

// Method 1: Load data from CSV file
async function loadRealDataFromCSV(csvFilePath) {
    try {
        const response = await fetch(csvFilePath);
        const csvText = await response.text();
        const data = parseCSVToJSON(csvText);
        
        // Set the real data globally
        window.REAL_AMP_DATA = data;
        console.log(`Loaded ${data.length} real records from CSV`);
        
        // Refresh the dashboard
        if (typeof loadData === 'function') {
            await loadData();
        }
        
        return data;
    } catch (error) {
        console.error('Failed to load CSV data:', error);
        throw error;
    }
}

// Method 2: Set real data directly (paste JSON data here)
function setRealData(jsonData) {
    window.REAL_AMP_DATA = jsonData;
    console.log(`Set ${jsonData.length} real records`);
    
    // Update auth indicator
    const authIndicator = document.getElementById('authIndicator');
    if (authIndicator) {
        authIndicator.textContent = '📊 Real Data Loaded';
        authIndicator.className = 'auth-indicator connected';
    }
    
    // Refresh the dashboard
    if (typeof loadData === 'function') {
        loadData();
    }
}

// Method 3: Load from BigQuery export (JSON format)
async function loadFromBigQueryExport(jsonFilePath) {
    try {
        const response = await fetch(jsonFilePath);
        const data = await response.json();
        
        setRealData(data);
        return data;
    } catch (error) {
        console.error('Failed to load BigQuery export:', error);
        throw error;
    }
}

// Utility function to parse CSV to JSON
function parseCSVToJSON(csvText) {
    const lines = csvText.split('\n');
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim()) {
            const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
            const record = {};
            
            headers.forEach((header, index) => {
                record[header] = values[index] || '';
            });
            
            data.push(record);
        }
    }
    
    return data;
}

// Example usage instructions:
console.log(`
Real Data Integration Instructions:

1. CSV File Method:
   - Place your CSV file in the dashboard folder
   - Call: loadRealDataFromCSV('your-data.csv')

2. Direct JSON Method:
   - Export your data as JSON
   - Call: setRealData(yourJsonArray)

3. BigQuery Export Method:
   - Export BigQuery table as JSON
   - Call: loadFromBigQueryExport('export.json')

4. Manual Data Paste:
   - Open browser console
   - Paste: setRealData([...your array of records...])

Current Status: ${window.REAL_AMP_DATA ? 'Real data loaded' : 'Using sample data'}
`);

// Export functions to global scope
window.loadRealDataFromCSV = loadRealDataFromCSV;
window.setRealData = setRealData;
window.loadFromBigQueryExport = loadFromBigQueryExport;