# 🗺️ Datasource Navigation Map

## Welcome! 👋 Start Here

This is your visual guide to the Activity Hub Datasource Documentation.

---

## 🎯 Your Journey Map

```
                    You are HERE
                        ↓
                    [Navigation Map]
                        ↓
                    Choose your path ↓

    ┌─────────────────────┬──────────────────┬──────────────────┐
    ↓                     ↓                  ↓                  ↓
┌─────────┐        ┌──────────┐      ┌────────────┐    ┌──────────┐
│ New to  │        │ Want to  │      │ Debugging  │    │Managing  │
│ Activity│        │ Query or │      │ Issues or  │    │ Syncs or │
│  Hub?   │        │Integrate?│      │Monitor?    │    │Security? │
└────┬────┘        └────┬──────┘      └──────┬─────┘    └────┬─────┘
     │                   │                    │              │
     ↓                   ↓                    ↓              ↓
  README.md         Specific Folder      SYNC-GUIDE.md    Admin Docs
  QUICKSTART.md     BigQuery/, APIs/,
                    File-Based/,
                    Databases/
```

---

## 📋 Document Roadmap

### Main Documents (Start Here)

```
┌─────────────────────────────────────────────────────────────────┐
│                     📚 MAIN DOCUMENTS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  README.md ⭐ START HERE                                   │
│      └─ Overview of all datasources                            │
│      └─ Quick reference table                                  │
│      └─ Data flow diagrams                                     │
│      └─ Related documents                                      │
│      └─ 📖 15 min read                                         │
│                                                                 │
│  2️⃣  QUICKSTART.md (Quick Reference)                           │
│      └─ "I need help with..." sections                         │
│      └─ Common tasks with steps                                │
│      └─ FAQ answers                                            │
│      └─ 📖 10 min read                                         │
│                                                                 │
│  3️⃣  DATASOURCE-MATRIX.md (Dependencies)                       │
│      └─ Which folders use which data?                          │
│      └─ Data flow diagrams                                     │
│      └─ Critical dependencies                                  │
│      └─ 📖 20 min read                                         │
│                                                                 │
│  4️⃣  SYNC-GUIDE.md (Operations)                                │
│      └─ When data gets updated                                 │
│      └─ Monitoring procedures                                  │
│      └─ Error recovery                                         │
│      └─ 📖 25 min read                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Datasource Documentation (Drill Down)

```
┌─────────────────────────────────────────────────────────────────┐
│               📊 DATASOURCE GUIDES (Pick One)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📦 BigQuery/ ..................... Cloud Data Warehouse       │
│     README.md                                                  │
│     ├─ Polaris Scheduling Data                               │
│     ├─ Asset Protection Projects                             │
│     ├─ Store Refresh Data                                    │
│     ├─ Pricing Operations                                    │
│     ├─ Query Examples & Optimization                         │
│     └─ Connection Guide                                      │
│                                                                 │
│  🔌 APIs/ ......................... External Integrations     │
│     README.md                                                  │
│     ├─ Workday HR System                                     │
│     ├─ Microsoft Active Directory                            │
│     ├─ Microsoft Graph (Teams, Outlook)                      │
│     ├─ Sparky AI Assistant                                   │
│     ├─ Authentication Methods                                │
│     └─ Code Examples                                         │
│                                                                 │
│  📄 File-Based/ ................... Uploads & Imports        │
│     README.md                                                  │
│     ├─ CSV File Format                                       │
│     ├─ Excel Workbook Structure                              │
│     ├─ JSON Configuration                                    │
│     ├─ Validation Rules                                      │
│     └─ Upload Process                                        │
│                                                                 │
│  🗄️  Databases/ ................... PostgreSQL & Redis       │
│     README.md                                                  │
│     ├─ PostgreSQL Setup                                      │
│     ├─ Database Schema                                       │
│     ├─ Redis Caching                                         │
│     ├─ Connection Strings                                    │
│     └─ Performance Tuning                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧭 Quick Navigation by Role

### 👨‍💻 **Backend Developer**

**Want to**: Query data, build APIs, integrate systems

**Your path**:
1. Read [README.md](./README.md) (5 min)
2. Go to [BigQuery/README.md](./BigQuery/README.md) or [APIs/README.md](./APIs/README.md)
3. Copy code examples and adapt
4. Check [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) for dependencies

**Key files**:
- [BigQuery/README.md](./BigQuery/README.md) - SQL queries & Python examples
- [APIs/README.md](./APIs/README.md) - OAuth, REST, code samples
- [Databases/README.md](./Databases/README.md) - Connection pooling, optimization

---

### 📊 **Data Analyst**

**Want to**: Find data sources, write queries, understand data lineage

