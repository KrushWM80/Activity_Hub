#!/usr/bin/env python3
"""Check raw Cosmos table format and msg_txt content"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check 1: What wm_yr_and_wk format does the raw table use?
print("=== Raw table: wm_yr_and_wk format samples ===")
try:
    q = """
    SELECT DISTINCT wm_yr_and_wk
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    ORDER BY wm_yr_and_wk DESC
    LIMIT 20
    """
    rows = list(client.query(q).result())
    print(f"Found {len(rows)} distinct wm_yr_and_wk values:")
    for r in rows:
        print(f"  {r.wm_yr_and_wk}")
except Exception as e:
    print(f"Error: {e}")

# Check 2: Get some event_ids from AMP ALL 2 and try to join them
print("\n=== Getting event_ids from Week 4 for cross-reference ===")
try:
    q2 = """
    SELECT DISTINCT event_id
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND Status LIKE '%Published%'
      AND Message_Type LIKE '%Store Updates%'
    LIMIT 5
    """
    rows = list(client.query(q2).result())
    event_ids = [r.event_id for r in rows]
    print(f"Sample event_ids: {event_ids}")

    if event_ids:
        # Try to find these in raw table
        ids_str = ", ".join([f"'{eid}'" for eid in event_ids])
        q3 = f"""
        SELECT event_id, wm_yr_and_wk,
               msg_subj_nm,
               msg_txt
        FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
        WHERE event_id IN ({ids_str})
        LIMIT 3
        """
        raw_rows = list(client.query(q3).result())
        print(f"\nFound {len(raw_rows)} matching raw rows")
        for r in raw_rows:
            print(f"\n  event_id: {r.event_id}")
            print(f"  wm_yr_and_wk: {r.wm_yr_and_wk}")

            # Parse msg_subj_nm
            subj = r.msg_subj_nm
            if subj:
                if isinstance(subj, dict):
                    arr = subj.get('array', [])
                    print(f"  Subject: {arr}")
                else:
                    print(f"  Subject: {subj}")

            # Parse msg_txt
            msg = r.msg_txt
            if msg:
                if isinstance(msg, dict):
                    arr = msg.get('array', [])
                    for i, chunk in enumerate(arr[:3]):
                        txt = str(chunk)
                        print(f"  msg_txt[{i}] ({len(txt)} chars): {txt[:500]}")
                else:
                    print(f"  msg_txt: {str(msg)[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Check 3: Look at ALL available columns in AMP ALL 2 that might have body text
print("\n=== Checking ALL text columns for body content (1 sample event) ===")
try:
    q4 = """
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND Status LIKE '%Published%'
      AND Message_Type LIKE '%Store Updates%'
      AND Store_Area = 'Fresh'
    LIMIT 1
    """
    rows = list(client.query(q4).result())
    if rows:
        row_dict = dict(rows[0])
        for k, v in row_dict.items():
            if v is not None and str(v).strip() != '' and str(v) != 'None':
                val_str = str(v)[:200]
                print(f"  {k}: {val_str}")
except Exception as e:
    print(f"Error: {e}")
