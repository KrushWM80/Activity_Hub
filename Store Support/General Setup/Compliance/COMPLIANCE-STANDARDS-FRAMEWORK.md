# Compliance Standards Framework - Reusable Reference Guide
**Version:** 1.0  
**Created:** January 14, 2026  
**Purpose:** Enterprise-wide compliance standard for all projects and systems

---

## 1. HOW TO DETERMINE COMPLIANCE REQUIREMENTS

### Step 1: Ask These Critical Questions

```
About Your Data:
1. Do you handle payment card data (credit card numbers, CVV)?
   → YES = PCI DSS applies
   
2. Do you handle or expose financial data used in SEC reporting/audits?
   → YES = SOX (Sarbanes-Oxley) applies
   
3. Do you have 50+ users accessing sensitive systems?
   → YES = SOC 2 Type II may apply
   
4. Do you collect/process personal data (names, emails, locations)?
   → YES = Privacy/GDPR/CCPA considerations apply
   
5. Do you use third-party AI/ML services with company data?
   → YES = DPA and MSO verification required
   
6. Is this system used for executive/board decision-making?
   → YES = SOX financial controls apply
```

### Step 2: Data Classification Matrix

| Data Type | Examples | PCI | SOX | SOC 2 | Privacy | DPA |
|-----------|----------|-----|-----|-------|---------|-----|
| **RESTRICTED** | Financial KPIs, payroll, legal docs | ❌ | ✅ | ✅ | ✅ | ✅* |
| **CONFIDENTIAL** | Store strategies, performance data | ❌ | 🟡 | ✅ | ✅ | ✅* |
| **INTERNAL** | General business info, user roles | ❌ | ❌ | ✅ | ✅ | ✅* |
| **PUBLIC** | Marketing materials, public docs | ❌ | ❌ | 🟡 | ❌ | ❌ |
| **Payment Cards** | PAN, CVV, expiry dates | ✅ | ❌ | ✅ | ✅ | ✅ |

**Legend:** ✅ = Required, 🟡 = Conditional, ❌ = Not applicable  
**\* DPA = Applies if data leaves organization or goes to 3rd-party AI**

---

## 2. COMPLIANCE FRAMEWORKS EXPLAINED

### PCI DSS (Payment Card Industry Data Security Standard)

**When It Applies:**
- You store, process, or transmit payment card data
- You have a payment card processor
- Any part of the system touches credit card information

**Key Requirements:**
```
Security Domains:
1. Network security (firewalls, network isolation)
2. Data protection (encryption at rest & transit)
3. Vulnerability management (patching, scanning)
4. Access control (authentication, RBAC)
5. Monitoring & testing (logging, penetration tests)
6. Security policy (documentation)
```

**Audit:** Annual internal audit + annual external audit (Level 1-2)  
**Timeline:** 6-12 months to compliance  
**Cost:** $25-50K (implementation) + $5-10K/year (audit)

---

### SOX (Sarbanes-Oxley Act)

**When It Applies:**
- Company is publicly traded (SEC regulated)
- System handles financial data used in SEC reporting
- Financial KPIs displayed on executive dashboards
- Approval workflows for financial decisions
- Board reporting systems

**Key Requirements:**
```
Control Objectives:
1. Segregation of Duties - No one person can approve own work
2. Financial Data Integrity - All changes logged and auditable
3. Access Control - Who accessed what data, when
4. Approval Workflows - Enforced authorization chains
5. Audit Trails - Immutable, tamper-proof logs (7-10 years)
6. Change Management - All code changes documented & approved
7. Disaster Recovery - Business continuity documented
```

**Critical Control:** **Black Out List** - Associates restricted from accessing SOX data
```
Implementation:
- Pre-login enforcement (check BEFORE granting access)
- Audit log entry for every attempt (successful or blocked)
- Categories: financial_kpis, budget_data, approval_workflows
- Enforcement: Database check during authentication
- Alert: Compliance team notified of violations
```

