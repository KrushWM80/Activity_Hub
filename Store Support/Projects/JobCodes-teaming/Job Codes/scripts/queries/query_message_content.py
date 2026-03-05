#!/usr/bin/env python3
"""
Query the actual AMP message content from the data warehouse
"""

from google.cloud import bigquery
import json

def query_message_content(event_id):
    """Query message content from data warehouse"""
    
    client = bigquery.Client(project='wmt-edw-prod')
    
    # Query the message event table
    query = f"""
    SELECT *
    FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
    WHERE EVENT_ID = '{event_id}'
    LIMIT 1
    """
    
    print(f"🔍 Querying for Event ID: {event_id}")
    print(f"📍 Table: wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT\n")
    print("="*70)
    
    try:
        results = client.query(query).result()
        
        rows = list(results)
        if not rows:
            print(f"\n❌ Event ID not found: {event_id}")
            print("\n📊 Let me check available columns first...\n")
            
            # Get table schema
            table = client.get_table("wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT")
            schema = table.schema
            
            print(f"Total Columns Available: {len(schema)}\n")
            print("Column Names:")
            for i, field in enumerate(schema, 1):
                print(f"{i:3}. {field.name:40} ({field.field_type})")
            
            return None
        
        event = rows[0]
        event_dict = dict(event)
        
        print(f"✅ EVENT FOUND!\n")
        
        # Display all fields
        print("EVENT DETAILS:")
        print("-" * 70)
        for key, value in event_dict.items():
            if value is not None:
                # Truncate long values for display
                display_value = str(value)
                if len(display_value) > 100:
                    display_value = display_value[:97] + "..."
                print(f"{key:40} : {display_value}")
        
        print("\n" + "="*70)
        
        # Find message body fields
        print("\n📝 MESSAGE CONTENT:\n")
        message_fields = {k: v for k, v in event_dict.items() 
                         if v and any(x in k.lower() for x in ['message', 'body', 'content', 'text', 'description'])}
        
        if message_fields:
            for key, value in message_fields.items():
                print(f"[{key}]:")
                print(f"{value}\n")
        else:
            print("(No dedicated message body field found)")
        
        print("="*70)
        
        return event_dict
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Check project: wmt-edw-prod")
        print(f"2. Check credentials are active")
        print(f"3. Verify table access permissions")
        return None

if __name__ == "__main__":
    event_id = "91202b13-3e65-4870-885f-f4a66e221eed"
    result = query_message_content(event_id)
