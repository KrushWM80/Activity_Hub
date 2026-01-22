# Data Classification Assessment - Activity Hub
**Date:** January 22, 2026  
**Status:** APPROVED & LOCKED  
**Last Updated:** January 22, 2026

---

## Assessment Summary

| Category | Count | Status |
|----------|-------|--------|
| YES Answers | 8 | Required Classification |
| NO Answers | 14 | Non-Applicable |
| **Classification Level** | **CONFIDENTIAL** | Requires SOX & Security Controls |

---

## Detailed Responses

### Question 1: Collect/Process/Store/Transmit PII?
**Answer: YES**  
**Reasoning:** Activity Hub collects and stores PII including:
- Associate names, emails, user IDs
- Organizational positions and assignments
- Manager relationships and reporting structure
- Last login timestamps and access audit trails

**Data Elements:** Name, Email, UserID, Org Position, Manager Identity

---

### Question 2: Real-Time GPS/Location Tracking?
**Answer: NO**  
**Reasoning:** Activity Hub does not collect real-time GPS data or similar technology. Only static information is used:
- Store numbers (identifiers, not location data)
- Store physical addresses (static, not tracked)
- Geographic regions for organizational structure

---

### Question 3: Government Issued Identifiers?
**Answer: NO**  
**Reasoning:** Activity Hub does not directly collect or process government-issued identifiers (SSN, passport numbers, driver's license numbers, etc.)

---

### Question 4: Personal Demographic Elements?
**Answer: NO**  
**Reasoning:** Activity Hub does not collect ethnicity, religion, sexual orientation, gender identity, or children's data.

---

### Question 5: Biometric Data or Video/Photo Processing?
**Answer: NO**  
**Reasoning:** Activity Hub does not involve:
- Facial recognition
- Fingerprint analysis
- Voice recognition
- Iris/retina scanning
- Computer processing of video or photo data

---

### Question 6: Investigative or HR Data?
**Answer: YES**  
**Reasoning:** Activity Hub processes HR data through daily synchronization with Walmart HR systems:
- Employee organizational assignments (current and historical)
- Manager relationships (current and historical)
- Role changes and assignments (SOX-tracked for audit trail)
- Position titles and classifications
- Org unit hierarchies

**Data Elements:** Employment history, manager relationships, role assignments, position information

---

### Question 7: Scope of Healthcare/Insurance Entities?
**Answer: NO**  
**Reasoning:** Activity Hub is designed for store operations and project management. It does not fall within the scope of:
- Walmart.com Rx
- SamsClub.com Rx
- Walmart Health
- Patient Safety Office
- Benefits administration
- Insurance services

---

### Question 8: Health Information/Data?
**Answer: NO**  
**Reasoning:** Activity Hub is not a healthcare application and does not collect or process:
- Patient names or identifiers
- Medical history
- Diagnoses
- Prescriptions
- Treatment information
- Health records

---

### Question 9: Credit Card Numbers (PAN)?
**Answer: NO**  
**Reasoning:** Activity Hub does not collect, process, or store:
- Debit card numbers
- Credit card numbers
- Card security codes (CVV)
- Any payment card data

---

### Question 10: Card Magnetic Stripe/Chip Data?
**Answer: NO**  
**Reasoning:** Activity Hub does not interact with credit/debit card payment systems or data from card magnetic stripes or chips.

---

### Question 11: PCI Encryption Keys/Secrets?
**Answer: NO**  
**Reasoning:** Activity Hub is not a PCI-compliant payment system and does not directly handle PCI encryption keys. However, note:
- Database encryption keys are managed separately (not part of this assessment)
- API keys for internal integrations are credentials (not PCI-specific)

---

### Question 12: PCI Passwords/Auth Factors?
**Answer: NO**  
**Reasoning:** Activity Hub is not a PCI system. While Activity Hub may use passwords for internal authentication, this question specifically refers to PCI system components, which does not apply.

---

### Question 13: Replace/Integrate with SOX Systems?
**Answer: YES**  
**Reasoning:** Activity Hub is subject to SOX compliance controls:
- Development roadmap explicitly includes "SOX Controls Hardening" (Phase 3)
- Contains segregation of duties requirements
- Maintains audit trails for all data changes
- Tracks role history for SOX compliance
- Requires approval workflows for sensitive operations
- Includes access controls and logging per SOX requirements

**Impact:** All changes must be audited and documented per SOX requirements.

---

### Question 14: Initiate/Authorize/Create Financial/Transactional Data?
**Answer: NO** *(Clarified from YES)*  
**Reasoning:** Activity Hub does NOT directly initiate, authorize, or create financial transactions:
- Activity Hub tracks and reports on projects with budget allocations
- Budget data is informational/coordination (not authorization or initiation)
- Financial transactions occur in other systems (procurement, payroll, accounting)
- Activity Hub provides visibility into budgeted amounts but does NOT process payments or create GL entries
- No direct impact to financial systems or transaction processing

**Note:** Budget information is reported within Activity Hub, but the financial authorization and processing happens in separate financial systems.

---

### Question 15: Access/Process/Disclose Financial Records?
**Answer: YES**  
**Reasoning:** Activity Hub processes and displays financial information:
- Project budget allocations and tracking
- Financial impact assessments for store operations
- Budget reporting and disclosure to project stakeholders
- Timeline and financial planning data visible to authorized users

**Data Elements:** Budget amounts, financial allocations, cost tracking

---

### Question 16: Transactions Exceed USD 250 Million?
**Answer: NO** *(Clarified from YES)*  
**Reasoning:** Activity Hub is NOT a transaction processing system:
- Does not process individual transactions
- Does not authorize payments or financial transfers
- Reports on project budgets but does not execute financial transactions
- Budget amounts within projects may total significant sums, but Activity Hub itself does not transact or move funds
- This question refers to transaction processing capability, which Activity Hub does not have

---

### Question 17: Impact Business Processes?
**Answer: NO** *(Clarified from YES)*  
**Reasoning:** Activity Hub provides coordination and visibility but does NOT directly impact or change core business processes:
- **Reporting:** Activity Hub reports on projects and activities (no direct system changes)
- **Visibility:** Provides coordination across teams (no direct transaction creation)
- **Visibility into:**
  - Accounts Receivable processes (reports only, doesn't create AR entries)
  - Accounts Payable processes (reports only, doesn't create AP entries)
  - Inventory management (reports only, doesn't change inventory)
  - Payroll (reports on project staff, doesn't process payroll)
  - Procure 2 Pay (reports on projects, doesn't create POs)
  - Sales (reports on sales support projects, doesn't create orders)

**Note:** Activity Hub coordinates information flow but is NOT the system that directly initiates, authorizes, or changes these processes. That happens in their respective source systems.

---

### Question 18: Proprietary Institutional Information?
**Answer: YES**  
**Reasoning:** Activity Hub stores and processes proprietary institutional information:
- **Proprietary Ways of Working:** Stores strategic operational approaches and methodologies being developed for stores
- **Product Development:** Tracks new product launches, pilot programs, and operational strategies
- **Institutional Knowledge:** Confidential project information, strategic initiatives, and ways of working not disclosed externally
- **Strategic Data:** Store support strategies, operational approaches, and business process innovations

**NOT about:** Passwords or authentication factors are managed separately in credential management systems, not within Activity Hub.

**Data Elements:** Strategic project information, proprietary operational methodologies, product launch plans, confidential store strategies

---

### Question 19: Confidential Business Information?
**Answer: YES**  
**Reasoning:** Activity Hub collects and stores confidential business information:
- Strategic store initiatives and operational strategies
- New product rollouts and launch plans
- Planned changes to business processes
- Operational forecasting and planning data
- Financial forecasting and budget allocations
- Competitive and strategic initiatives

**Data Elements:** Strategic initiatives, operational plans, financial forecasts, new program information

---

### Question 20: ONLY Publicly Available Information?
**Answer: NO**  
**Reasoning:** Activity Hub is an internal Walmart system with restricted access. It processes:
- Confidential operational strategies (not public)
- Internal employee information (not public)
- Strategic project information (not public)
- Financial and budget data (not public)

All information in Activity Hub is internal and confidential.

---

### Question 21: Authoritative Official Business Records?
**Answer: YES**  
**Reasoning:** Activity Hub serves as a system of record:
- **Single Source of Truth:** For project data across all integrated platforms
- **Authoritative Source:** For project status, timelines, and assignments
- **Official Record:** For activity and work coordination across Walmart store operations
- **Audit Trail:** Maintains official record of all changes for compliance

This is the authoritative record for project management across the Activity Hub ecosystem.

---

### Question 22: Third-Party Hosted Content?
**Answer: YES**  
**Reasoning:** Activity Hub includes third-party hosted content:
- **Frontend:** React framework and NPM packages (third-party JavaScript libraries)
- **Messaging Integration:** Teams Bot and Slack Bot APIs (Microsoft and Slack hosted)
- **Services:** External API integrations for platform connections
- **CDN:** Any hosted assets served through CDN providers

---

## Data Classification Level: **CONFIDENTIAL**

Based on the responses above, Activity Hub is classified as handling **CONFIDENTIAL** information and is subject to:

✓ PII protection requirements  
✓ SOX compliance controls  
✓ HR data protection  
✓ Financial data security  
✓ Proprietary information protection  
✓ Encryption and access controls  
✓ Audit logging  
✓ Change management and approval workflows  

---

## Approval & Governance

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Review | PrivacyPIA@walmart.com | 01/22/2026 | Pending |
| Compliance | SOX Compliance Team | 01/22/2026 | Pending |
| Application Owner | [To be assigned] | 01/22/2026 | Pending |

---

**Assessment Status:** LOCKED FOR REFERENCE  
**Effective Date:** January 22, 2026  
**Next Review:** As triggered by feature changes (see: CHANGE CONTROL GOVERNANCE)

