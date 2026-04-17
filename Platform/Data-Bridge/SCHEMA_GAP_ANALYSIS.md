# AH_Projects Schema - Gap Analysis & Required Updates
**Date:** April 17, 2026  
**Status:** Ready for schema updates before data loading

---

## SOURCE OF TRUTH CONFIRMED

✅ **Projects Schema** (`Interface/Admin/Data-Bridge/Schemas/projects-schema.json`) is the canonical definition.

All updates must be made there first, then propagated to:
- Admin > Data Bridge > Schema Overview > Projects Schema
- Admin > Data Bridge > Field Configuration

---

## COLUMN MAPPING: CURRENT STATE

### ✅ COLUMNS ALREADY IN SCHEMA (Ready to map from Intake Hub)

| AH_Projects Column | Schema Category | Type | Required | Intake Hub Source | Intake Hub Col # |
|-------------------|-----------------|------|----------|-------------------|-----------------|
| project_id | identifiers | string | YES | Intake_Card_Nbr | 11 |
| title | identifiers | string | YES | Project_Title | 54 |
| status | status | string | YES | Status | 133 |
| phase | status | string | NO | Phase | 16 |
| health | status | string | NO | PROJECT_HEALTH_DESC | 59 |
| business_area | location | string | NO | Store_Area | 51 |
| owner | ownership | string | NO | Owner | 50 |
| director | ownership | string | NO | PROJECT_DIRECTOR | 64 |
| sr_director | ownership | string | NO | PROJECT_SR_DIRECTOR | 66 |
| created_date | time | datetime | YES | CREATED_TS | 52 |
| last_updated | time | datetime | YES | Last_Updated | 37 |
| projected_completion | time | date | NO | PROJECT_END_DATE | 62 |
| summary | description | string | NO | PRESENTATION_SUMMARY | 71 |
| overview | description | string | NO | OVERVIEW | 76 |
| associate_impact | impact | string | NO | ASSOCIATE_IMPACT | 110 |
| customer_impact | impact | string | NO | CUSTOMER_IMPACT | 112 |
| sif_date | amp_meeting | date | NO | SIF_Date | 122 |
| aim_date | amp_meeting | date | NO | AIM_Date | 8 |
| **TOTAL READY:** | | | | | **18 columns** |

---

## ❌ COLUMNS MISSING FROM SCHEMA (Must be added)

### Missing: Employee IDs (for email notifications)

| Column Name | Type | Required | Description | Intake Hub Source | Intake Hub Col # | Category | Why Needed |
|-------------|------|----------|-------------|-------------------|-----------------|----------|-----------|
| owner_id | string | NO | Employee ID of project owner | PROJECT_OWNERID | 55 | ownership | Email routing to owner |
| director_id | string | NO | Employee ID of director | PROJECT_DIRECTOR_ID | 65 | ownership | Email routing to director |
| sr_director_id | string | NO | Employee ID of sr_director | PROJECT_SR_DIRECTOR_ID | 67 | ownership | Email routing to sr_director |

### Missing: Impact & Scope

| Column Name | Type | Required | Description | Intake Hub Source | Intake Hub Col # | Category | Why Needed |
|-------------|------|----------|-------------|-------------------|-----------------|----------|-----------|
| ho_impact | string | NO | Impact on Home Office/HQ associates | (Manual entry) | N/A | impact | NEW - User requested this for HQ impact |
| impact | string | NO | Consolidated impact summary (combines customer, associate, ho) | (Calculated/Manual) | N/A | impact | NEW - Combines all impacts into one field |
| store_count | integer | NO | Total unique number of stores affected | Count_of_Stores | 127 | location | For dashboard metrics & filtering |
| facility | NEEDS UPDATE | NO | Individual store/facility numbers affected | (Multiple from Intake Hub?) | ? | location | CURRENT: single integer; NEED: support multiple values |

### Missing: Project Updates

| Column Name | Type | Required | Description | Intake Hub Source | Intake Hub Col # | Category | Why Needed |
|-------------|------|----------|-------------|-------------------|-----------------|----------|-----------|
| project_update | string | NO | Most recent project update/news | Project_Update | 2 | description | For dashboard "Latest Updates" section |

### Missing: Project Timeline

| Column Name | Type | Required | Description | Intake Hub Source | Intake Hub Col # | Category | Why Needed |
|-------------|------|----------|-------------|-------------------|-----------------|----------|-----------|
| projected_start_date | date | NO | Planned project start date | PROJECT_START_DATE | 61 | time | For timeline/Gantt chart views |

---

## 🔧 REQUIRED SCHEMA UPDATES

### Update 1: ADD to "ownership" category (3 new fields)

```json
{
  "name": "owner_id",
  "type": "string",
  "required": false,
  "description": "Employee ID of project owner",
  "aliases": ["OWNER_ID", "owner_employee_id", "OwnerID"]
},
{
  "name": "director_id",
  "type": "string",
  "required": false,
  "description": "Employee ID of director",
  "aliases": ["DIRECTOR_ID", "director_employee_id", "DirectorID"]
},
{
  "name": "sr_director_id",
  "type": "string",
  "required": false,
  "description": "Employee ID of senior director",
  "aliases": ["SR_DIRECTOR_ID", "sr_director_employee_id", "SrDirectorID"]
}
```

