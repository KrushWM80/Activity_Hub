#!/usr/bin/env python3
"""Deep dive into week_at_glance_summary and msg_txt content"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json'

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Check 1: What does week_at_glance_summary look like for Week 4?
print("=== week_at_glance_summary content sample (Week 4) ===")
try:
    q1 = """
    SELECT event_id, Store_Area, Title, 
           SUBSTR(week_at_glance_summary, 1, 500) as summary_preview,
           LENGTH(week_at_glance_summary) as summary_len
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND week_at_glance_summary IS NOT NULL
      AND week_at_glance_summary != ''
    LIMIT 10
    """
    rows = list(client.query(q1).result())
    print(f"Found {len(rows)} rows with summary")
    for r in rows:
        print(f"\n  event_id: {r.event_id}")
        print(f"  Store_Area: {r.Store_Area}")
        print(f"  Title: {r.Title}")
        print(f"  Summary length: {r.summary_len} chars")
        print(f"  Preview: {r.summary_preview[:300]}...")
except Exception as e:
    print(f"Error: {e}")

# Check 2: Is the summary the same for all stores for a given event?
print("\n\n=== Is week_at_glance_summary per-event or per-store? ===")
try:
    q2 = """
    SELECT event_id, COUNT(*) as total_rows,
           COUNT(DISTINCT week_at_glance_summary) as distinct_summaries,
           SUBSTR(MAX(week_at_glance_summary), 1, 200) as sample_summary
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND week_at_glance_summary IS NOT NULL
      AND week_at_glance_summary != ''
      AND Status LIKE '%Published%'
    GROUP BY event_id
    LIMIT 5
    """
    rows = list(client.query(q2).result())
    for r in rows:
        print(f"  event_id: {r.event_id} | rows: {r.total_rows} | distinct summaries: {r.distinct_summaries}")
        print(f"    Sample: {r.sample_summary[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Check 3: Are ALL events for Week 4 Store Updates missing summaries, or just some?
print("\n\n=== Events WITH vs WITHOUT summary (Week 4, Store Updates) ===")
try:
    q3 = """
    SELECT 
      CASE WHEN week_at_glance_summary IS NOT NULL AND week_at_glance_summary != '' 
           THEN 'HAS_SUMMARY' ELSE 'NO_SUMMARY' END as status,
      COUNT(DISTINCT event_id) as event_count
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND Status LIKE '%Published%'
      AND Message_Type LIKE '%Store Updates%'
    GROUP BY status
    """
    rows = list(client.query(q3).result())
    for r in rows:
        print(f"  {r.status}: {r.event_count} distinct events")
except Exception as e:
    print(f"Error: {e}")

# Check 4: Try to get msg_txt from raw Cosmos table for a Week 4 event
print("\n\n=== Raw Cosmos msg_txt sample (Week 4) ===")
try:
    q4 = """
    SELECT event_id,
           msg_subj_nm,
           msg_txt,
           bus_domain_nm,
           wm_yr_and_wk
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE wm_yr_and_wk LIKE '%202704%'
    LIMIT 3
    """
    rows = list(client.query(q4).result())
    print(f"Found {len(rows)} raw rows")
    for r in rows:
        print(f"\n  event_id: {r.event_id}")
        print(f"  wm_yr_and_wk: {r.wm_yr_and_wk}")
        print(f"  bus_domain_nm: {r.bus_domain_nm}")
        # msg_txt is a STRUCT<array ARRAY<STRING>>
        msg = r.msg_txt
        if msg and hasattr(msg, 'get'):
            arr = msg.get('array', [])
            for i, chunk in enumerate(arr[:2]):
                print(f"  msg_txt[{i}] (first 400 chars): {str(chunk)[:400]}")
        elif msg:
            print(f"  msg_txt type: {type(msg)} | value: {str(msg)[:400]}")
except Exception as e:
    print(f"Error: {e}")

# Check 5: Search for "Summarized" in week_at_glance_summary
print("\n\n=== Checking for 'Summarized' text in week_at_glance_summary ===")
try:
    q5 = """
    SELECT event_id, Store_Area, Title,
           SUBSTR(week_at_glance_summary, 1, 500) as summary_preview
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND WM_Week = '4'
      AND Status LIKE '%Published%'
      AND Message_Type LIKE '%Store Updates%'
      AND LOWER(week_at_glance_summary) LIKE '%summarized%'
    LIMIT 10
    """
    rows = list(client.query(q5).result())
    print(f"Events with 'Summarized' in WaaG summary: {len(rows)}")
    for r in rows:
        print(f"  [{r.Store_Area}] {r.Title}")
        print(f"    Preview: {r.summary_preview[:300]}")
except Exception as e:
    print(f"Error: {e}")
