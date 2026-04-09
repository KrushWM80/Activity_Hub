"""
Query Polaris and CoreHR schemas to understand column structure for proper joins
This will help us understand:
1. How job codes are stored (single field vs broken into div/dept/code)
2. What User ID, Role, Role Type columns exist
3. How to join to TMS data
"""

# First, let's document the schema review we need to do

print("="*80)
print("SCHEMA REVIEW REQUIREMENTS")
print("="*80)

print("""
We need to examine two BigQuery sources:

1️⃣  POLARIS ANALYTICS (Job Code Authority)
   Source: polaris-analytics-prod.us_walmart.vw_polaris_current_schedule
   
   Questions to answer:
   ✓ Is job code stored as single field or three fields (div/dept/code)?
   ✓ Column names for: job_code, job_title, user_id
   ✓ Does it have role/role_type columns?
   ✓ Does it have workgroup/workgroupId columns?
   ✓ Sample data showing format (e.g., "1-202-2104" or "1", "202", "2104")

2️⃣  COREHR (User/Person Data)
   Source: wmt-corehr-prod.US_HUDI.UNIFIED_PROFILE_SENSITIVE_VW
   
   Questions to answer:
   ✓ Column names for: user_id, job_code, role, role_type
   ✓ How does job_code relate to Polaris (same format?)
   ✓ What other relevant columns for enrichment?
   ✓ Sample rows showing data relationships

---

CRITICAL INFORMATION FROM USER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  TMS Data Structure Issue:
   TMS breaks job codes into THREE columns:
   - jobCode       (likely: 1-202-2104 or just the code portion)
   - deptNumber    (likely: 202 or 0202)
   - divNumber     (likely: 1)
   
   ACTION: Confirm if Polaris stores these three ways or one way
   
✅ TMS-Specific Data (comes from TMS only):
   - teamName, teamId
   - baseDivisionCode, bannerCode
   - merchDeptNumbers
   - tlJobCode, tlJobTitle, tlDeptNumber, tlDivNumber
   - slJobCode, slDeptNumber, slDivNumber, slJobTitle
   - role (TMS role field)

❌ Data that SHOULD come from Polaris/CoreHR (not TMS):
   - workgroupId, workgroupName  ← Get from Polaris/CoreHR
   - jobCode ← Use Polaris as source of truth
   - deptNumber, divNumber ← Use Polaris breakdown
   - jobCodeTitle ← Use Polaris job name
   - accessLevel (Pay Type) ← Get from Polaris or CoreHR

---

PROPOSED QUERY STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Start with Polaris (authority)
   SELECT job_code, job_title, user_id, role, role_type, 
          workgroup_id, workgroup_name, div, dept, access_level
   FROM polaris-analytics-prod.us_walmart.vw_polaris_current_schedule

2. LEFT JOIN CoreHR (if CoreHR has additional role/user data)
   ON polaris.user_id = corehr.user_id

3. LEFT JOIN Job_Code_Master_Table.xlsx (enrichment: Category, Job Family, etc)
   ON polaris.job_code = excel.smart_code

4. LEFT JOIN TMS_Data (Teams/Teaming specific data)
   ON polaris.job_code = tms.jobCode
   (or match on div/dept/code combination if needed)

---

NEXT STEP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please provide:

A) Sample Polaris query result (first 5 rows) showing:
   - How job_code is formatted
   - Are div/dept/code separate columns?
   - What columns exist for user_id, role, role_type, workgroup?

B) Sample CoreHR query result (first 5 rows) showing:
   - What's available for user linking to job codes
   - Role/role type columns if they exist

C) Confirmation: Should I write the queries to extract this data?

If you have access to BigQuery, I can also write the SQL queries directly.
""")

print("\n" + "="*80)
print("SAVE THIS SCHEMA REVIEW TEMPLATE")
print("="*80)
print("""
Once you review the schemas, fill in this template:

POLARIS SCHEMA:
├─ Job Code Column(s):
│  ├─ Single field: _________________ (format: _______________)
│  └─ Split fields: div: _____, dept: _____, code: _____
├─ Job Title Column: _________________
├─ User ID Column: _________________
├─ Role Column: _________________
├─ Role Type Column: _________________
├─ Workgroup ID Column: _________________
├─ Workgroup Name Column: _________________
└─ Pay Type/Access Level Column: _________________

COREHR SCHEMA:
├─ User ID Column: _________________
├─ Role Column: _________________
├─ Role Type Column: _________________
├─ Job Code Link Column: _________________
└─ Other relevant columns: _________________

CONFIRMATION:
✓ Does Polaris job_code match TMS jobCode format?
✓ Do we need to reconstruct job code from div/dept/code?
✓ Should I write BigQuery SQL queries to extract this data?
""")
