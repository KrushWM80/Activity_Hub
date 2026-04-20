import os
import json
from sqlite_cache import get_cache

# Load from cache
cache = get_cache()
try:
    data = cache.get_job_codes()
    print(f"Loaded {len(data)} job codes from cache")
    
    print("\nFirst 5 job codes:")
    for i, j in enumerate(data[:5]):
        print(f"  {i+1}. {j.get('job_code')}: status={j.get('status')}, badges={j.get('source_badges')}")
    
    # Status distribution
    from collections import Counter
    status_counts = Counter(j.get('status') for j in data)
    print("\nStatus distribution:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    # Check Review + T
    review_with_t = [j for j in data if j.get('status') == 'Review' and 'T' in (j.get('source_badges') or [])]
    print(f"\nJob codes with status 'Review' and 'T' badge: {len(review_with_t)}")
    if review_with_t:
        print("First 5 examples:")
        for j in review_with_t[:5]:
            status_detail = j.get('status_detail', {})
            print(f"  {j.get('job_code')}: badges={j.get('source_badges')}, reason={status_detail.get('reason', 'N/A')}")
    
    # Also check Review + all other badges
    review_status = [j for j in data if j.get('status') == 'Review']
    print(f"\nAll 'Review' status items: {len(review_status)}")
    badge_combinations = Counter(tuple(sorted(j.get('source_badges', []))) for j in review_status)
    print("Badge combinations for Review status:")
    for badges, count in badge_combinations.items():
        print(f"  {list(badges)}: {count}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
