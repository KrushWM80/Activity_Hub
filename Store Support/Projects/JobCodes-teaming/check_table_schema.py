"""
Check the schema of Workforce Data table
"""

from google.cloud import bigquery

client = bigquery.Client()

print("=" * 80)
print("WORKFORCE DATA TABLE SCHEMA")
print("=" * 80)

try:
    dataset = client.get_dataset("wmt-assetprotection-prod.Store_Support_Dev")
    tables = list(client.list_tables(dataset))
    
    print(f"\nFound {len(tables)} tables:")
    for table in tables:
        print(f"  - {table.table_id}")
    
    # Get Workforce Data table
    table = client.get_table("wmt-assetprotection-prod.Store_Support_Dev.Workforce Data")
    print(f"\nTable: {table.table_id}")
    print(f"Schema:")
    for field in table.schema:
        print(f"  {field.name:30} {field.field_type:15} {field.mode}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("STORE ROSTER CONTACTS TABLE SCHEMA")
print("=" * 80)

try:
    table = client.get_table("wmt-assetprotection-prod.Store_Support_Dev.Store Roster Contacts")
    print(f"\nTable: {table.table_id}")
    print(f"Schema:")
    for field in table.schema:
        print(f"  {field.name:30} {field.field_type:15} {field.mode}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
