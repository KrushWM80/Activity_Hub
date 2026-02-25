#!/usr/bin/env python3
"""
Query BigQuery for AMP event data
"""

from google.cloud import bigquery
import json

def query_amp_event(event_id):
    """Query BigQuery for specific AMP event"""
    
    client = bigquery.Client(project='wmt-assetprotection-prod')
    
    # Query with proper table name escaping
    query = f"""
    SELECT *
    FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
    WHERE event_id = '{event_id}'
    LIMIT 1
    """
    
    print(f"Querying for Event ID: {event_id}\n")
    print("="*70)
    
    try:
        results = client.query(query).result()
        
        rows = list(results)
        if not rows:
            print(f"❌ Event ID not found: {event_id}")
            print("\n📊 Let me query all available events...")
            
            # Query all events to show what's available
            all_query = """
            SELECT DISTINCT event_id, message_title, business_area
            FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2`
            ORDER BY event_id
            LIMIT 20
            """
            all_results = client.query(all_query).result()
            print("\n✅ Available Events:\n")
            for i, row in enumerate(all_results, 1):
                print(f"{i}. Event ID: {row.event_id}")
                print(f"   Title: {row.message_title}")
                print(f"   Area: {row.business_area}\n")
            return None
        
        event = rows[0]
        print(f"✅ Event Found!\n")
        
        # Display all fields
        print("EVENT DETAILS:")
        print("-" * 70)
        event_dict = dict(event)
        for key, value in event_dict.items():
            if value is not None:
                print(f"{key}: {value}")
        
        print("\n" + "="*70)
        print("\n📝 MESSAGE BODY FOR PODCAST:\n")
        print(event_dict.get('message_description', 'N/A'))
        print("\n" + "="*70)
        
        return event_dict
        
    except Exception as e:
        print(f"❌ Error querying BigQuery: {e}")
        print(f"\nNote: Make sure you have:")
        print("1. Active Google Cloud credentials")
        print("2. BigQuery API enabled")
        print("3. Proper access to wmt-assetprotection-prod project")
        return None

if __name__ == "__main__":
    event_id = "91202b13-3e65-4870-885f-f4a66e221eed"
    result = query_amp_event(event_id)
