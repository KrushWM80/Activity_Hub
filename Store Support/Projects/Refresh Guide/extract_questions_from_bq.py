"""
Extract all unique questions with Area/Topic metadata directly from BigQuery
"""
import json
from google.cloud import bigquery
from collections import defaultdict

client = bigquery.Client(project='athena-gateway-prod')

# Query to get ALL unique questions with their descriptions
query = """
SELECT DISTINCT
    checklistQuestionId,
    description
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE DATE(exportDate) = '2026-02-23'
ORDER BY checklistQuestionId
"""

print("Querying BigQuery for all questions with descriptions on 2/23...")
results = client.query(query).result()

questions_data = {}

for row in results:
    q_id = row['checklistQuestionId']
    desc = row['description']
    
    questions_data[q_id] = {
        'id': q_id,
        'description': desc if desc else 'N/A'
    }

print(f"\nFound {len(questions_data)} unique questions")
print(f"\nChecking available columns in schema...")

# Let's also try to see if there are other columns with metadata
schema_query = """
SELECT column_name, data_type
FROM `athena-gateway-prod.store_refresh.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'store_refresh_data'
ORDER BY column_name
"""

print("\n📋 Schema columns available:")
schema_results = client.query(schema_query).result()
columns = []
for row in schema_results:
    col_name = row['column_name']
    col_type = row['data_type']
    columns.append(col_name)
    print(f"  - {col_name} ({col_type})")

print(f"\nTotal columns: {len(columns)}")

# Save for reference
with open('bq_schema_columns.json', 'w') as f:
    json.dump(columns, f, indent=2)

print("✓ Schema saved to bq_schema_columns.json")

# Now let's look at actual data samples for each question to see if there's hidden metadata
print("\n🔍 Sampling first few questions...")
sample_query = """
SELECT 
    checklistQuestionId,
    *
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE DATE(exportDate) = '2026-02-23'
LIMIT 3
"""

sample_results = client.query(sample_query).result()
for row in sample_results:
    print(f"\nSample record:")
    for key, value in row.items():
        print(f"  {key}: {value}")

# Export all unique questions with their descriptions
all_q_list = [
    questions_data[q_id]
    for q_id in sorted(questions_data.keys(), key=lambda x: int(x.split('_')[1]))
]

with open('all_questions_with_metadata.json', 'w') as f:
    json.dump(all_q_list, f, indent=2)

print(f"\n✓ All {len(all_q_list)} questions saved to all_questions_with_metadata.json")
print("\nQuestion summary:")
print(f"  Total unique questions: {len(all_q_list)}")
print(f"\nFirst 10 questions:")
for q in all_q_list[:10]:
    print(f"  {q['id']}: {q['description'][:60]}...")