**Audit:** Annual internal audit + depends on external auditor  
**Timeline:** 8-12 weeks for implementation + ongoing compliance  
**Cost:** $35-50K (implementation) + annual internal audits

---

### SOC 2 Type II (Service Organization Control)

**When It Applies:**
- 50+ users accessing the system
- Enterprise-critical system
- Processing sensitive company data
- May be required by enterprise customers
- Cloud-based SaaS products

**Key Requirements:**
```
Trust Service Criteria (5 pillars):
1. Security - Confidentiality & integrity of data
2. Availability - System available as promised
3. Processing Integrity - Data complete & accurate
4. Confidentiality - Non-public data protected
5. Privacy - Personal data handled per privacy laws
```

**Audit:** Annual external audit (26-33 weeks total)  
**Timeline:** 26-33 weeks (6-8 months) to certification  
**Cost:** $43-70K (with MSO optimization) or $67-108K (without)

---

## 3. THIRD-PARTY AI/ML SERVICES - DPA REQUIREMENTS

### When a DPA is Required

```
If you send data to any third-party service:
✅ Required DPA for:
- OpenAI (ChatGPT, GPT-4, Embeddings)
- Google Vertex AI
- Azure OpenAI
- AWS SageMaker
- Hugging Face APIs
- Any cloud service processing company data

Key Questions:
1. Does the service use my data for model training?
   → If YES = Must opt-out (DPA negotiation)
   
2. Where is the data stored?
   → Must be in approved geography (US/EU)
   
3. How long is data retained?
   → Should be 30 days maximum
   
4. Is my data encrypted in transit?
   → Must be TLS 1.2+
   
5. Does provider have SOC 2 Type II?
   → Helps with compliance but doesn't eliminate application-level requirements
```

### DPA Checklist - Before Sending Data

```
□ Data Classification:
  - What data type (RESTRICTED/CONFIDENTIAL/INTERNAL)?
  - Does it contain PII (names, emails, phone)?
  - Does it contain financial data?

□ Provider Verification:
  - Has SOC 2 Type II certification? (request report)
  - Offers DPA/BAA?
  - Privacy policy reviewed?
  - Data residency documented?

□ Data Handling:
  - Encryption BEFORE sending? (required for sensitive data)
  - Anonymization/PII removal? (best practice)
  - Minimal data transmission? (send only what's needed)
  
□ Legal/Compliance:
  - Company Legal signed off on DPA? ✅ Required
  - Data Processing Agreement executed?
```

---

## 4. QUICK DECISION TREE - WHICH STANDARDS APPLY?

```
START HERE:
│
├─ Do you handle payment card data?
│  ├─ YES → PCI DSS ✅
│  └─ NO → Continue
│
├─ Do you handle financial data for SEC reporting?
│  ├─ YES → SOX ✅ (+ Black Out List required)
│  └─ NO → Continue
│
├─ Is your system enterprise-critical or 50+ users?
│  ├─ YES → SOC 2 Type II ✅
│  └─ NO → Continue
│
├─ Do you use third-party AI with company data?
│  ├─ YES → DPA Required ✅
│  └─ NO → Continue
│
└─ RESULT: Review data classification table above
   (All data = some level of protection needed)
```

---

## 5. IMPLEMENTATION ROADMAP - GENERAL PATTERN

### Phase 1: Assessment (Week 1)
```
□ Identify all data types and classifications
□ Determine which standards apply
□ Document current security controls
□ Identify gaps
□ Estimate effort & budget
```

### Phase 2: Controls (Weeks 2-6)
```
□ Implement missing controls (authentication, encryption, audit logs)
□ Document all policies
□ Create procedures (change management, incident response)
□ Test controls
□ Internal audit/validation
```

### Phase 3: Documentation (Weeks 7-12)
```
□ Create System Security Plan (SSP)
□ Document data flows
□ Evidence collection
□ Policy package assembly
□ Internal review/sign-off
```

