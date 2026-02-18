# Email Reporting and Notifications System

## Overview

The Intake Hub Email Reporting system allows users to create automated, scheduled email reports based on their project data. Users can configure custom reports with specific filters, columns, content types, and delivery schedules.

## Features

### 🎯 Core Capabilities

- **Custom Report Configuration**: Create multiple report configurations with unique settings
- **Flexible Filtering**: Filter reports by Partner, Business Organization, Store Area, Owner, Phase, Health, and more
- **Content Type Selection**: Choose from 13 different content types:
  - Overview (project/facility counts)
  - My Actions (incomplete tasks)
  - Counts (breakdowns by Business Org, Store Area)
  - New Cards
  - Upcoming items
  - Notes
  - Activity Feeds (Details, Files, Links, Flow, Actions, Facilities)

### 📅 Scheduling Options

- **Frequencies**: Daily, Weekly, Bi-Weekly, Monthly, or Custom
- **Delivery Time**: Specify exact time for report delivery
- **Day Selection**: Choose specific day of week for weekly reports (e.g., Friday mornings)
- **Active/Inactive Toggle**: Pause and resume reports without deleting configuration

### 📧 Delivery Options

- **Multiple Recipients**: Primary email + CC list
- **Format Options**:
  - Email Body (HTML formatted)
  - PDF Attachment
  - Both Email + PDF
- **Timeframe Selection**: Current Day, Week, Month, Year, or Last 7/30 days

### 📊 Column Customization

**Standard Columns** (always included):
- Intake Card Number
- Title (with hyperlink)
- Facility Total Count

**Optional Columns**:
- Partner
- Business Organization
- Store Area
- Owner
- Phase
- Facility Phase
- Health Status
- Projected Completion Date
- Implementation WM Week
- Director
- SR Director
- Facility Type
- SC Count, NHM Count, Div1 Count, Other Count

## Architecture

### Backend Components

#### 1. **email_report_models.py**
Data models and configurations:
- `EmailReportConfig`: Complete report configuration
- `ReportContentType`: Enum of available content types
- `ReportFrequency`: Scheduling frequency options
- `ReportColumnConfig`: Column selection configuration
- `ReportFilterConfig`: Filter criteria

#### 2. **email_service.py**
Report generation and delivery:
- `EmailReportService`: Main service class
- `generate_and_send_report()`: Generates HTML and PDF reports
- `_gather_report_data()`: Collects data from BigQuery
- `_generate_html_report()`: Creates styled HTML email
- `_generate_pdf_report()`: Creates PDF attachment
- `_send_email()`: Sends via SMTP

#### 3. **report_scheduler.py**
Scheduled execution management:
- `ReportScheduler`: Manages all scheduled reports
- Uses APScheduler for cron-based scheduling
- Stores configurations in JSON file
- Logs execution history

#### 4. **main.py** (Updated)
REST API endpoints:
- `GET /api/reports/configs` - List all report configurations
- `GET /api/reports/configs/{id}` - Get specific configuration
- `POST /api/reports/configs` - Create new configuration
- `PUT /api/reports/configs/{id}` - Update configuration
- `DELETE /api/reports/configs/{id}` - Delete configuration
- `POST /api/reports/configs/{id}/toggle` - Enable/disable report
- `POST /api/reports/generate` - Generate report immediately
- `GET /api/reports/logs` - View execution logs
- `GET /api/reports/options` - Get available configuration options

### Frontend Component

#### **reports.html**
Full-featured management interface:
- View all configured reports
- Create/Edit/Delete report configurations
- Test reports immediately
- Pause/Resume scheduled reports
- Modern, responsive UI with modal dialogs

## Installation & Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `apscheduler==3.10.4` - Scheduled task execution
- `reportlab==4.0.7` - PDF generation
- `email-validator==2.1.0` - Email validation

### 2. Environment Variables

Add to your `.env` file:

```bash
# SMTP Configuration (for Walmart internal use)
SMTP_SERVER=mailhub.wal-mart.com
SMTP_PORT=25
FROM_EMAIL=IntakeHub-Reports@walmart.com
```

### 3. Start the Backend

The scheduler automatically starts with the FastAPI application:

```bash
python main.py
```

You should see:
```
✅ Email report scheduler initialized
📁 Loaded X report configurations
```

### 4. Access the Reports Interface

Navigate to: `http://localhost:8001/reports.html`

## Usage Guide

### Creating a Report

1. **Click "Create New Report"**
2. **Fill in Basic Info**:
   - Report Name (e.g., "Weekly Partner Status")
   - Your User ID
   - Primary Email
   - Optional CC Emails

3. **Select Content Types**:
   - Check boxes for desired content (Overview, Counts, New, etc.)

4. **Configure Columns**:
   - Standard columns always included
   - Select additional optional columns

5. **Set Filters** (optional):
   - Partner names (comma-separated)
   - Store Area
   - Business Organization
   - Other filters

