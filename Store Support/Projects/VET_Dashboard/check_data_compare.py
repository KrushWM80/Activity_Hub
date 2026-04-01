"""Compare: All 51 projects vs TDA Report vs VET Dashboard"""
from google.cloud import bigquery
client = bigquery.Client(project='wmt-assetprotection-prod')

# 1. All projects (excluding Complete phase, like TDA does)
q_all = """SELECT DISTINCT Topic, TDA_Ownership, Phase, Health_Update
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Phase != 'Complete'
ORDER BY Topic"""

all_projects = {}
for row in client.query(q_all).result():
    all_projects[row.Topic] = {
        'ownership': row.TDA_Ownership,
        'phase': row.Phase,
        'health': row.Health_Update
    }

# 2. VET Dashboard projects (Dallas POC only)
vet_projects = {t for t, d in all_projects.items() if d['ownership'] == 'Dallas POC'}

# 3. Dallas VET projects (new name)
vet_new = {t for t, d in all_projects.items() if d['ownership'] == 'Dallas VET'}

# 4. TDA Report shows ALL non-Complete projects (no ownership filter)
tda_projects = set(all_projects.keys())

print(f"=== PROJECT COUNTS (excluding 'Complete' phase) ===")
print(f"  All projects: {len(all_projects)}")
print(f"  TDA Report shows: {len(tda_projects)} (all non-Complete)")
print(f"  VET Dashboard shows: {len(vet_projects)} (Dallas POC only)")
print(f"  Dallas VET ownership: {len(vet_new)}")
print()

# Projects on TDA but NOT on VET
tda_not_vet = tda_projects - vet_projects - vet_new
print(f"=== ON TDA BUT NOT ON VET ({len(tda_not_vet)}) ===")
for t in sorted(tda_not_vet):
    d = all_projects[t]
    print(f"  [{d['ownership']:<25}] [{d['phase']:<15}] {t}")

# Projects on VET but NOT on TDA (should be zero)
vet_not_tda = (vet_projects | vet_new) - tda_projects
print(f"\n=== ON VET BUT NOT ON TDA ({len(vet_not_tda)}) ===")
for t in sorted(vet_not_tda):
    print(f"  {t}")

# Check Complete phase projects (excluded from both)
q_complete = """SELECT DISTINCT Topic, TDA_Ownership
FROM `wmt-assetprotection-prod.Store_Support_Dev.Output- TDA Report`
WHERE Phase = 'Complete'"""
print(f"\n=== EXCLUDED (Complete phase) ===")
for row in client.query(q_complete).result():
    print(f"  [{row.TDA_Ownership:<25}] {row.Topic}")

# Summary
print(f"\n=== SUMMARY ===")
print(f"  TDA Report: {len(tda_projects)} projects (all ownership, excludes Complete)")
print(f"  VET Dashboard: {len(vet_projects) + len(vet_new)} projects (Dallas POC + Dallas VET only)")
print(f"  Gap: {len(tda_not_vet)} projects on TDA but missing from VET")
print(f"  All 51 unique topics, {len(all_projects)} after excluding Complete")