**Your path**:
1. Read [README.md](./README.md) (5 min)
2. Check [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) (10 min)
3. Open [BigQuery/README.md](./BigQuery/README.md) for query help
4. Use SQL templates provided

**Key files**:
- [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) - Data flow
- [BigQuery/README.md](./BigQuery/README.md) - Current tables
- [SYNC-GUIDE.md](./SYNC-GUIDE.md) - When data updates

---

### 🚀 **DevOps/SRE**

**Want to**: Monitor syncs, troubleshoot issues, maintain infrastructure

**Your path**:
1. Read [SYNC-GUIDE.md](./SYNC-GUIDE.md) (20 min)
2. Set up monitoring from health check section
3. Review [Databases/README.md](./Databases/README.md) for DB maintenance
4. Check error recovery procedures

**Key files**:
- [SYNC-GUIDE.md](./SYNC-GUIDE.md) - Operations runbook
- [Databases/README.md](./Databases/README.md) - Database admin
- [README.md](./README.md) - Overview of all services

---

### 👨‍💼 **Project Manager**

**Want to**: Understand data dependencies, track sync schedules

**Your path**:
1. Read [README.md](./README.md) (5 min)
2. Check [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) (10 min)
3. Review [SYNC-GUIDE.md](./SYNC-GUIDE.md) sync schedule (5 min)
4. Understand critical dependencies section

**Key files**:
- [README.md](./README.md) - System overview
- [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) - Dependencies
- [SYNC-GUIDE.md](./SYNC-GUIDE.md) - Timeline

---

### 🆕 **New Team Member**

**Want to**: Learn Activity Hub datasources quickly

**Your path**:
1. Start with [QUICKSTART.md](./QUICKSTART.md) (10 min)
2. Read [README.md](./README.md) (15 min)
3. Skim [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) (5 min)
4. Pick your role above and dive deeper

**Key files**:
- [QUICKSTART.md](./QUICKSTART.md) - Your best starting point
- [README.md](./README.md) - Complete overview
- Role-specific guides above

---

### 🔒 **Security/Compliance**

**Want to**: Understand data classification, access control

**Your path**:
1. Read [README.md](./README.md) security section (5 min)
2. Check [Databases/README.md](./Databases/README.md) security part (10 min)
3. Review [APIs/README.md](./APIs/README.md) auth section (10 min)
4. See related DATA-CLASSIFICATION-ASSESSMENT.md in project root

**Key files**:
- [README.md](./README.md) - Security overview
- [Databases/README.md](./Databases/README.md) - Encryption, access
- [APIs/README.md](./APIs/README.md) - Authentication

---

## 🔍 Finding Information

### I want to know... WHERE TO LOOK

| Question | File | Section |
|---|---|---|
| What data sources exist? | README.md | Quick Reference |
| Which folder uses which data? | DATASOURCE-MATRIX.md | Complete Mapping |
| How do I query Polaris? | BigQuery/README.md | Polaris section |
| When is data updated? | SYNC-GUIDE.md | Sync Schedule |
| How do I connect to APIs? | APIs/README.md | Authentication |
| How do I import CSV? | File-Based/README.md | CSV Import Process |
| What database feels slow? | Databases/README.md | Query Optimization |
| What went wrong? | SYNC-GUIDE.md | Error Handling |
| Is my data source down? | SYNC-GUIDE.md | Health Check |
| How do I get started? | QUICKSTART.md | "I need help..." |

---

## 📁 Folder Structure Visualization

```
Datasource/  (You are here)
│
├─ 📚 MASTER GUIDES
│  ├─ README.md ..................... 👈 START HERE
│  ├─ QUICKSTART.md
│  ├─ DATASOURCE-MATRIX.md
│  ├─ SYNC-GUIDE.md
│  └─ CREATION-SUMMARY.md
│
├─ 📦 DATASOURCE DOCUMENTATION
│  ├─ BigQuery/ (Cloud data warehouse)
│  │  └─ README.md (3 BigQuery projects + queries)
│  │
│  ├─ APIs/ (External integrations)
│  │  └─ README.md (4 APIs + auth + examples)
│  │
│  ├─ File-Based/ (Uploads)
│  │  └─ README.md (CSV, Excel, JSON)
│  │
│  └─ Databases/ (PostgreSQL + Redis)
│     └─ README.md (2 database systems)
│
├─ 🔧 TEMPLATES (Coming soon)
│  ├─ BigQuery/templates/
│  ├─ APIs/templates/
│  ├─ File-Based/templates/
│  └─ Databases/templates/
│
└─ 📖 DETAILED GUIDES (Coming soon)
   ├─ BigQuery/Polaris.md
   ├─ BigQuery/Asset-Protection.md
   ├─ APIs/Workday.md
   ├─ APIs/Active-Directory.md
   └─ ...more
```

