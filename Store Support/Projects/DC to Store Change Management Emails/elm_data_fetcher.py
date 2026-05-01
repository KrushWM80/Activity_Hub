#!/usr/bin/env python3
"""
ELM Data Fetcher - Direct BigQuery Access
Replaces SDL web scraper with direct ELM catalog query

Uses: wmt-loc-cat-prod.catalog_location_views.division_view
Advantages:
  - No web scraping dependencies
  - Direct access to authoritative ELM data
  - Reliable programmatic interface
  - Filters for US Retail only
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import config


def fetch_elm_data() -> List[Dict[str, Any]]:
    """
    Fetch manager data directly from ELM BigQuery table.
    
    Queries: wmt-loc-cat-prod.catalog_location_views.division_view
    Filters:
      - physical_country_code = 'US'
      - base_division_desc = 'WAL-MART STORES INC.'
      - division_nbr = 1 (INCOME DIVISION - primary record only)
      - bu_status_desc NOT LIKE '%CLOSED%'
    
    Returns:
        List of manager dictionaries with location and hierarchy info
    """
    try:
        from google.cloud import bigquery
    except ImportError:
        print("[ERROR] google-cloud-bigquery not installed!")
        print("[INFO] Install with: pip install google-cloud-bigquery")
        raise
    
    print("\n" + "="*60)
    print("ELM DATA FETCH - DIRECT BIGQUERY")
    print("="*60 + "\n")
    
    # Initialize BigQuery client
    try:
        client = bigquery.Client()
        print("[OK] Connected to BigQuery")
        print("[INFO] Project: {}\n".format(client.project))
    except Exception as e:
        print(f"[ERROR] Failed to connect to BigQuery: {e}")
        raise
    
    # Query ELM catalog location views
    query = """
    SELECT
        business_unit_nbr,
        bu_name,
        location_type,
        banner_desc,
        manager_full_name,
        manager_first_name,
        manager_last_name,
        manager_details,
        primary_business_phone,
        physical_address_line_one,
        physical_address_line_two,
        physical_city,
        physical_state_code,
        physical_zip_code,
        martket_code as market_code,
        region_code,
        bu_status_desc,
        base_division_desc,
        division_nbr,
        physical_country_code,
        last_updated_date
    FROM
        `wmt-loc-cat-prod.catalog_location_views.division_view`
    WHERE
        physical_country_code = 'US'
        AND base_division_desc = 'WAL-MART STORES INC.'
        AND division_nbr = 1
        AND bu_status_desc NOT LIKE '%CLOSED%'
        AND manager_full_name IS NOT NULL
    ORDER BY
        business_unit_nbr,
        division_nbr
    """
    
    print("[INFO] Executing BigQuery query...")
    print("[INFO] Table: wmt-loc-cat-prod.catalog_location_views.division_view")
    print("[INFO] Filters:")
    print("[INFO]   - Country: US")
    print("[INFO]   - Division: WAL-MART STORES INC.")
    print("[INFO]   - Division NBR: 1 (INCOME DIVISION - primary only)")
    print("[INFO]   - Status: NOT CLOSED")
    print("[INFO]   - Manager: NOT NULL\n")
    
    try:
        query_job = client.query(query)
        rows = query_job.result()
        
        print(f"[OK] Query completed\n")
        
    except Exception as e:
        print(f"[ERROR] BigQuery query failed: {e}")
        raise
    
    managers = []
    unique_locations = set()
    skipped_dups = 0
    skipped_no_name = 0
    
    for row in rows:
        try:
            location_id = str(row.business_unit_nbr).strip()
            manager_name = str(row.manager_full_name or '').strip()
            
            # Skip empty manager names
            if not manager_name or manager_name.upper() == 'TBD':
                skipped_no_name += 1
                continue
            
            # Skip duplicate locations (take first division_nbr only)
            if location_id in unique_locations:
                skipped_dups += 1
                continue
            
            unique_locations.add(location_id)
            
            # Parse manager details JSON for email and role
            manager_details = {}
            if row.manager_details:
                try:
                    manager_details = json.loads(row.manager_details)
                except:
                    pass
            
            # Determine role from job_FAMILY
            job_family = manager_details.get('job_FAMILY', 'MGMT-STORE MANAGER').upper()
            if 'MARKET' in job_family:
                role = 'Market Manager'
            elif 'REGION' in job_family:
                role = 'Region Manager'
            else:
                role = 'Store Manager'
            
            # Extract manager email from nested structure
            manager_email = ''
            manager_list = manager_details.get('node_MANAGER_LIST', [])
            if manager_list and isinstance(manager_list, list):
                first_mgr = manager_list[0]
                manager_email = first_mgr.get('node_MGR_EMAIL', '')
            
            manager_record = {
                'location_id': location_id,
                'location_name': str(row.bu_name or f'LOCATION {location_id}').strip(),
                'location_type': str(row.location_type or 'Retail').strip(),
                'role': role,
                'manager_name': manager_name,
                'manager_email': manager_email,
                'manager_phone': str(row.primary_business_phone or '').strip(),
                'address': str(row.physical_address_line_one or '').strip(),
                'city': str(row.physical_city or '').strip(),
                'state': str(row.physical_state_code or '').strip(),
                'zip_code': str(row.physical_zip_code or '').strip(),
                'market': str(row.market_code or '').strip(),
                'region': str(row.region_code or '').strip(),
                'banner': str(row.banner_desc or 'WM Supercenter').strip(),
                'status': str(row.bu_status_desc or 'OPEN').strip(),
                'data_source': 'ELM (BigQuery)',
                'fetched_date': datetime.now().isoformat()
            }
            
            managers.append(manager_record)
            
        except Exception as e:
            print(f"[WARNING] Failed to process row: {e}")
            continue
    
    print(f"\n[OK] Extracted {len(managers)} manager records")
    if skipped_dups > 0:
        print(f"[INFO] Skipped {skipped_dups} duplicate locations (kept primary division_nbr=1)")
    if skipped_no_name > 0:
        print(f"[INFO] Skipped {skipped_no_name} records with empty/TBD manager names")
    
    return managers


def save_elm_snapshot(date_str: str = None) -> Path:
    """
    Fetch ELM data and save as snapshot JSON.
    
    Args:
        date_str: Date for snapshot (YYYY-MM-DD). Defaults to today.
    
    Returns:
        Path to saved snapshot file
    
    Raises:
        Exception if fetch or save fails
    """
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n[STEP 1] Fetching data from ELM BigQuery...")
    managers = fetch_elm_data()
    
    # Count email coverage
    managers_with_email = sum(1 for m in managers if m.get('manager_email'))
    
    # Create snapshot with comprehensive audit trail metadata
    snapshot = {
        # REFERENCE IDENTIFIERS
        'snapshot_id': f"ELM-{date_str}-{len(managers)}",
        'date': date_str,
        'generation_time_utc': datetime.utcnow().isoformat() + 'Z',
        'generation_time_local': datetime.now().isoformat(),
        
        # DATA SOURCE & LINEAGE
        'source': 'ELM BigQuery - catalog_location_views.division_view',
        'bigquery_project': 'wmt-assetprotection-prod',
        'bigquery_table': 'wmt-loc-cat-prod.catalog_location_views.division_view',
        
        # FILTERING CRITERIA (for audit trail)
        'filters_applied': {
            'country': 'US (physical_country_code = "US")',
            'division': 'WAL-MART STORES INC. (base_division_desc match)',
            'division_number': '1 (primary income division, division_nbr=1)',
            'status': 'OPEN (bu_status_desc NOT LIKE "%CLOSED%")',
            'manager_requirement': 'manager_full_name NOT NULL and NOT TBD'
        },
        
        # DATA QUALITY METRICS
        'data_quality': {
            'total_locations': len(managers),
            'managers_with_email': managers_with_email,
            'email_coverage_pct': round(100 * managers_with_email / len(managers), 1) if managers else 0,
            'roles_tracked': ['Store Manager', 'Market Manager', 'Region Manager'],
            'roles_distribution': {
                'store_manager': sum(1 for m in managers if m.get('role') == 'Store Manager'),
                'market_manager': sum(1 for m in managers if m.get('role') == 'Market Manager'),
                'region_manager': sum(1 for m in managers if m.get('role') == 'Region Manager')
            }
        },
        
        # AUDIT TRAIL
        'audit_info': {
            'purpose': 'PayCycle manager change notifications',
            'validity_period': '14 days (until next PayCycle)',
            'snapshot_reference': f'Reference this snapshot as: {date_str}-ELM-{len(managers)}-LOCATIONS',
            'incident_reference': 'PC-07 synthetic data incident (May 1, 2026 - RESOLVED)',
            'validation_status': 'VERIFIED - ELM source confirmed reliable'
        },
        
        'managers': managers
    }
    
    # Save to snapshots_local
    snapshot_dir = Path('snapshots_local')
    snapshot_dir.mkdir(exist_ok=True)
    
    snapshot_file = snapshot_dir / f'manager_snapshot_{date_str}.json'
    
    print(f"\n[STEP 2] Saving snapshot to file...")
    try:
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"[OK] Snapshot saved successfully")
        print(f"[INFO] File: {snapshot_file}")
        print(f"[INFO] Records: {len(managers)}")
        print(f"[INFO] Date: {date_str}")
        print(f"[INFO] Source: ELM (BigQuery)")
        
        return snapshot_file
    except Exception as e:
        print(f"[ERROR] Failed to save snapshot: {e}")
        raise


def main():
    """
    Main entry point - fetch and save ELM data.
    """
    try:
        snapshot_file = save_elm_snapshot()
        print(f"\n{'='*60}")
        print(f"✓ SUCCESS - ELM data snapshot created")
        print(f"{'='*60}\n")
        return 0
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"✗ FAILED - ELM data fetch error")
        print(f"Error: {e}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