### Update 2: ADD to "impact" category (3 new fields)

```json
{
  "name": "ho_impact",
  "type": "string",
  "required": false,
  "description": "Impact description for Home Office (HQ) associates",
  "example": "HQ staff will need 1 hour training",
  "aliases": ["HO_IMPACT", "hq_impact", "headquarters_impact"]
},
{
  "name": "impact",
  "type": "string",
  "required": false,
  "description": "Consolidated impact summary combining customer, associate, and HO impacts",
  "example": "Multi-faceted impact: customers see UX improvement, associates need 2hr training, HQ needs 1hr training",
  "aliases": ["IMPACT", "combined_impact", "total_impact"]
}
```

### Update 3: UPDATE "location" category - ADD store_count (1 new field)

```json
{
  "name": "store_count",
  "type": "integer",
  "required": false,
  "description": "Total number of unique stores/facilities affected by project",
  "validation": {
    "minimum": 1,
    "maximum": 5000
  },
  "aliases": ["Store_Count", "store_count", "facility_count"]
}
```

### Update 4: UPDATE "location" category - CHANGE facility definition

**Current definition:**
```json
{
  "name": "facility",
  "type": "integer",
  "required": false,
  "description": "Store/facility number",
  "validation": { "minimum": 1, "maximum": 99999 },
  "aliases": ["Facility", "FACILITY", "store_number", "store", "Store", "store_id"]
}
```

**New definition (support multiple facilities):**
```json
{
  "name": "facility",
  "type": "string",
  "required": false,
  "description": "Comma-delimited list of store/facility numbers affected (e.g., '1001,1023,1456,4567')",
  "validation": {
    "pattern": "^[0-9]{4,5}(,[0-9]{4,5})*$"
  },
  "example": "1001,1023,1456",
  "aliases": ["Facility", "FACILITY", "store_numbers", "facility_list", "store_list"]
}
```

### Update 5: ADD to "description" category (1 new field)

```json
{
  "name": "project_update",
  "type": "string",
  "required": false,
  "description": "Most recent project update or news",
  "validation": {
    "maxLength": 5000
  },
  "aliases": ["PROJECT_UPDATE", "Project_Update", "project_update_text", "latest_news"]
}
```

### Update 6: ADD to "time" category (1 new field)

```json
{
  "name": "projected_start_date",
  "type": "date",
  "required": false,
  "description": "Planned project start date",
  "format": "YYYY-MM-DD",
  "aliases": ["Projected_Start_Date", "start_date", "project_start"]
}
```

---

## SUMMARY: COLUMNS FOR AH_PROJECTS POPULATION

### ✅ READY TO LOAD (18 columns - already in schema)
1. project_id
2. title
3. status
4. phase
5. health
6. business_area
7. owner
8. director
9. sr_director
10. created_date
11. last_updated
12. projected_completion
13. summary
14. overview
15. associate_impact
16. customer_impact
17. sif_date
18. aim_date

### ⚠️ NEED SCHEMA UPDATES FIRST (8 columns - must add before loading)
1. owner_id (from PROJECT_OWNERID)
2. director_id (from PROJECT_DIRECTOR_ID)
3. sr_director_id (from PROJECT_SR_DIRECTOR_ID)
4. store_count (from Count_of_Stores)
5. facility (change type to string, support multiple stores)
6. project_update (from Project_Update)
7. projected_start_date (from PROJECT_START_DATE)
8. ho_impact (manual entry or new Intake Hub column)
9. impact (calculated/manual field)

---

## NEXT STEPS

### Step 1: Update Projects Schema (in Admin UI)
You will need to add/update the schema fields in:
- Admin > Data Bridge > Schema Overview > Projects Schema
- Admin > Data Bridge > Field Configuration

**Fields to add/update:**
- ownership: owner_id, director_id, sr_director_id
- impact: ho_impact, impact
- location: store_count, facility (change type)
- description: project_update
- time: projected_start_date

### Step 2: Once Schema is Updated
I will:
1. Generate BigQuery table creation SQL with all 26 columns
2. Create data loader to map Intake Hub → AH_Projects
3. Deploy AH_Projects table with correct schema

---

## ANSWER TO YOUR QUESTION

> "Do you have the columns you need for Projects to populate the Intake Hub Data?"

**Almost.** I have 18 columns ready to go from Intake Hub. 

But I need 8 additional columns in the schema first:
- ✅ 3 employee IDs (owner_id, director_id, sr_director_id) - available from Intake Hub
- ✅ 1 update field (project_update) - available from Intake Hub  
- ✅ 1 date field (projected_start_date) - available from Intake Hub
- ✅ 1 count field (store_count) - available from Intake Hub
- ✅ 1 facility field (needs type change to string) - **might** need custom source (TBD)
- ⚠️ 2 impact fields (ho_impact, impact) - NOT in Intake Hub, need manual/calculated mechanism

**Can we proceed with schema updates?** Once you update the Projects Schema in Admin UI, I can build the full data loader.

