# Application Portfolio Management (APM) Setup

## Service Ticket
- **APM Creation Request**: RITM74792480

## Resources

### Core Resources
1. **APM FAQ & Guidance**: https://teams.wal-mart.com/sites/GBSConnect/SitePages/Frequently-Asked-Questions---APM-and-SOF.aspx
2. **APM Overview**: https://teams.wal-mart.com/sites/GBSConnect/SitePages/What-Is-Application-Portfolio-Management-.aspx
3. **APM Field Glossary**: https://walmart.sharepoint.com/sites/GBSConnect/SitePages/APM-Fields-GLossar.aspx
4. **Application Hub**: https://walmartglobal.service-now.com/apm?id=wm_application_hub
5. **Onboarding Request**: https://walmartglobal.service-now.com/wm_sp/?id=sc_cat_item_guide&sys_id=e5a706c887c3cd102d2433fc3fbb35c3
6. **SSP Initiation**: https://walmartglobal.service-now.com/ssp?id=ssp_plan_form

**Access**: All resources require Walmart internal authentication

## Overview

Application Portfolio Management (APM) is Walmart's framework for managing, classifying, and governing applications across the enterprise. This guide covers the complete APM onboarding process from initial request submission through Security and Scalability Planning (SSP) initiation.

The APM process ensures applications meet governance, security, compliance, and scalability requirements before production deployment.

## 🧭 What is APM?

APM provides:
- Governance structure and compliance frameworks
- Data classification and security assessments
- Risk and privacy risk evaluation
- Integration requirements and standards
- Success metrics and KPIs

**Key Point**: APM treats your entire application (UI, backend, database) as a single unified record for governance purposes.

---

## 📝 How to Draft Your APM Onboarding Description

The "Name" and "Description" fields are critical for approval. They will be reviewed by APM governance teams.

### DO:
- [ ] Describe the business functionality the application provides
- [ ] Include the full stack (UI, backend, database) as one application—not as separate records
- [ ] Be specific about what business problems the application solves
- [ ] Clearly state business value and use cases
- [ ] Reference field definitions from: https://walmart.sharepoint.com/sites/GBSConnect/SitePages/APM-Fields-GLossar.aspx

### DO NOT:
- [ ] State reasons for the request (e.g., "needed for compliance")
- [ ] Onboard instance-specific records (e.g., DEV, TEST, PROD)
- [ ] Onboard version-specific applications
- [ ] Onboard data migrations or transfers (unless described as a formal solution)
- [ ] Onboard OneOps Assemblies, WCNP Namespaces, or Managed Services unless they are high-level and strategic

### Example Descriptions:

**❌ Bad Examples:**
- "We need this for SOX compliance"
- "Backend database for our system"
- "Test version of application X"

**✅ Good Examples:**
- "This application manages [specific business function] for [business unit], handling [data types] and providing [specific business value]"
- "Customer Order Management System - handles order placement, fulfillment tracking, and customer communication for Global Commerce operations"
- "Supply Chain Optimization Platform - manages inventory allocation, demand forecasting, and logistics routing across distribution centers"

---

## 🧭 Navigating the Application Hub

The Application Hub is your central workspace for managing assessments and application data.

### Initial Navigation:
1. [ ] Go to Application Hub: https://walmartglobal.service-now.com/apm?id=wm_application_hub
2. [ ] Locate "My Pending Assessments" in the center of the screen
3. [ ] Review all pending assessment items
4. [ ] Track assessment status and completion dates

---

## Setup Steps: APM Onboarding Process

### Step 1: Submit Onboarding Request

1. [ ] Go to ServiceNow Onboarding Request: https://walmartglobal.service-now.com/wm_sp/?id=sc_cat_item_guide&sys_id=e5a706c887c3cd102d2433fc3fbb35c3
2. [ ] Verify Application Owner has no outstanding certification tasks (request will be blocked if they do)
3. [ ] Complete "Name" field with clear application identifier
4. [ ] Complete "Description" field using the guidance from "📝 How to Draft Your APM Onboarding Description" section above
5. [ ] Submit onboarding request
6. [ ] **Record your APM#** once approved (you'll receive this via email)
7. [ ] Note: Not ready for SSP yet at this stage

**Timeline**: Approval typically takes 2-5 business days

---

### Step 2: Complete Data Classification Assessment (DCA)

⚠️ **CRITICAL**: Once PCI, FINC, and SOX categories are added via DCA, they cannot be removed except during SSP review. Choose carefully!

1. [ ] Navigate to Application Hub: https://walmartglobal.service-now.com/apm?id=wm_application_hub
2. [ ] Go to "My Pending Assessments" section
3. [ ] Locate and open the **Data Classification Assessment (DCA)**
4. [ ] Determine your app's data categories:
   - [ ] Does it handle PCI (Payment Card Industry) data?
   - [ ] Does it handle FINC (Financial) data?
   - [ ] Does it handle SOX (Sarbanes-Oxley) data?
