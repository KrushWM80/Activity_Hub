import sys
from datetime import datetime
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from sqlite_cache import get_cache

cache = get_cache()
last_sync = cache.get_last_sync_time()
now = datetime.now()

print(f"Now: {now}")
print(f"Last sync: {last_sync}")
if last_sync:
    age_minutes = (now - last_sync).total_seconds() / 60
    print(f"Age (minutes): {age_minutes}")
    print(f"Cache max age: 30 minutes")
    print(f"Cache valid (based on age): {age_minutes < 30}")
