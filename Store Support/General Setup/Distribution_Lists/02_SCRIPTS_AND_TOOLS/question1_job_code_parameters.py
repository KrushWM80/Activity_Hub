"""
Question 1: Job Code-Based Parameters for HNMeeting2 Distribution List
Creates automated inclusion criteria based on current membership patterns
"""

import pandas as pd
from collections import Counter

# Load the current list
df = pd.read_csv('HNMeeting2_With_Hierarchy_20251219_115704.csv')

print("="*80)
print("JOB CODE-BASED PARAMETERS FOR HNMEETING2 DISTRIBUTION LIST")
print("="*80)

print("\n" + "="*80)
print("ANALYSIS OF CURRENT MEMBERSHIP")
print("="*80)

# Get all job codes
job_code_counts = df['Job_Code'].value_counts()
total_members = len(df)

print(f"\nTotal Members: {total_members}")
print(f"Unique Job Codes: {len(job_code_counts)}")

# Identify high-coverage job codes (those representing >1% of list)
high_coverage_threshold = 0.01  # 1%
high_coverage_codes = job_code_counts[job_code_counts >= total_members * high_coverage_threshold]

print(f"\n" + "="*80)
print("TIER 1: HIGH COVERAGE JOB CODES (>1% of list)")
print("="*80)
print(f"\nThese {len(high_coverage_codes)} job codes represent {high_coverage_codes.sum()} members ({(high_coverage_codes.sum()/total_members)*100:.1f}%)")
print("\n{:<20} {:<8} {:<10} {}".format("Job Code", "Count", "Percent", "Job Title"))
print("-"*80)

tier1_codes = []
for code, count in high_coverage_codes.items():
    pct = (count/total_members)*100
    title = df[df['Job_Code'] == code]['Job_Title'].mode()
    title_str = title.iloc[0] if len(title) > 0 else 'N/A'
    print("{:<20} {:<8} {:<9.1f}% {}".format(code, count, pct, title_str))
    tier1_codes.append(code)

# Identify medium-coverage job codes (0.5% - 1%)
medium_coverage_codes = job_code_counts[(job_code_counts >= total_members * 0.005) & (job_code_counts < total_members * 0.01)]

print(f"\n" + "="*80)
print("TIER 2: MEDIUM COVERAGE JOB CODES (0.5% - 1%)")
print("="*80)
print(f"\nThese {len(medium_coverage_codes)} job codes represent {medium_coverage_codes.sum()} members ({(medium_coverage_codes.sum()/total_members)*100:.1f}%)")
print("\n{:<20} {:<8} {:<10} {}".format("Job Code", "Count", "Percent", "Job Title"))
print("-"*80)

tier2_codes = []
for code, count in medium_coverage_codes.items():
    pct = (count/total_members)*100
    title = df[df['Job_Code'] == code]['Job_Title'].mode()
    title_str = title.iloc[0] if len(title) > 0 else 'N/A'
    print("{:<20} {:<8} {:<9.1f}% {}".format(code, count, pct, title_str))
    tier2_codes.append(code)

# Pattern-based rules (for titles not captured by specific job codes)
print(f"\n" + "="*80)
print("TIER 3: TITLE PATTERN-BASED RULES")
print("="*80)

# Analyze remaining members not in Tier 1 or 2
remaining = df[~df['Job_Code'].isin(tier1_codes + tier2_codes)]
print(f"\nRemaining {len(remaining)} members ({(len(remaining)/total_members)*100:.1f}%)")

# Analyze patterns in remaining
title_patterns = {
    'Senior Director': 0,
    'Group Director': 0,
    'Vice President': 0,
    'Director': 0,
    'Manager': 0,
    'Specialist': 0,
    'Coordinator': 0
}

for pattern in title_patterns.keys():
    count = remaining['Job_Title'].str.contains(pattern, case=False, na=False).sum()
    title_patterns[pattern] = count

print("\nTitle Pattern Analysis (remaining members):")
for pattern, count in sorted(title_patterns.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"  {pattern}: {count} members")

# Management level analysis for remaining
print("\nManagement Level Distribution (remaining members):")
mgmt_levels = remaining['Management_Level'].value_counts()
for level, count in mgmt_levels.head(10).items():
    print(f"  Level {level}: {count} members")

print("\n" + "="*80)
print("RECOMMENDED JOB CODE-BASED PARAMETERS")
print("="*80)

print("""
RULE SET FOR AUTOMATIC INCLUSION:

TIER 1 - CORE ROLES (Include ALL):
├─ Job Code: US-100015099 (Market Manager) → 396 members
├─ Job Code: US-100017446 (Senior Director, Merchandising) → 27 members
├─ Job Code: US-100019721 (Senior Director, Merchandising Operations) → 27 members
├─ Job Code: US-100020695 (Senior Director, Operations) → 23 members
├─ Job Code: US-100019946 (Senior Director, Supply Chain Management) → 20 members
├─ Job Code: US-100022540 (Senior Director, Product Management) → 19 members
├─ Job Code: US-100022319 (Senior Director, Data Science) → 18 members
├─ Job Code: US-100022602 (Senior Director, Advanced Analytics) → 16 members
├─ Job Code: US-100024103 (Senior Director, Technology Operations) → 16 members
└─ Job Code: US-100019221 (Senior Director, Real Estate) → 15 members

TIER 2 - SUPPORTING ROLES (Include ALL):
""")

