"""Find events missing summarized text and show details."""
import json

with open('week_13_fy2027.json') as f:
    d = json.load(f)

events = d.get('events', [])
missing = [e for e in events if not e.get('summarized_text', '').strip()]

print(f"Total events: {len(events)}, Missing summary: {len(missing)}")
for e in missing:
    eid = e.get('Event_ID', '?')
    title = e.get('Event_Title', '?')
    status = e.get('Status', '?')
    area = e.get('Business_Area', '?')
    print(f"\n  Event_ID: {eid}")
    print(f"  Title: {title}")
    print(f"  Status: {status}")
    print(f"  Business_Area: {area}")
    # Show all keys for context
    for k, v in e.items():
        if k not in ('summarized_text', 'message_body') and v:
            print(f"  {k}: {v}")
