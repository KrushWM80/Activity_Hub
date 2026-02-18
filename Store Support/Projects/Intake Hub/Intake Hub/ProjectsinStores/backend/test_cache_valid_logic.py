import sys
sys.path.insert(0, '/c/Users/krush/Documents/VSCode/Intake Hub/ProjectsinStores/backend')

from sqlite_cache import get_cache

cache = get_cache()
print(f"Cache valid: {cache.is_cache_valid()}")
print(f"Record count: {cache.get_record_count()}")

# Check the is_cache_valid logic step-by-step
last_sync = cache.get_last_sync_time()
has_data = cache.get_record_count() > 0

print(f"Has data: {has_data}")
print(f"Last sync: {last_sync}")

if has_data and not last_sync:
    print("Branch 1: Has data but no sync time - VALID")
elif not last_sync:
    print("Branch 2: No sync time - INVALID")
else:
    from datetime import datetime
    age = (datetime.now() - last_sync).total_seconds() / 60
    print(f"Age (min): {age}")
    print(f"Max age: 30 min")
    if age < 0:
        print("Branch 3: Negative age - VALID (clock skew)")
    elif has_data and age < 30:
        print("Branch 4: Has data and < 30 min - VALID")
    else:
        print(f"Branch 5: Failed check - INVALID (has_data={has_data}, age={age})")
