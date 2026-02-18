# Path to Production - Application Process

**Project:** Activity Hub  
**Status:** 🔄 IN PROGRESS  
**Current Step:** Step 3 - APM Setup (Waiting for Product ID system propagation)

---

## 📋 Application Process Overview

The Path to Production process for deploying applications to Walmart's production environment follows these sequential steps:

```
Step 0: Clipper Setup
    ↓
Step 1: DQC Assignment
    ↓
Step 2: Team Rosters
    ↓
Step 3: APM Setup
    ↓
Step 4: SSP Process
    ↓
Step 5: Azure Setup
    ↓
🚀 Production Ready
```

---

## 📊 Current Progress - Activity Hub

### ✅ Completed Steps

#### [Step 0: Clipper Setup](./00-Clipper_Setup/README.md)
- **Status:** ✅ COMPLETE
- **Completed:** January 2026
- **Output:** Product ID 6426
- **Details:**
  - ✅ Clipper account confirmed (after cost center white-list resolution)
  - ✅ Product ID created: 6426
  - ✅ Product URL: https://clipper.walmart.com/products/entity/product/6426
  - 🔄 System propagation: In progress (3-5 business days, expected Jan 15-17)

**Key Learning:** Cost Center must be white-listed before Clipper account confirmation. This was a critical blocker resolved in January 2026.

---

### 🔄 In Progress Steps

#### [Step 1: DQC Assignment](./01-DQC_Assignment/README.md)
- **Status:** ✅ ASSIGNED (No action needed)
- **DQC:** Kevin Tadda
- **Business Group:** Walmart US (Store Support)
- **Timeline:** 1-3 days
- **Next Action:** Contact Kevin Tadda to coordinate on Team Rosters request

**Notes:** Kevin Tadda is already assigned as DQC for Walmart US pillar. No action required for this step.

---

#### [Step 3: APM Setup](./03-APM_Setup/README.md) ⏭️ **CURRENT STEP**
- **Status:** 🔄 IN PROGRESS
- **Timeline:** 2-4 weeks
- **Blockers:**
  - 🔄 Product ID system propagation (Jan 15-17, 2026)
  - 🔄 Tech Group finalization (REQ65217701) - 1-2 weeks
- **Completion Requirements:**
  - ✅ APM registration form (partially started)
  - ⏳ Product ID linkage (blocked on system propagation)
  - ⏳ Data Classification Assessment (DCA)
  - ⏳ Compliance assessments (RISK, EPRA)
  - ⏳ APM Certified status

**Progress:** APM form is 50% complete. Awaiting Product ID system update to continue.

---

### ⏳ Upcoming Steps

#### [Step 2: Team Rosters](./02-Team_Rosters/README.md)
- **Status:** ⏳ BLOCKED (Awaiting Step 1 completion)
- **Timeline:** 3-5 days
- **Prerequisites:** DQC assignment (Step 1) complete
- **Owner:** DQC (Kevin Tadda)

#### [Step 4: SSP Process](./04-SSP_Process/README.md)
- **Status:** ⏳ BLOCKED (Awaiting Step 3 completion)
- **Timeline:** 2-3 weeks
- **Prerequisites:** APM Certified status
- **Output:** SSP Approved status

#### [Step 5: Azure Setup](./05-Azure_Setup/README.md)
- **Status:** ⏳ BLOCKED (Awaiting Step 4 completion)
- **Timeline:** 3-4 weeks
- **Prerequisites:** SSP Approved status
- **Output:** Production infrastructure ready

---

## 📅 Critical Path Timeline

