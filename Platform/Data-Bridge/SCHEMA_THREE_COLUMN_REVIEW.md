# AH_Projects Schema - Three-Column Review
**Date:** April 17, 2026  
**Owner:** Kendall Rush  
**Status:** Awaiting review to identify gaps

---

## HOW TO READ THIS DOCUMENT

Three columns tell the complete story:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **AH_Projects Table** (BigQuery storage) | **Intake Hub Source** (Input data) | **Projects Tab UI** (What users see) |
| What we permanently store | Where data comes from, column name | What displays in the Projects dashboard |
| Our schema | Source schema reference | Frontend display requirements |

**Gaps to identify:**
- ❌ If column X is in UI but missing from AH_Projects → we need to ADD it to schema
- ❌ If column X is in AH_Projects but missing from UI → might be data for other features (emails, reports)
- ❌ If column X is in AH_Projects but missing from Intake Hub → need to source from elsewhere (manual entry, ELM lookup, etc.)

---

## IDENTIFIERS

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `project_id` | STRING | YES | `Intake_Card_Nbr` (col 11) | INT64 | YES - Primary project identifier | Primary key for all projects |

---

## CORE PROJECT INFO

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `title` | STRING | YES | `Project_Title` (col 54) | STRING | YES - Large header "Infrastructure Modernization" | Project name |
| `status` | STRING | YES | `Status` (col 133) | STRING | YES - Status badge (Active, Archived, etc.) | Current project status |
| `phase` | STRING | NO | `Phase` (col 16) | STRING | Possibly? (Vet, Test, Roll/Deploy, Complete, Pending) | Project phase in lifecycle |
| `health` | STRING | NO | `PROJECT_HEALTH_DESC` (col 59) | STRING | YES - Health indicator (On Track / At Risk / Off Track) | Project health status |
| `business_area` | STRING | NO | `Store_Area` (col 51) | STRING | YES - Business area (Technology, Supply Chain, HR, Store Ops) | Department/business unit |

---

## OWNERSHIP & LEADERSHIP

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `owner` | STRING | NO | `Owner` (col 50) | STRING | YES - Owner name displayed | Person responsible for project |
| `owner_id` | STRING | NO | `PROJECT_OWNERID` (col 55) | STRING | NO - Used for email/lookups | Employee ID for owner |
| `director` | STRING | NO | `PROJECT_DIRECTOR` (col 64) | STRING | NO - Stored for email notifications | Director of owner |
| `director_id` | STRING | NO | `PROJECT_DIRECTOR_ID` (col 65) | STRING | NO - Used for leader emails | Employee ID for director |
| `sr_director` | STRING | NO | `PROJECT_SR_DIRECTOR` (col 66) | STRING | NO - Stored for leader communications | Senior Director of owner |
| `sr_director_id` | STRING | NO | `PROJECT_SR_DIRECTOR_ID` (col 67) | STRING | NO - Used for leader emails | Employee ID for sr_director |

---

## DATES & TIMING

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `created_date` | TIMESTAMP | YES | `CREATED_TS` (col 52) | TIMESTAMP | Possibly? (metadata) | When project recorded |
| `last_updated` | TIMESTAMP | YES | `Last_Updated` (col 37) | TIMESTAMP | YES? - "Updated: [date]" | Last modification timestamp |
| `projected_start_date` | DATE | NO | `PROJECT_START_DATE` (col 61) | DATE | Possibly? (timeline view) | Planned start date |
| `projected_completion` | DATE | NO | `PROJECT_END_DATE` (col 62) | DATE | Possibly? (timeline, Gantt) | Planned end date |
| `sif_date` | DATE | NO | `SIF_Date` (col 122) | DATE | NO - Used in backend notifications | Store Impact Forum meeting date |
| `aim_date` | DATE | NO | `AIM_Date` (col 8) | DATE | NO - Used in backend notifications | Area/Activity Impact Meeting date |

---

## PROJECT DESCRIPTION & SUMMARY

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `summary` | STRING | NO | `PRESENTATION_SUMMARY` (col 71) | STRING | YES - Brief description below title | Short 1-2 line summary |
| `overview` | STRING | NO | `OVERVIEW` (col 76) | STRING | YES (expanded) - Full description on click | Detailed multi-line overview |

---

## IMPACT ASSESSMENT

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `associate_impact` | STRING | NO | `ASSOCIATE_IMPACT` (col 110) | STRING | YES? (collapsible Impact section) | Impact on store associates |
| `customer_impact` | STRING | NO | `CUSTOMER_IMPACT` (col 112) | STRING | YES? (collapsible Impact section) | Impact on customers |
| `hq_associate_impact` | STRING | NO | **(TO BE ADDED - NOT IN INTAKE HUB)** | (new) | YES? (Impact section) | Impact on HQ associates - **NEW COLUMN NEEDED** |