---

## ⏱️ Reading Time Guide

| Document | Time | Audience |
|---|---|---|
| QUICKSTART.md | 10 min | Everyone |
| README.md | 15 min | Everyone |
| DATASOURCE-MATRIX.md | 20 min | DevOps, PMs, Developers |
| SYNC-GUIDE.md | 25 min | DevOps, Backend |
| BigQuery/README.md | 30 min | Data analysts, Developers |
| APIs/README.md | 30 min | Backend developers |
| File-Based/README.md | 20 min | Project managers |
| Databases/README.md | 30 min | DevOps, Backend |

**Total orientation time**: ~2-3 hours depending on role

---

## 🎓 Learning Paths

### Path 1: Understanding Activity Hub (Beginner - 1 hour)
```
1. QUICKSTART.md ..................... 10 min
2. README.md ......................... 15 min
3. DATASOURCE-MATRIX.md (skim) ....... 10 min
4. Pick your role guide above ........ 15-20 min
```

### Path 2: Setting Up Integration (Developer - 2 hours)
```
1. README.md ......................... 15 min
2. Relevant datasource READ.md:
   - BigQuery/README.md (30 min) OR
   - APIs/README.md (30 min) OR
   - File-Based/README.md (20 min)
3. Code examples + templates ......... 30 min
4. Test connection .................. 15 min
```

### Path 3: Operational Knowledge (DevOps - 3 hours)
```
1. README.md ......................... 15 min
2. DATASOURCE-MATRIX.md .............. 20 min
3. SYNC-GUIDE.md ..................... 25 min
4. Databases/README.md ............... 30 min
5. Set up monitoring ................. 30 min
6. Review error procedures ........... 20 min
```

### Path 4: Complete Mastery (All - 5-8 hours)
```
1. All main documents ................ 2 hours
2. All datasource folders ............ 2-3 hours
3. Code examples + templates ......... 1-2 hours
4. Hands-on testing .................. 1-2 hours
```

---

## 🔗 Cross-Document Links

Documents reference each other for easy navigation:

```
README.md
├─ Links to: BigQuery/, APIs/, File-Based/, Databases/
├─ References: SYNC-GUIDE.md
└─ Related: DATASOURCE-MATRIX.md

DATASOURCE-MATRIX.md
├─ References: README.md, SYNC-GUIDE.md
├─ Links to: Each datasource README

SYNC-GUIDE.md
├─ References: README.md, DATASOURCE-MATRIX.md
└─ Links to: Error handling procedures

BigQuery/README.md, APIs/README.md, etc.
├─ Link back to: README.md
└─ Reference: DATASOURCE-MATRIX.md, SYNC-GUIDE.md
```

---

## ✅ Checklist: What You'll Learn

After reading the appropriate docs for your role, you'll be able to:

### Backend Engineer
- [ ] Query BigQuery data with confidence
- [ ] Write efficient SQL queries
- [ ] Authenticate to APIs properly
- [ ] Handle errors gracefully
- [ ] Optimize database access

### Data Analyst
- [ ] Find any dataset in Activity Hub
- [ ] Write SQL queries to get data
- [ ] Understand data freshness
- [ ] Know which fields to use
- [ ] Troubleshoot missing data

### DevOps/SRE
- [ ] Monitor all datasource syncs
- [ ] Detect sync failures early
- [ ] Understand recovery procedures
- [ ] Optimize database performance
- [ ] Maintain backup systems

### Project Manager
- [ ] Understand data dependencies
- [ ] Know sync schedules
- [ ] Understand critical issues impact
- [ ] Plan around maintenance windows
- [ ] Coordinate with teams

### New Team Member
- [ ] Know what Activity Hub is
- [ ] Understand available data
- [ ] Know who to ask for help
- [ ] Understand your role's scope
- [ ] Know where to find answers

---

## 🚀 Now You're Ready!

**Pick your starting point**:

1. **Just browsing?** → Read [README.md](./README.md) (15 min)
2. **New team member?** → Read [QUICKSTART.md](./QUICKSTART.md) (10 min)
3. **Need specific help?** → Use [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) (5 min)
4. **Setting up new integration?** → Go to relevant folder (BigQuery/, APIs/, etc.)
5. **Debugging issue?** → Check [SYNC-GUIDE.md](./SYNC-GUIDE.md) (20 min)

---

## 📞 Questions?

**Can't find what you need?**
1. Check [QUICKSTART.md](./QUICKSTART.md) FAQ section
2. Search relevant README for keywords
3. Message your team for help

**Found an error or gap?**
1. Update docs yourself if you can
2. Create an issue for your team
3. Contact documentation owner

---

**Welcome to Activity Hub! 🎉**

Start with [README.md](./README.md) →