```
Week 1 (Jan 12-18, 2026)
├─ ✅ Clipper Setup Complete
├─ ✅ Product ID 6426 Created
├─ 🔄 APM Form Partially Started
├─ 🔄 Product ID System Propagating (Jan 15-17)
├─ 🔄 Tech Group REQ65217701 In Progress
└─ 💬 Ready to Contact Kevin Tadda (DQC)

Week 2 (Jan 19-25, 2026)
├─ ✅ Product ID Propagation Complete (expected)
├─ ⏭️ Complete APM Form
├─ ⏭️ Submit Team Rosters Request
└─ ⏭️ Begin APM Assessments (DCA, RISK, EPRA)

Week 3-4 (Jan 26 - Feb 8, 2026)
├─ ⏭️ Complete APM Assessments
├─ ⏭️ Await APM Certification
└─ ⏭️ Initiate SSP Process

Week 5-7 (Feb 9 - Feb 28, 2026)
├─ ⏭️ Complete SSP Assessment
├─ ⏭️ Await SSP Approval
└─ ⏭️ Begin Azure Environment Setup

Week 8+ (Mar 1+, 2026)
├─ ⏭️ Complete Azure Infrastructure
├─ ⏭️ Configure CI/CD Pipelines
├─ ⏭️ Security Testing & Validation
└─ 🚀 Production Ready

**Estimated Full Path to Production:** 8-10 weeks (target: Late February/Early March 2026)
```

---

## 🔗 Step-by-Step Guide

### Step 0: Clipper Setup
- **Purpose:** Create Product ID in Walmart's enterprise product catalog
- **Owner:** Product Owner / Application Lead
- **Duration:** 3-5 days
- **Key Output:** Product ID (6426)
- **Why First:** All downstream processes require a Product ID
- **Status:** ✅ COMPLETE
- **[View Details →](./00-Clipper_Setup/README.md)**

### Step 1: DQC Assignment
- **Purpose:** Identify Data Quality Champion who can submit Team Rosters request
- **Owner:** DQC Search / Product Owner
- **Duration:** 1-3 days (mostly coordination)
- **Key Output:** DQC contact and confirmation
- **Why Second:** DQC is required before Team Rosters (Step 2)
- **Status:** ✅ ASSIGNED (Kevin Tadda)
- **[View Details →](./01-DQC_Assignment/README.md)**

### Step 2: Team Rosters
- **Purpose:** Create Product Team record in HR systems
- **Owner:** DQC (Kevin Tadda)
- **Duration:** 3-5 days
- **Key Output:** Product Team ID, team roster confirmation
- **Why Third:** Proves team exists before APM registration
- **Status:** ⏳ NOT STARTED (blocked on DQC coordination)
- **[View Details →](./02-Team_Rosters/README.md)**

### Step 3: APM Setup
- **Purpose:** Register application in Application Portfolio Management system
- **Owner:** Application Owner / Technical Owner
- **Duration:** 2-4 weeks (includes assessments)
- **Key Output:** APM Certified status
- **Why Fourth:** APM is prerequisite for security compliance
- **Status:** 🔄 IN PROGRESS (50% complete, blocked on Product ID update)
- **[View Details →](./03-APM_Setup/README.md)**

### Step 4: SSP Process
- **Purpose:** Complete Solution Security Plan for production deployment
- **Owner:** Security Lead / Application Owner
- **Duration:** 2-3 weeks
- **Key Output:** SSP Approved status
- **Why Fifth:** Security assessment required before infrastructure setup
- **Status:** ⏳ NOT STARTED (blocked on APM certification)
- **[View Details →](./04-SSP_Process/README.md)**

### Step 5: Azure Setup
- **Purpose:** Provision production infrastructure in Microsoft Azure
- **Owner:** Infrastructure Lead / Cloud Team
- **Duration:** 3-4 weeks
- **Key Output:** Production environment ready for deployment
- **Why Sixth:** Can't deploy until security approved and infrastructure ready
- **Status:** ⏳ NOT STARTED (blocked on SSP approval)
- **[View Details →](./05-Azure_Setup/README.md)**

---

## ⚠️ Critical Blockers & Dependencies

