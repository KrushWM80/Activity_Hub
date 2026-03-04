"""
Extract all unique questions from 2/23 data with Area/Topic grouping
"""
import json
from google.cloud import bigquery
from collections import defaultdict

# Initialize BigQuery client
client = bigquery.Client(project='athena-gateway-prod')

# Query to get all unique questions with any available metadata on 2/23
query = """
SELECT DISTINCT
    checklistQuestionId,
    CAST(NULL AS STRING) as area,
    CAST(NULL AS STRING) as topic
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
WHERE DATE(exportDate) = '2026-02-23'
ORDER BY checklistQuestionId
"""

print("Extracting all unique questions from 2/23 data...")
results = client.query(query).result()

questions = []
for row in results:
    questions.append({
        'id': row['checklistQuestionId'],
        'area': row['area'],
        'topic': row['topic']
    })

print(f"\nFound {len(questions)} unique questions on 2/23")
print("\nQuestion IDs:")
for q in questions:
    print(f"  {q['id']}")

# Save to JSON for reference
with open('all_questions_2_23.json', 'w') as f:
    json.dump(questions, f, indent=2)

print("\nSaved to all_questions_2_23.json")