5. [ ] Document the business reasons for each category selected
6. [ ] Complete and submit DCA
7. [ ] **Document which categories were added** (these are permanent unless changed during SSP)

**Timeline**: 3-7 business days for completion

---

### Step 3: Additional Assessments Triggered

After DCA is complete, the system will automatically initiate additional assessments. Complete these as required:

1. [ ] **PCI Assessment** - Evaluate Payment Card Industry compliance requirements
2. [ ] **RISK Assessment** - General business and operational risk evaluation
3. [ ] **Enterprise Privacy Risk Assessment (EPRA)** via One Trust - If triggered by One Trust based on data classification

**Important**: Do not delay these assessments. They must all be completed before certification.

**Timeline**: 2-3 weeks depending on complexity

---

### Step 4: Achieve Certification and Initiate SSP

Once all assessments are complete:

1. [ ] Wait for DCA and PCI completion confirmation
2. [ ] System automatically evaluates for "Certified" status
3. [ ] Monitor your Application Hub for certification confirmation
4. [ ] Once Certified, initiate an SSP at: https://walmartglobal.service-now.com/ssp?id=ssp_plan_form
5. [ ] Complete SSP with security and scalability requirements
6. [ ] Obtain SSP approval before production deployment

**Timeline**: SSP process typically takes 1-2 weeks

---

## 📌 Important Approval Criteria

**Before submitting your onboarding request, verify:**

- [ ] Application Owner has no outstanding certification tasks
- [ ] Name field clearly identifies the application
- [ ] Description field clearly defines business functionality
- [ ] Description articulates specific business value and use cases
- [ ] Record does NOT separate by component (UI/backend/database), instance (DEV/TEST/PROD), or version
- [ ] Data classification choices (PCI/FINC/SOX) are justified by actual data handled
- [ ] Full application stack (UI, backend, database) is represented as ONE record

**Common Rejection Reasons:**
- ❌ Vague or compliance-focused descriptions
- ❌ Separating application layers into multiple records
- ❌ Onboarding test/non-production instances
- ❌ Application Owner has pending certifications
- ❌ Missing or incomplete required fields

---

## 📬 Quick Reference: APM Onboarding Process Flow

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Draft & Submit Onboarding Request              │
│ Output: APM# (approval may take 2-5 days)              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 2: Complete Data Classification Assessment (DCA)   │
│ Output: Data categories identified (PCI/FINC/SOX)       │
│ ⚠️  These are PERMANENT - choose carefully!             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 3: Complete Auto-Triggered Assessments             │
│ - PCI Assessment                                         │
│ - RISK Assessment                                        │
│ - EPRA (if triggered)                                    │
│ Output: All assessments passed                           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 4: Achieve Certification & Initiate SSP            │
│ Output: Certified status + SSP initiation               │
│ Next: Security and Scalability Planning phase            │
└─────────────────────────────────────────────────────────┘
```

---

## Key Information to Document

Create a document or use the "Notes" section below to track:

- [ ] Application Name and Description (as submitted)
- [ ] **APM#** (assigned at approval)
- [ ] Application Owner name and contact
- [ ] DCA categories selected (PCI/FINC/SOX) and justification
- [ ] DCA submission date and completion date
- [ ] PCI Assessment results and completion date
- [ ] RISK Assessment results and completion date
- [ ] EPRA Assessment results (if applicable) and completion date
- [ ] Certification status and date achieved
- [ ] SSP submission date
- [ ] SSP approval date
- [ ] Production deployment date

---

## Support Contacts

**APM Questions & Support:**
- Email: apmmailbox@wal-mart.com
- SharePoint: https://teams.wal-mart.com/sites/GBSConnect

**SSP (Security & Scalability Planning) Support:**
- Email: Secrisk@wal-mart.com
- Workplace Group: https://walmart.workplace.com/groups/807323419664741/

**Application Hub Technical Issues:**
- ServiceNow Platform Support (in-application support link)

---

## 📖 Additional Resources

- **APM Overview & Definition**: https://teams.wal-mart.com/sites/GBSConnect/SitePages/What-Is-Application-Portfolio-Management-.aspx
- **APM FAQ & SOF**: https://teams.wal-mart.com/sites/GBSConnect/SitePages/Frequently-Asked-Questions---APM-and-SOF.aspx
- **Field Definitions & Glossary**: https://walmart.sharepoint.com/sites/GBSConnect/SitePages/APM-Fields-GLossar.aspx
- **Governance Standards**: Contact APM Help (apmmailbox@wal-mart.com)

---

## Notes

### Pre-Onboarding Planning
_Add your initial planning notes here_

### Onboarding Progress
_Track your progress through each step_

### Assessment Results
_Document DCA, PCI, RISK, and EPRA findings_

### Lessons Learned
_Document insights for future APM submissions_

### Contact Logs
_Record any communications with APM or SSP teams_
