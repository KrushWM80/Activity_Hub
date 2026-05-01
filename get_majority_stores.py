#!/usr/bin/env python3
import urllib.request
import json

try:
    url = "http://weus42608431466:8081/api/amp-data?fy=2027&weeks=13&limit=200"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    
    activities = data.get('data', [])
    total = data.get('total_results', 0)
    
    print(f"\n{'='*100}")
    print(f"WEEK 13 (May 1, 2026) - MAJORITY STORES ACTIVITIES")
    print(f"{'='*100}\n")
    print(f"Total Activities: {total}\n")
    
    # Sort by store count
    sorted_activities = sorted(activities, key=lambda x: int(x.get('Stores_With_Access', 0)), reverse=True)
    
    print(f"{'Activity Title':<60} {'Stores':<10} {'Message Type':<20}")
    print("-" * 100)
    
    for activity in sorted_activities[:20]:
        title = activity.get('Activity_Title', '')[:60]
        stores = activity.get('Stores_With_Access', 0)
        msg_type = activity.get('Message_Type', '')[:20]
        print(f"{title:<60} {stores:<10} {msg_type:<20}")
    
    print(f"\n{'='*100}")
    print("STATISTICS")
    print(f"{'='*100}\n")
    
    store_counts = [int(a.get('Stores_With_Access', 0)) for a in activities]
    avg_stores = sum(store_counts) / len(store_counts) if store_counts else 0
    max_stores = max(store_counts) if store_counts else 0
    min_stores = min(store_counts) if store_counts else 0
    
    print(f"Average Stores per Activity:  {avg_stores:.1f}")
    print(f"Max Stores (Single Activity): {max_stores}")
    print(f"Min Stores (Single Activity): {min_stores}")
    print(f"\nMajority Activities (>= {int(avg_stores)} stores): {len([s for s in store_counts if s >= avg_stores])}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
