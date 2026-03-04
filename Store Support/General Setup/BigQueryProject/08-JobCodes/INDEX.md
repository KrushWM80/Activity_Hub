# 📚 Job Codes Documentation Index

## Quick Navigation

**Looking for something specific?** Use this index to find the right documentation.

---

## 🎯 By Audience

### 👤 **Enterprise Users / Managers**
**Start Here**: [KNOWLEDGE_HUB.md - Job Codes Section](../../../KNOWLEDGE_HUB.md#-job-codes-multi-source-discovery--bridging)

**What You'll Learn**:
- What are job codes and why they matter
- Real-world example (AMP Roles project)
- Success metrics (191/195 = 98% coverage)
- Key learnings from the project

**Time**: 10-15 minutes

---

### 👨‍💻 **Developers / Data Analysts (Quick Start)**
**Start Here**: [QUICKSTART.md](./QUICKSTART.md)

**What You'll Learn**:
- 5-minute job code lookup script (copy-paste ready)
- Finding job codes at a store
- Common queries by department
- Quick troubleshooting

**Time**: 5-10 minutes

**Next**: Once you understand basics, read [README.md](#complete-technical-guide)

---

### 🔬 **Data Scientists / Technical Deep Dive**
**Start Here**: [README.md](./README.md)

**What You'll Learn**:
- Complete job code system architecture
- All 4 data sources in detail
- Multi-source bridging workflow
- Python implementation (JobCodeLookup service)
- SQL query patterns and best practices
- Troubleshooting guide

**Time**: 30-60 minutes for full reading

**Code Files**: Copy patterns from sections:
- [Complete Python Example](./README.md#-complete-python-example-job-code-lookup-service)
- [Common Patterns](./README.md#-common-job-code-lookup-patterns)
- [SQL Templates](./README.md#-sql-query-examples)

---

### 📊 **BigQuery Team**
**Start Here**: [BigQueryProject/README.md - Section 08-JobCodes](../README.md#-jobcodes)

**Then Read**: 
- [README.md](./README.md) - Focus on data sources section
- [Datasource BigQuery/README.md - Job Codes Section](../../Datasource/BigQuery/README.md#-job-code-lookup--mapping)

**What You'll Get**:
- All BigQuery tables with job codes
- Table locations, update frequency, permissions
- Best practices for querying
- Integration patterns

---

### 🏢 **JobCodes-teaming Project Team**
**Start Here**: [JobCodes-teaming Project README](../../Projects/JobCodes-teaming/Job%20Codes/README.md)

**What You'll Find**:
- Project context and objectives
- Current data status (191/195 populated)
- How to use the generated files
- Next steps for improvement
- Usage scenarios with code

---

## 📖 By Document

### This Folder (08-JobCodes)

#### **README.md** - Complete Technical Guide
- **Sections**: 15+
- **Length**: 3,500+ lines
- **Code Examples**: 20+
- **Best For**: Technical deep dive, implementation reference
- **Read Time**: 45-60 minutes

**Key Sections**:
1. Three-tier Job Code system
2. Data source #1: job_codes_master.json
3. Data source #2: BigQuery Polaris tables
4. Data source #3: BigQuery CoreHR tables
5. Data source #4: Local BigQuery
6. Bridging multiple datasources workflow
7. Complete Python JobCodeLookup service
8. Common patterns and SQL templates
9. Troubleshooting guide
10. Weekly maintenance checklist

---

#### **QUICKSTART.md** - 5-Minute Lookup Guide
- **Sections**: 8+
- **Length**: 1,000+ lines
- **Code Examples**: 8+
- **Best For**: Immediate practical use
- **Read Time**: 5-10 minutes

**Key Sections**:
1. What are job codes (format table)
2. 5-minute lookup script
3. Finding job codes by role
4. Job codes at a store
5. Validate a mapping
6. Common job codes by department
7. Troubleshooting quick fixes
8. Key formulas for spreadsheets

---

#### **DOCUMENTATION_UPDATE_SUMMARY.md** - This Update
- **Purpose**: Document what was created and updated
- **Coverage**: All changes, cross-references, impact
- **Best For**: Understanding the documentation initiative
- **Read Time**: 15-20 minutes

---

### Related Documentation

#### **KNOWLEDGE_HUB.md** - Enterprise Knowledge Repository
📍 Location: `Activity_Hub/KNOWLEDGE_HUB.md`

**Job Codes Section**:
- Overview of 3 formats
- 4 data sources summary
- Complete workflow diagram
- Common query patterns
- Real-world case study
- Key learnings
- Maintenance checklist

**Why Read**: Enterprise-level overview, cross-project context

---

#### **BigQueryProject/README.md** - Central BQ Hub
📍 Location: `General Setup/BigQueryProject/README.md`

**Mentions Job Codes**:
- Section 08-JobCodes introduction
- Links to quick start and guide
- Success story (AMP Roles)

**Why Read**: See where Job Codes fit in overall BQ strategy

---

#### **Datasource/BigQuery/README.md** - Data Source Reference
📍 Location: `General Setup/Datasource/BigQuery/README.md`

**Job Codes Section**:
- Data source overview
- Table references (Polaris, CoreHR)
- SQL query examples
- Workflow diagram
- Success metrics

**Why Read**: If researching data sources for job codes

---

#### **JobCodes Project README** - Project-Specific Reference
📍 Location: `Projects/JobCodes-teaming/Job Codes/README.md`

**Contents**:
- Project objectives and overview
- Current data status
- How to use generated files
- ETL pipeline
- 4 usage scenarios
- Data source details
- Next steps

**Why Read**: If working on JobCodes-teaming project

---

## 🔍 By Task

### I need to find a User ID for a job code RIGHT NOW
1. Go to: [QUICKSTART.md - Page 1](./QUICKSTART.md#5-minute-lookup-find-user-ids-for-a-job-code)
2. Copy the Python script
3. Change job code variable
4. Run it

**Time**: 2 minutes

---

### I need to understand the complete system
1. Start: [QUICKSTART.md](./QUICKSTART.md) (5 min)
2. Then: [KNOWLEDGE_HUB.md Job Codes Section](../../../KNOWLEDGE_HUB.md#-job-codes-multi-source-discovery--bridging) (10 min)
3. Finally: [README.md](./README.md) (45 min for full reading)

**Time**: 1 hour total

---

### I'm building integration that uses job codes
1. Read: [README.md Data Sources section](./README.md#-data-source-1-job_codes_masterjson)
2. Copy: [Python JobCodeLookup service](./README.md#-complete-python-example-job-code-lookup-service)
3. Adapt: For your specific needs
4. Reference: [Common patterns](./README.md#-common-job-code-lookup-patterns)

**Time**: 30 minutes

---

### I need to validate a mapping
1. Read: [QUICKSTART.md - Validate section](./QUICKSTART.md#validate-a-mapping-smart--workday--user-id)
2. Or: [README.md - Bridging section](./README.md#-bridging-multiple-datasources-complete-workflow)

**Time**: 10 minutes

---

### I found missing/invalid job codes
1. Reference: [README.md Troubleshooting](./README.md#-troubleshooting)
2. Check: [Job Code Project README - Next Steps](../../Projects/JobCodes-teaming/Job%20Codes/README.md#next-steps--improvements)

**Time**: 15 minutes

---

### I need SQL query templates
1. See: [QUICKSTART.md - Common patterns](./QUICKSTART.md#common-job-codes-by-department)
2. Or: [README.md - SQL Examples](./README.md#-sql-query-examples)

**Time**: 5 minutes

---

## 📊 By Document Type

### **Technical Guides** (Deep Learning)
- [README.md](./README.md) - Comprehensive reference
- [Datasource BQ README](../../Datasource/BigQuery/README.md) - Data source details

### **Quick Start** (Immediate Use)
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute lookup
- [KNOWLEDGE_HUB.md](../../../KNOWLEDGE_HUB.md#-job-codes-multi-source-discovery--bridging) - Overview

### **Project Docs** (Specific Use)
- [JobCodes Project README](../../Projects/JobCodes-teaming/Job%20Codes/README.md) - Project context
- [BigQueryProject README](../README.md) - BQ integration context

### **Data References** (Lookup)
- job_codes_master.json - Master database
- Job_Code_Master_Complete.xlsx - Complete lookup table
- Missing_User_IDs_Assignment_Summary.txt - Gap analysis

---

## 🗂️ File Structure

```
Activity_Hub/
├── KNOWLEDGE_HUB.md (updated)
│   └─ 💼 Job Codes Section
│
├── Store Support/
│   ├── General Setup/
│   │   ├── BigQueryProject/ (updated)
│   │   │   ├── README.md (updated)
│   │   │   │   └─ Section 08-JobCodes
│   │   │   └── 08-JobCodes/ (NEW FOLDER)
│   │   │       ├── README.md ⭐ MAIN GUIDE
│   │   │       ├── QUICKSTART.md ⭐ QUICK START
│   │   │       └── DOCUMENTATION_UPDATE_SUMMARY.md
│   │   │
│   │   └── Datasource/ (updated)
│   │       └── BigQuery/README.md (updated)
│   │           └─ Job Codes Section
│   │
│   └── Projects/
│       └── JobCodes-teaming/Job Codes/
│           ├── README.md (updated) ⭐ PROJECT REFERENCE
│           ├── job_codes_master.json
│           ├── AMP_Roles_CORRECTED.xlsx (deliverable)
│           ├── Job_Code_Master_Complete.xlsx
│           └── Other supporting files...

```

---

## 🚀 Getting Started Paths

### **Path 1: I Need Answers RIGHT NOW** (5 minutes)
```
QUICKSTART.md
    ↓
Run 5-minute lookup script
    ↓
You have: User ID for job code
```

### **Path 2: I Want to Understand** (1 hour)
```
KNOWLEDGE_HUB.md (Job Codes section)
    ↓
README.md (sections 1-4: Data Sources)
    ↓
README.md (section 6: Bridging Workflow)
    ↓
You know: Complete system architecture
```

### **Path 3: I'm Building Integration** (1.5 hours)
```
QUICKSTART.md
    ↓
README.md (Data Sources 1-4)
    ↓
README.md (Python JobCodeLookup service)
    ↓
README.md (Common patterns)
    ↓
Copy code, adapt, test
```

### **Path 4: I'm in JobCodes Project** (2 hours)
```
JobCodes Project README
    ↓
README.md (complete read)
    ↓
QUICKSTART.md (practical reference)
    ↓
Run queries/scripts
```

---

## 📋 Checklist: Did You Know?

- [ ] Job codes exist in 3 different formats (SMART/Workday/User ID)
- [ ] job_codes_master.json has 44,934 lines of mappings
- [ ] Polaris table shows current employee assignments
- [ ] User ID from Polaris = User ID in CoreHR
- [ ] Role-based representatives can fill ~98% of gaps
- [ ] AMP Roles project succeeded at 191/195 coverage
- [ ] Python JobCodeLookup service is copy-paste ready
- [ ] SQL templates available for all common patterns
- [ ] Complete troubleshooting guide exists
- [ ] Weekly maintenance checklist provided

---

## 💡 Key Facts

**Job Code Formats**:
- SMART: `1-993-1026` (human-readable)
- Workday: `US-01-0202-002104` (structured)
- User ID: `e0c0l5x.s03935` (system reference)

**Main Data Sources**:
1. job_codes_master.json (local, 44,934 mappings)
2. Polaris (BigQuery, current schedules)
3. CoreHR (BigQuery, master profiles)
4. Local BQ (wmt-assetprotection-prod)

**Success Story**:
- AMP Roles: 191/195 rows populated (98%)
- 130 existing + 61 role-based assignments

**Representatives**:
- Hourly: `drm009t.s05301`
- Salary: `e0c0l5x.s03935`

---

## 📞 Still Have Questions?

### Where to look first:
1. **General question**: Check [KNOWLEDGE_HUB.md](../../../KNOWLEDGE_HUB.md#-job-codes-multi-source-discovery--bridging)
2. **Practical help**: Check [QUICKSTART.md](./QUICKSTART.md)
3. **Technical details**: Check [README.md](./README.md)
4. **Project context**: Check [JobCodes Project README](../../Projects/JobCodes-teaming/Job%20Codes/README.md)
5. **Data sources**: Check [Datasource BQ README](../../Datasource/BigQuery/README.md)

### Not finding answer?
1. Check [README.md Troubleshooting](./README.md#-troubleshooting)
2. Review [QUICKSTART.md Troubleshooting](./QUICKSTART.md#troubleshooting)
3. Look at [Project README Next Steps](../../Projects/JobCodes-teaming/Job%20Codes/README.md#next-steps--improvements)

---

## 🎓 Learning Resources Summary

| Resource | Type | Time | Audience |
|----------|------|------|----------|
| QUICKSTART.md | Quick ref | 5 min | Anyone |
| KNOWLEDGE_HUB | Overview | 10 min | Managers |
| README.md | Technical | 45 min | Developers |
| Project README | Context | 20 min | Project team |
| Job_codes_master.json | Data | - | Reference |
| SQL Templates | Code | 5 min | Analysts |
| Python Examples | Code | 10 min | Developers |

---

**Last Updated**: March 4, 2026  
**Version**: 1.0  
**Status**: ✅ Complete
