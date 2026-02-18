# 📱 Step 3: Application Portfolio Management (APM) Setup

**Timeline:** 2-4 weeks  
**Owner:** Application Owner / Technical Owner  
**Prerequisites:** Step 2 completed (Product ID received)

---

## 🎯 Overview

Application Portfolio Management (APM) is Walmart's framework for managing, classifying, and governing applications across the enterprise. This step includes application registration, data classification, and completion of all required assessments before production deployment.

**Key Output:** APM ID and "Certified" status, which are required to initiate SSP (Step 4)

---

## 📚 Complete Guide

For the **complete, detailed APM setup guide**, see:

**[APM Registration Complete Guide →](./APM_Registration_Complete_Guide.md)**

This comprehensive guide includes:
- Full APM onboarding process
- Data Classification Assessment (DCA) instructions
- PCI, RISK, and EPRA assessment guides
- Field-by-field instructions
- Common mistakes and how to avoid them
- Approval criteria and timelines

---

## 🔧 ServiceNow Application Hub

APM registration and assessments are managed through ServiceNow's Application Hub. For detailed instructions on:
- Accessing Application Hub
- Navigating to "My Pending Assessments"
- Completing assessments in ServiceNow
- Tracking your APM certification status

**See:** [ServiceNow Guide for APM Setup](./ServiceNow_Guide.md)

---

## ✅ Quick Start Checklist

Use this high-level checklist to track your APM progress:

### Phase 1: Prepare Information (Week 1)
- [ ] Draft application name (business-focused, not technical)
- [ ] Write application description (business value and use cases)
- [ ] Identify business owner and technical owner
- [ ] Determine application type (Business/Technical)
- [ ] Identify business unit/organization
- [ ] Determine data classification (Public, Internal, Confidential, Restricted)
- [ ] Document hosting details (on-prem, cloud, hybrid)
- [ ] List integrations and dependencies
- [ ] Determine lifecycle state (Active, Retired, etc.)
- [ ] Identify compliance requirements (PCI, SOX, HIPAA, etc.)
- [ ] List deployment environments (Prod, Non-Prod)
- [ ] Prepare architecture diagram (optional but recommended)

