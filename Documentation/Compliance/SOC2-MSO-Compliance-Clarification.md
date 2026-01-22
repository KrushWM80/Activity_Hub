# SOC 2 Type II Compliance with Walmart Managed Service Offerings (MSOs)
**Date:** January 14, 2026  
**Status:** Clarification & Implementation Guidance  
**Focus:** Using Licensed AI Solutions (Azure OpenAI, Google Vertex AI)

---

## EXECUTIVE SUMMARY

Using Walmart's licensed/pre-approved Managed Service Offerings (MSOs) for AI—such as **Azure OpenAI** or **Google Vertex AI**—significantly simplifies SOC 2 Type II compliance but does NOT eliminate the documentation requirement.

**Key Point:** MSOs handle platform-level compliance; you handle application-level compliance.

---

## 1. THE SOC 2 TYPE II LANDSCAPE

### 1.1 What is SOC 2 Type II?

**Definition:** A third-party audit report that verifies a service provider's controls across five dimensions:

| Dimension | Scope | Walmart's Interest |
|-----------|-------|---|
| **Security (CC)** | Access control, encryption, authentication | Protects Walmart data |
| **Availability (A)** | System uptime, redundancy, disaster recovery | Business continuity |
| **Processing Integrity (PI)** | Data accuracy, completeness, timely processing | Data quality assurance |
| **Confidentiality (C)** | Data protection, encryption, access restrictions | Data privacy |
| **Privacy (P)** | Personal data handling, consent, retention | GDPR/regulatory compliance |

### 1.2 Traditional vs. MSO Approach

**Traditional Approach (Without MSO):**
```
Activity Hub Application (YOU BUILD IT ALL)
├── Encryption at rest (build)
├── Encryption in transit (build)
├── Access control (build)
├── Audit logging (build)
├── Disaster recovery (build)
├── Monitoring & alerting (build)
└── SOC 2 audit (external audit firm reviews all 5 dimensions)
```

**MSO Approach (With Azure OpenAI/Google Vertex):**
```
Activity Hub Application (YOU BUILD SOME)
├── Application-level integration (build)
├── Data governance (build)
├── Access control for YOUR app (build)
├── Data classification (build)
└── Platform-level controls (ALREADY PROVIDED by MSO)
    ├── Encryption at rest (Microsoft/Google)
    ├── Encryption in transit (Microsoft/Google)
    ├── Access control at platform level (Microsoft/Google)
    ├── Audit logging (Microsoft/Google)
    ├── Disaster recovery (Microsoft/Google)
    └── SOC 2 Type II audit (Microsoft/Google already certified)
```

---

## 2. WHY MSOs DON'T ELIMINATE SOC 2 REQUIREMENTS

### 2.1 Shared Responsibility Model

When using an MSO, compliance responsibility is **split**:

```
┌─────────────────────────────────────────────────────┐
│          SOC 2 Type II Responsibility Model          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  PLATFORM LEVEL (Microsoft/Google)                 │
│  ├─ ✅ Infrastructure security (encrypted DBs)     │
│  ├─ ✅ Network security (TLS, firewalls)           │
│  ├─ ✅ Physical data center security               │
│  ├─ ✅ Disaster recovery capabilities              │
│  ├─ ✅ SOC 2 Type II certification                 │
│  └─ ✅ Annual third-party audit                    │
│                                                     │
│  APPLICATION LEVEL (YOUR RESPONSIBILITY)           │
│  ├─ ⚠️ How you configure the platform              │
│  ├─ ⚠️ Which data you send to the platform         │
│  ├─ ⚠️ Access controls for your users              │
│  ├─ ⚠️ How you handle the data returned            │
│  ├─ ⚠️ Audit trail for YOUR operations             │
│  ├─ ⚠️ Data classification & handling              │
│  ├─ ⚠️ Encryption of your additional data layers   │
│  └─ ⚠️ Your application's SOC 2 readiness          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2.2 Why Documentation is Still Required

**Reason 1: Compliance Verification Chain**
- Walmart compliance team needs to verify ENTIRE data flow
- Platform SOC 2 only covers platform layer
- Activity Hub's configuration and data handling still need review

**Reason 2: Sensitive Data Classification**
- Even if platform is SOC 2 certified, Walmart needs to know:
  - What data is being processed?
  - Is it encrypted before sending to AI service?
  - What's the retention policy?
  - How is data classified?

**Reason 3: Regulatory Requirements (SOX/PCI/HIPAA)**
- SOC 2 covers security/availability/integrity/confidentiality/privacy
- SOX specifically requires segregation of duties and audit trails (Activity Hub's responsibility)
- PCI has specific encryption key handling requirements (Activity Hub's responsibility)

**Reason 4: Walmart Risk Management**
- Walmart has a duty to verify third-party and application-level controls
- Internal auditors need end-to-end control assessment
- Board reporting requires complete security posture

---

## 3. WHAT DOCUMENTATION YOU NEED

### 3.1 Documentation Checklist

#### For SSP Submission (System Security Plan)

```
PLATFORM-LEVEL COMPLIANCE:
├─ [ ] Azure OpenAI SOC 2 Type II Report (from Microsoft)
│  └─ Location: Obtain from Walmart cloud governance team
│  └─ Format: PDF audit report (usually 50-100 pages)
│  └─ What it proves: Microsoft's controls are certified
│
├─ [ ] Google Vertex AI SOC 2 Type II Report (from Google)
│  └─ Location: Obtain from Walmart cloud governance team
│  └─ What it proves: Google's controls are certified
│
└─ [ ] Data Processor Agreement (DPA) with MSO
   └─ Location: Walmart legal team (usually negotiated)
   └─ What it proves: Data handling responsibilities defined

APPLICATION-LEVEL COMPLIANCE:
├─ [ ] Data Flow Diagram
│  ├─ Where data enters Activity Hub
│  ├─ Which data goes to Azure OpenAI vs. stays internal
│  ├─ Which data goes to Google Vertex vs. stays internal
│  └─ Where data is stored after AI processing
│
├─ [ ] Data Classification Policy
│  ├─ Which fields = RESTRICTED (encrypted)
│  ├─ Which fields = CONFIDENTIAL (encrypted)
│  ├─ Which fields = INTERNAL (encrypted)
│  └─ Justification for each classification
│
├─ [ ] AI Data Handling Procedures
│  ├─ What data is sent to Azure OpenAI? (activity descriptions, KPI metrics)
│  ├─ What data is sent to Google Vertex? (sentiment analysis only)
│  ├─ Is data encrypted before sending? (MUST BE: YES)
│  ├─ What retention policy with MSO? (typically 30 days)
│  ├─ Does MSO use data for model training? (verify: usually NO for enterprise)
│  ├─ Can Walmart delete data from MSO? (verify: usually YES)
│  └─ Is there a DPA covering this? (verify: MUST EXIST)
│
├─ [ ] Encryption at Rest & In Transit
│  ├─ Database encryption enabled? (MUST BE: YES)
│  ├─ TLS 1.3 for API communications? (MUST BE: YES)
│  ├─ Encryption for data before MSO transmission? (MUST BE: YES)
│  ├─ Key management procedures? (documented & audited)
│  └─ Key rotation schedule? (defined & enforced)
│
├─ [ ] Access Control Procedures
│  ├─ Who has access to what data?
│  ├─ How are access rights granted/revoked?
│  ├─ MFA enforcement status?
│  ├─ Role-based access control (RBAC) implemented?
│  ├─ Black Out List for SOX/FINC data?
│  └─ Segregation of duties validated?
│
├─ [ ] Audit Logging & Monitoring
│  ├─ What events are logged?
│  ├─ Log retention period? (7-10 years for compliance)
│  ├─ Are logs immutable? (append-only, no deletion)
│  ├─ Are logs encrypted?
│  ├─ Who has access to logs? (limited to audit team)
│  ├─ Real-time alerting for suspicious activity? (YES/NO)
│  └─ SOX compliance: can logs prove segregation of duties?
│
├─ [ ] Incident Response Plan
│  ├─ What qualifies as a security incident?
│  ├─ Response procedures documented?
│  ├─ Who to notify? (Walmart security team)
│  ├─ Timeline for notification? (typically <4 hours)
│  ├─ Investigation procedures?
│  └─ Root cause analysis process?
│
├─ [ ] Backup & Disaster Recovery
│  ├─ Backup frequency? (daily/hourly)
│  ├─ Backup location? (geographically separate)
│  ├─ Recovery time objective (RTO)? (e.g., 4 hours)
│  ├─ Recovery point objective (RPO)? (e.g., 1 hour)
│  ├─ Backup encryption? (MUST BE: YES)
│  ├─ Restore testing? (quarterly/annual)
│  └─ Backup retention? (7 years for SOX)
│
├─ [ ] Privacy & Consent Procedures
│  ├─ Privacy notice provided to users?
│  ├─ Consent for data processing?
│  ├─ Data retention limits enforced?
│  ├─ Right to access/correction procedures?
│  ├─ Right to deletion (GDPR "right to be forgotten")?
│  └─ Data minimization procedures?
│
└─ [ ] Change Management
   ├─ Change control process documented?
   ├─ Changes tracked in audit trail?
   ├─ Approval workflow for sensitive changes?
   ├─ Testing before production deployment?
   └─ Rollback procedures if needed?
