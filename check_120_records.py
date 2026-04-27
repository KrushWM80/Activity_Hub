#!/usr/bin/env python3
from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Try different grouping combinations to find what gives ~120 records
print("\n" + "="*100)
print("Testing different grouping approaches")
print("="*100 + "\n")

# Test 1: Group by event_id, Message_Type (might separate message variants)
result1 = client.query("""
SELECT COUNT(DISTINCT CONCAT(event_id, '|', Message_Type)) as count_event_message
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()
for row in result1:
    print(f"1. CONCAT(event_id, Message_Type):        {row['count_event_message']}")

# Test 2: Group by Activity_Title, Message_Type
result2 = client.query("""
SELECT COUNT(DISTINCT CONCAT(Activity_Title, '|', Message_Type)) as count_title_message
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()
for row in result2:
    print(f"2. CONCAT(Activity_Title, Message_Type):  {row['count_title_message']}")

# Test 3: Group by event_id, Message_Type, Business_Area
result3 = client.query("""
SELECT COUNT(DISTINCT CONCAT(event_id, '|', Message_Type, '|', Business_Area)) as count_multi
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()
for row in result3:
    print(f"3. CONCAT(event_id, Message_Type, Area): {row['count_multi']}")

# Test 4: Group by Activity_Title only
result4 = client.query("""
SELECT COUNT(DISTINCT Activity_Title) as count_titles
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()
for row in result4:
    print(f"4. Distinct Activity_Title:                {row['count_titles']}")

# Test 5: Check for rows with same event_id but different Store_Area
result5 = client.query("""
SELECT COUNT(DISTINCT CONCAT(event_id, '|', Business_Area)) as count_area_variant
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
WHERE FY = 2027 AND Week = 13
    AND Activity_Title IS NOT NULL
    AND Activity_Type IS NOT NULL
    AND COALESCE(Status, Message_Status) = 'Published - Published'
""").result()
for row in result5:
    print(f"5. CONCAT(event_id, Business_Area):       {row['count_area_variant']}")

print()
