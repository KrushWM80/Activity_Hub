# Job Code Teaming Dashboard

A local web dashboard for managing job codes and their teaming assignments.

## Features

- **User Authentication**: Only approved users can access the dashboard
- **Job Code Overview**: View all job codes with their teaming status (Assigned/Missing)
- **Team Assignment Requests**: Users can request to assign job codes to teams
- **Admin Approval Workflow**: Admins approve/reject requests before they're processed
- **Export for TMS Update**: Export approved requests in a format ready for TMS API or manual update

## Quick Start

### 1. Start the Server

Double-click `start_server.bat` or run:

```powershell
cd dashboard
C:\Users\krush\.code-puppy-venv\Scripts\python.exe backend\main.py
```

### 2. Access the Dashboard

Open your browser to: **http://leus62315243171.homeoffice.wal-mart.com:8080/static/index.html**

### 3. Default Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Change this password immediately after first login!**

## User Roles

### Admin
- View all job codes and requests
- Approve/reject user registrations
- Approve/reject teaming update requests
- Export approved requests for TMS update
- Manage user roles

### User
- View all job codes
- Submit teaming update requests
- View their own request history

## Workflow

1. **User Registration**: New users register and wait for admin approval
2. **View Job Codes**: See which job codes are missing teaming assignments
3. **Submit Request**: Select a job code and choose a team to assign it to
4. **Admin Review**: Admin reviews and approves/rejects the request
5. **Export**: Admin exports approved requests for TMS update

## Data Files

The dashboard uses these data sources:
- `../TMS Data (3).xlsx` - Current teaming configurations
- `../polaris_job_codes.csv` - Job codes from Polaris/BigQuery

Generated data:
- `data/users.json` - User accounts
- `data/sessions.json` - Active sessions
- `data/update_requests.json` - Teaming update requests

## TMS API Integration

When ready to integrate with the TMS API, the export data includes:
- `jobCode` - The job code number
- `deptNumber` - Department number
- `divNumber` - Division number
- `teamName` - Target team name
- `teamId` - Target team ID
- `workgroupName` - Workgroup name
- `workgroupId` - Workgroup ID

This can be used to build API requests to `https://tms-metadata-ui.us.walmart.com/` or similar endpoints.

## Troubleshooting

### Server won't start
- Ensure Python is installed
- Check that required packages are installed: `fastapi`, `uvicorn`, `pandas`, `openpyxl`

### Can't login
- Check that the `data/users.json` file exists
- Reset by deleting `data/users.json` (will recreate default admin)

### Data not loading
- Ensure `TMS Data (3).xlsx` and `polaris_job_codes.csv` exist in the parent folder
