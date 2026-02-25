#!/usr/bin/env python3
"""
Get all column names from the AMP table
"""

from google.cloud import bigquery

def get_table_schema():
    """Get all columns in the AMP table"""
    
    client = bigquery.Client(project='wmt-assetprotection-prod')
    table_id = "wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2"
    
    try:
        table = client.get_table(table_id)
        schema = table.schema
        
        print(f"\n📊 Table: {table_id}")
        print(f"Total Columns: {len(schema)}\n")
        print("Column Names:\n")
        
        message_related = []
        body_related = []
        description_related = []
        content_related = []
        
        for i, field in enumerate(schema, 1):
            col_name = field.name
            col_type = field.field_type
            
            # Categorize columns
            if 'message' in col_name.lower():
                message_related.append((col_name, col_type))
            if 'body' in col_name.lower():
                body_related.append((col_name, col_type))
            if 'description' in col_name.lower():
                description_related.append((col_name, col_type))
            if 'content' in col_name.lower():
                content_related.append((col_name, col_type))
        
        if message_related:
            print("🔍 MESSAGE-RELATED FIELDS:")
            for col, typ in message_related:
                print(f"   - {col} ({typ})")
        
        if body_related:
            print("\n📄 BODY-RELATED FIELDS:")
            for col, typ in body_related:
                print(f"   - {col} ({typ})")
        
        if description_related:
            print("\n📋 DESCRIPTION-RELATED FIELDS:")
            for col, typ in description_related:
                print(f"   - {col} ({typ})")
        
        if content_related:
            print("\n📝 CONTENT-RELATED FIELDS:")
            for col, typ in content_related:
                print(f"   - {col} ({typ})")
        
        print("\n\n📌 ALL COLUMNS:")
        print("-" * 60)
        for i, field in enumerate(schema, 1):
            print(f"{i:3}. {field.name:30} ({field.field_type})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_table_schema()
