# 🔒 Step 4: Solution Security Plan (SSP) Process

**Timeline:** 1-3 weeks  
**Owner:** Application Owner / Technical Owner  
**Prerequisites:** Step 3 completed (APM ID + "Certified" status)

---

## 🎯 Overview

The Solution Security Plan (SSP) is Walmart's comprehensive security and scalability assessment process. It ensures your application meets enterprise standards for security, privacy, compliance, and operational readiness before production deployment.

**Key Output:** Approved SSP status, which authorizes production deployment

---

## 🔧 ServiceNow SSP Portal

The SSP process is managed entirely through ServiceNow's SSP Portal. For detailed instructions on:
- Accessing SSP Portal
- Initiating a new SSP with your APM ID
- Monitoring auto-generated tasks
- Responding to SME questions
- Tracking SSP approval status

**See:** [ServiceNow Guide for SSP Process](./ServiceNow_Guide.md)

---

## ✅ What You Need to Do

### Phase 1: Prepare Required Information (Week 1)
- [ ] **APM ID** from Step 3 (REQUIRED)
- [ ] Solution details and architecture
- [ ] Data types and data flows
- [ ] Integration points and dependencies
- [ ] Security controls and measures
- [ ] Privacy impact assessment details
- [ ] SOX controls (if applicable)
- [ ] Vendor information (if applicable)
- [ ] Infrastructure and hosting details
- [ ] Scalability and performance requirements

