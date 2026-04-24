import json
d = json.load(open('week_13_fy2027.json'))
print(f"summarized: {d['summarized_count']}")
missing = d.get('events_without_summary', [])
print(f"without summary: {len(missing)}")
for e in missing:
    print(json.dumps(e, indent=2, default=str))
