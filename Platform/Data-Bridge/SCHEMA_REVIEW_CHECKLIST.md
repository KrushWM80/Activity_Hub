# Project Schema Review & Finalization Checklist
**Date:** April 17, 2026  
**Owner:** Kendall Rush  
**Purpose:** Finalize which 40 columns we actually need before recreating AH_Projects table

---

## Instructions
1. Go through each section below
2. For each column, mark **Keep** (✓), **Remove** (✗), or **Rename** (with new name)
3. Add notes if mapping from Intake Hub is different than shown
4. Examples: `Intake_Card` = project identifier from source, but we call it `project_id`

---

## IDENTIFIERS (3 columns)
**Purpose:** Unique identifiers for projects and records

| Column | Type | Required | Description | Keep? | Notes |
|--------|------|----------|-------------|-------|-------|
| `project_id` | string | ✓ YES | **Our primary key** - Unique project identifier | ✓ KEEP | Maps from Intake Hub: `intake_card` or generated UUID |
| `intake_card` | string | NO | Intake card number (source system identifier) | ❓ REVIEW | Is this needed? Or covered by `project_id`? |
| `title` | string | ✓ YES | Project name/title | ✓ KEEP | From Intake Hub: `Title` or `project_name` |

**Your input here:**
- [ ] Keep `project_id` as primary identifier
- [ ] Keep `intake_card` (YES / NO) - Why or why not?
- [ ] Keep `title` as project name

**Notes on Identifiers:**
```
Current confusion: "intake_card" suggests it's an Intake Hub field, but we use "project_id" 
as our primary key. Need clarity: is intake_card a secondary reference to the source system?
```

---

## STATUS (4 columns)
**Purpose:** Project status and health indicators

| Column | Type | Required | Enum Values | Keep? | Notes |
|--------|------|----------|-------------|-------|-------|
| `status` | string | ✓ YES | Active, Archived, Pending, Cancelled, Complete | ✓ KEEP | Project lifecycle status |
| `phase` | string | NO | Vet, Test, Test Markets, Roll/Deploy, Complete, Pending, Planning | ❓ REVIEW | Do we track phase separately? |
| `health` | string | NO | Green, Yellow, Red, Unknown | ❓ REVIEW | Used in current dashboard? |
| `project_source` | string | ✓ YES (auto) | Operations, Realty, Intake Hub, Manual Upload, API | ✓ KEEP | Auto-populated by upload method |

**Your input here:**
- [ ] Keep `status` (primary status field)
- [ ] Keep `phase` (YES / NO) - Same as status or different?
- [ ] Keep `health` (YES / NO) - Used for dashboards?
- [ ] Keep `project_source` (auto-populated field)

**Current issue in AH_Projects:**
```
We have both "health_status" and "project_status" which map to "health" and "status" here.
Confirm we only need one of each.
```

---

## LOCATION (10 columns)
**Purpose:** Geographic and organizational location data

| Column | Type | Required | Validation | Keep? | Notes |
|--------|------|----------|-----------|-------|-------|
| `division` | string | NO | EAST, WEST, NORTH, SOUTH, SOUTHEAST, SOUTHWEST, NHM, SAM | ❓ REVIEW | For store-level projects only? |
| `region` | string | NO | (no preset enum) | ❓ REVIEW | Regional classification? |
| `market` | string | NO | 3-digit format: "001"-"999" | ❓ REVIEW | Market number usage? |
| `facility` | integer | NO | 1-99999 | ❓ REVIEW | Store number for facility-specific projects? |
| `city` | string | NO | (no preset enum) | ❓ REVIEW | Store city? |
| `state` | string | NO | 2-letter US state code | ❓ REVIEW | Store state? |
| `postal_code` | string | NO | US ZIP format validation | ❓ REVIEW | Store ZIP code? |
| `latitude` | float | NO | -90 to +90 | ❓ REVIEW | Geographic coordinates? |
| `longitude` | float | NO | -180 to +180 | ❓ REVIEW | Geographic coordinates? |
| `business_area` | string | NO | (no preset enum) | ✓ KEEP | Department/business unit within facility |

