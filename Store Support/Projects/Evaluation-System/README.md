# Evaluation System - README

**Performance Evaluation System** is a standalone web application that enables employees to generate professional self-evaluations from structured work data.

## Features

### 🎯 Core Capabilities
- **Multiple Input Methods**
  - Upload CSV or Excel files with your project data
  - Manual data entry form for individual projects
  - Drag-and-drop file upload interface

- **Intelligent Column Mapping**
  - Map your file columns to system fields
  - Built-in help tooltips for every field (click "i" icon)
  - Automatic field detection and suggestions
  - Support for optional and required fields

- **Automatic Evaluation Generation**
  - Converts raw project data into professional narrative
  - Maps work to 4 leadership competencies
  - Calculates performance score (0-100)
  - Generates key metrics and statistics

- **Professional Output**
  - Beautiful HTML evaluation document
  - Print-friendly formatting
  - Editable HTML before download
  - One-page executive summary with score

- **Evaluation Periods**
  - Quarterly (3 months)
  - Mid-Year (6 months)
  - Fiscal Year (12 months)
  - Custom periods

### 📊 Supported Fields

**Core Project Information**
- Project Name, Status, Description, Accomplishment

**Metrics & Business Value**
- Metric Value, Metric Label, Business Value

**Team & Collaboration**
- Team Size, Departments Involved

**Timeline**
- Start Date, End Date, Hours Invested

**Leadership Competencies**
- Respect for the Individual
- Act with Integrity
- Service to Customer/Member
- Strive for Excellence

**Narrative**
- Challenges Faced, Future Plans

## Quick Start

### 1. Install Dependencies

```bash
cd Evaluation-System
npm install
```

### 2. Start the Server

```bash
npm start
```

Server will run on `http://localhost:3001`