### Phase 2: Submit APM Registration (Week 1-2)
- [ ] Go to [Application Hub](https://walmartglobal.service-now.com/apm?id=wm_application_hub)
- [ ] Click "Register Application" or "Create New Record"
- [ ] Complete all required fields
- [ ] Submit for review
- [ ] Await APM ID assignment (2-5 business days)
- [ ] **Document your APM ID**

### Phase 3: Complete Data Classification Assessment (Week 2)
- [ ] Navigate to Application Hub → My Pending Assessments
- [ ] Open Data Classification Assessment (DCA)
- [ ] Determine data categories:
  - [ ] PCI (Payment Card Industry) data?
  - [ ] FINC (Financial) data?
  - [ ] SOX (Sarbanes-Oxley) data?
- [ ] **⚠️ CRITICAL:** These classifications are permanent - choose carefully!
- [ ] Document business justification for each category
- [ ] Complete and submit DCA
- [ ] **Document which categories were selected**

### Phase 4: Complete Triggered Assessments (Week 2-3)
- [ ] Complete PCI Assessment (if PCI data category selected)
- [ ] Complete RISK Assessment (always required)
- [ ] Complete EPRA via OneTrust (if triggered by data classification)
- [ ] Respond to any clarifying questions promptly

### Phase 5: Achieve Certification (Week 3-4)
- [ ] Monitor Application Hub for assessment completion
- [ ] Verify all assessments show "Complete" status
- [ ] System automatically evaluates for "Certified" status
- [ ] Confirm "Certified" status achieved
- [ ] **Ready to initiate SSP (Step 4)**

---

## 🔑 Critical Success Factors

### 1. **Business-Focused Descriptions**
✅ **DO:**
- "Customer Order Management System - handles order placement, fulfillment tracking, and customer communication for Global Commerce operations"
- "Supply Chain Optimization Platform - manages inventory allocation, demand forecasting, and logistics routing across distribution centers"

❌ **DON'T:**
- "We need this for SOX compliance"
- "Backend database for our system"
- "Test version of application X"

### 2. **Unified Application Record**
✅ **DO:**
- Treat full stack (UI, backend, database) as ONE application

❌ **DON'T:**
- Create separate records for UI, backend, database
- Create separate records for DEV, TEST, PROD
- Create separate records for different versions

### 3. **Careful Data Classification**
⚠️ **PERMANENT DECISION:**
- PCI, SOX, FINC classifications **cannot be removed** except during SSP review
- Over-classification adds unnecessary compliance burden
- Under-classification can cause delays during SSP

### 4. **Application Owner Prerequisites**
- Application Owner must have **NO outstanding certification tasks**
- Request will be **blocked** if owner has pending certifications
- Verify clean certification status before submitting

---

## 📋 Required Information Summary

| Category | What You Need |
|----------|---------------|
| **Identity** | Application name, description, type |
| **Ownership** | Business owner, technical owner, contacts |
| **Organization** | Business unit, pillar, product association |
| **Data** | Data classification, compliance requirements |
| **Infrastructure** | Hosting details, environments, architecture |
| **Integrations** | Dependencies, connected systems |
| **Lifecycle** | Current state, roadmap |

---

## 📞 Support Contacts

### APM Questions & Support
- **Email:** apmmailbox@wal-mart.com
- **SharePoint:** [GBS Connect](https://teams.wal-mart.com/sites/GBSConnect)
- **Application Hub:** [ServiceNow APM](https://walmartglobal.service-now.com/apm?id=wm_application_hub)

### Assessment-Specific Support
- **DCA Questions:** apmmailbox@wal-mart.com
- **PCI Questions:** PCI Compliance Team (via Application Hub)
- **RISK Questions:** Risk Management Team (via Application Hub)
- **EPRA Questions:** OneTrust Support (via OneTrust portal)

---

## 🎯 Success Criteria

You've successfully completed Step 3 when:

- ✅ APM ID assigned and documented
- ✅ Data Classification Assessment (DCA) completed
- ✅ PCI Assessment completed (if applicable)
- ✅ RISK Assessment completed
- ✅ EPRA completed (if triggered)
- ✅ **"Certified" status achieved**
- ✅ All assessment documentation saved

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Request rejected - vague description | Rewrite focusing on business value, not technical details |
| Application Owner has pending tasks | Owner must complete existing certifications first |
| DCA classifications uncertain | Consult with data governance team before submitting |
| Assessments not triggered | Verify APM record is approved and active |
| Can't achieve Certified status | Ensure ALL assessments show "Complete" status |
| EPRA not triggered | May not be required based on data classification |

---

## 📈 Timeline Expectations

| Phase | Expected Duration |
|-------|-------------------|
| Information preparation | 2-3 days |
| APM registration submission | Same day |
| APM ID assignment | 2-5 business days |
| Data Classification Assessment | 3-7 business days |
| Triggered assessments | 1-2 weeks |
| Certification achievement | 1-3 days after assessments complete |
| **Total** | **2-4 weeks** |

---

## 📝 Documentation Template

```markdown
### APM Setup - Step 3

**Date Started:** [Date]
**Date Completed:** [Date]
**Application:** [Your Application Name]

#### APM Registration
- **APM ID:** [ID]
- **Registration Date:** [Date]
- **Application Name:** [As submitted]
- **Description:** [As submitted]
- **Business Owner:** [Name]
- **Technical Owner:** [Name]

#### Data Classification Assessment
- **Submission Date:** [Date]
- **Completion Date:** [Date]
- **Data Categories Selected:**
  - [ ] PCI (Payment Card Industry) - Justification: [Brief reason]
  - [ ] FINC (Financial) - Justification: [Brief reason]
  - [ ] SOX (Sarbanes-Oxley) - Justification: [Brief reason]
  - [ ] Other: [Specify]

#### Triggered Assessments
- **PCI Assessment:**
  - Submission: [Date]
  - Completion: [Date]
  - Status: [Pass/Fail/N/A]
  
- **RISK Assessment:**
  - Submission: [Date]
  - Completion: [Date]
  - Status: [Pass/Fail]
  
- **EPRA (OneTrust):**
  - Triggered: [Yes/No]
  - Submission: [Date]
  - Completion: [Date]
  - Status: [Pass/Fail/N/A]

#### Certification
- **Certified Status Achieved:** [Date]
- **Certification Confirmation:** [Screenshot or email saved]

#### Key Documents
- [ ] APM registration confirmation email
- [ ] DCA submission and approval
- [ ] Assessment completion confirmations
- [ ] Certification notification
- [ ] Architecture diagram (if submitted)

#### Next Steps
- [ ] Move to Step 4: SSP Initiation
- [ ] Prepare security and scalability documentation
```

---

## 🚀 Next Step

Once you achieve "Certified" status and have your APM ID, proceed to:

**[Step 4: Solution Security Plan (SSP) →](../04-SSP_Process/)**

---

**💡 Pro Tip:** Don't rush through the Data Classification Assessment. Once PCI, SOX, or FINC categories are added, they're permanent and will trigger additional compliance requirements throughout your application's lifecycle.

---

## 📚 Additional Resources

- **[Complete APM Registration Guide](./APM_Registration_Complete_Guide.md)** - Detailed field-by-field instructions
- **APM FAQ:** https://teams.wal-mart.com/sites/GBSConnect/SitePages/Frequently-Asked-Questions---APM-and-SOF.aspx
- **APM Field Glossary:** https://walmart.sharepoint.com/sites/GBSConnect/SitePages/APM-Fields-GLossar.aspx
- **Application Hub:** https://walmartglobal.service-now.com/apm?id=wm_application_hub