---

## STORE/LOCATION INFORMATION

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `store_count` | INTEGER | NO | `Count_of_Stores` (col 127) | INT64 | YES - "Affects 45 locations" | Total unique stores affected |
| `store_numbers` | STRING | NO | **(NEED TO DETERMINE SOURCE)** | (array/delimited) | YES? (map view, filter by store) | Individual store numbers affected |
| `division` | STRING | NO | **(NEED TO CHECK IF IN INTAKE HUB)** | ? | Possibly? (geographic filter) | Division (EAST, WEST, etc.) |
| `region` | STRING | NO | **(NEED TO CHECK IF IN INTAKE HUB)** | ? | Possibly? (regional reporting) | Region name/ID |

---

## SYSTEM METADATA

| AH_Projects Column | Type | Required | Intake Hub Source | Intake Hub Type | Projects Tab UI | Notes |
|-------------------|------|----------|-------------------|-----------------|-----------------|-------|
| `project_source` | STRING | YES (auto) | **(AUTO-POPULATED)** | (none) | NO - System only | Always "Intake Hub" for synced projects |

---

## SUMMARY: COLUMNS BY CATEGORY

### ✅ CONFIRMED (All three columns aligned)
- project_id, title, status, health, business_area
- owner, owner_id, director, director_id, sr_director, sr_director_id
- created_date, last_updated
- summary, overview
- associate_impact, customer_impact
- store_count

### ⚠️ NEED CLARIFICATION (In AH_Projects but UI not confirmed)
- phase (Is this displayed? Or used in backend?)
- projected_start_date, projected_completion (Timeline view planned?)
- sif_date, aim_date (Backend only or display somewhere?)
- store_numbers (How should we store? As delimited string, JSON array, separate junction table?)

### ❌ GAP: NEW COLUMNS NEED TO BE ADDED

| What | Purpose | Source | AH_Projects Type | Notes |
|------|---------|--------|-----------------|-------|
| **hq_associate_impact** | Impact on HQ/Corporate associates | Manual entry or new Intake Hub column | STRING | **NEW** - You said Activity Hub needs this option |
| **store_numbers** | Individual store IDs/numbers | Intake Hub? Or separate lookup? | STRING (delimited) or JSON | **DECISION NEEDED** - How to store list of affected stores |
| **division** | Geographic division | Intake Hub or ELM lookup | STRING | For mapping/filtering purposes |
| **region** | Geographic region | Intake Hub or ELM lookup | STRING | For mapping/filtering purposes |

---

## QUESTIONS FOR YOU

Before I generate the final schema, please answer:

### Q1: Projects Tab UI Columns
Looking at the **Projects Tab UI** column above, which fields are actually displayed on the current Projects dashboard?
- [ ] project_id
- [ ] title
- [ ] status
- [ ] health
- [ ] business_area
- [ ] owner
- [ ] created_date / last_updated
- [ ] summary
- [ ] overview
- [ ] store_count
- [ ] phase
- [ ] Other: _________

### Q2: Store Numbers Storage
For `store_numbers` (individual store IDs affected), how should we store this?
- [ ] **Option A:** Delimited string - "1001,1023,1456,4567" (simple, searchable in SQL)
- [ ] **Option B:** JSON array - `["1001", "1023", "1456", "4567"]` (cleaner for API)
- [ ] **Option C:** Separate junction table - `AH_Projects_Stores{project_id, store_number}` (normalized, best for querying stores in dataset)
- [ ] **Option D:** Not storing individual stores, only count - pull store list separately from Intake Hub each time

### Q3: Geographic Columns
Do we need division/region in AH_Projects, or should we look those up dynamically from ELM when needed?
- [ ] Yes, store in AH_Projects (for faster filtering/reporting)
- [ ] No, look up from ELM separately (kept normalized in ELM only)
- [ ] Yes, but only if primary store is specified (not practical for multi-store projects)

### Q4: New HQ Associate Impact Column
For `hq_associate_impact` - is this:
- [ ] Free text (like associate_impact and customer_impact)?
- [ ] Dropdown with options?
- [ ] Calculated field (auto-populated based on project type)?
- [ ] Something else?

---

## NEXT STEPS

Once you answer the above questions, I will:

1. ✅ Generate final AH_Projects BigQuery table creation SQL
2. ✅ Update projects-schema.json with confirmed columns
3. ✅ Create data loader to map Intake Hub → AH_Projects
4. ✅ Identify any columns that need to come from ELM or other sources
5. ✅ Recreate the table with final schema

---

## CURRENT COLUMN COUNT

- **AH_Projects columns defined:** 20 (from earlier review)
- **New columns needed:** 4+ (HQ impact, store_numbers, division, region - TBD)
- **Estimated final count:** 24-26 columns

