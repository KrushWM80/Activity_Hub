"""
Job Codes Dashboard Configuration
Centralized settings for URL, IP, and connection details.
Modify these settings to control where the dashboard is accessible.
"""

from pathlib import Path

# ============================================================================
# CONNECTION CONFIGURATION
# ============================================================================
# This controls how users access Job Codes Dashboard

# Current active connection method
ACTIVE_CONNECTION = "IP"  # Options: "HOSTNAME" or "IP"

# IP-based access (direct, no DNS dependency)
IP_ADDRESS = "10.97.114.181"
IP_PORT = 8080
IP_URL = f"http://{IP_ADDRESS}:{IP_PORT}/static/index.html#"

# Hostname-based access (requires DNS fix)
# NOTE: DNS currently points 10.97.108.66 (wrong). Pending IT fix to point to 10.97.114.181
HOSTNAME = "leus62315243171.homeoffice.wal-mart.com"
HOSTNAME_PORT = 8080
HOSTNAME_URL = f"http://{HOSTNAME}:{HOSTNAME_PORT}/static/index.html#"

# ============================================================================
# ACTIVE URL (Choose which connection to use)
# ============================================================================
if ACTIVE_CONNECTION == "IP":
    ACCESS_URL = IP_URL
    ACCESS_DESCRIPTION = "IP Address (Direct - No DNS)"
elif ACTIVE_CONNECTION == "HOSTNAME":
    ACCESS_URL = HOSTNAME_URL
    ACCESS_DESCRIPTION = "Hostname (Requires DNS fix)"
else:
    ACCESS_URL = IP_URL
    ACCESS_DESCRIPTION = "IP Address (Direct - No DNS) [Default]"

# ============================================================================
# SERVER CONFIGURATION
# ============================================================================
HOST = "0.0.0.0"
PORT = 8080

# ============================================================================
# DATABASE & FILE CONFIGURATION
# ============================================================================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEAMING_DIR = BASE_DIR.parent
JOB_CODES_DIR = TEAMING_DIR.parent / "Job Codes"

# Data files
TEAMING_DATA_FILE = TEAMING_DIR / "TMS Data (3).xlsx"
POLARIS_DATA_FILE = TEAMING_DIR / "polaris_job_codes.csv"
USER_COUNTS_FILE = TEAMING_DIR / "polaris_user_counts.csv"
JOB_CODE_MASTER_EXCEL = JOB_CODES_DIR / "Job_Code_Master_Table.xlsx"

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================
NOTIFY_EMAIL = "ATCTEAMSUPPORT@walmart.com"
SMTP_SERVER = "smtp-gw1.homeoffice.wal-mart.com"
SMTP_PORT = 25
FROM_EMAIL = "JobCodeTeamingDashboard@walmart.com"

# ============================================================================
# STATUS
# ============================================================================
"""
CURRENT STATUS (March 12, 2026):
================================

✓ Job Codes Backend: RUNNING on 10.97.114.181:8080
✓ Frontend: ACCESSIBLE via http://10.97.114.181:8080/static/index.html#

Issue: Hostname DNS points to wrong IP
  - Hostname: leus62315243171.homeoffice.wal-mart.com
  - DNS resolves to: 10.97.108.66 (no service listening)
  - Actual service: 10.97.114.181:8080
  
✓ SOLUTION ACTIVE: Using IP-based access (10.97.114.181:8080)
  
NEXT STEP: Contact IT to update DNS
  - Request: Update A record for leus62315243171.homeoffice.wal-mart.com
  - To point to: 10.97.114.181 (instead of 10.97.108.66)
  - Once DNS is fixed: Switch ACTIVE_CONNECTION to "HOSTNAME" above
"""
