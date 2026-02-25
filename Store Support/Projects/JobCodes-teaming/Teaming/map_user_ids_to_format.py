import csv
from collections import defaultdict

# File paths
EXTRACTED_CSV = "EXTRACTED_USER_IDS_BY_JOB_CODE_20260223_080251.csv"
USER_DETAILS_CSV = "User_Details_JobCodes.csv"
OUTPUT_CSV = "EXTRACTED_USER_IDS_WITH_USERID_FORMAT.csv"


# Helper to normalize names for matching
def normalize(name):
    return name.strip().lower().replace(" ", "")

def normalize_full_name(row):
    # Try to combine first and last name for robust matching
    return normalize(row.get('first_name', '') + row.get('last_name', ''))

# Step 1: Build lookup from User_Details_JobCodes.csv
user_lookup = defaultdict(list)
full_name_lookup = defaultdict(list)
user_keys_debug = []
with open(USER_DETAILS_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        key = (normalize(row['first_name']), normalize(row['last_name']), str(row['location_nm']).strip())
        user_lookup[key].append(row)
        # Also build a lookup by full name for fallback
        full_name_key = (normalize(row['first_name'] + ' ' + row['last_name']), str(row['location_nm']).strip())
        full_name_lookup[full_name_key].append(row)
        if idx < 10:
            user_keys_debug.append({'first_name': row['first_name'], 'last_name': row['last_name'], 'location_nm': row['location_nm'], 'key': key, 'full_name_key': full_name_key})

# Step 2: Process extracted associates and map to user_id format
def build_user_id(row):
    # Example: a0a0dwp.s01497 (pattern: 1 letter + 6 chars + .s + 5 digits)
    # Try to use WIN, worker_id, or construct from available fields
    # Here, just return WIN if available, else worker_id, else blank
    win = row.get('win_nbr', '')
    worker_id = row.get('worker_id', '')
    # Placeholder: you may need to adjust this logic to match your actual user_id format
    if win and win.isdigit():
        return f"w{win[-6:]}.s{row.get('location_nm','')[-5:]}"
    elif worker_id and worker_id.isdigit():
        return f"a{worker_id[-6:]}.s{row.get('location_nm','')[-5:]}"
    return ''



extracted_keys_debug = []
with open(EXTRACTED_CSV, newline='', encoding='utf-8') as fin, \
     open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as fout:
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames + ['user_id']
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    unmatched = []
    for idx, row in enumerate(reader):
        key = (normalize(row['first_name']), normalize(row['last_name']), str(row['store_number']).strip())
        matches = user_lookup.get(key, [])
        user_id = ''
        if not matches:
            # Try matching by full name (concatenated first+last)
            full_name_key = (normalize(row['full_name']), str(row['store_number']).strip())
            matches = full_name_lookup.get(full_name_key, [])
        if matches:
            user_id = build_user_id(matches[0])
        else:
            unmatched.append(row)
        row['user_id'] = user_id
        writer.writerow(row)
        if idx < 10:
            extracted_keys_debug.append({'first_name': row['first_name'], 'last_name': row['last_name'], 'store_number': row['store_number'], 'key': key, 'full_name_key': (normalize(row['full_name']), str(row['store_number']).strip())})

# Optionally, print unmatched for debugging
if unmatched:
    print(f"Unmatched rows: {len(unmatched)}. Example:")
    for r in unmatched[:10]:
        print(r)

# Print debug keys for comparison
print("\nSample keys from User_Details_JobCodes.csv:")
for k in user_keys_debug:
    print(k)
print("\nSample keys from EXTRACTED_USER_IDS_BY_JOB_CODE_20260223_080251.csv:")
for k in extracted_keys_debug:
    print(k)

print(f"Done. Output written to {OUTPUT_CSV}")
