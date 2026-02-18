# 🚀 Store Updates Dashboard - Quick Start

## Starting the Server

### Method 1: Double-click the batch file
**File:** `start-server.bat`  
**Action:** Double-click to start server  
**URL:** http://localhost:8080

### Method 2: PowerShell
```powershell
cd "C:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard"
python -m http.server 8080
```

### Method 3: Use existing start script
```powershell
.\start-server.ps1
```

## Current Status

✅ **Dashboard UI:** Fully functional with Walmart branding  
✅ **Filters:** Week, Status, Category working  
✅ **Location Drill-down:** Market → Region → Store  
✅ **Preview Links:** Working for real GUID format  
⚠️ **Data Source:** Using embedded sample data (15 items)  

## BigQuery Integration

**All BigQuery files moved to Spark-Playground repository:**  
`https://gecgithub01.walmart.com/krush/Spark-Playground.git`  
**Location:** `General Setup/BigQueryProject/`

### To Connect Real Data:
1. Clone Spark-Playground repository if not already cloned
2. Navigate to `Spark-Playground/General Setup/BigQueryProject/`
2. Read `README.md` for complete integration guide
3. Choose connection method:
   - **Quick:** Use `real-amp-data.csv` (cached data)
   - **Live:** Run `fetch_live_data.py` (requires auth)
   - **API:** Run `bigquery_rest_service.py` (REST service)

### Current Data Files:
- `real-data-loader.js` - Loads CSV data into dashboard
- `amp-sample.csv` - Sample data structure
- `data-test.html` - Data loading test page

## Files in This Folder

### Core Dashboard
- **`index.html`** - Main dashboard (Walmart branded)
- **`enhanced-styles.css`** - Dashboard styling
- **`walmart-spark.svg`** - Walmart logo

### Data Loading
- **`real-data-loader.js`** - CSV data loader
- **`amp-sample.csv`** - Sample AMP data
- **`data-test.html`** - Data loading test

### Server Scripts
- **`start-server.bat`** - Windows batch server starter
- **`start-server.ps1`** - PowerShell server starter  
- **`http-server.ps1`** - Alternative server script

### Testing
- **`test-dashboard.html`** - Dashboard feature testing

## Next Steps

1. **Test Current Dashboard:**
   - Open http://localhost:8080
   - Verify all filters work
   - Test location drill-down
   - Check preview links (Week 41 should work)

2. **Connect Real Data:**
   - Go to Spark-Playground repository: `General Setup/BigQueryProject/`
   - Follow README to set up connection
   - Choose cached CSV or live BigQuery

3. **Verify All Features:**
   - All 75+ titles loading
   - All preview links working
   - Real Market/Region/Store data showing

## BigQuery Connection Quick Reference

```javascript
// Option 1: Load from CSV (No auth needed)
// CSV file located in Spark-Playground repository
import { loadCSVData } from './real-data-loader.js';
const data = await loadCSVData('../../Spark-Playground/General Setup/BigQueryProject/real-amp-data.csv');

// Option 2: Connect to BigQuery (Auth required)
// Connector located in Spark-Playground repository
import { fetchAMPData } from '../../Spark-Playground/General Setup/BigQueryProject/unlimited-bigquery-connector.js';
const data = await fetchAMPData();
```

## Troubleshooting

### Server won't start
- Check if port 8080 is in use: `Get-NetTCPConnection -LocalPort 8080`
- Try different port: `python -m http.server 8081`

### Data not loading
- Verify `real-data-loader.js` exists
- Check browser console (F12) for errors
- Test with `data-test.html`

### Preview links not working
- Only Week 41 has real preview link currently
- See `Spark-Playground/General Setup/BigQueryProject/real-amp-data.csv` for all real links
- Update `realAMPData` array in `index.html`

---

**Server is now running!** Open http://localhost:8080 to view the dashboard.