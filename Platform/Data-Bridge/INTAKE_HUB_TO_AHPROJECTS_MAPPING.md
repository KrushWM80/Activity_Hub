# AH_Projects Table - Focused Column Mapping
**Date:** April 17, 2026  
**Source:** Intake Hub - `Output - Intake Accel Council Data` (197 columns total)  
**Target:** AH_Projects table (to be created)

---

## KEY FINDINGS

**Intake Hub has 197 columns** - but we only need a subset for AH_Projects.

### Essential Intake Hub Columns (MUST HAVE)

| Position | Intake Hub Column | Data Type | Maps To AH_Projects | Notes |
|----------|-------------------|-----------|-------------------|-------|
| 11 | `Intake_Card_Nbr` | INT64 | `project_id` | Primary unique identifier for project coming from Intake Hub |
| 54 | `Project_Title` | STRING | `title` | Project name |
| 50 | `Owner` | STRING | `owner` | Project owner name |
| 55 | `PROJECT_OWNERID` | STRING | `owner_id` | Project owner employee ID |
| 52 | `CREATED_TS` | TIMESTAMP | `created_date` | When project was created |
| 37 | `Last_Updated` | TIMESTAMP | `last_updated` | Last time project was updated |
| 133 | `Status` | STRING | `status` | Project status (Active, etc.) |

### Important Columns (Business Logic)

| Position | Intake Hub Column | Data Type | Maps To AH_Projects | Notes |
|----------|-------------------|-----------|-------------------|-------|
| 51 | `Store_Area` | STRING | `business_area` | Business area within organization |
| 59 | `PROJECT_HEALTH_DESC` | STRING | `health` | Project health (Green/Yellow/Red) |
| 16 | `Phase` | STRING | `phase` | Project phase (Vet, Test, Roll/Deploy, Complete, Pending) |
| 54 | `Project_Title` | STRING | `title` | Project title |
| 76 | `OVERVIEW` | STRING | `overview` | Detailed project description |
| 71 | `PRESENTATION_SUMMARY` | STRING | `summary` | Brief project summary |
| 61 | `PROJECT_START_DATE` | DATE | `projected_start_date` | When project starts |
| 62 | `PROJECT_END_DATE` | DATE | `projected_completion` | When project ends |

### Leadership/Approval Chain

| Position | Intake Hub Column | Data Type | Maps To AH_Projects | Notes |
|----------|-------------------|-----------|-------------------|-------|
| 64 | `PROJECT_DIRECTOR` | STRING | `director` | Director overseeing project |
| 65 | `PROJECT_DIRECTOR_ID` | STRING | `director_id` | Director employee ID |
| 66 | `PROJECT_SR_DIRECTOR` | STRING | `sr_director` | Senior Director overseeing project |
| 67 | `PROJECT_SR_DIRECTOR_ID` | STRING | `sr_director_id` | Senior Director employee ID |

### Meeting Dates

| Position | Intake Hub Column | Data Type | Maps To AH_Projects | Notes |
|----------|-------------------|-----------|-------------------|-------|
| 122 | `SIF_Date` | DATE | `sif_date` | Store Impact Forum (SIF) meeting date |
| 8 | `AIM_Date` | DATE | `aim_date` | Area/Activity Impact Meeting (AIM) date |

### Impact/Scope

| Position | Intake Hub Column | Data Type | Maps To AH_Projects | Notes |
|----------|-------------------|-----------|-------------------|-------|
| 110 | `ASSOCIATE_IMPACT` | STRING | `associate_impact` | Impact on associates/employees |
| 112 | `CUSTOMER_IMPACT` | STRING | `customer_impact` | Impact on customers |
| 127 | `Count_of_Stores` | INT64 | `store_count` | Number of stores affected |

### Project Source/Reference

| Position | Intake Hub Column | Data Type | Maps To AH_Projects | Notes |
|----------|-------------------|-----------|-------------------|-------|
| (auto) | (N/A) | STRING | `project_source` | AUTO-POPULATED: Always "Intake Hub" for synced projects |

---

## STORE LOCATION DATA - HANDLED SEPARATELY

**Important:** You mentioned store locations are specific and should come from ELM knowledge base, NOT from Intake Hub directly.

