# 🚀 Walmart Production Path
## Complete Guide to Production Deployment Process

**Last Updated:** November 25, 2025  
**Purpose:** Master guide for navigating Walmart's complete production onboarding process from DQC assignment through SSP approval

---

## 📋 Process Overview

The Walmart Solution Onboarding Process follows this sequence:

```
Standard:      DQC → Team Rosters → APM → SSP → Azure Setup
With AI/ML:    DQC → Team Rosters → APM → AI Assessments → SSP → Azure Setup
```

**Total Timeline:** 
- **Standard Solutions:** 5-10 weeks
- **AI/ML Solutions:** 7-14 weeks (includes AI Compliance Assessment, EPRA, GenAI Legal Review)

> **💡 Using AI/ML in your solution?** See [AI Policy Guide](../AI_Policy/) for required assessments and compliance requirements.

---

## 🗺️ The Complete Production Path

### Step 1: Data Quality Champion (DQC) Assignment
**Folder:** [`01-DQC_Assignment/`](./01-DQC_Assignment/)  
**Owner:** Your Pillar's Data Governance Lead  
**Timeline:** 1-3 days

#### What You Need:
- [ ] Identify your Data Quality Champion (DQC)
- [ ] If no DQC exists, request assignment from your pillar's data governance lead

#### Key Resources:
- **DQC Network List:** [Find your DQC here](https://walmart.sharepoint.com/sites/dqc-network)
- **Why it matters:** Only a DQC can submit new Product Team requests in Team Rosters

#### Outputs:
- ✅ DQC identified and assigned
- ✅ DQC contact information documented

---

### Step 2: Team Rosters Product ID Creation
**Folder:** [`02-Team_Rosters/`](./02-Team_Rosters/)  
**Owner:** DQC (Data Quality Champion)  
**Timeline:** 3-5 business days

#### What You Need:
- [ ] Engineering work source (Enterprise JIRA, Global JIRA, ServiceNow, Azure DevOps)
- [ ] Project/component name used for tracking work
- [ ] Product team name
- [ ] Pillar and product association
- [ ] Any additional required fields

#### Process:
1. DQC logs into Team Rosters (via ServiceNow)
2. Navigate: **Admin tab** → **Request Product Teams** → **Request Product Team**
3. Complete all required fields
4. Submit request and await approval

#### Outputs:
- ✅ **Product ID** assigned and available for allocation
- ✅ Product team registered in Team Rosters

> **📌 ServiceNow:** Team Rosters requests are submitted via ServiceNow. See [ServiceNow Guide](./02-Team_Rosters/ServiceNow_Guide.md) for portal access and tracking.

---

### Step 3: Application Portfolio Management (APM) Registration
**Folder:** [`03-APM_Setup/`](./03-APM_Setup/)  
**Owner:** Application Owner / Technical Owner  
**Timeline:** 2-4 weeks

#### What You Need:
- [ ] Application name and description (business functionality, NOT technical details)
- [ ] Business owner and technical owner (names/contact info)
- [ ] Application type (Business/Technical)
- [ ] Business unit/organization
- [ ] Data classification (Public, Internal, Confidential, Restricted)
- [ ] Hosting details (on-prem, cloud, hybrid)
- [ ] Integrations/dependencies
- [ ] Lifecycle state (Active, Retired, etc.)
- [ ] Compliance requirements (PCI, SOX, HIPAA, etc.)
- [ ] Deployment environments (Prod, Non-Prod)
- [ ] Architecture diagram (optional but recommended)

#### Process:
1. Go to [APM SharePoint](https://teams.wal-mart.com/sites/GBSConnect) or [Application Hub](https://walmartglobal.service-now.com/apm?id=wm_application_hub)
2. Click "Register Application" or "Create New Record"
3. Complete all required fields using business-focused descriptions
4. Submit for review and certification
5. Complete Data Classification Assessment (DCA)
6. Complete auto-triggered assessments (PCI, RISK, EPRA if applicable)
7. Achieve "Certified" status

#### Critical Guidelines:
- ✅ Describe **business functionality**, not technical architecture
- ✅ Treat full stack (UI, backend, database) as **ONE application**
- ✅ Focus on **business value** and **use cases**
- ❌ DO NOT separate by component, instance (DEV/TEST/PROD), or version
- ❌ DO NOT state compliance reasons as the application description

#### Outputs:
- ✅ **APM ID** assigned
- ✅ Certified status achieved
- ✅ All assessments completed (DCA, PCI, RISK, EPRA)

> **📌 ServiceNow:** APM registration and all assessments are completed via ServiceNow Application Hub. See [ServiceNow Guide](./03-APM_Setup/ServiceNow_Guide.md) for portal access and navigation.

---

### Step 4: Solution Security Plan (SSP) Completion
**Folder:** [`04-SSP_Process/`](./04-SSP_Process/)  
**Owner:** Application Owner / Technical Owner  
**Timeline:** 1-3 weeks

#### What You Need:
- [ ] **APM ID** from Step 3
- [ ] Solution details: data types, integrations, ownership
- [ ] Security requirements and controls
- [ ] Architecture diagrams
- [ ] Data flow diagrams
- [ ] Privacy impact assessment details
- [ ] SOX controls (if applicable)
- [ ] Vendor assessment details (if applicable)

#### Process:
1. Go to [SSP Portal](https://walmartglobal.service-now.com/ssp?id=ssp_plan_form)
2. Start a new SSP for your solution
3. Reference your **APM ID** from Step 3
4. Complete solution details, data types, integrations, ownership
5. Submit the SSP for review
6. Complete all auto-generated tasks:
   - Privacy assessment
   - SOX controls (if applicable)
   - Data Governance review
   - Vendor Assessment (if applicable)
   - TCA (Technical Compliance Assessment)
7. Respond to SME/TCA analyst questions as needed
8. Await final approval

#### Outputs:
- ✅ **SSP Approved** status
- ✅ Authorization to deploy to production
- ✅ All compliance tasks completed

#### Post-SSP (Ongoing):
- Monitor compliance continuously
- Address security findings promptly
- Update APM/SSP for significant changes
- Complete annual recertification
- Follow incident response procedures if needed

> **📌 ServiceNow:** SSP is initiated and managed entirely via ServiceNow SSP Portal. All tasks, questions, and approvals happen in ServiceNow. See [ServiceNow Guide](./04-SSP_Process/ServiceNow_Guide.md) for SSP-specific guidance.

---

### Step 5: Azure Cloud Setup & Production Deployment
**Folder:** [`05-Azure_Setup/`](./05-Azure_Setup/)  
**Owner:** Application Owner / Cloud Infrastructure Team  
**Timeline:** 1-2 weeks

#### What You Need:
- [ ] SSP Approved status from Step 4
- [ ] Azure subscription (request if needed)
- [ ] Resource planning (compute, storage, database, networking)
- [ ] Security controls from SSP
- [ ] Monitoring and logging requirements
- [ ] Budget approval for Azure costs
- [ ] Architecture diagram (Azure-specific)

#### Process:
1. Request Azure subscription and access
2. Plan resource groups and naming conventions (follow Walmart standards)
3. Provision Azure resources (VMs, databases, storage, networking)
4. Implement security controls from SSP
5. Configure monitoring, logging, and alerting
6. Set up backup and disaster recovery
7. Complete integration testing
8. Deploy application to production
9. Perform post-deployment verification
10. Begin ongoing compliance monitoring

#### Outputs:
- ✅ Production-ready Azure infrastructure
- ✅ Security controls implemented (matching SSP)
- ✅ Application deployed and operational
- ✅ Monitoring and logging active
- ✅ Ongoing compliance process established

---

## 📋 Complete Process Summary Table

| Step | Folder | Owner | Key Information Needed | Timeline | Output/ID |
|------|--------|-------|------------------------|----------|-----------|
| **1** | [01-DQC_Assignment](./01-DQC_Assignment/) | Pillar Data Governance Lead | DQC assignment | 1-3 days | DQC identified |
| **2** | [02-Team_Rosters](./02-Team_Rosters/) | DQC | Product team/work source details | 3-5 days | **Product ID** |
| **3** | [03-APM_Setup](./03-APM_Setup/) | App Owner | App details, owners, data, compliance | 2-4 weeks | **APM ID** + Certified |
| **3.5** | [AI_Policy](../AI_Policy/) *(if AI/ML)* | App Owner / ModelReview Team | AI/ML models, compliance, ethics | 2-4 weeks | **AI Compliance Approved** |
| **4** | [04-SSP_Process](./04-SSP_Process/) | App Owner | APM ID, solution/integration/security | 1-3 weeks | **Approved SSP** |
| **5** | [05-Azure_Setup](./05-Azure_Setup/) | App Owner / Cloud Team | Azure resources, security, deployment | 1-2 weeks | **Production-ready infrastructure** |

> **📌 Note:** Step 3.5 (AI Compliance) only applies to solutions using AI, ML, or GenAI. See [AI Policy Guide](../AI_Policy/) for details.

---

## 🎯 Quick Start Checklist

Use this as your master checklist to track progress through the complete production path:

### Phase 1: Foundation (Week 1)
- [ ] Identify or request DQC assignment
- [ ] Gather engineering work source information
- [ ] Document product team details
- [ ] Prepare business-focused application description

### Phase 2: Team Rosters (Week 1-2)
- [ ] DQC submits Team Rosters request
- [ ] Await Product ID approval
- [ ] Document Product ID for records

### Phase 3: APM Registration (Week 2-5)
- [ ] Draft application name and business-focused description
- [ ] Identify business owner and technical owner
- [ ] Complete application details and compliance requirements
- [ ] Submit APM onboarding request
- [ ] Receive APM ID
- [ ] Complete Data Classification Assessment (DCA)
- [ ] Complete PCI Assessment (if applicable)
- [ ] Complete RISK Assessment
- [ ] Complete EPRA (if triggered)
- [ ] Achieve Certified status

### Phase 3.5: AI Compliance Assessments (Week 5-7) - **If Using AI/ML**
- [ ] Complete AI Compliance Assessment (contact: ModelReview@walmart.com)
- [ ] Complete EPRA for PII data (if AI processes personal information)
- [ ] Complete GenAI Legal Review (if using generative AI tools)
- [ ] Address all AI governance findings
- [ ] Document AI/ML models and monitoring plans
- [ ] See [AI Policy Guide](../AI_Policy/) for complete requirements

### Phase 4: SSP Completion (Week 6-8 standard, Week 7-9 with AI)
- [ ] Initiate SSP with APM ID reference
- [ ] Complete solution security details
- [ ] Submit SSP for review
- [ ] Complete all auto-generated tasks
- [ ] Respond to analyst questions
- [ ] Receive SSP Approved status
- [ ] Document production deployment authorization

### Phase 5: Azure Setup & Deployment (Week 9-10)
- [ ] Request Azure subscription and access
- [ ] Plan resource groups and naming conventions
- [ ] Provision Azure resources
- [ ] Implement security controls from SSP
- [ ] Configure monitoring and logging
- [ ] Complete integration testing
- [ ] Deploy to production
- [ ] Begin ongoing compliance monitoring

---

## 🔑 Critical Success Factors

### 1. **DQC Identification**
- Cannot proceed without a DQC
- DQC is the gatekeeper for Team Rosters
- Identify early to avoid delays

### 2. **Business-Focused Descriptions**
- APM requires **business value**, not technical details
- Describe what the application **does for the business**
- Avoid compliance-focused language

### 3. **Data Classification Accuracy**
- PCI, SOX, FINC classifications are **permanent** once set
- Choose carefully based on actual data handled
- Over-classification adds unnecessary compliance burden

### 4. **AI/ML Compliance (If Applicable)**
- **Identify AI usage early** - Adds 2-4 weeks to timeline
- Contact ModelReview@walmart.com at project start
- Complete AI Governance Microlearning: wmlink/AICompliance
- Plan for AI Compliance Assessment, EPRA, and GenAI Legal Review
- See [AI Policy Guide](../AI_Policy/) for complete requirements

### 5. **Stakeholder Availability**
- Application Owner must have no pending certification tasks
- SME responses required for SSP approval
- Plan for 1-2 week response windows

### 6. **Documentation Completeness**
- Architecture diagrams accelerate reviews
- Data flow diagrams help security assessments
- Complete documentation reduces back-and-forth

### 7. **Platform Familiarity**
- **Most Production Path steps happen in ServiceNow**
- Familiarize yourself with ServiceNow navigation early
- Bookmark key portals (Application Hub, SSP Portal)
- See ServiceNow guides in each step folder (02-05) for portal-specific help

---

## 🔧 Platform Tools Reference

Most Production Path steps are executed through these platforms:

| Platform | Used In Steps | Purpose | ServiceNow Guide |
|----------|---------------|---------|------------------|
| **ServiceNow** | Steps 2, 3, 4, 5 | Primary platform for APM, SSP, requests | See each step folder |
| **Team Rosters** | Step 2 | Product ID registration | [02-Team_Rosters/ServiceNow_Guide.md](./02-Team_Rosters/ServiceNow_Guide.md) |
| **Application Hub** | Step 3 | APM registration and assessments | [03-APM_Setup/ServiceNow_Guide.md](./03-APM_Setup/ServiceNow_Guide.md) |
| **SSP Portal** | Step 4 | Security and scalability planning | [04-SSP_Process/ServiceNow_Guide.md](./04-SSP_Process/ServiceNow_Guide.md) |
| **Azure Portal** | Step 5 | Cloud infrastructure setup | [05-Azure_Setup/ServiceNow_Guide.md](./05-Azure_Setup/ServiceNow_Guide.md) |
| **OneTrust** | Step 3 (if EPRA) | Enterprise privacy assessments | Triggered via APM |
| **ai.walmart.com** | Step 3.5 (if AI) | AI tools and resources | [AI Policy Guide](../AI_Policy/) |

---

## 📞 Key Support Contacts

### DQC Network
- **Portal:** [DQC Network List](https://walmart.sharepoint.com/sites/dqc-network)
- **Purpose:** Find your Data Quality Champion

### Team Rosters Support
- **Portal:** [Team Rosters](https://teamrosters.walmart.com)
- **Purpose:** Product ID registration

### APM Support
- **Email:** apmmailbox@wal-mart.com
- **SharePoint:** [GBS Connect](https://teams.wal-mart.com/sites/GBSConnect)
- **Application Hub:** [ServiceNow APM](https://walmartglobal.service-now.com/apm?id=wm_application_hub)
- **Purpose:** Application registration and certification

### SSP Support
- **Email:** Secrisk@wal-mart.com
- **Portal:** [SSP Portal](https://walmartglobal.service-now.com/ssp?id=ssp_plan_form)
- **Workplace Group:** [Security & Risk](https://walmart.workplace.com/groups/807323419664741/)
- **Purpose:** Security and scalability planning

---

## 📁 Folder Structure

```
Production_Path/
├── README.md (this file)
├── 01-DQC_Assignment/
│   └── README.md
├── 02-Team_Rosters/
│   ├── README.md
│   └── ServiceNow_Guide.md
├── 03-APM_Setup/
│   ├── README.md
│   ├── APM_Registration_Complete_Guide.md (detailed guide)
│   └── ServiceNow_Guide.md
├── 04-SSP_Process/
│   ├── README.md (includes post-SSP ongoing compliance)
│   └── ServiceNow_Guide.md
└── 05-Azure_Setup/
    ├── README.md
    ├── ServiceNow_Guide.md
    ├── Azure_Account_Setup_Guide.md
    ├── Azure_HTML_Publishing_Guide.md
    ├── Azure_Management_Groups_AccessLevels.md
    └── Azure_Permission_Error_Resolution.md
```

---

## 🎓 Best Practices & Lessons Learned

### Before You Start
1. **Gather all information first** - Don't start until you have complete details
2. **Align with stakeholders** - Ensure business owner and technical owner are identified and available
3. **Review field definitions** - Use the APM Field Glossary to understand requirements
4. **Draft descriptions carefully** - Focus on business value, not technical architecture
5. **Identify AI/ML usage early** - If using AI, contact ModelReview@walmart.com and add 2-4 weeks to timeline

### During the Process
1. **Monitor assessments daily** - Don't let tasks sit idle
2. **Respond to questions promptly** - Delays compound across multiple review stages
3. **Document everything** - Track APM ID, Product ID, assessment dates, and decisions
4. **Escalate blockers early** - Don't wait until deadlines to raise issues

### After Approval
1. **Maintain records** - Keep all IDs and approval documentation accessible
2. **Update as needed** - Notify APM/SSP teams of significant changes
3. **Share learnings** - Document insights for future onboarding efforts

---

## 🚦 Common Blockers & Solutions

| Blocker | Solution |
|---------|----------|
| No DQC assigned | Contact pillar data governance lead immediately |
| Application Owner has pending certifications | Owner must complete existing tasks before new onboarding |
| APM description rejected | Rewrite to focus on business value, not technical details or compliance |
| Data classification uncertainty | Consult with data governance team before submitting DCA |
| SSP tasks not triggered | Verify APM record is "Certified" status |
| TCA analyst questions | Respond within 2 business days with complete information |
| AI compliance unclear | Review [AI Policy Guide](../AI_Policy/) and contact ModelReview@walmart.com |
| GenAI tool not approved | Use only approved tools listed in GenAI Usage Standard (DC-DG-06-02) |

---

## 📈 Progress Tracking Template

Use this template to track your journey through the Production Path:

```markdown
### Production Path Progress

**Project:** [Your Application Name]
**Start Date:** [Date]
**Target Production Date:** [Date]

#### Step 1: DQC Assignment
- [ ] DQC identified: [Name]
- [ ] DQC contact: [Email]
- [ ] Completion date: [Date]

#### Step 2: Team Rosters Product ID
- [ ] Request submitted: [Date]
- [ ] Product ID received: [ID]
- [ ] Completion date: [Date]

#### Step 3: APM Registration
- [ ] Onboarding request submitted: [Date]
- [ ] APM ID received: [ID]
- [ ] DCA completed: [Date]
- [ ] PCI Assessment completed: [Date]
- [ ] RISK Assessment completed: [Date]
- [ ] EPRA completed: [Date] (if applicable)
- [ ] Certified status achieved: [Date]

#### Step 3.5: AI Compliance (if applicable)
- [ ] Uses AI/ML: [Yes/No]
- [ ] AI Compliance Assessment submitted: [Date]
- [ ] AI Compliance Assessment approved: [Date]
- [ ] EPRA for AI data completed: [Date] (if processing PII)
- [ ] GenAI Legal Review completed: [Date] (if using GenAI)
- [ ] AI governance controls documented: [Date]
- [ ] Contact: ModelReview@walmart.com

#### Step 4: SSP Completion
- [ ] SSP initiated: [Date]
- [ ] All tasks completed: [Date]
- [ ] SSP approved: [Date]
- [ ] Production deployment authorized: [Date]

#### Step 5: Azure Setup & Production Deployment
- [ ] Azure subscription requested: [Date]
- [ ] Resources provisioned: [Date]
- [ ] Security controls implemented: [Date]
- [ ] Production deployment: [Date]
- [ ] Post-deployment verification: [Date]
- [ ] Ongoing compliance monitoring started: [Date]

#### Key Information
- **Product ID:** [ID]
- **APM ID:** [ID]
- **SSP Reference:** [Reference]
- **Azure Subscription ID:** [ID]
- **Business Owner:** [Name]
- **Technical Owner:** [Name]
- **Data Classifications:** [PCI/SOX/FINC/etc.]
```

---

## 🔄 Continuous Improvement

This Production Path guide is a living document. As you progress through the process:

- **Document new learnings** in the appropriate folder
- **Update timelines** based on actual experience
- **Add clarifications** for commonly misunderstood requirements
- **Share success patterns** that accelerated your onboarding

---

**💡 Remember:** The Production Path is a compliance and governance framework designed to protect Walmart and its customers. While it may seem lengthy, each step ensures your application meets enterprise standards for security, privacy, and operational excellence.

**Start early, stay organized, and communicate proactively!**
