"""
HNMeeting2 Distribution List Analysis
Identifies patterns, parameters, and outliers
"""

import csv
from collections import Counter, defaultdict
import pandas as pd

# Load the enhanced data
file = 'HNMeeting2_With_Hierarchy_20251219_115704.csv'

print("="*80)
print("HNMEETING2 DISTRIBUTION LIST ANALYSIS")
print("="*80)

# Read CSV
df = pd.read_csv(file)
total_count = len(df)

print(f"\nTotal Members: {total_count}")
print(f"Total Unique WINs: {df['WIN'].nunique()}")
print(f"Total Unique Emails: {df['Email'].nunique()}")

print("\n" + "="*80)
print("1. DEPARTMENT ANALYSIS")
print("="*80)

dept_counts = df['Department'].value_counts()
print(f"\nDepartments:")
for dept, count in dept_counts.items():
    pct = (count/total_count)*100
    print(f"  {dept}: {count} ({pct:.1f}%)")

print("\n" + "="*80)
print("2. JOB CODE ANALYSIS")
print("="*80)

job_code_counts = df['Job_Code'].value_counts()
print(f"\nTotal Unique Job Codes: {len(job_code_counts)}")
print(f"\nTop 20 Job Codes:")
for i, (code, count) in enumerate(job_code_counts.head(20).items(), 1):
    pct = (count/total_count)*100
    # Get common job title for this code
    common_title = df[df['Job_Code'] == code]['Job_Title'].mode()
    title = common_title.iloc[0] if len(common_title) > 0 else 'N/A'
    print(f"  {i:2}. {code}: {count:4} ({pct:5.1f}%) - {title}")

# Calculate threshold for "majority"
top_10_codes = job_code_counts.head(10)
top_10_total = top_10_codes.sum()
top_10_pct = (top_10_total/total_count)*100

print(f"\n✓ Top 10 Job Codes represent {top_10_total} members ({top_10_pct:.1f}%)")

print("\n" + "="*80)
print("3. JOB TITLE ANALYSIS")
print("="*80)

job_title_counts = df['Job_Title'].value_counts()
print(f"\nTotal Unique Job Titles: {len(job_title_counts)}")
print(f"\nTop 15 Job Titles:")
for i, (title, count) in enumerate(job_title_counts.head(15).items(), 1):
    pct = (count/total_count)*100
    print(f"  {i:2}. {title}: {count} ({pct:.1f}%)")

print("\n" + "="*80)
print("4. MANAGEMENT LEVEL ANALYSIS")
print("="*80)

mgmt_level_counts = df['Management_Level'].value_counts()
print(f"\nManagement Levels:")
for level, count in mgmt_level_counts.items():
    pct = (count/total_count)*100
    print(f"  {level}: {count} ({pct:.1f}%)")

print("\n" + "="*80)
print("5. HIERARCHY ANALYSIS")
print("="*80)

print(f"\nExecutive Coverage:")
print(f"  Members with EVP: {df['EVP'].notna().sum()} ({(df['EVP'].notna().sum()/total_count)*100:.1f}%)")
print(f"  Members with SVP: {df['SVP'].notna().sum()} ({(df['SVP'].notna().sum()/total_count)*100:.1f}%)")
print(f"  Members with VP: {df['VP'].notna().sum()} ({(df['VP'].notna().sum()/total_count)*100:.1f}%)")
print(f"  Members with Group Director: {df['Group_Director'].notna().sum()} ({(df['Group_Director'].notna().sum()/total_count)*100:.1f}%)")
print(f"  Members with Senior Director: {df['Senior_Director'].notna().sum()} ({(df['Senior_Director'].notna().sum()/total_count)*100:.1f}%)")
print(f"  Members with Director: {df['Director'].notna().sum()} ({(df['Director'].notna().sum()/total_count)*100:.1f}%)")

# Top EVPs
print(f"\nTop EVPs:")
evp_counts = df[df['EVP'].notna()]['EVP'].value_counts()
for evp, count in evp_counts.head(5).items():
    print(f"  {evp}: {count} members")

# Top SVPs
print(f"\nTop SVPs:")
svp_counts = df[df['SVP'].notna()]['SVP'].value_counts()
for svp, count in svp_counts.head(5).items():
    print(f"  {svp}: {count} members")

# Top VPs
print(f"\nTop VPs:")
vp_counts = df[df['VP'].notna()]['VP'].value_counts()
for vp, count in vp_counts.head(5).items():
    print(f"  {vp}: {count} members")

print("\n" + "="*80)
print("6. PATTERN IDENTIFICATION")
print("="*80)

# Define the core pattern based on top job codes
# Use actual job code from the data
market_manager_code = 'US-100015099'
market_managers = df[df['Job_Code'] == market_manager_code]
mm_count = len(market_managers)
mm_pct = (mm_count/total_count)*100

print(f"\n✓ CORE PATTERN IDENTIFIED: Market Managers")
print(f"  Job Code: {market_manager_code}")
print(f"  Count: {mm_count} members ({mm_pct:.1f}%)")
print(f"  Common Titles:")
for title in market_managers['Job_Title'].value_counts().head(5).items():
    print(f"    - {title[0]}: {title[1]}")

