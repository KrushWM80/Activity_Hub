#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# First, check if Message_ID field exists
print("\n" + "="*100)
print("Checking for Message_ID field")
print("="*100 + "\n")

schema_results = client.query("""
SELECT column_name
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Output - AMP ALL 2'
AND LOWER(column_name) LIKE '%message%'
""").result()

print("Columns with 'message' in name:")
for row in schema_results:
    print(f"  - {row['column_name']}")

# Now test grouping by (event_id, Message_ID) if it exists
print("\n" + "="*100)
print("Count by event_id and Message_ID")
print("="*100 + "\n")

# Check sample data with event_id and Message_ID relationship
result = client.query("""
SELECT
    event_id,
    COUNT(DISTINCT Message_ID) as message_id_count,
    COUNT(DISTINCT Activity_Title) as title_count
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
GROUP BY event_id
ORDER BY message_id_count DESC
LIMIT 15
""").result()

print("Top 15 events with multiple Message_IDs:")
for row in result:
    print(f"  event_id: {row['event_id'][:40]:40} | Message_IDs: {row['message_id_count']:2} | Titles: {row['title_count']}")

# Total count by (event_id, Message_ID)
print("\n" + "="*100)
print("Total distinct (event_id, Message_ID) combinations")
print("="*100 + "\n")

result = client.query("""
SELECT COUNT(DISTINCT CONCAT(event_id, '|', Message_ID)) as event_message_pairs
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()

for row in result:
    print(f"Distinct (event_id, Message_ID):       {row['event_message_pairs']}")
