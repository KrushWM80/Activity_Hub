#!/usr/bin/env python3
"""
Find Kendall Rush's Leadership Chain from CoreHR and Polaris Data
- Direct Manager
- Skip-Level Manager (Manager's Manager)
"""

import os
from google.cloud import bigquery
import pandas as pd

# Set credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
)

client = bigquery.Client()

def search_kendall_corehr():
    """Search CoreHR for Kendall Rush profile including manager info"""
    print("\n" + "=" * 80)
    print("SEARCHING: CoreHR - UNIFIED_PROFILE_SENSITIVE_VW")
    print("=" * 80)
    
    # First, let's see what fields are available for manager relationships
    query = """
    SELECT 
        userID,
        employeeID,
        personalInfo.legalFirstName,
        personalInfo.legalLastName,
        workRelationship.managerID,
        workRelationship.managerName,
        workRelationship.jobTitle,
        workRelationship.businessUnit,
        workRelationship.department,
        workRelationship.organization
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    WHERE LOWER(CONCAT(personalInfo.legalFirstName, ' ', personalInfo.legalLastName)) LIKE '%kendall%rush%'
       OR LOWER(personalInfo.legalFirstName) = 'kendall'
    LIMIT 10
    """
    
    try:
        print("\nQuery:")
        print(query)
        print("\nExecuting...")
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"\n✓ Found {len(df)} record(s):\n")
            print(df.to_string())
            return df
        else:
            print("\n✗ No records found for 'Kendall Rush'")
            return None
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def search_kendall_polaris():
    """Search Polaris for Kendall Rush's manager information"""
    print("\n" + "=" * 80)
    print("SEARCHING: Polaris - vw_polaris_current_schedule")
    print("=" * 80)
    
    query = """
    SELECT 
        worker_id,
        first_name,
        last_name,
        location_id,
        location_nm,
        job_code,
        job_nm,
        mgr_id,
        mgr_nm,
        hire_date,
        empl_type_code
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE LOWER(first_name) = 'kendall'
      AND LOWER(last_name) = 'rush'
    LIMIT 10
    """
    
    try:
        print("\nQuery:")
        print(query)
        print("\nExecuting...")
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"\n✓ Found {len(df)} record(s):\n")
            print(df.to_string())
            return df
        else:
            print("\n✗ No records found for Kendall Rush in Polaris")
            return None
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_manager_chain_polaris(manager_id: str):
    """Get manager's manager (skip-level) from Polaris"""
    print(f"\n" + "=" * 80)
    print(f"SEARCHING: Skip-Level Manager for manager_id: {manager_id}")
    print("=" * 80)
    
    query = f"""
    SELECT 
        worker_id,
        first_name,
        last_name,
        mgr_id,
        mgr_nm,
        job_nm,
        location_nm
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE worker_id = '{manager_id}'
    LIMIT 5
    """
    
    try:
        print("\nQuery:")
        print(query)
        print("\nExecuting...")
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        df = pd.DataFrame(rows)
        
        if not df.empty:
            print(f"\n✓ Found manager details:\n")
            print(df.to_string())
            return df
        else:
            print(f"\n✗ No manager details found for: {manager_id}")
            return None
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print("=" * 80)
    print("KENDALL RUSH ORGANIZATIONAL HIERARCHY SEARCH")
    print("=" * 80)
    
    # Search CoreHR
    print("\n[STEP 1] Searching CoreHR...")
    kendall_corehr = search_kendall_corehr()
    
    # Search Polaris
    print("\n[STEP 2] Searching Polaris...")
    kendall_polaris = search_kendall_polaris()
    
    # If found in Polaris, get manager chain
    if kendall_polaris is not None and not kendall_polaris.empty:
        print("\n[STEP 3] Getting Skip-Level Manager...")
        
        # Get manager ID
        manager_id = kendall_polaris.iloc[0].get('mgr_id')
        manager_nm = kendall_polaris.iloc[0].get('mgr_nm')
        
        print(f"\nKendall Rush's Direct Manager:")
        print(f"  Manager ID: {manager_id}")
        print(f"  Manager Name: {manager_nm}")
        
        if manager_id:
            # Get skip-level manager
            skip_level_df = get_manager_chain_polaris(manager_id)
    
    print("\n" + "=" * 80)
    print("SEARCH COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