# Senior Directors pattern
sr_director_titles = df[df['Job_Title'].str.contains('Senior Director', case=False, na=False)]
sr_dir_count = len(sr_director_titles)
sr_dir_pct = (sr_dir_count/total_count)*100

print(f"\n✓ SECONDARY PATTERN: Senior Directors")
print(f"  Count: {sr_dir_count} members ({sr_dir_pct:.1f}%)")
print(f"  Top Job Codes:")
for code in sr_director_titles['Job_Code'].value_counts().head(5).items():
    print(f"    - {code[0]}: {code[1]}")

# Combined pattern coverage
combined_pattern = mm_count + sr_dir_count
combined_pct = (combined_pattern/total_count)*100

print(f"\n✓ COMBINED PATTERN COVERAGE:")
print(f"  Market Managers + Senior Directors: {combined_pattern} members ({combined_pct:.1f}%)")

print("\n" + "="*80)
print("7. OUTLIER IDENTIFICATION")
print("="*80)

# Define outliers as anyone NOT in the core patterns
core_patterns_mask = (
    (df['Job_Code'] == market_manager_code) |
    df['Job_Title'].str.contains('Senior Director', case=False, na=False)
)

outliers = df[~core_patterns_mask]
outlier_count = len(outliers)
outlier_pct = (outlier_count/total_count)*100

print(f"\n✓ OUTLIERS: {outlier_count} members ({outlier_pct:.1f}%)")
print(f"\nOutlier Job Titles (Top 15):")
for i, (title, count) in enumerate(outliers['Job_Title'].value_counts().head(15).items(), 1):
    print(f"  {i:2}. {title}: {count}")

print(f"\nOutlier Job Codes (Top 10):")
for i, (code, count) in enumerate(outliers['Job_Code'].value_counts().head(10).items(), 1):
    # Get title
    title = df[df['Job_Code'] == code]['Job_Title'].mode()
    title_str = title.iloc[0] if len(title) > 0 else 'N/A'
    print(f"  {i:2}. {code}: {count} - {title_str}")

# Specific outlier categories
print(f"\nOutlier Categories:")

# Directors
directors = outliers[outliers['Job_Title'].str.contains('Director', case=False, na=False)]
print(f"  Directors (not Senior): {len(directors)}")

# Vice Presidents
vps = outliers[outliers['Job_Title'].str.contains('Vice President|VP', case=False, na=False)]
print(f"  Vice Presidents: {len(vps)}")

# Managers (not Market Managers)
other_managers = outliers[
    outliers['Job_Title'].str.contains('Manager', case=False, na=False) &
    ~outliers['Job_Title'].str.contains('Market Manager', case=False, na=False)
]
print(f"  Other Managers: {len(other_managers)}")

# Specialists/Analysts
specialists = outliers[outliers['Job_Title'].str.contains('Specialist|Analyst|Coordinator', case=False, na=False)]
print(f"  Specialists/Analysts/Coordinators: {len(specialists)}")

print("\n" + "="*80)
print("8. SUMMARY & RECOMMENDATIONS")
print("="*80)

print(f"""
DISTRIBUTION LIST COMPOSITION:

PRIMARY AUDIENCE ({combined_pct:.1f}%):
  • Market Managers (Job Code: {market_manager_code}): {mm_count} members ({mm_pct:.1f}%)
  • Senior Directors: {sr_dir_count} members ({sr_dir_pct:.1f}%)

OUTLIERS ({outlier_pct:.1f}%):
  • Total: {outlier_count} members
  • Include: Other Directors, VPs, Other Managers, Specialists

HIERARCHY ALIGNMENT:
  • Most members report to VPs ({(df['VP'].notna().sum()/total_count)*100:.1f}%)
  • Strong SVP alignment ({(df['SVP'].notna().sum()/total_count)*100:.1f}%)
  • {len(evp_counts)} unique EVPs in hierarchy

DEPARTMENT:
  • Primarily Home Office (HO): {dept_counts.get('HO', 0)} ({(dept_counts.get('HO', 0)/total_count)*100:.1f}%)

KEY PARAMETERS FOR DISTRIBUTION LIST:
  1. Job Code: {market_manager_code} (Market Manager)
  2. Job Title Pattern: Contains "Market Manager" OR "Senior Director"
  3. Department: Home Office (HO)
  4. Management Level: Predominantly E-level ({(df['Management_Level'] == 'E').sum()} members, {((df['Management_Level'] == 'E').sum()/total_count)*100:.1f}%)

OUTLIER EXPLANATION:
The {outlier_pct:.1f}% outliers include:
  • Support roles for Market Manager operations
  • Executive stakeholders (VPs, other Directors)
  • Cross-functional partners (Merchandising, Operations, etc.)
  • Special project team members
""")

# Export outliers for review
outliers_file = 'HNMeeting2_Outliers_Analysis.csv'
outliers.to_csv(outliers_file, index=False)
print(f"\n✓ Outliers exported to: {outliers_file}")

print("\n" + "="*80)