| Blocker | Status | Impact | Resolution Timeline |
|---------|--------|--------|-------------------|
| **Cost Center White List** | ✅ Resolved | Clipper account confirmation | Resolved Jan 2026 |
| **Product ID System Propagation** | 🔄 In Progress | APM form completion | Jan 15-17, 2026 |
| **Tech Group Finalization (REQ65217701)** | 🔄 In Progress | APM registration quality | 1-2 weeks |
| **APM Certification** | ⏳ Pending | SSP process start | After APM complete |
| **SSP Approval** | ⏳ Pending | Azure setup start | After SSP complete |

---

## 📝 Key Contacts

| Role | Name | Area | Purpose |
|------|------|------|---------|
| **Product Manager** | Kendall Rush | Product Strategy | Product oversight, APM coordination |
| **Engineering Manager** | Kendall Rush | Technical Direction | Architecture, infrastructure decisions |
| **DQC** | Kevin Tadda | Data Quality & Governance | Gateway for Team Rosters, APM support |
| **APM Support** | [APM Team] | Application Portfolio Mgmt | APM registration and certification |
| **Security Lead** | [To Be Assigned] | Information Security | SSP process and security assessment |
| **Infrastructure Lead** | [To Be Assigned] | Cloud Infrastructure | Azure environment setup and management |

---

## 📚 Supporting Documentation

### Process Documentation
- [STORE_SUPPORT_PATH_TO_PRODUCTION.md](../STORE_SUPPORT_PATH_TO_PRODUCTION.md) - Executive overview and ROI
- [Clipper Setup Process](./00-Clipper_Setup/README.md) - Product ID creation
- [DQC Assignment](./01-DQC_Assignment/README.md) - Finding your Data Quality Champion
- [Team Rosters](./02-Team_Rosters/README.md) - Creating product team record
- [APM Setup Complete Guide](./03-APM_Setup/APM_Registration_Complete_Guide.md) - Detailed APM instructions
- [APM ServiceNow Guide](./03-APM_Setup/ServiceNow_Guide.md) - ServiceNow Application Hub navigation
- [SSP Process](./04-SSP_Process/README.md) - Security assessment process
- [Azure Setup](./05-Azure_Setup/README.md) - Infrastructure provisioning

### Progress Tracking
- [Clipper Setup Progress](./00-Clipper_Setup/PROGRESS_LOG.md) - Step 0 status and learnings
- [APM Setup Progress](./03-APM_Setup/PROGRESS_LOG.md) - Step 3 status and blockers

---

## ✅ Success Checklist

### For Completing Path to Production
- [ ] Step 0: Clipper Setup Complete (Product ID 6426)
- [ ] Step 1: DQC Assignment Complete (Kevin Tadda assigned)
- [ ] Step 2: Team Rosters Complete (Product Team created)
- [ ] Step 3: APM Certified Status Awarded
- [ ] Step 4: SSP Approved Status Awarded
- [ ] Step 5: Azure Infrastructure Operational
- [ ] Production deployment ready
- [ ] Activity Hub live in production

### For Full Activity Hub Deployment
- [ ] Path to Production complete ✓ (above checklist)
- [ ] Activity Hub core development complete
- [ ] 16-platform integrations implemented
- [ ] Data migration and validation complete
- [ ] User training and documentation complete
- [ ] Production deployment and launch
- [ ] Post-launch monitoring and support

---

## 📊 Metrics & KPIs

### Timeline Tracking
- **Planned Start:** January 2026
- **Planned Completion:** Late February / Early March 2026
- **Total Duration:** 8-10 weeks (accounting for blockers and approvals)

### Status Dashboard
- **Steps Completed:** 1/6 (17%)
- **Steps In Progress:** 1/6 (17%)
- **Steps Blocked:** 4/6 (67%)
- **Overall Progress:** ~20%

### Next Milestones
- **Immediate (This Week):** Product ID system propagation complete
- **Week 2:** APM form finalized and submitted
- **Week 3-4:** APM certification achieved
- **Week 5+:** SSP approval and Azure setup begin

---

**Last Updated:** January 12, 2026  
**Next Review:** January 19, 2026  
**Owner:** Kendall Rush (Product Manager), Kevin Tadda (DQC)  
**Status:** ON TRACK - Awaiting Product ID System Update