**Your input here:**
- In current dashboard, are projects location-specific (store #1234 in Dallas) or company-wide?
- Do you track regional/market/facility info or just business area (HR, Store Ops, Supply Chain)?
- [ ] Keep only `business_area` (remove geographic fields)
- [ ] Keep some geographic fields: ___________ (list which ones)
- [ ] Keep all 10 location fields

---

## TIME (6 columns)
**Purpose:** Dates, timestamps, and calendar references

| Column | Type | Required | Format | Keep? | Notes |
|--------|------|----------|--------|-------|-------|
| `created_date` | datetime | ✓ YES | ISO8601 | ✓ KEEP | Record creation timestamp |
| `last_updated` | datetime | ✓ YES | ISO8601 | ✓ KEEP | Last update timestamp |
| `projected_completion` | date | NO | YYYY-MM-DD | ❓ REVIEW | Project end date? |
| `wm_week` | integer | NO | 1-53 | ❓ REVIEW | Walmart week number (current WM WK)? |
| `fiscal_year` | integer | NO | YYYY format | ❓ REVIEW | Fiscal year tracking? |
| `implementation_week` | string | NO | (no format spec) | ❓ REVIEW | When project goes live? |

**Your input here:**
- Do projects have target completion dates?
- Do you track Walmart week numbers (WM WK 11)?
- Do you need to track fiscal year (FY26, FY27)?
- [ ] Keep `created_date`, `last_updated` only
- [ ] Add `projected_completion` or `end_date`
- [ ] Add `wm_week` or `fiscal_year` tracking
- [ ] Add other time fields: _________

**Note:** Current AH_Projects has `latest_update_timestamp` which isn't in the schema. Is that different from `last_updated`?

---

## OWNERSHIP (3 columns)
**Purpose:** Project ownership and personnel

| Column | Type | Required | Description | Keep? | Notes |
|--------|------|----------|-------------|-------|-------|
| `owner` | string | NO | Project owner name | ✓ KEEP | Should map to `owner_name` in current table |
| `director` | string | NO | Director overseeing project | ❓ REVIEW | Multi-level approval chain needed? |
| `sr_director` | string | NO | Senior Director overseeing project | ❓ REVIEW | Or just one approval level? |

**Your input here:**
- Current dashboard shows `owner_name` - is this the same as `owner`?
- Do projects have approval chain (owner → director → sr_director)?
- [ ] Keep `owner` only
- [ ] Keep `owner`, `director`, `sr_director` (full chain)
- [ ] Rename `owner` to something else: ___________

**Note:** Current AH_Projects also has `owner_id`. Should we keep numeric IDs along with names?

---

## CATEGORIZATION (6 columns)
**Purpose:** Project type and classification fields

| Column | Type | Required | Description | Keep? | Notes |
|--------|------|----------|-------------|-------|-------|
| `project_type` | string | NO | Type of project | ❓ REVIEW | E.g., "Store Remodel", "System Upgrade", etc.? |
| `initiative_type` | string | NO | Initiative classification | ❓ REVIEW | E.g., "Cost Reduction", "Revenue Growth"? |
| `business_type` | string | NO | Business type classification | ❓ REVIEW | Same as business_area or different? |
| `facility_type` | string | NO | Facility type (store format) | ❓ REVIEW | E.g., "Supercenter", "Neighborhood Market"? |
| `partner` | string | NO | Partner organization | ❓ REVIEW | External vendor/partner? |
| `business_organization` | string | NO | Business organization/department | ❓ REVIEW | Org structure (e.g., "Store Operations", "Supply Chain")? |

**Your input here:**
- Do you categorize projects by type (Store Remodel, System Upgrade)?
- Do you track initiative type (Revenue vs. Cost)?
- Is `business_organization` same as `business_area`?
- [ ] Keep none of these (too granular)
- [ ] Keep `project_type` only
- [ ] Keep `initiative_type` only
- [ ] Keep all 6
- [ ] Custom list: ___________

---

## IMPACT (2 columns)
**Purpose:** Project impact assessment fields

| Column | Type | Required | Description | Keep? | Notes |
|--------|------|----------|-------------|-------|-------|
| `associate_impact` | string | NO | Impact for associates/employees | ❓ REVIEW | E.g., "2 hours training required" |
| `customer_impact` | string | NO | Impact for customers | ❓ REVIEW | E.g., "Improved checkout experience" |

**Your input here:**
- Do projects document impact on associates and customers?
- [ ] Keep both
- [ ] Keep `associate_impact` only
- [ ] Keep `customer_impact` only
- [ ] Remove both (not tracked)

---

## AMP MEETING INTEGRATION (5 columns)
**Purpose:** AMP Events and Meeting scheduling integration

| Column | Type | Required | Description | Keep? | Notes |
|--------|------|----------|-------------|-------|-------|
| `amp_event_id` | string | NO | Associated AMP Event ID | ❓ REVIEW | Links project to AMP system |
| `amp_activity_title` | string | NO | AMP Activity title linked to project | ❓ REVIEW | Activity name from AMP |
| `meeting_type` | string | NO | Type: SIF, AIM, Store Meeting, None | ❓ REVIEW | Which meeting types? |
| `sif_date` | date | NO | Store Impact Forum (SIF) meeting date | ❓ REVIEW | SIF scheduled date |
| `aim_date` | date | NO | Area/Activity Impact Meeting (AIM) date | ❓ REVIEW | AIM scheduled date |

**Your input here:**
- Do projects connect to AMP Events?
- Do projects have associated store/area meetings (SIF/AIM)?
- [ ] Keep AMP integration fields
- [ ] Remove AMP integration (handle separately)
- [ ] Simplify to: `meeting_type`, `meeting_date` only

---

## DESCRIPTION (2 columns)
**Purpose:** Project descriptions and summaries

| Column | Type | Required | Max Length | Keep? | Notes |
|--------|------|----------|-----------|-------|-------|
| `summary` | string | NO | 2,000 chars | ✓ KEEP | Brief project summary |
| `overview` | string | NO | 10,000 chars | ✓ KEEP | Detailed project overview/description |

**Your input here:**
- [ ] Keep both (short + long description)
- [ ] Keep only `summary`
- [ ] Keep only `overview`
- [ ] Rename to: _________

---

## SUMMARY TABLE - COLUMN DECISIONS

**Total in current schema:** 40 columns  
**Your target (estimate):** ______ columns

| Category | Total | Keep? | Remove? | Rename? | Notes |
|----------|-------|-------|---------|---------|-------|
| Identifiers | 3 | | | | |
| Status | 4 | | | | |
| Location | 10 | | | | |
| Time | 6 | | | | |
| Ownership | 3 | | | | |
| Categorization | 6 | | | | |
| Impact | 2 | | | | |
| AMP Meeting | 5 | | | | |
| Description | 2 | | | | |
| **TOTAL** | **40** | **?** | **?** | **?** | |

---

## ADDITIONS / CUSTOM COLUMNS

Are there columns we need that aren't in the 40 above?

**Example:** If you currently use `latest_update` in AH_Projects, should we add that?

```
New columns needed:
1. _________________ (type: ___, required: yes/no)
2. _________________ (type: ___, required: yes/no)
3. _________________ (type: ___, required: yes/no)
```

---

## FINAL SIGN-OFF

Once you complete the above review:

- [ ] I have reviewed all 40 columns
- [ ] I have marked Keep/Remove/Rename for each
- [ ] I have confirmed which columns are required vs. optional
- [ ] I have identified any new columns to add
- [ ] I am ready to recreate AH_Projects with the finalized schema

**Ready to proceed?** Once approved, we will:
1. Create updated `projects-schema.json` with confirmed columns
2. Generate BigQuery DDL to recreate `AH_Projects` table
3. Migrate any existing data (if applicable)
4. Update all code to use new schema

---

## VERSION HISTORY

| Date | Action | Status |
|------|--------|--------|
| Apr 17, 2026 | Created schema review checklist | ⏳ Awaiting user input |
| | Finalize schema | ⏳ Pending |
| | Recreate AH_Projects table | ⏳ Pending |

