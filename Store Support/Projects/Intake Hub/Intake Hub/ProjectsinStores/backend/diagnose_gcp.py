#!/usr/bin/env python3
"""
Quick diagnostic script - checks BigQuery client + shows authentication options
No credentials needed - just verifies your system setup
"""

import os
import sys
from pathlib import Path

def diagnose_setup():
    print("\n" + "="*70)
    print("BigQuery Setup Diagnostic")
    print("="*70)
    
    # Check 1: BigQuery package
    print("\n1️⃣  Checking BigQuery Package...")
    try:
        import google.cloud.bigquery
        print("   ✅ google-cloud-bigquery is installed")
    except ImportError:
        print("   ❌ google-cloud-bigquery NOT installed")
        print("   Install with: pip install google-cloud-bigquery")
        return False
    
    # Check 2: Google Auth package
    print("\n2️⃣  Checking Google Auth Package...")
    try:
        import google.auth
        print("   ✅ google-auth is installed")
    except ImportError:
        print("   ❌ google-auth NOT installed")
        print("   Install with: pip install google-auth")
        return False
    
    # Check 3: Environment variable
    print("\n3️⃣  Checking Authentication Methods...")
    
    creds_env = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_env:
        print(f"   ✅ GOOGLE_APPLICATION_CREDENTIALS set:")
        print(f"      {creds_env}")
        if os.path.exists(creds_env):
            print(f"      ✅ File exists")
        else:
            print(f"      ❌ File NOT found - check path")
    else:
        print("   ⚠️  GOOGLE_APPLICATION_CREDENTIALS not set")
        print("      (Try gcloud auth application-default login)")
    
    # Check 4: Local gcloud credentials
    print("\n4️⃣  Checking gcloud Credentials Cache...")
    gcloud_creds = Path.home() / ".config/gcloud/application_default_credentials.json"
    if gcloud_creds.exists():
        print(f"   ✅ Found: {gcloud_creds}")
    else:
        print(f"   ⚠️  Not found: {gcloud_creds}")
    
    # Check 5: Provide next steps
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
Option A: Service Account JSON (Recommended)
───────────────────────────────────────────
1. Ask GCP admin for service-account-key.json
2. Save to: backend/service-account-key.json
3. Set environment variable:
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account-key.json"
4. Run: python test_bigquery_access.py

Option B: gcloud CLI Authentication
────────────────────────────────────
1. Open PowerShell as Administrator
2. Run: gcloud auth application-default login
3. Complete browser authentication
4. Run: python test_bigquery_access.py

Option C: Check with Your GCP Admin
────────────────────────────────────
Ask if credentials are already configured on this system
    """)
    
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    diagnose_setup()