### Phase 4: External Audit (Weeks 13-26)
```
□ Select/engage auditor
□ Pre-audit readiness review
□ Auditor testing phase
□ Remediation of findings
□ Final certification
```

---

## 6. CRITICAL CONTROL CHECKLIST - REQUIRED FOR ALL SYSTEMS

```
AUTHENTICATION & ACCESS CONTROL:
□ SSO or federated authentication
□ Multi-factor authentication (MFA) enforced
□ Password policy enforced (12+ chars, complexity)
□ Session timeout (8 hours or less)
□ Role-based access control (RBAC) implemented
□ Regular access reviews (quarterly)

DATA PROTECTION:
□ Encryption at rest (databases, files, backups)
□ Encryption in transit (TLS 1.2+, HTTPS)
□ Field-level encryption for PII/financial data
□ Key management procedures
□ Data masking in non-production environments

AUDIT & LOGGING:
□ All access logged (who, what, when, outcome)
□ All changes logged (code, config, database)
□ Immutable audit logs (append-only, hash chain)
□ PII not logged in plaintext
□ Log retention (7-10 years for SOX)
□ Real-time alerting for anomalies

SEGREGATION OF DUTIES:
□ No person can approve their own changes
□ Development ≠ Production access
□ Code review required before deployment
□ Financial approvals require 2+ people

CHANGE MANAGEMENT:
□ All code changes documented (comments)
□ All changes reviewed by second person
□ Change log maintained
□ Test environment ≠ Production
□ Rollback procedure documented

INCIDENT RESPONSE:
□ Incident response plan written
□ Roles & responsibilities assigned
□ Communication plan documented
□ Legal notification procedure documented
□ Post-incident review process

VENDOR MANAGEMENT:
□ All vendors have signed DPA/BAA
□ Vendor SOC 2 reports obtained/reviewed
□ Vendor security practices documented
□ Regular vendor security reviews (annual)
□ Ability to audit vendor if needed
```

---

## 7. COMMON MISTAKES TO AVOID

```
❌ MISTAKE 1: Treating data as generic
   ✅ FIX: Classify all data (RESTRICTED/CONFIDENTIAL/INTERNAL/PUBLIC)
   
❌ MISTAKE 2: Assuming SOC 2 means no other work needed
   ✅ FIX: SOC 2 documents requirements; you still implement them
   
❌ MISTAKE 3: Using third-party AI without DPA
   ✅ FIX: DPA required before ANY data goes to third-party
   
❌ MISTAKE 4: Encryption planned but not implemented
   ✅ FIX: Implement encryption BEFORE data collection begins
   
❌ MISTAKE 5: Black Out List as data filter (post-login)
   ✅ FIX: Black Out List as login denial (pre-login)
   
❌ MISTAKE 6: Audit logs stored in same database as data
   ✅ FIX: Audit logs in separate, immutable storage
   
❌ MISTAKE 7: No incident response plan
   ✅ FIX: Document procedures before incidents happen
   
❌ MISTAKE 8: Compliance done at end of project
   ✅ FIX: Start compliance planning in Week 1
```

---

## 8. FUTURE PROJECT CHECKLIST

**Use this before starting ANY new project:**

```
□ Step 1: Identify data types (PII, financial, health, etc.)
□ Step 2: Apply decision tree (Section 4)
□ Step 3: Determine required standards
□ Step 4: Create Compliance Determination Report
□ Step 5: Build critical controls (Section 6) from Day 1
□ Step 6: Document architecture & data flows
□ Step 7: If using 3rd-party AI → DPA process
□ Step 8: Plan for audits (internal @ Week 12, external if needed)
□ Step 9: Assign compliance owner
□ Step 10: Include compliance metrics in project planning
```

---

**Document Version History:**
- v1.0 (Jan 14, 2026) - Initial framework based on Activity Hub compliance review

**Next Update:** Quarterly review or after new compliance engagement

