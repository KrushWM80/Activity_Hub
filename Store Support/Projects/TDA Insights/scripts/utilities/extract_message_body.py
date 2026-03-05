#!/usr/bin/env python3
"""
Extract and display the actual message content from AMP event
"""

from google.cloud import bigquery
import html
import re

def extract_text_from_html(html_content):
    """Extract plain text from HTML"""
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html_content)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def get_message_body(event_id):
    """Get the full message body from AMP event"""
    
    try:
        client = bigquery.Client(project='wmt-assetprotection-prod')
        
        query = f"""
        SELECT 
            event_id,
            actv_title_home_ofc_nm,
            msg_subj_nm,
            msg_txt,
            msg_start_dt,
            msg_end_dt,
            bus_domain_nm
        FROM `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
        WHERE EVENT_ID = '{event_id}'
        LIMIT 1
        """
        
        results = client.query(query).result()
        rows = list(results)
        
        if not rows:
            print(f"❌ Event not found: {event_id}")
            return None
        
        event = rows[0]
        
        print("="*80)
        print("✅ AMP EVENT MESSAGE BODY")
        print("="*80)
        
        print(f"\n📌 Event Details:")
        print(f"  Event ID: {event.event_id}")
        print(f"  Title: {event.actv_title_home_ofc_nm}")
        print(f"  Business Area: {event.bus_domain_nm}")
        print(f"  Active: {event.msg_start_dt} to {event.msg_end_dt}")
        
        print(f"\n📝 RAW HTML MESSAGE:\n")
        
        # Extract the message text from the complex data structure
        msg_txt_str = str(event.msg_txt)
        print(f"[HTML Length: {len(msg_txt_str)} characters]\n")
        print(msg_txt_str[:2000])  # Show first 2000 chars
        
        if len(msg_txt_str) > 2000:
            print(f"\n... [Truncated - total length: {len(msg_txt_str)}]")
        
        print(f"\n{'='*80}")
        print("📄 CLEAN TEXT FOR PODCAST:\n")
        
        # Extract clean text
        clean_text = extract_text_from_html(msg_txt_str)
        print(clean_text)
        
        print(f"\n{'='*80}")
        print(f"\n✨ Ready for podcast generation!")
        print(f"   Event: {event.event_id}")
        print(f"   Title: {event.actv_title_home_ofc_nm}")
        print(f"   Content Length: {len(clean_text)} characters")
        
        return {
            'event_id': event.event_id,
            'title': event.actv_title_home_ofc_nm,
            'subject': event.msg_subj_nm,
            'business_area': event.bus_domain_nm,
            'start_date': event.msg_start_dt,
            'end_date': event.msg_end_dt,
            'html_content': msg_txt_str,
            'clean_content': clean_text
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    data = get_message_body("91202b13-3e65-4870-885f-f4a66e221eed")
    
    if data:
        # Save to file
        with open('amp_event_message.txt', 'w') as f:
            f.write(f"Event ID: {data['event_id']}\n")
            f.write(f"Title: {data['title']}\n")
            f.write(f"Business Area: {data['business_area']}\n")
            f.write(f"\n--- MESSAGE CONTENT ---\n\n")
            f.write(data['clean_content'])
        
        print(f"\n✅ Message saved to: amp_event_message.txt")
