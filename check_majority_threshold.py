#!/usr/bin/env python3
import urllib.request
import json

try:
    url = "http://weus42608431466:8081/api/amp-data?fy=2027&weeks=13&limit=200"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    
    activities = data.get('data', [])
    
    # Categorize by store reach
    high_reach = [a for a in activities if int(a.get('Stores_With_Access', 0)) >= 2000]
    medium_reach = [a for a in activities if 500 <= int(a.get('Stores_With_Access', 0)) < 2000]
    low_reach = [a for a in activities if int(a.get('Stores_With_Access', 0)) < 500]
    
    print("\n" + "="*100)
    print("ACTIVITIES BY STORE REACH THRESHOLD")
    print("="*100 + "\n")
    
    print(f"Activities >= 2000 stores:  {len(high_reach)}")
    print(f"Activities 500-1999 stores: {len(medium_reach)}")
    print(f"Activities < 500 stores:    {len(low_reach)}")
    print(f"TOTAL:                      {len(activities)}\n")
    
    print("="*100)
    print("HIGH-REACH ACTIVITIES (>= 2000 STORES)")
    print("="*100 + "\n")
    
    high_reach_sorted = sorted(high_reach, key=lambda x: int(x.get('Stores_With_Access', 0)), reverse=True)
    
    for i, activity in enumerate(high_reach_sorted, 1):
        title = activity.get('Activity_Title', '')[:60]
        stores = activity.get('Stores_With_Access', 0)
        print(f"{i:2}. {title:<60} | {stores:>5} stores")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
