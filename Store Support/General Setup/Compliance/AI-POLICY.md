# AI Policy - Enterprise Guidelines
**Version:** 1.0  
**Effective Date:** January 14, 2026  
**Owner:** CISO / Compliance Officer

---

## 1. Policy Overview

This policy establishes enterprise-wide guidelines for the safe, secure, and compliant use of Artificial Intelligence (AI), Machine Learning (ML), and Large Language Models (LLMs) across Walmart's technology systems.

### Scope

This policy applies to:
- All developers, engineers, and architects
- All projects using AI/ML services
- All third-party AI integrations (OpenAI, Google Vertex AI, Azure AI, etc.)
- All systems processing company data with AI

### Purpose

To ensure that AI usage complies with:
- Data protection regulations (SOX, SOC 2, GDPR, CCPA)
- Company data classification standards
- Intellectual property protection requirements
- Ethical AI principles

---

## 2. Key Principles

### Principle 1: Data Classification Before AI Usage

**Rule:** Only classified data can be processed by AI services

```
Classification Level → Can Use AI? → Requirements
─────────────────────────────────────────────────────
RESTRICTED (Financial)  ❌ NO            Don't use AI
CONFIDENTIAL           🟡 CONDITIONAL   Encryption required
INTERNAL               ✅ YES           Normal safeguards
PUBLIC                 ✅ YES           No restrictions
```

### Principle 2: Data Processing Agreement (DPA) Required

**Rule:** Every third-party AI service MUST have a signed DPA before use

```
Before Using Any AI Service:
□ Obtain DPA from vendor
□ Get Legal/Compliance approval
□ Confirm encryption standards
□ Verify data retention limits
□ Confirm opt-out from model training
```

### Principle 3: Data Minimization

**Rule:** Send only the minimum data needed to AI services

```
Example - Activity Summarization:
❌ DON'T send: Full activity record with all PII
✅ DO send: Anonymized activity text (no names/emails)

Example - Sentiment Analysis:
❌ DON'T send: Store names, manager names, customer data
✅ DO send: Text only (activity/comment text)
```

### Principle 4: Encryption in Transit

**Rule:** All data sent to AI services MUST be encrypted

```
Implementation:
1. Classify data sensitivity
2. If CONFIDENTIAL+: Encrypt before API call
3. Use AES-256 encryption
4. Manage encryption key in AWS Secrets Manager
5. Log: Audit trail of all transmissions
```

### Principle 5: No Training Data Opt-In (Default)

**Rule:** Vendors must agree that Walmart data is NOT used for model training

```
MSO Requirement:
☑ Service will NOT use our data for model training
☑ Our data will NOT improve their models
☑ We have right to audit data usage
☑ Verified in DPA before contract signing
```

### Principle 6: Data Retention Limits

**Rule:** AI vendors must delete data after processing

```
Standard Retention:
- Azure OpenAI: 30 days (approved by default)
- Google Vertex AI: 30 days (approve by default)
- Others: Must negotiate to 30 days maximum
```

### Principle 7: Audit Logging Mandatory

**Rule:** Every AI API call must be logged

```
What to Log:
✅ User making the request
✅ Timestamp
✅ What data was sent (sanitized)
✅ API response status
✅ Time taken
✅ Any errors
```

### Principle 8: Human Review Required for Sensitive Use Cases

**Rule:** AI outputs used for financial decisions require human review

```
Sensitive Use Cases (Require Review):
- Financial forecasting
- Budget recommendations
- Performance-based decisions
```

---

## 3. Prohibited Uses of AI

```
❌ PROHIBITED:

1. Processing financial data without encryption
2. Processing health information (HIPAA data)
3. Using AI to replace human judgment in decisions
4. Sending unencrypted PII to vendors
5. Using vendors without signed DPA
6. Training models on company data
7. Sending trade secrets to AI
8. Automated decisions without human oversight
9. Using AI without auditing
10. Using unapproved AI vendors
```

---

## 4. Approved AI Vendors

### Approved MSOs (Managed Service Operators)

```
For Activity Summarization:
✅ Azure OpenAI (Microsoft)
   - SOC 2 Type II: ✅ Yes
   - Approved for: Activity summarization, sentiment analysis
   - DPA: ✅ Signed
   - Data Retention: 30 days

✅ Google Vertex AI
   - SOC 2 Type II: ✅ Yes
   - Approved for: Activity summarization, sentiment analysis
   - DPA: ✅ Signed (pending)
   - Data Retention: 30 days
```

---

## 5. DPA Requirements Checklist

**Before Using ANY AI Service, Verify:**

```
Security & Compliance:
□ Vendor has SOC 2 Type II certification (or equivalent)
□ Vendor provides current SOC 2 report (annual)
□ Vendor has data processing agreement available
□ Vendor uses AES-256 encryption at minimum
□ Vendor commits to TLS 1.2+ for data in transit

Data Handling:
□ Our data is NOT used for vendor model training
□ Our data is NOT used to improve vendor's service
□ Data is deleted after 30 days (or less)
□ Walmart can audit data usage (right to audit)
□ Walmart can request data deletion

Geographic & Legal:
□ Data stored in US or EU only
□ Vendor complies with US data protection laws
□ Vendor not subject to unauthorized seizure
□ Vendor has DPA addendum if subpoenaed
```

---

## 6. Approval & Accountability

### Policy Approval

```
□ CISO: _________________________ Date: _____
□ Chief Compliance Officer: _____ Date: _____
□ Legal/Privacy: ________________ Date: _____
□ Executive Sponsor: ____________ Date: _____
```

---

**Questions? Contact:** CISO@walmart.com or Compliance Officer

