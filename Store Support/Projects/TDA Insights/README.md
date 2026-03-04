# TDA Initiatives Insights Dashboard

A professional, web-based dashboard for tracking TDA (Test/Deployment Actions) Initiative status across Walmart stores. Built with FlaskPython backend and a modern HTML/CSS frontend following Walmart Living Design principles.

## Overview

The TDA Insights Dashboard provides:

- **📊 Real-time Data Visualization** - Load TDA initiative data from BigQuery
- **🔍 Advanced Filtering** - Filter by Phase, Health Status, and more
- **📈 Executive Summary** - Key metrics and statistics at a glance
- **📥 Data Export** - Export filtered data as CSV
- **📊 PPT Report Generation** - Create professional PowerPoint presentations with phase-based slides
- **🎨 Living Design Compliance** - Walmart-compliant design system with colors, typography, and spacing

## Data Source

**Database:** `wmt-assetprotection-prod.Store_Support_Dev.Output_TDA Report`

The dashboard pulls data from the TDA Report table in BigQuery, which contains:
- Initiative/Project Title
- Health Status (On Track, At Risk, Off Track)
- Phase (Test, Production, etc.)
- Number of Stores Impacted
- Intake & Testing Status
- Dallas POC (Point of Contact)
- Deployment Information

## Features

### Dashboard
- ✅ Responsive, modern interface with Walmart branding
- ✅ Real-time BigQuery data integration
- ✅ Phase-based filtering
- ✅ Health status summary cards
- ✅ Detailed initiative table with status badges
- ✅ CSV export functionality
- ✅ Connection status indicator
- ✅ Last updated timestamp

### Backend API
- `GET /api/health` - Health check endpoint
- `GET /api/data` - Get filtered TDA data
- `GET /api/phases` - Get list of unique phases
- `GET /api/health-statuses` - Get list of health statuses
- `GET /api/summary` - Get summary statistics
- `GET /api/export/csv` - Export data as CSV

### PowerPoint Report Generator
- Creates professional PowerPoint presentations
- One slide per phase with detailed metrics
- Color-coded health status indicators
- Summary statistics and insights
- Walmart branding and colors
- Automatic table of top initiatives per phase

## Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** Google BigQuery
- **Reports:** python-pptx
- **Design:** Walmart Living Design System

## Design System

The dashboard implements the **Walmart Living Design System** with:

