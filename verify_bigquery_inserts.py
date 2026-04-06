#!/usr/bin/env python3
"""Verify BigQuery inserts for custom trigger Logic Requests"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query logic_requests table
query = """
SELECT 
    request_id,
    name,
    trigger_type,
    custom_trigger_text,
    approval_status,
    has_notification_component,
    created_at
FROM `wmt-assetprotection-prod.Store_Support_Dev.logic_requests`
WHERE trigger_type = 'custom'
ORDER BY created_at DESC
LIMIT 10
"""

print("\nLogic Requests Table (Custom Triggers)")
print("=" * 80)

try:
    results = client.query(query).result()
    count = 0
    for row in results:
        count += 1
        print(f"\n✓ Record #{count}")
        print(f"  Request ID: {row.request_id}")
        print(f"  Name: {row.name}")
        print(f"  Trigger Type: {row.trigger_type}")
        print(f"  Custom Trigger Text: {row.custom_trigger_text}")
        print(f"  Status: {row.approval_status}")
        print(f"  Has Notification: {row.has_notification_component}")
        print(f"  Created: {row.created_at}")
    
    if count == 0:
        print("No custom trigger records found")
    else:
        print(f"\n{count} record(s) found in BigQuery")
    
    print("=" * 80)
except Exception as e:
    print(f"✗ Error querying BigQuery: {e}")

# Query notification_logic_rules
print("\n\nNotification Logic Rules Table")
print("=" * 80)

query2 = """
SELECT 
    rule_id,
    logic_request_id,
    category,
    title_template,
    channels,
    status,
    created_at
FROM `wmt-assetprotection-prod.Store_Support_Dev.notification_logic_rules`
ORDER BY created_at DESC
LIMIT 5
"""

try:
    results = client.query(query2).result()
    count = 0
    for row in results:
        count += 1
        print(f"\n✓ Rule #{count}")
        print(f"  Rule ID: {row.rule_id}")
        print(f"  Logic Request ID: {row.logic_request_id}")
        print(f"  Category: {row.category}")
        print(f"  Title: {row.title_template}")
        print(f"  Channels: {row.channels}")
        print(f"  Status: {row.status}")
        print(f"  Created: {row.created_at}")
    
    if count == 0:
        print("No notification rules found")
    else:
        print(f"\n{count} rule(s) found in BigQuery")
    
    print("=" * 80)
except Exception as e:
    print(f"✗ Error querying notification rules: {e}")