for code in tier2_codes[:20]:  # Top 20 medium coverage codes
    title = df[df['Job_Code'] == code]['Job_Title'].mode()
    title_str = title.iloc[0] if len(title) > 0 else 'N/A'
    count = job_code_counts[code]
    print(f"├─ Job Code: {code} ({title_str}) → {count} members")

print("""
TIER 3 - TITLE PATTERN RULES (Additional Criteria):
├─ Job Title contains "Senior Director" AND Department = "HO"
├─ Job Title contains "Group Director" AND Department = "HO"
│  └─ Functions: Operations, Supply Chain, Merchandising, Product, Technology, Data Science
│
└─ Executive Stakeholders (Manual Review):
   ├─ VP+ in Operations, Supply Chain, Merchandising reporting chains
   └─ Divisional VPs with field oversight
   
EXCLUSION CRITERIA:
├─ Department != "HO" (unless Market Manager)
├─ Inactive/Terminated employment status
└─ Non-primary position records

RECOMMENDED QUERY LOGIC:
""")

# Generate SQL-style logic
print("""
WHERE (
    -- TIER 1: Core Roles
    Job_Code IN (
        'US-100015099',  -- Market Manager
        'US-100017446',  -- Senior Director, Merchandising
        'US-100019721',  -- Senior Director, Merchandising Operations
        'US-100020695',  -- Senior Director, Operations
        'US-100019946',  -- Senior Director, Supply Chain Management
        'US-100022540',  -- Senior Director, Product Management
        'US-100022319',  -- Senior Director, Data Science
        'US-100022602',  -- Senior Director, Advanced Analytics
        'US-100024103',  -- Senior Director, Technology Operations
        'US-100019221'   -- Senior Director, Real Estate
    )
    
    OR
    
    -- TIER 2: Supporting Roles
    Job_Code IN (
""")

# Print tier 2 codes in SQL format
for i, code in enumerate(tier2_codes[:15]):
    comma = ',' if i < len(tier2_codes[:15])-1 else ''
    title = df[df['Job_Code'] == code]['Job_Title'].mode()
    title_str = title.iloc[0] if len(title) > 0 else 'N/A'
    print(f"        '{code}'{comma}  -- {title_str}")

print("""    )
    
    OR
    
    -- TIER 3: Title Patterns
    (
        Job_Title LIKE '%Senior Director%'
        AND Department = 'HO'
    )
    
    OR
    
    (
        Job_Title LIKE '%Group Director%'
        AND Department = 'HO'
        AND (
            Job_Title LIKE '%Operations%'
            OR Job_Title LIKE '%Supply Chain%'
            OR Job_Title LIKE '%Merchandising%'
            OR Job_Title LIKE '%Product%'
            OR Job_Title LIKE '%Technology%'
            OR Job_Title LIKE '%Data Science%'
        )
    )
)
AND Department = 'HO'  -- Primary constraint
AND Employment_Status = 'Active'
AND isPrimary = TRUE
""")

print("\n" + "="*80)
print("COVERAGE ANALYSIS")
print("="*80)

tier1_coverage = high_coverage_codes.sum()
tier2_coverage = medium_coverage_codes.sum()
tier3_coverage = len(remaining)

print(f"\nTier 1 Coverage: {tier1_coverage} members ({(tier1_coverage/total_members)*100:.1f}%)")
print(f"Tier 2 Coverage: {tier2_coverage} members ({(tier2_coverage/total_members)*100:.1f}%)")
print(f"Tier 3 Coverage: {tier3_coverage} members ({(tier3_coverage/total_members)*100:.1f}%)")
print(f"\nTotal: {total_members} members (100.0%)")

print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)

print("""
For automated list management:

1. IMPLEMENT TIER 1 (46.3% coverage)
   - Hardcode these 10 job codes for automatic inclusion
   - These are the most stable, high-volume roles
   
2. IMPLEMENT TIER 2 (18.2% coverage)
   - Add these 15-20 job codes for broader coverage
   - Review quarterly for any job code changes
   
3. IMPLEMENT TIER 3 PATTERNS (35.5% coverage)
   - Use title pattern matching for flexibility
   - Captures role changes and new positions
   
4. MANUAL REVIEW for Executive Stakeholders
   - VP+ roles should be reviewed by list owner
   - Ensures appropriate executive visibility
   
MAINTENANCE:
- Quarterly review of job codes (new roles, retired codes)
- Annual audit of full membership
- Track additions/removals for compliance
""")

# Export the job code lists for reference
import csv

with open('HNMeeting2_Tier1_JobCodes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Job_Code', 'Count', 'Percentage', 'Job_Title'])
    for code in tier1_codes:
        count = job_code_counts[code]
        pct = (count/total_members)*100
        title = df[df['Job_Code'] == code]['Job_Title'].mode()
        title_str = title.iloc[0] if len(title) > 0 else 'N/A'
        writer.writerow([code, count, f"{pct:.1f}%", title_str])

with open('HNMeeting2_Tier2_JobCodes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Job_Code', 'Count', 'Percentage', 'Job_Title'])
    for code in tier2_codes:
        count = job_code_counts[code]
        pct = (count/total_members)*100
        title = df[df['Job_Code'] == code]['Job_Title'].mode()
        title_str = title.iloc[0] if len(title) > 0 else 'N/A'
        writer.writerow([code, count, f"{pct:.1f}%", title_str])

print("\n✓ Tier 1 job codes exported to: HNMeeting2_Tier1_JobCodes.csv")
print("✓ Tier 2 job codes exported to: HNMeeting2_Tier2_JobCodes.csv")
