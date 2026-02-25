#!/usr/bin/env python3
"""
Configuration file for Manager Change Detection System.
Modify these settings to customize the snapshot behavior.
"""

from pathlib import Path

# OneDrive configuration
ONEDRIVE_FOLDER = "ManagerSnapshots"  # Folder in your OneDrive root
SNAPSHOT_FILENAME_PATTERN = "manager_snapshot_{date}.json"  # {date} will be replaced with YYYY-MM-DD

# Roles to track
ROLES_TO_TRACK = [
    "Store Manager",
    "Market Manager",
    "Regional General Manager",
    "DC General Manager",
    "DC Assistant General Manager"
]

# SDL (Store Directory Lookup) configuration
SDL_URL = "https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/"
SDL_SEARCH_TIMEOUT = 30  # seconds

# Location Filters - Only track specific types of locations
FILTER_ENABLED = True

# Operating Status Filter - Exclude specific status codes
# Code 7: (doesn't exist in data)
# Code 8: TEMPORARILY CLOSED
EXCLUDE_OPERATING_STATUS_CODES = [7, 8]

# Base Division Filter - Only track these divisions
INCLUDE_BASE_DIVISIONS = [
    "WAL-MART STORES INC.",
    "SAM'S CLUB"
]

# Banner Filter - Only track these banner types
INCLUDE_BANNERS = [
    "WM Supercenter",
    "Neighborhood Market",
    "Wal-Mart",
    "Sam's Club"
]

# Expected location count after filters (for validation)
EXPECTED_LOCATION_COUNT = 5207  # Approximate - will vary slightly with openings/closings

# VPN Retry Configuration
VPN_RETRY_ENABLED = True
VPN_MAX_RETRY_DAYS = 7  # Keep trying for up to 7 days
VPN_RETRY_INTERVAL_HOURS = 1  # Check every hour

# Email notification configuration
EMAIL_ENABLED = True  # Set to True to enable email notifications
EMAIL_METHOD = "MSGRAPH"  # Options: "MSGRAPH" (Microsoft Graph), "HERMES" (future)

# Test mode - send all emails to these addresses instead of distribution lists
TEST_MODE = True
TEST_EMAILS = [
    "Kristine.Torres@walmart.com",
    "Matthew.Farnworth@walmart.com",
    "Kendall.Rush@walmart.com"
]  # Test recipients during testing phase
TEST_EMAIL = TEST_EMAILS[0]  # Backward compatibility

# Distribution lists per role type (will be used when TEST_MODE = False)
EMAIL_DISTRIBUTION = {
    "Store Manager": [
        "jhendr6@homeoffice.wal-mart.com",  # You, for now
        # Add more emails later: "market.manager@homeoffice.wal-mart.com", "hr.team@homeoffice.wal-mart.com"
    ],
    "Club Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    "Market Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    "Regional General Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    "DC General Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    "DC Assistant General Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    "Fulfillment Center Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    "Transportation Manager": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
    # Default for any other roles
    "_default": [
        "jhendr6@homeoffice.wal-mart.com",
    ],
}

# Logging configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "manager_snapshot.log"
