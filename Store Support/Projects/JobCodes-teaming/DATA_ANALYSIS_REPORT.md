# Job Codes Dashboard - Data Analysis Report
## April 8, 2026

---

## EXECUTIVE SUMMARY

**Problem:** Excel job codes (Workday format: `US-01-0202-002104`) don't match Polaris codes (SMART format: `1-202-2104`)

**Opportunity:** Can map ~38% of codes using existing data, with more available via openpyxl

---

## YOUR SPECIFIC QUESTION

### Looking for: `US-01-0202-002104`

| Field | Value |
|-------|-------|
| **Found in** | Excel Master Table ✓ |
| **Excel SMART Code** | US-01-0202-002104 |
| **Job Title** | **Adult Beverage DM** |
| **Workday Job Code** | 30614.1 |
| **Category** | Hourly |
| **Job Family** | TL2 |
| **PG Level** | 7 |
| **Team** | TL2 |  
| **Workgroup** | Specialty Supervisor |

### Matching in Polaris:

| Field | Value |
|-------|-------|
| **Found in** | Polaris CSV ✓ |
| **Polaris SMART Code** | **1-202-2104** |
| **Job Title** | Adult Beverage DM 1-202-2104 |
| **From Column** | job_nm (job name) |
| **Match Quality** | EXCELLENT - titles match perfectly! |

**Insight:** The job TITLE is the same ("Adult Beverage DM") but the codes are different formats!

---

## DATASET COMPARISON

### Code Formats Observed

| Aspect | Polaris | Excel |
|--------|---------|-------|
| **Total Records** | 271 | 864 |
| **Code Format** | SMART (internal) | Workday (external) |
| **Example** | `1-202-2104` | `US-01-0202-002104` |
| **Structure** | `division-dept-code` | `country-division-dept-code` |

### Code Samples

**POLARIS (271 active job codes):**
```
1-630-7410      MFC ON TA
1-910-600       Office Assoc  
1-0-40386       MFC Store Lead
1-9-201         Sport Goods SA
30-49-859       Optician Dual Cert
1-635-7240      Stocking ON TL
```

**EXCEL (864 job code records):**
```
US-71-0076-000624   Academy Coordinator
US-01-0202-002104   Adult Beverage DM         ← Your example
US-01-0615-007410   Team Associate
US-01-0996-000754   AP Investigator
US-01-0996-007400   AP Operations TA
US-01-0695-007500   AP Team Lead
```

---

## MAPPING STRATEGY ANALYSIS

### Strategy #1: Map using Excel "Workday Job Code" Column  
**Success Rate: 90 / 271 codes (33.2%)**

The Excel file has a "Workday Job Code" column that sometimes matches Polaris codes directly!

**Why this works:**
- Excel records sometimes have the Polaris SMART code in a different column
- 90 Polaris codes can be directly matched this way

**Examples:**
```
Excel Workday Code: 1-930-745    → Polaris: 1-930-745 (MRA Merch Recon Assoc)
Excel Workday Code: 1-980-530    → Polaris: 1-980-530 (Cart Assoc)
Excel Workday Code: 24-93-101    → Polaris: 24-93-101 (Meat Dept Mgr)
```

### Strategy #2: Map by Job Title Match
**Success Rate: 19 / 271 codes (7.0%)**

Exact matching of job titles after cleaning the Polaris code suffix

**Why this works:**
- Excel title and Polaris title often match exactly
- Example: Both have "Adult Beverage DM" (though formatted differently)

**Examples:**
```
Excel: US-01-0930-000745 "MRA Merch Recon Assoc"    
Polaris: 1-930-745 "MRA Merch Recon Assoc 1-930-745"  ✓ MATCH

Excel: US-06-0010-000201 "Auto Care Ctr SA"
Polaris: 6-10-201 "Auto Care Ctr SA 6-10-201"  ✓ MATCH
```

### Combined Mapping Achievement  
**Total Mappable: 104 / 271 codes (38.4%)**

```
Workday Code matches ············· 90 codes
Title matches ···················· 19 codes
Overlap  ························· (5 codes counted twice)
= TOTAL ·························· 104 codes

UNMAPPABLE: 167 codes not found in Excel
```

---

## EXCEL FILES AVAILABLE

Your JobCodes project contains 2 Master Excel files:

1. **Job_Code_Master_Table.xlsx** (currently in use)
   - Contains 864 records
   - Has Workday codes that partially match Polaris
   - We've successfully parsed this with XML+ZIP fallback

2. **Job_Code_Master_Complete.xlsx** (not yet examined)
   - Unknown - may have additional mapping data or sheets
   - Needs openpyxl to read

---

## NEXT STEPS

### Option A: Use Existing Mapping (38% enrichment) 
**What I Can Do Today:** 
- Build a job code mapping CSV using the two strategies above
- 104 codes would get enrichment (Category, PG Level, etc.)
- Takes ~5 minutes
- Works without openpyxl

**Result:** 38% of dashboard populated with enrichment data

---

### Option B: Install openpyxl for Complete Analysis
**What Requires Your Action:**
1. Go off VPN
2. I install openpyxl via pip
3. I examine `Job_Code_Master_Complete.xlsx`
4. Check if there's better mapping data in there
5. Potentially map more codes

**Time Required:** ~10-15 minutes
**Potential Gain:** Unknown (may get 50-80% coverage)

---

## RECOMMENDATION

**I suggest BOTH approaches:**

1. **Immediately (5 min):** Build mapping from existing XML-parsed Excel
   - Use Workday Code + Title matching
   - Creates 104 enriched records right away
   
2. **When you're off VPN (10-15 min):** Install openpyxl
   - Examine Job_Code_Master_Complete.xlsx
   - Find if it has the missing code mappings
   - Improve coverage from 38% to potentially 60-80%

---

## SUMMARY TABLE

| Dataset | Records | Polaris SMART Format | Workday Format | Mapped |
|---------|---------|---------------------|-----------------|--------|
| Polaris Job Codes | 271 | ✓ (1-202-2104) | ✗ | - |
| Excel Master | 864 | ✗ (US-01-0202-002104) | ✓ | 90 direct |
| Mapping via Title | - | - | - | 19 additional |
| **Total Enrichable** | **104** | - | - | **38.4%** |

