#!/usr/bin/env python3
"""Check raw Cosmos table for message body text with Summarized: sections"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# First, check if we can access the raw EDW table with msg_txt
print("=== Checking Raw Cosmos Table Schema ===")
try:
    raw_query = """
    SELECT column_name, data_type
    FROM `wmt-edw-prod.WW_SOA_DL_VM.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT'
    ORDER BY ordinal_position
    """
    rows = list(client.query(raw_query).result())
    print(f"Raw table columns: {len(rows)}")
    for r in rows:
        print(f"  {r.column_name} ({r.data_type})")
except Exception as e:
    print(f"Cannot access INFORMATION_SCHEMA: {e}")
    print("\nTrying direct query with LIMIT 1...")
    try:
        test_q = """
        SELECT *
        FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
        LIMIT 1
        """
        rows = list(client.query(test_q).result())
        if rows:
            for key in dict(rows[0]).keys():
                print(f"  {key}")
    except Exception as e2:
        print(f"Cannot access raw table: {e2}")

# Also check if there's a week_at_glance_summary or any text field populated
print("\n=== Checking week_at_glance_summary for ANY week ===")
try:
    wag_query = """
    SELECT DISTINCT WM_Week, FY, COUNT(*) as cnt
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE week_at_glance_summary IS NOT NULL
      AND week_at_glance_summary != ''
      AND FY >= 2027
    GROUP BY WM_Week, FY
    ORDER BY FY, WM_Week
    """
    rows = list(client.query(wag_query).result())
    if rows:
        print(f"Weeks with week_at_glance_summary data:")
        for r in rows:
            print(f"  FY{r.FY} Week {r.WM_Week}: {r.cnt} events")
    else:
        print("No weeks have week_at_glance_summary populated")
except Exception as e:
    print(f"Error: {e}")

# Check Headline content - does it have enough detail?
print("\n=== Sample Headlines with detail for Week 4 ===")
try:
    headline_query = """
    SELECT DISTINCT event_id, Store_Area, Headline, Title
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND Status LIKE '%Published%'
      AND Message_Type LIKE '%Store Updates%'
      AND Store_Area IN ('Fresh', 'Food', 'Consumables', 'Entertainment', 'Fashion', 'Hardlines', 'Home', 'Seasonal')
    ORDER BY Store_Area, Title
    """
    rows = list(client.query(headline_query).result())
    print(f"Merchant area events: {len(rows)}")
    for r in rows:
        print(f"  [{r.Store_Area}] {r.Headline}")
except Exception as e:
    print(f"Error: {e}")
