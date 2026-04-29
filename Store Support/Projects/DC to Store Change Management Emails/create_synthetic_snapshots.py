#!/usr/bin/env python3
"""
Create Synthetic Manager Snapshots for Testing
Generates test snapshots for April 17 and May 1, 2026
Allows full pipeline testing without SDL scraper access

⚠️ WARNING: THIS CREATES TEST DATA ONLY
All manager names, stores, and changes are FAKE/SYNTHETIC
Used only for testing email pipeline functionality

PRODUCTION DATA comes from:
  - sdl_scraper.py → Real SDL system export (runs May 1 @ 05:00 AM)
  - Generates actual Walmart manager data
  - Replaces synthetic test data automatically

See: DATA_SOURCE_CLARIFICATION.md
"""

import json
from pathlib import Path
from datetime import datetime

# Create snapshots_local directory if needed
snapshot_dir = Path("snapshots_local")
snapshot_dir.mkdir(exist_ok=True)

# Baseline snapshot (April 17 - PC-06)
april_17_snapshot = {
    "generation_time": "2026-04-17T08:00:00",
    "date": "2026-04-17",
    "managers": [
        {"location_id": "100", "location_name": "Rogers, AR", "role": "Store Manager", "manager_name": "JAMES RICHARDSON", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTHEAST"},
        {"location_id": "103", "location_name": "Bentonville, AR", "role": "Store Manager", "manager_name": "LISA ANDERSON", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTHEAST"},
        {"location_id": "108", "location_name": "Fort Smith, AR", "role": "Store Manager", "manager_name": "MARK STEPHENS", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        {"location_id": "121", "location_name": "Little Rock, AR", "role": "Store Manager", "manager_name": "PATRICIA LOPEZ", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        {"location_id": "123", "location_name": "Hot Springs, AR", "role": "Store Manager", "manager_name": "ROBERT WILLIAMS", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        {"location_id": "125", "location_name": "Texarkana, AR", "role": "Store Manager", "manager_name": "JENNIFER MARTINEZ", "location_type": "Store", "market": "TEXAS", "region": "SOUTH"},
        {"location_id": "130", "location_name": "Pine Bluff, AR", "role": "Store Manager", "manager_name": "DAVID BROWN", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        {"location_id": "136", "location_name": "Fayetteville, AR", "role": "Store Manager", "manager_name": "SUSAN TAYLOR", "location_type": "Store", "market": "ARKANSAS", "region": "NORTHWEST"},
    ]
}

# May 1 snapshot (PC-07) - with some manager changes
may_01_snapshot = {
    "generation_time": "2026-05-01T08:00:00",
    "date": "2026-05-01",
    "managers": [
        # PC-07 detects changes:
        # 1. Rogers (100): JAMES RICHARDSON -> CHRISTOPHER JONES
        {"location_id": "100", "location_name": "Rogers, AR", "role": "Store Manager", "manager_name": "CHRISTOPHER JONES", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTHEAST"},
        # 2. Bentonville (103): LISA ANDERSON -> MARGARET WILSON
        {"location_id": "103", "location_name": "Bentonville, AR", "role": "Store Manager", "manager_name": "MARGARET WILSON", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTHEAST"},
        # 3. Fort Smith (108) - Stays same
        {"location_id": "108", "location_name": "Fort Smith, AR", "role": "Store Manager", "manager_name": "MARK STEPHENS", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        # 4. Little Rock (121): PATRICIA LOPEZ -> LAURA ANDERSON
        {"location_id": "121", "location_name": "Little Rock, AR", "role": "Store Manager", "manager_name": "LAURA ANDERSON", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        # 5. Hot Springs (123) - Stays same
        {"location_id": "123", "location_name": "Hot Springs, AR", "role": "Store Manager", "manager_name": "ROBERT WILLIAMS", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        # 6. Texarkana (125) - Stays same
        {"location_id": "125", "location_name": "Texarkana, AR", "role": "Store Manager", "manager_name": "JENNIFER MARTINEZ", "location_type": "Store", "market": "TEXAS", "region": "SOUTH"},
        # 7. Pine Bluff (130): DAVID BROWN -> THOMAS GARCIA
        {"location_id": "130", "location_name": "Pine Bluff, AR", "role": "Store Manager", "manager_name": "THOMAS GARCIA", "location_type": "Store", "market": "ARKANSAS", "region": "SOUTH"},
        # 8. Fayetteville (136) - Stays same
        {"location_id": "136", "location_name": "Fayetteville, AR", "role": "Store Manager", "manager_name": "SUSAN TAYLOR", "location_type": "Store", "market": "ARKANSAS", "region": "NORTHWEST"},
    ]
}

# Write snapshots
april_file = snapshot_dir / "manager_snapshot_2026-04-17.json"
may_file = snapshot_dir / "manager_snapshot_2026-05-01.json"

try:
    with open(april_file, 'w') as f:
        json.dump(april_17_snapshot, f, indent=2)
    print(f"[OK] Created: {april_file}")
    print(f"     Managers: {len(april_17_snapshot['managers'])}")
    
    with open(may_file, 'w') as f:
        json.dump(may_01_snapshot, f, indent=2)
    print(f"[OK] Created: {may_file}")
    print(f"     Managers: {len(may_01_snapshot['managers'])}")
    print()
    print("Snapshots ready for PC-07 testing!")
    print()
    print("CHANGES DETECTED (April 17 → May 1):")
    print("  1. ATLANTA GM: JAMES RICHARDSON → CHRISTOPHER JONES")
    print("  2. HARRISON AGM: LISA ANDERSON → MARGARET WILSON")
    print("  3. DENVER AGM: PATRICIA LOPEZ → LAURA ANDERSON")
    print("  4. KANSAS_CITY GM: DAVID BROWN → THOMAS GARCIA")
    print()
    print("Ready to test: python send_paycycle_production_email_generic.py 7")
    
except Exception as e:
    print(f"[ERROR] Failed to create snapshots: {e}")
    exit(1)
