"""
Find tables that might have email to WIN mapping
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Search for possible employee/identity tables
queries = [
    # Try to find a sample from Unified Profile
    """
    SELECT *
    FROM `wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW`
    LIMIT 1
    """,
    
    # Try Polaris
    """
    SELECT *
    FROM `polaris-analytics-prod.us_walmart.vw_polaris_current_schedule`
    WHERE email_address IS NOT NULL OR email IS NOT NULL
    LIMIT 1
    """
]

for i, query in enumerate(queries, 1):
    print(f"\n{'='*80}")
    print(f"Query {i}")
    print('='*80)
    try:
        results = client.query(query).result()
        for row in results:
            print("\nSample row:")
            for key, value in row.items():
                if value and ('email' in key.lower() or 'win' in key.lower() or 'employee' in key.lower() or 'name' in key.lower()):
                    print(f"  {key}: {value}")
            break
    except Exception as e:
        print(f"Error: {e}")
