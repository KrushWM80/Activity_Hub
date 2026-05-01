#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Test the exact query from the endpoint
query = """
    SELECT COUNT(DISTINCT event_id) as majority_count
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = CAST(2027 AS INT64)
        AND Week IN (13)
        AND Activity_Title IS NOT NULL
        AND Activity_Type IS NOT NULL
        AND COALESCE(Status, Message_Status) = 'Published - Published'
        AND COALESCE(Store_Cnt, 0) >= 2000
"""

print("Testing majority query...")
result = client.query(query).result()
row = next(result)
majority_count = row['majority_count']

print(f"Majority activities (>= 2000 stores): {majority_count}")

# Now test with Stores_With_Access field
query2 = """
    SELECT 
        COUNT(DISTINCT event_id) as majority_count,
        AVG(CAST(Store_Cnt AS INT64)) as avg_store_cnt
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027
        AND Week = 13
        AND Activity_Title IS NOT NULL
        AND Activity_Type IS NOT NULL
        AND COALESCE(Status, Message_Status) = 'Published - Published'
    GROUP BY event_id
    HAVING MAX(CAST(COALESCE(Store_Cnt, 0) AS INT64)) >= 2000
"""

print("\nTesting with GROUP BY and HAVING...")
result2 = client.query(query2).result()
rows = list(result2)
print(f"Rows returned: {len(rows)}")