### Colors
- **Primary Blue:** #0071CE (Walmart Blue)
- **Dark Blue:** #1E3A8A (Header background)
- **Accent Yellow:** #FFCC00 (Walmart Yellow)
- **Status Colors:**
  - Green (#107C10) - On Track
  - Orange (#F7630C) - At Risk
  - Red (#DC3545) - Off Track

### Typography
- **Font Family:** -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- **Weights:** Light (300), Regular (400), Semi-bold (600), Bold (700)
- **Sizes:** 12px (small), 14px (base), 16px (lg), 24px (xl), 32px (2xl)

### Components
- **Cards:** Clean white cards with subtle shadows
- **Buttons:** Primary (blue), Secondary (outlined)
- **Tables:** Striped rows with hover effects
- **Filters:** Dropdown selects with visual feedback
- **Badges:** Color-coded status indicators

## Installation

### Prerequisites
- Python 3.8+
- Google Cloud authentication (service account or credentials)
- BigQuery access to the TDA Report table

### Setup

1. **Clone/Navigate to the project:**
   ```bash
   cd "Store Support\Projects\TDA Insights"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud authentication:**
   ```bash
   # Option 1: Export credentials path
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   
   # Option 2: Use gcloud CLI
   gcloud auth application-default login
   ```

## Usage

### Running the Dashboard

#### Method 1: Standalone (Simplest)
```bash
# Terminal 1: Start the backend
python backend.py

# Terminal 2: Open dashboard
start dashboard.html  # Windows
open dashboard.html   # macOS
```

Then navigate to `http://localhost:5000` (or the URL shown in the backend logs).

#### Method 2: With Static Server
```bash
# Terminal 1: Start backend
python backend.py

# Terminal 2: Start a simple HTTP server
python -m http.server 8000

# Open http://localhost:8000/dashboard.html
```

#### Method 3: With Flask (Complete Setup)
```bash
export FLASK_APP=backend.py
export FLASK_DEBUG=True
flask run
```

### Generating PowerPoint Reports

**From Python:**
```python
from generate_ppt import TDAPowerPointGenerator

generator = TDAPowerPointGenerator()
generator.fetch_data()
output_file = generator.generate_report("TDA_Report.pptx")
print(f"Report saved to: {output_file}")
```

**From Command Line:**
```bash
python generate_ppt.py
```

This will create a PowerPoint file with:
- Title slide
- One slide per phase with key initiatives
- Summary statistics and color-coded health status
- Professional Walmart branding

## Configuration

### Environment Variables

```bash
# Backend port
PORT=5000

# Flask debug mode
FLASK_DEBUG=True

# BigQuery project (optional, defaults to connection settings)
GCP_PROJECT=wmt-assetprotection-prod
```

### API Configuration

Edit the `API_BASE` variable in `dashboard.html` if running on a different server:

```javascript
const API_BASE = 'http://localhost:5000/api';  // Change this
```

## Troubleshooting

### "Connection error" on dashboard
- **Issue:** Backend is not running
- **Solution:** Start backend with `python backend.py`
- **Check:** Visit `http://localhost:5000/api/health` to verify backend is running

### "BigQuery connection failed"
- **Issue:** Authentication or credentials not set
- **Solution:** 
  1. Run `gcloud auth application-default login`
  2. Or set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
  3. Verify BigQuery API is enabled in GCP project

### "No data found"
- **Issue:** Table name or dataset is incorrect
- **Solution:** 
  1. Verify table exists: `wmt-assetprotection-prod.Store_Support_Dev.Output_TDA Report`
  2. Check BigQuery permissions
  3. Run test query in BigQuery console

### PowerPoint generation fails
- **Issue:** Missing dependencies
- **Solution:** `pip install python-pptx`

## Project Structure

```
TDA Insights/
├── backend.py              # Flask backend API
├── dashboard.html          # HTML/CSS/JavaScript frontend
├── generate_ppt.py         # PowerPoint report generator
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── QUICKSTART.md          # Quick start guide
```

## API Examples

### Get all data
```bash
curl http://localhost:5000/api/data
```

### Get data for a specific phase
```bash
curl "http://localhost:5000/api/data?phase=Test"
```

### Filter by health status
```bash
curl "http://localhost:5000/api/data?health_status=On%20Track"
```

### Get available phases
```bash
curl http://localhost:5000/api/phases
```

### Get summary statistics
```bash
curl http://localhost:5000/api/summary
```

## Design Guidelines

### Color Usage
- **Blue (#0071CE):** Primary actions, headers, important data
- **Yellow (#FFCC00):** Accents, highlights, call-to-action
- **Green (#107C10):** Success, on-track status
- **Orange (#F7630C):** Warning, at-risk status
- **Red (#DC3545):** Error, off-track status

### Typography Rules
- **Headers:** 700 weight, BLUE color
- **Body text:** 400 weight, #212121 color
- **Secondary text:** 400 weight, #666666 color
- **Status text:** 600 weight, color-coded per status

### Component Guidelines
- **Padding:** Use multiples of 8px (8px, 16px, 24px, 32px)
- **Border radius:** 4px for components, 8px for cards
- **Shadows:** Use subtle shadows (0 1px 3px rgba(0,0,0,0.08))
- **Spacing:** Maintain consistent gaps using CSS variables

## Performance

- **Data Caching:** Backend caches data for 5 minutes to reduce BigQuery calls
- **Lazy Loading:** Dashboard loads filters before full data
- **Response Times:** Optimized for <2s initial load
- **Export:** CSV export works with 1000+ records

## Security

- **CORS Enabled:** Frontend and backend can run on different origins
- **No Authentication (Local):** For internal use; add OAuth2 for production
- **Data Validation:** Input sanitization on all API endpoints
- **SQL Injection Protection:** Uses BigQuery parameterized queries

## Future Enhancements

- [ ] PDF export option
- [ ] Email report scheduling
- [ ] Real-time notifications for status changes
- [ ] Add authentication/authorization
- [ ] Dashboard snapshot history
- [ ] Custom date range filtering
- [ ] Comparison view (previous periods)
- [ ] Map visualization of store locations
- [ ] Mobile app version

## Support & Documentation

For more information:
- [Walmart Living Design System](../General%20Setup/Design/DESIGN_SYSTEM.md)
- [BigQuery Setup Guide](../Intake%20Hub/ProjectsinStores/BIGQUERY_SETUP.md)
- [Google Cloud BigQuery Docs](https://cloud.google.com/bigquery/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)

## License

Internal Walmart Tool - Use within Walmart Enterprise only

## Contact

For questions or issues:
- Check the QUICKSTART.md for common tasks
- Review troubleshooting section above
- Contact the Activity Hub team
