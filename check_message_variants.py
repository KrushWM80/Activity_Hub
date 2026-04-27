#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Query to find what distinguishes message variants
results = client.query("""
SELECT
    event_id,
    Activity_Title,
    Message_Type,
    Activity_ID,
    AMP_ID,
    Status,
    COUNT(*) as occurrence_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
GROUP BY event_id, Activity_Title, Message_Type, Activity_ID, AMP_ID, Status
HAVING occurrence_count > 1
ORDER BY occurrence_count DESC
LIMIT 10
""").result()

print("\n" + "="*100)
print("Messages with multiple records (potential variants)")
print("="*100 + "\n")

for row in results:
    print(f"event_id: {row['event_id']}")
    print(f"  Title: {row['Activity_Title']}")
    print(f"  Message_Type: {row['Message_Type']}")
    print(f"  Activity_ID: {row['Activity_ID']}")
    print(f"  AMP_ID: {row['AMP_ID']}")
    print(f"  Status: {row['Status']}")
    print(f"  Count: {row['occurrence_count']}")
    print()

# Now let's get the total counts using different approaches
print("="*100)
print("Count Comparison")
print("="*100 + "\n")

for row in client.query("""
SELECT COUNT(DISTINCT event_id) as count_by_event_id
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result():
    print(f"Distinct event_id:              {row['count_by_event_id']}")

for row in client.query("""
SELECT COUNT(DISTINCT Activity_ID) as count_by_activity_id
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result():
    print(f"Distinct Activity_ID:           {row['count_by_activity_id']}")

for row in client.query("""
SELECT COUNT(*) as total_rows
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result():
    print(f"Total rows in table:            {row['total_rows']}")
