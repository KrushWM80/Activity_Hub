"""
Check schema of employee tables to find correct column names
"""

from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

tables = [
    'wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW',
    'polaris-analytics-prod.us_walmart.vw_polaris_current_schedule'
]

for table_id in tables:
    print(f"\n{'='*80}")
    print(f"Table: {table_id}")
    print('='*80)
    
    try:
        table = client.get_table(table_id)
        
        print(f"\nColumns ({len(table.schema)} total):")
        print("-" * 80)
        
        # Look for email, name, WIN, job-related columns
        keywords = ['email', 'name', 'employee', 'id', 'win', 'job', 'title', 'department', 'hire', 'manager', 'location']
        
        matching_cols = []
        for field in table.schema:
            field_lower = field.name.lower()
            if any(keyword in field_lower for keyword in keywords):
                matching_cols.append(f"  {field.name:50} {field.field_type}")
        
        for col in sorted(matching_cols):
            print(col)
            
        print(f"\nTotal matching columns: {len(matching_cols)}")
        
    except Exception as e:
        print(f"Error accessing table: {e}")