6. **Configure Schedule**:
   - Frequency (Daily, Weekly, etc.)
   - Day of Week (for weekly reports)
   - Delivery Time
   - Report Format (Email/PDF/Both)
   - Timeframe(s)

7. **Save Configuration**

### Testing a Report

Click the "🧪 Test" button on any report card to:
- Generate report immediately
- Optionally send to different email for testing
- Verify content and formatting

### Managing Reports

- **Edit**: Click "✏️ Edit" to modify configuration
- **Pause/Resume**: Click "⏸️ Pause" or "▶️ Resume" to control delivery
- **Delete**: Click "🗑️" to permanently remove configuration

### Viewing Logs

Access execution history via API:
```bash
GET /api/reports/logs?config_id={id}&limit=50
```

## Data Storage

### Report Configurations
- Stored in: `backend/report_configs.json`
- Format: JSON array of configurations
- Automatically saved on create/update/delete

### Execution Logs
- Stored in: `backend/report_execution_log.json`
- Contains: timestamp, success status, recipients, errors
- Limited to last 1000 entries

## Email Template

Reports are sent as professionally styled HTML emails featuring:
- **Header**: Walmart blue gradient with report name and timestamp
- **Overview Section**: Key metrics in stat cards
- **Counts Section**: Tables with breakdowns
- **Projects Table**: Paginated list with selected columns
- **Responsive Design**: Works on desktop and mobile
- **Branded Styling**: Walmart colors and typography

### PDF Format

When PDF is enabled:
- Landscape orientation for wider tables
- Professional table styling
- Repeating headers on multiple pages
- Optimized for printing

## API Examples

### Create a Report Configuration

```bash
POST /api/reports/configs
Content-Type: application/json

{
  "user_id": "user123",
  "report_name": "Weekly Partner Status",
  "content_types": ["Overview", "Counts", "New"],
  "frequency": "Weekly",
  "delivery_day": "Friday",
  "delivery_time": "09:00",
  "timeframes": ["Current Week"],
  "primary_email": "user@walmart.com",
  "cc_emails": ["team@walmart.com"],
  "report_format": "Both",
  "columns": {
    "partner": true,
    "phase": true,
    "owner": true
  },
  "filters": {
    "partner": ["Operations"]
  }
}
```

### Generate Report Immediately

```bash
POST /api/reports/generate
Content-Type: application/json

{
  "config_id": "abc-123-def-456",
  "override_email": "test@walmart.com"  // Optional
}
```

### Get All Reports for User

```bash
GET /api/reports/configs?user_id=user123
```

## Troubleshooting

### Reports Not Sending

1. **Check Scheduler Status**:
   - Look for "✅ Email report scheduler initialized" in logs
   - Verify report is marked as "Active"

2. **Check SMTP Configuration**:
   - Ensure you're on Walmart network
   - Verify `SMTP_SERVER` environment variable
   - Test with manual generation

3. **Check Execution Logs**:
   ```bash
   GET /api/reports/logs?config_id={id}
   ```

### PDF Generation Issues

If PDFs aren't generating:
1. Verify reportlab is installed: `pip install reportlab==4.0.7`
2. Check for error messages in logs
3. Test with "Email Body" format first

### Scheduling Issues

1. **Verify Cron Syntax**: Check delivery day and time
2. **Check Timezone**: Server uses UTC by default
3. **Restart Scheduler**: Restart the FastAPI application

## Future Enhancements

Potential additions (requiring additional database tables):

1. **Notes Section**: 
   - Requires `notes` table with project associations
   - Would show recent notes across all projects

2. **My Actions Section**:
   - Requires `tasks` or `actions` table
   - Show incomplete tasks assigned to user

3. **Activity Feed**:
   - Requires `activity_log` table
   - Track changes to Details, Files, Links, etc.

4. **Health Status Tracking**:
   - Requires health status field in projects table
   - Color-coded indicators in reports

5. **Advanced Filtering**:
   - Director/SR Director filters
   - Facility Type filters
   - Custom date ranges

6. **Report Templates**:
   - Save common configurations as templates
   - Clone existing configurations

7. **User Authentication**:
   - Integrate with Walmart SSO
   - User-specific permissions

## Security Considerations

1. **Email Validation**: All emails validated via `email-validator`
2. **User Isolation**: Reports filtered by `user_id`
3. **Rate Limiting**: Consider adding rate limits for manual generation
4. **Authentication**: Currently basic - should integrate with corporate auth

## Support

For issues or questions:
1. Check execution logs: `/api/reports/logs`
2. Review backend console output
3. Contact: Intake Hub Development Team

## Summary

The Email Reporting system provides comprehensive, automated reporting capabilities for Intake Hub users. With flexible configuration options, professional formatting, and reliable scheduled delivery, users can stay informed about their projects without manual effort.

**Key Benefits**:
- ✅ Automated weekly/daily reports
- ✅ Customizable content and filters
- ✅ Professional HTML + PDF output
- ✅ Easy management interface
- ✅ Scheduled delivery via email
- ✅ Test before scheduling
- ✅ Comprehensive logging

Start creating your first report today at `/reports.html`!