```

### 3.2 Sample SSP Section: AI Usage with MSO

```
SECTION: AI SERVICES & MANAGED SERVICE OFFERINGS

1. AZURE OPENAI USAGE

   1.1 Service Description
   - Activity Hub uses Azure OpenAI for activity description summarization
   - Data sent: Activity titles, descriptions (max 2000 chars)
   - Data NOT sent: PII (emails, names), financial KPIs, confidential communications
   
   1.2 Data Protection
   - Data encrypted in transit using TLS 1.3
   - Data encrypted at rest in Azure (Microsoft-managed encryption keys)
   - Activity Hub encrypts sensitive fields before transmission (double encryption)
   
   1.3 Compliance Documentation
   - Microsoft SOC 2 Type II Report: [ATTACHED]
   - Data Processor Agreement with Walmart: [REFERENCE #]
   - Azure Data Residency: [REGION]
   
   1.4 Access Control
   - Azure OpenAI API key stored in AWS Secrets Manager
   - API key rotated quarterly
   - API calls logged in audit trail
   - Only service account has access to Azure OpenAI
   
   1.5 Data Retention
   - Default: 30 days (per Microsoft policy)
   - Walmart has right to request deletion
   - No data used for model training

2. GOOGLE VERTEX AI USAGE

   2.1 Service Description
   - Activity Hub uses Google Vertex AI for communication sentiment analysis
   - Data sent: Communication content (text only, max 5000 chars)
   - Data NOT sent: PII, sender information, metadata
   
   2.2 Data Protection
   - Data encrypted in transit using TLS 1.3
   - Data encrypted at rest in Google Cloud (Google-managed encryption)
   - Activity Hub masks user identifiers before transmission
   
   2.3 Compliance Documentation
   - Google SOC 2 Type II Report: [ATTACHED]
   - Data Processor Agreement with Walmart: [REFERENCE #]
   - Google Data Residency: [REGION]
   
   2.4 Access Control
   - Google API credentials in AWS Secrets Manager
   - API key rotation: quarterly
   - API calls logged and audited
   - Service account only (no human access)
   
   2.5 Data Retention
   - Default: 30 days (per Google policy)
   - Walmart can request deletion
   - No data used for model training (verified in DPA)

3. ACTIVITY HUB APPLICATION-LEVEL CONTROLS

   3.1 Data Classification Before Sending to MSO
   - [RESTRICTED] data: NOT sent to any external MSO
   - [CONFIDENTIAL] data: Masked/anonymized before sending
   - [INTERNAL] data: Can be sent with encryption
   - [PUBLIC] data: Can be sent without encryption
   
   3.2 Encryption Strategy
   - Database: PostgreSQL with pgcrypto extension (AES-256)
   - Encryption keys: Stored in AWS Secrets Manager
   - Key rotation: Annual + emergency rotation if compromised
   - Backup encryption: Same AES-256 standard
   
   3.3 Access Control
   - RBAC with 8 role types
   - MFA enforcement: Yes (for admin roles)
   - SOX Black Out List: Implemented at login
   - Segregation of duties: Enforced via approval workflows
   
   3.4 Audit Logging
   - All API calls logged
   - MSO API calls logged with request/response hash
   - Audit logs: Immutable, 10-year retention
   - Log encryption: AES-256
   
   3.5 Incident Response
   - Security team alerted in real-time
   - Incidents categorized by severity
   - Root cause analysis within 48 hours
   - Notification to Walmart InfoSec within 4 hours of critical events
   
CONCLUSION: While Azure OpenAI and Google Vertex AI are SOC 2 Type II certified
at the platform level, Activity Hub maintains its own SOC 2 readiness through
application-level controls and secure integration practices.
```

---

## 4. WHERE TO GET MSO COMPLIANCE DOCUMENTATION

### 4.1 Obtaining SOC 2 Reports

| MSO | Where to Get SOC 2 Report | Contact |
|-----|---|---|
| **Azure (Microsoft)** | Walmart cloud governance team | cloud-governance@walmart.com |
| | OR Microsoft Customer Portal | https://servicetrust.microsoft.com |
| | (Requires Walmart Azure account) | |
| **Google Cloud** | Walmart cloud governance team | cloud-governance@walmart.com |
| | OR Google Cloud Security Command Center | https://cloud.google.com/security |
| | (Requires Walmart GCP account) | |
| **AWS** | Walmart cloud governance team | cloud-governance@walmart.com |
| | OR AWS Artifact Portal | https://aws.amazon.com/artifact |
| | (If Activity Hub uses AWS infrastructure) | |

### 4.2 Obtaining Data Processor Agreements (DPAs)

```
Process:
1. Contact Walmart Legal/InfoSec
   Email: walmart-legal@walmart.com

2. Request Data Processor Agreement
   Specify: Azure OpenAI, Google Vertex AI, or specific service
   Provide: Data types to be processed, retention requirements

3. MSO Completes Agreement
   Typical turnaround: 2-4 weeks

4. Walmart Legal Reviews
   Verify: Data protection obligations, subprocessor rights, audit rights

5. Execute & Archive
   Store in: Compliance documentation repository
   Reference in: SSP submission
```

### 4.3 What to Ask MSO Before Using

**Before deploying Activity Hub with any MSO, verify:**

```
SECURITY QUESTIONS:
□ Is this service SOC 2 Type II certified? (must be YES)
□ Can you provide current audit report? (must be available)
□ What encryption do you provide at rest? (must be AES-256+)
□ What encryption in transit? (must be TLS 1.2+)
□ Do you encrypt with customer-managed keys or MSO-managed? (either OK, must be specified)

DATA HANDLING QUESTIONS:
□ Do you use customer data for model training? (must be NO for sensitive data)
□ Can Walmart request data deletion? (must be YES)
□ What's your default data retention? (typically 30 days, must be defined)
□ Can we specify different retention? (should be YES)
□ Can we restrict data to specific geographic regions? (should be YES)

COMPLIANCE QUESTIONS:
□ Do you have Data Processor Agreement (DPA)? (must be YES)
□ Do you support GDPR data subject rights? (must be YES)
□ Can you sign Walmart's MSA/DPA? (must be YES)
□ Do you provide audit trail/logs of API access? (must be YES)
□ Can you support SOX compliance needs? (must be YES)

ACCESS & AUDIT QUESTIONS:
□ Who has access to Walmart data? (should be: only you, no MSO staff)
□ Can Walmart audit your controls? (should be YES)
□ Do you provide audit logs? (should be: yes, detailed)
□ API rate limiting available? (should be YES)
□ Can you disable API access if needed? (should be YES)
```

---

## 5. RISK MITIGATION WITH MSOs

### 5.1 Reduced Risk Areas (MSO Handles)

| Risk | Traditional Approach | MSO Approach |
|------|---|---|
| **Infrastructure Security** | 🔴 You build from scratch | ✅ MSO already certified |
| **Physical Data Center Security** | 🔴 You outsource to cloud provider | ✅ MSO handles (SOC 2 proven) |
| **Encryption at Platform Level** | 🔴 You implement & maintain | ✅ MSO handles (SOC 2 proven) |
| **Disaster Recovery** | 🔴 You design & test | ✅ MSO handles (SOC 2 proven) |
| **Platform Availability/SLA** | 🔴 You guarantee uptime | ✅ MSO guarantees (99.9%+) |
| **Platform Audit Compliance** | 🔴 You undergo SOC 2 audit | ✅ MSO already certified |

### 5.2 Remaining Risk Areas (You Still Responsible)

| Risk | MSO Approach | Your Responsibility |
|------|---|---|
| **Data Classification** | MSO agnostic | You decide what to send |
| **Pre-MSO Encryption** | MSO provides encryption | You encrypt sensitive data BEFORE sending |
| **Access Control to MSO** | MSO provides API keys | You manage API key security |
| **Application-Level Controls** | MSO doesn't control | You implement RBAC, audit trails, etc. |
| **Data Retention Policy** | MSO provides default | You enforce company policy |
| **Incident Response** | MSO provides logs | You detect & respond to incidents |
| **SOX Segregation of Duties** | MSO doesn't enforce | You implement in Activity Hub |
| **User Access Management** | MSO provides API authentication | You manage user access to Activity Hub |

---

## 6. IMPLEMENTATION CHECKLIST: USING MSO WITH SOC 2 COMPLIANCE

### Phase 1: MSO Selection & Agreement (Week 1-2)

- [ ] Decision: Azure OpenAI vs. Google Vertex AI vs. other
- [ ] Request MSO's current SOC 2 Type II report from Walmart
- [ ] Contact Walmart Legal for DPA template/negotiation
- [ ] Verify MSO's data retention & deletion policies
- [ ] Verify no data used for model training without consent
- [ ] Execute DPA and archive

### Phase 2: SSP Documentation (Week 3-4)

- [ ] Document data flows: what goes to MSO, what stays internal
- [ ] Create data classification policy
- [ ] Document encryption strategy (pre-MSO + in transit)
- [ ] Document access control procedures for MSO API
- [ ] Document audit logging for MSO API calls
- [ ] Reference MSO's SOC 2 Type II report in SSP

### Phase 3: Implementation (Week 5-6)

- [ ] Implement encryption of sensitive data before MSO transmission
- [ ] Implement MSO API key rotation (quarterly)
- [ ] Add logging for all MSO API calls
- [ ] Implement audit trail for MSO data handling
- [ ] Implement data anonymization/masking before transmission
- [ ] Document MSO service credentials in secure vault

### Phase 4: Validation & Testing (Week 7-8)

- [ ] Security review of MSO integration
- [ ] Test data encryption before MSO transmission
- [ ] Verify MSO DPA compliance
- [ ] Test incident response with MSO data
- [ ] Audit log verification
- [ ] Compliance team sign-off

### Phase 5: Ongoing Monitoring (Continuous)

- [ ] Annual MSO SOC 2 report review
- [ ] Quarterly API key rotation
- [ ] Monitor for MSO security incidents
- [ ] Maintain incident response procedures
- [ ] Document any MSO policy changes

---

## 7. SAMPLE MSO INTEGRATION: AZURE OPENAI

### 7.1 Code Example with Compliance Comments

```python
# app/services/azure_openai_service.py
import os
import json
import logging
from azure.openai import AzureOpenAI
from cryptography.fernet import Fernet
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class AzureOpenAIService:
    """
    Service for integrating Azure OpenAI with SOC 2 compliance
    
    Compliance Controls:
    1. Encryption of sensitive data BEFORE sending to Azure
    2. Audit logging of all API calls
    3. Data anonymization of PII
    4. Secure credential management (AWS Secrets Manager)
    """
    
    def __init__(self):
        # COMPLIANCE: Load API key from secure vault (not hardcoded)
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")  # From AWS Secrets Manager
        self.api_version = "2024-02-15"
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.encryption_key = os.getenv("DATA_ENCRYPTION_KEY")  # For pre-MSO encryption
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    def summarize_activity(self, activity_id: int, activity_text: str) -> str:
        """
        Summarize activity using Azure OpenAI
        
        COMPLIANCE: 
        1. Anonymize PII before sending to Azure
        2. Encrypt sensitive data
        3. Log API call for audit trail
        """
        
        try:
            # Step 1: Data Classification & Anonymization
            # Remove any PII from activity text
            anonymized_text = self._anonymize_pii(activity_text)
            
            # Step 2: Encryption (optional but recommended for sensitive data)
            if self._is_sensitive_data(activity_text):
                # COMPLIANCE: Encrypt before sending to Azure
                encrypted_data = self._encrypt_data(anonymized_text)
                logger.info(
                    "sensitive_data_encrypted_before_azure",
                    activity_id=activity_id,
                    data_classification="CONFIDENTIAL"
                )
            else:
                encrypted_data = anonymized_text
            
            # Step 3: Call Azure OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes store activities."},
                    {"role": "user", "content": f"Summarize: {anonymized_text}"}
                ],
                max_tokens=200
            )
            
            summary = response.choices[0].message.content
            
            # Step 4: Audit Logging (COMPLIANCE - SOC 2 Control)
            self._log_api_call(
                activity_id=activity_id,
                operation="summarize",
                input_hash=hashlib.sha256(anonymized_text.encode()).hexdigest(),
                output_hash=hashlib.sha256(summary.encode()).hexdigest(),
                data_classification="CONFIDENTIAL",
                pii_anonymized=True,
                encryption_used=self._is_sensitive_data(activity_text),
                api_endpoint="azure_openai.chat.completions.create",
                timestamp=datetime.utcnow().isoformat(),
                request_id=response.id
            )
            
            logger.info(
                "azure_openai_api_call_successful",
                activity_id=activity_id,
                api_request_id=response.id
            )
            
            return summary
            
        except Exception as e:
            logger.error(
                "azure_openai_api_call_failed",
                activity_id=activity_id,
                error=str(e)
            )
            # Log failure for audit trail
            self._log_api_call(
                activity_id=activity_id,
                operation="summarize",
                status="failed",
                error_message=str(e)
            )
            raise
    
    def _anonymize_pii(self, text: str) -> str:
        """
        COMPLIANCE: Remove PII before sending to Azure
        """
        import re
        
        # Remove email addresses
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL]', text)
        
        # Remove phone numbers
        text = re.sub(r'\d{3}-\d{3}-\d{4}', '[PHONE]', text)
        
        # Remove store numbers (5-6 digits)
        text = re.sub(r'\b\d{4,5}\b', '[STORE_ID]', text)
        
        return text
    
    def _is_sensitive_data(self, text: str) -> bool:
        """Determine if data should be encrypted before sending to Azure"""
        # Keywords that indicate sensitive data
        sensitive_keywords = ['financial', 'budget', 'salary', 'confidential', 'private']
        return any(keyword in text.lower() for keyword in sensitive_keywords)
    
    def _encrypt_data(self, data: str) -> str:
        """COMPLIANCE: Encrypt data before sending to external service"""
        cipher = Fernet(self.encryption_key.encode())
        encrypted = cipher.encrypt(data.encode())
        return encrypted.decode()
    
    def _log_api_call(self, **kwargs):
        """
        COMPLIANCE: Log all Azure OpenAI API calls for audit trail
        This is critical for SOC 2 audit evidence
        """
        audit_log = {
            "service": "azure_openai",
            "timestamp": kwargs.get("timestamp", datetime.utcnow().isoformat()),
            "activity_id": kwargs.get("activity_id"),
            "operation": kwargs.get("operation"),
            "input_hash": kwargs.get("input_hash"),  # Don't log actual input (privacy)
            "output_hash": kwargs.get("output_hash"),  # Hash for integrity verification
            "data_classification": kwargs.get("data_classification"),
            "pii_anonymized": kwargs.get("pii_anonymized", False),
            "encryption_used": kwargs.get("encryption_used", False),
            "api_endpoint": kwargs.get("api_endpoint"),
            "request_id": kwargs.get("request_id"),
            "status": kwargs.get("status", "success"),
            "error_message": kwargs.get("error_message")
        }
        
        # Log to audit trail (this gets stored in immutable audit log table)
        logger.info(json.dumps(audit_log))
        
        # Also store in database for compliance reporting
        # self.db.add(AuditLog(**audit_log))
        # self.db.commit()