### Phase 2: Initiate SSP (Week 1)
- [ ] Go to [SSP Portal](https://walmartglobal.service-now.com/ssp?id=ssp_plan_form)
- [ ] Click "Start New SSP"
- [ ] Reference your **APM ID** from Step 3
- [ ] Complete solution overview section
- [ ] Submit SSP for review

### Phase 3: Complete Auto-Generated Tasks (Week 1-2)
After SSP submission, the system automatically generates review tasks based on your APM data classification and compliance requirements:

- [ ] **Privacy Assessment** - Data privacy impact and controls
- [ ] **SOX Controls** (if SOX data classification) - Financial controls and audit trails
- [ ] **Data Governance Review** - Data management and quality standards
- [ ] **Vendor Assessment** (if third-party vendors) - Vendor security and compliance
- [ ] **TCA (Technical Compliance Assessment)** - Security architecture and controls
- [ ] **Other assessments** based on your specific requirements

### Phase 4: SME Review & Questions (Week 2-3)
- [ ] Monitor SSP portal for analyst questions
- [ ] Respond to SME (Subject Matter Expert) questions within 2 business days
- [ ] Provide additional documentation as requested
- [ ] Clarify security controls or architecture as needed
- [ ] Track task completion status

### Phase 5: Final Approval (Week 3)
- [ ] Verify all auto-generated tasks show "Complete" or "Approved"
- [ ] System evaluates for final SSP approval
- [ ] Receive SSP Approved notification
- [ ] **Production deployment authorized**

---

## 📋 Required Information Details

### 1. Solution Details
**What you need:**
- High-level solution description
- Business purpose and use cases
- Target users and stakeholders
- Expected transaction volumes
- Data retention requirements

**Why it matters:** Sets context for all security and scalability assessments

---

### 2. Architecture Documentation
**What you need:**
- Architecture diagram showing all components
- Data flow diagram showing data movement
- Integration points with other systems
- Technology stack (languages, frameworks, databases)
- Hosting environment details

**Why it matters:** TCA analysts need to understand technical architecture to assess security controls

**📎 Recommended Format:**
- High-level architecture (PowerPoint or Visio)
- Component diagram with security zones
- Data flow with encryption points marked
- Integration diagram with authentication methods

---

### 3. Data Types and Classification
**What you need:**
- List of all data types processed/stored
- Data classification for each type (based on APM DCA)
- Data sources and destinations
- Data retention and archival policies
- PII (Personally Identifiable Information) details

**Why it matters:** Determines privacy assessment scope and security control requirements

---

### 4. Security Controls
**What you need:**
- Authentication methods (SSO, MFA, etc.)
- Authorization model (RBAC, ABAC, etc.)
- Encryption at rest and in transit
- Network security (firewalls, VPC, etc.)
- Logging and monitoring
- Vulnerability management process
- Incident response plan

**Why it matters:** Core of TCA evaluation

---

### 5. Privacy Impact
**What you need:**
- PII collection justification
- User consent mechanisms
- Data subject rights (access, deletion, etc.)
- Third-party data sharing details
- Privacy policy alignment

**Why it matters:** Required for Privacy Assessment task completion

---

### 6. SOX Controls (if applicable)
**What you need:**
- Financial data processing details
- Segregation of duties
- Change management process
- Access controls and audit trails
- Automated controls vs. manual controls

**Why it matters:** Required if SOX data classification was selected in APM

---

### 7. Vendor Assessment (if applicable)
**What you need:**
- Vendor names and contact information
- Services provided by each vendor
- Data shared with vendors
- Vendor security certifications (SOC 2, ISO 27001, etc.)
- Contract and SLA details

**Why it matters:** Third-party risk assessment requirement

---

### 8. Scalability & Performance
**What you need:**
- Expected transaction volumes (current and projected)
- Peak load expectations
- Performance requirements (response times, throughput)
- Scalability strategy (horizontal, vertical)
- Disaster recovery plan
- Business continuity plan

**Why it matters:** Ensures solution can handle production loads

---

## 🔄 SSP Submission Process

### Step-by-Step:

1. **You:** Prepare all required information
2. **You:** Go to SSP Portal and initiate new SSP
3. **You:** Enter APM ID to link SSP to APM record
4. **You:** Complete solution overview and details
5. **You:** Submit SSP for review
6. **System:** Auto-generates tasks based on APM data classification
7. **System:** Routes tasks to appropriate SME teams (Privacy, SOX, TCA, etc.)
8. **SMEs:** Review submission and ask clarifying questions
9. **You:** Respond to questions within 2 business days
10. **SMEs:** Complete assessment and mark tasks as approved
11. **System:** Evaluates when all tasks are approved
12. **System:** Marks SSP as "Approved"
13. **You:** Receive approval notification
14. **You:** Production deployment authorized

---

## 📞 Support Contacts

### SSP Support
- **Email:** Secrisk@wal-mart.com
- **Portal:** [SSP Portal](https://walmartglobal.service-now.com/ssp?id=ssp_plan_form)
- **Workplace Group:** [Security & Risk](https://walmart.workplace.com/groups/807323419664741/)

### Task-Specific Support
- **Privacy Assessment:** Privacy Team (via SSP task comments)
- **SOX Controls:** SOX Compliance Team (via SSP task comments)
- **Data Governance:** Data Governance Team (via SSP task comments)
- **Vendor Assessment:** Third-Party Risk Team (via SSP task comments)
- **TCA:** TCA Analysts (via SSP task comments)

---

## 🎯 Success Criteria

You've successfully completed Step 4 when:

- ✅ SSP initiated with APM ID reference
- ✅ All solution details submitted
- ✅ All auto-generated tasks completed
- ✅ All SME questions answered
- ✅ All assessments marked "Approved"
- ✅ **SSP Approved status achieved**
- ✅ Production deployment authorized

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Can't initiate SSP | Verify APM record has "Certified" status |
| Tasks not auto-generated | Ensure SSP references correct APM ID |
| TCA questions unclear | Request clarification via SSP task comments |
| Missing documentation | Provide requested docs within 2 business days |
| Task stuck in review | Follow up with SME team via Secrisk@wal-mart.com |
| Privacy assessment blocked | Ensure privacy policy and consent mechanisms documented |
| SOX controls insufficient | Work with SOX team to identify required controls |

---

## 📈 Timeline Expectations

| Phase | Expected Duration |
|-------|-------------------|
| Information preparation | 3-5 days |
| SSP initiation | Same day |
| Auto-generated tasks creation | 1-2 days |
| SME review and questions | 5-10 business days |
| Question responses | 2 business days per round |
| Final approval | 2-3 days after all tasks complete |
| **Total** | **1-3 weeks** |

**⚠️ Note:** Timeline heavily depends on:
- Completeness of initial submission
- Response time to SME questions
- Complexity of solution
- Number of compliance requirements (PCI, SOX, etc.)

---

## 📝 Documentation Template

```markdown
### SSP Completion - Step 4

**Date Started:** [Date]
**Date Completed:** [Date]
**Application:** [Your Application Name]
**APM ID:** [From Step 3]

#### SSP Initiation
- **SSP Reference:** [SSP ID or reference number]
- **Initiation Date:** [Date]
- **Initial Submission Date:** [Date]

#### Auto-Generated Tasks
- **Privacy Assessment:**
  - Task ID: [ID]
  - Assigned To: [Team]
  - Questions Received: [Date]
  - Responses Submitted: [Date]
  - Status: [In Progress / Complete / Approved]
  
- **SOX Controls:** (if applicable)
  - Task ID: [ID]
  - Assigned To: [Team]
  - Questions Received: [Date]
  - Responses Submitted: [Date]
  - Status: [In Progress / Complete / Approved]
  
- **Data Governance Review:**
  - Task ID: [ID]
  - Assigned To: [Team]
  - Questions Received: [Date]
  - Responses Submitted: [Date]
  - Status: [In Progress / Complete / Approved]
  
- **Vendor Assessment:** (if applicable)
  - Task ID: [ID]
  - Assigned To: [Team]
  - Questions Received: [Date]
  - Responses Submitted: [Date]
  - Status: [In Progress / Complete / Approved]
  
- **TCA (Technical Compliance Assessment):**
  - Task ID: [ID]
  - Assigned To: [Team]
  - Questions Received: [Date]
  - Responses Submitted: [Date]
  - Status: [In Progress / Complete / Approved]

#### SME Communication Log
- [Date] - Initial submission
- [Date] - Privacy team questions received
- [Date] - Privacy questions answered
- [Date] - TCA questions received
- [Date] - TCA questions answered
- [Date] - Additional documentation provided
- [Date] - All tasks approved

#### Final Approval
- **SSP Approved Date:** [Date]
- **Approval Confirmation:** [Screenshot or email saved]
- **Production Authorization:** [Date]

#### Key Documents Submitted
- [ ] Architecture diagram
- [ ] Data flow diagram
- [ ] Security controls documentation
- [ ] Privacy policy
- [ ] SOX controls matrix (if applicable)
- [ ] Vendor contracts (if applicable)
- [ ] Disaster recovery plan
- [ ] Business continuity plan

#### Lessons Learned
- What went well: [Notes]
- What could improve: [Notes]
- Recommendations for future SSPs: [Notes]
```

---

## 🎓 Best Practices

### Before Submission:
1. ✅ Have APM ID ready and verified as "Certified"
2. ✅ Complete architecture and data flow diagrams
3. ✅ Document all security controls
4. ✅ Review privacy policy and consent mechanisms
5. ✅ Prepare SOX controls matrix (if applicable)
6. ✅ Gather vendor certifications (if applicable)

### During Review:
1. ✅ Monitor SSP portal daily for new questions
2. ✅ Respond to questions within 2 business days
3. ✅ Provide complete answers with supporting documentation
4. ✅ Ask for clarification if questions are unclear
5. ✅ Track task completion status in a spreadsheet

### After Approval:
1. ✅ Save all SSP documentation for audit purposes
2. ✅ Update SSP for significant architecture changes
3. ✅ Maintain security controls as documented
4. ✅ Document production deployment date

---

## 🚀 Post-SSP Approval: Production Deployment & Ongoing Compliance

Once your SSP is approved:

✅ **You are authorized to deploy to production!**

**However, your work doesn't end here.** SSP approval is the beginning of ongoing compliance and operational excellence.

---

## 📋 Post-SSP Approval Checklist

### 1. Implement Approved Controls
**Owner:** Application Owner / Development Team  
**Timeline:** Before production go-live

- [ ] Ensure **all security controls** identified in the SSP are implemented before deployment
- [ ] Complete any technical configurations required by InfoSec or compliance
- [ ] Implement all documentation requirements
- [ ] Complete any process changes required by InfoSec
- [ ] Verify all controls match SSP documentation exactly

**🎯 Goal:** All controls in place before go-live

---

### 2. Production Deployment
**Owner:** Application Owner / DevOps Team  
**Timeline:** Per deployment schedule

- [ ] Deploy solution to production **only after all SSP requirements are met**
- [ ] Confirm all launch criteria are satisfied:
  - ✅ Security controls implemented
  - ✅ Privacy protections active
  - ✅ Compliance requirements met
  - ✅ Monitoring and logging operational
- [ ] Document production deployment date
- [ ] Perform post-deployment verification
- [ ] Validate all security controls are functioning

**🎯 Goal:** Solution live, compliant, and secure

---

### 3. Ongoing Compliance & Monitoring
**Owner:** Application Owner / InfoSec Team  
**Timeline:** Continuous

- [ ] **Continuously monitor** your solution for compliance with Walmart security policies
- [ ] Address vulnerabilities from security scans promptly
- [ ] Respond to findings from InfoSec reviews within SLA
- [ ] Maintain all security controls as documented in SSP
- [ ] Keep logging and monitoring active and reviewed
- [ ] Conduct regular security assessments
- [ ] Track and remediate security findings

**Key Activities:**
- Review security scan results weekly
- Address critical vulnerabilities within 24-48 hours
- Respond to InfoSec audit findings within required timeframes
- Maintain compliance with all data classification requirements

**🎯 Goal:** Ongoing compliance, address findings proactively

---

### 4. Change Management
**Owner:** Application Owner  
**Timeline:** Before making significant changes

**When is a new or updated SSP required?**

A new or updated SSP is needed for **significant changes**:
- ✅ New integrations with other systems
- ✅ Data classification changes (adding PCI, SOX, FINC, etc.)
- ✅ Architecture updates (new components, hosting changes)
- ✅ New third-party vendors or services
- ✅ Changes to data flows or data storage
- ✅ Significant security control modifications

**Change Management Process:**
- [ ] Evaluate if change requires SSP update
- [ ] Update APM record as needed
- [ ] Create new or updated SSP if required
- [ ] Obtain approval before implementing change
- [ ] Document all changes and approvals

**Reference:** [When is a new SSP required?](https://walmartglobal.service-now.com/ssp?id=ssp_guidance)

**🎯 Goal:** Update APM/SSP for major changes

---

### 5. Annual Review / Recertification
**Owner:** Application Owner / InfoSec Team  
**Timeline:** Annually or as notified

- [ ] Complete periodic reviews when notified by InfoSec or SSP portal
- [ ] Recertify application security controls
- [ ] Update documentation to reflect current state
- [ ] Verify all controls still meet requirements
- [ ] Update architecture diagrams if changes occurred
- [ ] Confirm contact information is current
- [ ] Revalidate data classifications

**What to expect:**
- Annual notification from SSP portal or InfoSec
- Review of current security controls
- Validation of compliance status
- Updates to reflect any changes in past year

**🎯 Goal:** Recertification as required

---

### 6. Incident Response
**Owner:** Application Owner / InfoSec Team  
**Timeline:** Immediate upon incident

**If a security incident occurs:**

- [ ] **Immediately notify InfoSec** - Do not delay!
- [ ] Follow [Walmart's Incident Response Procedures](https://walmartglobal.service-now.com/security_incident)
- [ ] Cooperate fully with investigations
- [ ] Document incident details and timeline
- [ ] Implement corrective actions
- [ ] Update SSP and controls if needed post-incident
- [ ] Conduct post-incident review

**Critical Actions:**
1. **Contain** the incident immediately
2. **Notify** InfoSec: Secrisk@wal-mart.com
3. **Preserve** evidence for investigation
4. **Document** everything
5. **Remediate** root cause
6. **Learn** and improve controls

**🎯 Goal:** Timely reporting and resolution

---

### 7. Solution Decommissioning
**Owner:** Application Owner  
**Timeline:** When retiring solution

**When retiring or decommissioning your solution:**

- [ ] Update APM record to reflect decommissioning status
- [ ] Formally close out the SSP
- [ ] Document decommission date and reason
- [ ] Ensure all data is properly archived or deleted per retention policies
- [ ] Remove all access and credentials
- [ ] Decommission infrastructure resources
- [ ] Update all documentation

**Reference:** [Solution Decommission Guidance](https://walmartglobal.service-now.com/apm?id=decommission_guidance)

**🎯 Goal:** Proper closure of APM and SSP

---

## 📊 Post-SSP Summary Table

| Step | Owner | Timeline | Output/Goal |
|------|-------|----------|-------------|
| **Implement Controls** | App Owner/Team | Before go-live | All controls in place before go-live |
| **Deploy to Prod** | App Owner/DevOps | Per schedule | Solution live, compliant, and secure |
| **Monitor Compliance** | App Owner/InfoSec | Continuous | Ongoing compliance, address findings |
| **Change Management** | App Owner | Before changes | Update APM/SSP for major changes |
| **Annual Review** | App Owner/InfoSec | Annually | Recertification as required |
| **Incident Response** | App Owner/InfoSec | Immediate | Timely reporting and resolution |
| **Decommission** | App Owner | When retiring | Proper closure of APM and SSP |

---

## 🎯 Ongoing Compliance Best Practices

### Daily/Weekly:
- ✅ Monitor application logs and security alerts
- ✅ Review security scan results
- ✅ Track and triage vulnerabilities

### Monthly:
- ✅ Review access logs and permissions
- ✅ Verify security controls are functioning
- ✅ Update documentation for any changes

### Quarterly:
- ✅ Conduct security control validation
- ✅ Review and update runbooks
- ✅ Assess need for SSP updates

### Annually:
- ✅ Complete recertification process
- ✅ Comprehensive security review
- ✅ Update all APM and SSP documentation

---

## 📞 Post-SSP Support Contacts

### Ongoing Compliance Support
- **Email:** Secrisk@wal-mart.com
- **Purpose:** Compliance questions, security findings, incident reporting

### SSP Updates
- **Portal:** [SSP Portal](https://walmartglobal.service-now.com/ssp?id=ssp_plan_form)
- **Purpose:** Submit SSP updates for significant changes

### APM Updates
- **Email:** apmmailbox@wal-mart.com
- **Portal:** [Application Hub](https://walmartglobal.service-now.com/apm?id=wm_application_hub)
- **Purpose:** Update APM record for changes

### Security Incidents
- **Emergency:** Follow incident response procedures immediately
- **Email:** Secrisk@wal-mart.com
- **Portal:** [Security Incident Portal](https://walmartglobal.service-now.com/security_incident)

---

## 🎉 Congratulations!

You've completed the full Walmart Production Path:

1. ✅ DQC Assignment
2. ✅ Team Rosters Product ID
3. ✅ APM Registration & Certification
4. ✅ SSP Approval

**Your application is now ready for production deployment!**

**Next Step:** [Step 5: Azure Cloud Setup →](../05-Azure_Setup/)

---

## 💡 Critical Reminders

### The SSP is a Living Document
- Significant changes to architecture, data classification, or security controls **may require SSP updates**
- Keep your SSP current to maintain compliance
- When in doubt, consult with InfoSec before making major changes

### Compliance is Continuous
- SSP approval is not a "one and done" activity
- Ongoing monitoring and compliance are required
- Stay proactive about security and compliance

### You're Not Alone
- InfoSec team is your partner, not an obstacle
- Reach out early with questions or concerns
- Use available resources and support channels

---

**Need help?** Contact Secrisk@wal-mart.com or your TCA analyst.

**For detailed Azure setup guidance after SSP approval, see:** [Step 5: Azure Cloud Setup →](../05-Azure_Setup/)
