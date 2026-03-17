# Data Source Alignment Analysis

## TMS Data (3).xlsx - Column Alignment

| Column Name | Expected | Actual | Status | Used For |
|---|---|---|---|---|
| jobCode | ✓ | ✓ | **ALIGNED** | Part of composite key (div-dept-job) |
| deptNumber | ✓ | ✓ | **ALIGNED** | Part of composite key |
| divNumber | ✓ | ✓ | **ALIGNED** | Part of composite key |
| jobCodeTitle | ✓ | ✗ | **MISSING** | Job title in API response |
| teamName | ✓ | ✗ | **MISSING** | Teams aggregation |
| teamId | ✓ | ✗ | **MISSING** | Team IDs in response |
| workgroupName | ✓ | ✗ | **MISSING** | Workgroup aggregation |
| workgroupId | ✓ | ✗ | **MISSING** | Workgroup IDs in response |

**Score: 3/8 columns (37.5%)**

---

## polaris_job_codes.csv - Column Alignment

| Column Name | Expected | Actual | Status | Used For |
|---|---|---|---|---|
| job_code | ✓ | ✓ | **ALIGNED** | Merge key with Teaming summary |
| job_nm | ✓ | ✓ | **ALIGNED** | Job name in API response |

**Score: 2/2 columns (100%)**

---

## polaris_user_counts.csv - Column Alignment

| Column Name | Expected | Actual | Status | Used For |
|---|---|---|---|---|
| job_code | ✓ | ✓ | **ALIGNED** | Merge key |
| user_count | ✓ | ✓ | **ALIGNED** | Employee count in response |

**Score: 2/2 columns (100%)**

---

## API Response Field Mapping

| Field | Source Table | Column | Status | Impact |
|---|---|---|---|---|
| job_code | polaris_job_codes | job_code | ✓ | Data returned |
| job_name | polaris_job_codes | job_nm | ✓ | Data returned |
| job_title | **TMS Data** | jobCodeTitle | ✗ | **500 ERROR** - Column missing |
| status | polaris_job_codes → TMS (merge) | composite_job_code | ✗ | **500 ERROR** - Can't merge, TMS incomplete |
| teams | **TMS Data** | teamName | ✗ | **500 ERROR** - Column missing |
| team_ids | **TMS Data** | teamId | ✗ | **500 ERROR** - Column missing |
| workgroups | **TMS Data** | workgroupName | ✗ | **500 ERROR** - Column missing |
| workgroup_ids | **TMS Data** | workgroupId | ✗ | **500 ERROR** - Column missing |
| user_count | polaris_user_counts | user_count | ✓ | Data returned |
| division | **TMS Data** | divNumber | ✓ | Data available |
| department | **TMS Data** | deptNumber | ✓ | Data available |

---

## Summary

### ✓ What Works
- Polaris job codes file: 100% aligned
- User counts file: 100% aligned
- Basic composite key creation: divNumber + deptNumber + jobCode
- Division & Department fields available in TMS

### ✗ What Breaks the API
- **TMS Data is 62.5% incomplete** (5 out of 8 required columns missing)
- **Missing critical fields**: jobCodeTitle, teamName, teamId, workgroupName, workgroupId
- **Result**: Backend crashes when trying to aggregate/merge these columns (lines 205-212 in main.py)

### 🔧 Solutions
1. **Add the 5 missing columns to TMS Data (3).xlsx** - Populate with teaming assignment data
2. **Simplify the backend** - Remove team/workgroup aggregation if not needed
3. **Use a different data source** - Replace TMS Data with a complete teaming dataset