```

---

## 8. COMPLIANCE CHECKLIST: MSO + SOC 2 TYPE II

```
BEFORE DEPLOYMENT:
─────────────────
□ MSO's SOC 2 Type II report obtained & reviewed
□ Data Processor Agreement (DPA) signed
□ Data classification policy defined (what goes to MSO)
□ Encryption strategy documented
□ Access control procedures documented
□ Audit logging procedures documented
□ Data retention policy documented
□ Incident response procedures documented
□ MSO credentials stored in secure vault

DURING IMPLEMENTATION:
─────────────────────
□ Pre-MSO encryption implemented for sensitive data
□ Audit logging for all MSO API calls
□ PII anonymization/masking implemented
□ API key rotation procedure implemented (quarterly)
□ Data retention enforcement implemented
□ Secure credential management implemented
□ Incident response tested with MSO data

AFTER DEPLOYMENT:
─────────────────
□ Security review completed & approved
□ Compliance team sign-off obtained
□ SSP updated with MSO compliance documentation
□ MSO SOC 2 report added to compliance folder
□ DPA filed and referenced
□ Audit logging validated
□ Documentation prepared for auditor review

ONGOING:
────────
□ Annual MSO SOC 2 report review
□ Quarterly API key rotation
□ Monthly audit log review for anomalies
□ Incident response procedures tested
□ Compliance documentation updated annually
□ Audit evidence collected continuously
```

---

## SUMMARY: MSO DOES NOT ELIMINATE SOC 2 COMPLIANCE

| Statement | Reality |
|-----------|---------|
| "MSO has SOC 2, so we're done" | ❌ FALSE - MSO covers platform, not your app |
| "MSO SOC 2 replaces our SOC 2" | ❌ FALSE - Different scopes |
| "We don't need to document anything" | ❌ FALSE - You need to document your layer |
| "We can send any data to MSO" | ❌ FALSE - Classify & protect first |
| "Auditors won't ask for SOC 2" | ❌ FALSE - Likely will (just easier to provide) |
| "MSO handles all compliance" | ❌ FALSE - Shared responsibility |
| **"MSO simplifies SOC 2 compliance"** | ✅ **TRUE - Platform layer already proven** |
| **"We still need SSP & documentation"** | ✅ **TRUE - For your application layer** |
| **"MSO SOC 2 is supporting evidence"** | ✅ **TRUE - Shows platform is secure** |

---

## NEXT STEPS

1. **Obtain MSO SOC 2 Report**
   - Contact Walmart cloud governance
   - Timeline: 1 week

2. **Negotiate DPA**
   - Contact Walmart Legal
   - Timeline: 2-4 weeks

3. **Update SSP with MSO Information**
   - Document data flows to MSO
   - Reference MSO's SOC 2 Type II
   - Timeline: 1 week

4. **Implement Application-Level Controls**
   - See code examples above
   - Timeline: 2-3 weeks

5. **Compliance Review & Sign-Off**
   - Internal compliance team review
   - Timeline: 1 week

---

**Recommendation:** Using Walmart's pre-approved MSOs significantly reduces compliance burden and accelerates SOC 2 readiness. However, still plan for 8-12 weeks to full certification due to application-level requirements and audit process.

