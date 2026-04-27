#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

print("\n" + "="*100)
print("Checking different grouping combinations to find 120")
print("="*100 + "\n")

combinations = [
    ("Activity_Title + Message_Type", "COUNT(DISTINCT CONCAT(Activity_Title, '|', Message_Type))"),
    ("Activity_Title + Business_Area + Store_Type", "COUNT(DISTINCT CONCAT(Activity_Title, '|', Business_Area, '|', COALESCE(Store_Type, 'NULL')))"),
    ("event_id + Business_Area", "COUNT(DISTINCT CONCAT(event_id, '|', Business_Area))"),
    ("Activity_Title + Activity_Type + Store_Type", "COUNT(DISTINCT CONCAT(Activity_Title, '|', Activity_Type, '|', COALESCE(Store_Type, 'NULL')))"),
]

for label, count_expr in combinations:
    result = client.query(f"""
    SELECT {count_expr} as combo_count
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE FY = 2027 AND Week = 13
        AND Activity_Title IS NOT NULL
        AND Activity_Type IS NOT NULL
        AND COALESCE(Status, Message_Status) = 'Published - Published'
    """).result()
    
    for row in result:
        count = row['combo_count']
        marker = " ← MATCHES!" if count == 120 else ""
        print(f"{label:55} : {count:3}{marker}")

print()