**Design Decision:**
- Do NOT include individual store columns from Intake Hub (store_id, city, state, etc.)
- `store_count` tells us HOW MANY stores affected
- Store location details should be looked up separately via ELM data if needed
- AH_Projects stores a reference/indicator, not full location details

---

## COLUMNS TO EXCLUDE (NOT NEEDED FOR AH_PROJECTS)

These 197 - 20 = **177 columns exist in Intake Hub but are NOT needed for AH_Projects:**
- Defect tracking columns (Defect_Type, Defect_ID, etc.)
- Validation columns (Validation_Type, Validation_Status, etc.)
- Task/JIRA columns (ASSIGNED_TO, TASK_START_DATE, etc.)
- Process/approval columns (various "Status_" fields)
- Calendar/fiscal year columns (not needed - we use Intake Hub timing)
- And many others that are Intake Hub-specific

---

## FINAL AH_PROJECTS SCHEMA (20 COLUMNS)

**This is what we need to create in BigQuery:**

```
1. project_id (STRING, PRIMARY KEY)
   - Source: Intake_Card_Nbr from Intake Hub
   - Required: YES
   
2. title (STRING)
   - Source: Project_Title
   - Required: YES
   
3. status (STRING)
   - Source: Status
   - Required: YES
   - Enum: Active, Archived, Pending, Cancelled, Complete
   
4. project_source (STRING)
   - Auto-populated: "Intake Hub"
   - Required: YES
   
5. owner (STRING)
   - Source: Owner
   - Required: NO
   
6. owner_id (STRING)
   - Source: PROJECT_OWNERID
   - Required: NO
   
7. director (STRING)
   - Source: PROJECT_DIRECTOR
   - Required: NO
   
8. director_id (STRING)
   - Source: PROJECT_DIRECTOR_ID
   - Required: NO
   
9. sr_director (STRING)
   - Source: PROJECT_SR_DIRECTOR
   - Required: NO
   
10. sr_director_id (STRING)
    - Source: PROJECT_SR_DIRECTOR_ID
    - Required: NO
    
11. business_area (STRING)
    - Source: Store_Area
    - Required: NO
    
12. health (STRING)
    - Source: PROJECT_HEALTH_DESC
    - Required: NO
    - Enum: Green, Yellow, Red, Unknown
    
13. phase (STRING)
    - Source: Phase
    - Required: NO
    - Enum: Vet, Test, Test Markets, Roll/Deploy, Complete, Pending, Planning
    
14. created_date (TIMESTAMP)
    - Source: CREATED_TS
    - Required: YES
    
15. last_updated (TIMESTAMP)
    - Source: Last_Updated
    - Required: YES
    
16. projected_start_date (DATE)
    - Source: PROJECT_START_DATE
    - Required: NO
    
17. projected_completion (DATE)
    - Source: PROJECT_END_DATE
    - Required: NO
    
18. summary (STRING)
    - Source: PRESENTATION_SUMMARY
    - Required: NO
    - Max length: 2000 chars
    
19. overview (STRING)
    - Source: OVERVIEW
    - Required: NO
    - Max length: 10000 chars
    
20. associate_impact (STRING)
    - Source: ASSOCIATE_IMPACT
    - Required: NO

21. customer_impact (STRING)
    - Source: CUSTOMER_IMPACT
    - Required: NO

22. sif_date (DATE)
    - Source: SIF_Date
    - Required: NO
    
23. aim_date (DATE)
    - Source: AIM_Date
    - Required: NO
    
24. store_count (INTEGER)
    - Source: Count_of_Stores
    - Required: NO
    - Purpose: How many stores affected (for informational use)
```

---

## YOUR REVIEW CHECKLIST

Please confirm:

- [ ] **project_id mapping:** Using `Intake_Card_Nbr` from Intake Hub? (column 11)
- [ ] **Essential fields:** title, owner, status, dates - correct?
- [ ] **Leadership chain:** Need director + sr_director? Or simplify to owner only?
- [ ] **Store info:** NOT pulling individual store data from Intake Hub - correct? (ELM lookup separately)
- [ ] **Meeting dates:** Keep sif_date and aim_date?
- [ ] **Impact fields:** Keep associate_impact and customer_impact?
- [ ] **Count:** Store count field useful?

Once you confirm, I'll:
1. Generate BigQuery table creation SQL
2. Update projects-schema.json with final columns
3. Create the data loader to map Intake Hub → AH_Projects
