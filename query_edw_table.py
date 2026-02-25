#!/usr/bin/env python3
"""
Query EDW message content table with proper permissions handling
"""

from google.cloud import bigquery

def query_edw_message(event_id):
    """Query EDW message table"""
    
    try:
        # Use wmt-assetprotection-prod project but query EDW table
        client = bigquery.Client(project='wmt-assetprotection-prod')
        
        query = f"""
        SELECT *
        FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
        WHERE EVENT_ID = '{event_id}'
        LIMIT 1
        """
        
        print(f"🔍 Querying EDW Message Table")
        print(f"📍 Table: wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT")
        print(f"🎯 Event ID: {event_id}\n")
        print("="*70 + "\n")
        
        results = client.query(query).result()
        rows = list(results)
        
        if not rows:
            print(f"❌ No data found for event: {event_id}\n")
            return None
        
        event = rows[0]
        event_dict = dict(event)
        
        print("✅ EVENT FOUND!\n")
        print("Full Event Data:")
        print("-" * 70)
        
        for key, value in sorted(event_dict.items()):
            if value is not None:
                val_str = str(value)
                if len(val_str) > 80:
                    val_str = val_str[:77] + "..."
                print(f"{key:40} : {val_str}")
        
        print("\n" + "="*70)
        
        # Extract message content
        print("\n📝 MESSAGE BODY FOR PODCAST:\n")
        
        # Look for common message content fields
        content_fields = ['MESSAGE_TEXT', 'MESSAGE_BODY', 'CONTENT', 'DESCRIPTION', 
                         'MESSAGE_CONTENT', 'BODY_TEXT', 'MESSAGE_DESC']
        
        for field in content_fields:
            if field in event_dict and event_dict[field]:
                print(event_dict[field])
                print("\n" + "="*70)
                return event_dict
        
        # If no specific field, try any field with "message" or "body"
        for key, value in event_dict.items():
            if value and isinstance(value, str) and len(str(value)) > 50:
                if any(x in key.lower() for x in ['message', 'body', 'content', 'text', 'description']):
                    print(f"Field: {key}")
                    print(value)
                    print("\n" + "="*70)
                    return event_dict
        
        print("(No dedicated message content field found - showing all fields above)")
        return event_dict
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ Error: {error_str}\n")
        
        if "403" in error_str or "Access Denied" in error_str:
            print("⚠️ PERMISSION ISSUE:")
            print("Your current credentials don't have access to wmt-edw-prod project.")
            print("\nOptions:")
            print("1. Switch to credentials that have wmt-edw-prod access")
            print("2. Check if the table is available in wmt-assetprotection-prod")
            print("3. Provide the message content directly")
        
        return None

if __name__ == "__main__":
    query_edw_message("91202b13-3e65-4870-885f-f4a66e221eed")