### 3. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:3001
```

### 4. Generate Your Evaluation

**Follow the 5-step process:**

1. **User Info** - Enter name, title, email, and evaluation period
2. **Input Data** - Upload CSV/Excel file or enter projects manually
3. **Map Columns** - Match your file columns to system fields
4. **Generate** - Convert data to evaluation with score
5. **Review** - Edit, preview, and download as HTML

## File Format Guide

### CSV Example

```csv
Project,Status,Description,Accomplishment,Impact,Hours
Refresh Guide,In Production,Modernized store operations platform,Deployed to production,50000 users,400
Activity-Hub,Active,Central platform for store assignments,Completed business case,27M annual value,200
```

### Excel Requirements

- First sheet will be used
- Headers in first row
- One project per row
- Supported extensions: .csv, .xlsx, .xls

## Column Mapping

When uploading a file:

1. System will detect available columns
2. Match each column to a system field:
   - **"i" icon** shows field description
   - **Required fields** marked with *
   - Required: Project Name, Description, Accomplishment
   - Optional: Everything else

3. Unmapped columns will be ignored

### Example Mapping

| Your Column | Maps To | Type |
|-------------|---------|------|
| Project | project_name | text |
| Status | project_status | select |
| What | description | textarea |
| Result | accomplishment | textarea |
| Value | metrics_value | number |
| Users | metrics_label | text |

## Field Descriptions

### Required Fields
- **Project Name** - Name of the project or initiative
- **Description** - What the project does and business purpose
- **Accomplishment** - Major achievement or deliverable completed

### Metrics Fields
- **Metric Value** - Quantifiable result (e.g., 50000 for 50,000 users)
- **Metric Label** - What the metric represents (e.g., "Users Served")
- **Business Value** - Dollar value or efficiency gain

### Collaboration Fields
- **Team Size** - Number of collaborators
- **Departments** - Comma-separated department list

### Competency Fields
- **Respect for Individual** - Team building, mentoring examples
- **Act with Integrity** - Ethics, compliance, accountability
- **Service to Customer/Member** - User needs, data-driven decisions
- **Strive for Excellence** - Innovation, learning, improvement

## Output Format

### Generated HTML Includes

1. **Header**
   - Employee name and title
   - Evaluation date and period
   - Performance score

2. **Executive Summary**
   - Overview of projects and impact
   - Leadership competency alignment
   - Key metrics summary

3. **Leadership Competencies Section**
   - Evidence for all 4 competencies
   - Specific examples from your work

4. **Project Portfolio**
   - Individual project narratives
   - Status, impact, collaboration
   - Challenges and solutions

5. **Statistics**
   - Total projects, hours, team members
   - Department spread
   - Project status breakdown

## Performance Score Calculation

The system calculates a 0-100 score based on:

- **Projects with metrics** (20 points) - Shows quantified impact
- **Team collaboration** (15 points) - Cross-functional breadth
- **Team size** (15 points) - Coordination complexity
- **Production projects** (20 points) - Delivered outcomes
- **Competency coverage** (10 points) - Leadership alignment
- **Base score** (50 points) - Foundation

**Score Ratings:**
- 80+: Exceeds Expectations ⭐
- 70-79: Meets Expectations ✓
- Below 70: Developing 📈

## Use Cases

### Self-Evaluation Preparation
Upload previous evaluation's project list, map columns, auto-generate updated narrative with new metrics.

### Progress Tracking
Generate evaluations quarterly to track growth against leadership competencies.

### Team Manager Review
Collect employee project data via spreadsheet, generate standardized evaluations for comparison.

### Promotion Packages
Generate professional evaluation documents ready for promotion/calibration conversations.

## Troubleshooting

### File Upload Issues

**"Supported file type: xlsx"**
- File extension not recognized
- Solution: Save as .csv or .xlsx

**"Failed to parse file"**
- File is corrupted or invalid format
- Solution: Verify file can open in Excel/Sheets

**"No data provided"**
- File is empty
- Solution: Verify file has content and headers

### Mapping Issues

**"Missing required fields"**
- One of: Project Name, Description, Accomplishment not mapped
- Solution: Map each required field from your columns

**"Column not appearing in dropdown"**
- System couldn't detect column
- Solution: Verify file has headers and data

### Generation Issues

**Evaluation won't generate**
- Missing required fields in data
- Solution: Check validation errors, ensure all rows have project name

## API Reference

### POST /api/upload
Upload and parse CSV/Excel file

**Request:**
```
Content-Type: multipart/form-data
file: <binary>
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "totalRows": 100,
  "availableColumns": ["Project", "Status", ...]
}
```

### POST /api/evaluate
Generate evaluation from mapped data

**Request:**
```json
{
  "data": [{project: "...", ...}],
  "columnMappings": {"Project": "project_name", ...},
  "userInfo": {"name": "...", "period": "..."}
}
```

**Response:**
```json
{
  "success": true,
  "evaluation": {...},
  "score": 85,
  "summary": {...}
}
```

### POST /api/download-html
Generate and download HTML file

## Future Enhancements

- [ ] Integration with Activity-Hub platform
- [ ] Database storage for evaluation history
- [ ] Recurring evaluation schedules
- [ ] Team calibration view
- [ ] Export to Word/PDF formats
- [ ] Email integration for reminders
- [ ] Comparison between evaluation periods
- [ ] Customizable templates

## Development

### Project Structure
```
Evaluation-System/
├── server/
│   ├── index.js              # Express server
│   ├── config.js             # Field definitions
│   ├── dataProcessor.js      # File parsing & mapping
│   ├── evaluationEngine.js   # Evaluation generation
│   └── templateEngine.js     # HTML output
├── client/
│   ├── index.html            # UI interface
│   └── app.js                # Client logic
├── package.json              # Dependencies
└── README.md
```

### Tech Stack
- **Backend**: Node.js, Express, CSV-parser, XLSX
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **File Types**: CSV, Excel (.xlsx, .xls)

### Environment Variables

Create `.env` file (optional):
```
PORT=3001
NODE_ENV=development
```

## License

Internal use only

## Support

For issues or feature requests, contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Status**: Production Ready
