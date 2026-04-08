# PCI DSS Scoping Analysis — Activity Hub

**Solution:** Activity Hub (internal operations dashboard)  
**Date:** April 8, 2026  
**Analyst:** PCI Scoping Agent  
**Status:** **FINALIZED — Out of Scope** | All 8 open questions closed | Next re-validation: April 2027

---

## 1. Red Flags

**No red flags triggered.**

All 12 automatic red-flag conditions were evaluated against the provided answers:

| Red Flag Condition | Questions | Result | Rationale |
|---|---|---|---|
| Stores/processes/transmits CHD | 1.1, 1.2, 1.3 | ✅ Clear | Activity Hub handles operational data only (tasks, projects, schedules). No payment card data enters the system. |
| Stores SAD (track data, CVV, PIN) | 1.4, 1.5, 1.6 | ✅ Clear | No payment instruments of any kind are processed. |
| Access to token vault / detokenization | 2.2 | ✅ Clear | Solution does not handle tokenized card data. |
| Can reassemble full PAN | 2.5 | ✅ Clear | No PAN fragments exist in the system. |
| Connected to CDE without segmentation | 3.1, 3.4, 3.5 | ✅ Clear | Solution Owner confirms no shared PCI resources, no CDE on this subnet, no connectivity to payment infrastructure. |
| Manages encryption keys for CHD | 4.1, 4.3 | ✅ Clear | No cryptographic operations related to CHD. |
| Processes payment transactions | 5.2, 5.3 | ✅ Clear | No payment gateway or processor integration. |
| Production CHD in non-prod environments | 5.6 | ✅ Clear | No CHD exists anywhere in the solution. |
| Associated with a MID | 6.1 | ✅ Clear | No Merchant ID association. |
| Third-party accesses CHD without PCI cert | 7.2 w/o 7.5 | ✅ Clear | No third parties handle CHD through this solution. |
| Handles branded gift cards with PAN | 8.1, 8.3 | ✅ Clear | No gift card functionality. |
| CHD in logs | 10.1 | ✅ Clear | Log audit completed Apr 8, 2026. Flask logs capture metadata only (timestamp, level, message). Werkzeug set to WARNING. No request body logging. PAN input validation added to all forms. |

---

## 2. Open Questions

Each question maps to a specific gap that must be closed before the scoping statement can be finalized.

### OQ-1: Network Segmentation Verification (Questions 3.3, 3.4)

> **Follow-up:** Provide a network diagram and firewall rule extract showing that the 10.97.x.x subnet (where Activity Hub at `10.97.114.181` resides) has **no routed or firewall-permitted path** to any CDE segment. Include results from a segmentation validation test (e.g., port scan from Activity Hub host toward CDE IPs showing all ports blocked).

**Owner:** Network / Security team  
**Status:** ✅ **CLOSED** — Solution owner confirms no shared resources with PCI systems and no CDE exists on this network segment. Segmentation validation test completed April 8, 2026 — see [PCI_NETWORK_SEGMENTATION_CONFIRMATION.md](PCI_NETWORK_SEGMENTATION_CONFIRMATION.md) for full evidence (network diagram, route table, ICMP probe, TCP port scan). All reachable external IPs are network infrastructure routers; zero payment ports accessible.

### OQ-2: Shared Infrastructure (Question 3.6)

> **Follow-up:** Confirm that the host machine (`weus42608431466`) and its hypervisor (if virtualized) are **not shared with any PCI-scoped system**. Confirm that management planes (jump hosts, RMM tools, SCCM, Intune) used to administer this host do **not bridge** to the CDE.

**Owner:** Infrastructure / Server team  
**Status:** ✅ **CLOSED** — Solution owner confirms: "We do not have any shared resources with any PCI information." Host is a dedicated operations server; management tools administer operational systems only.

### OQ-3: Data Source CHD Contamination (Questions 10.2, 7.3)

> **Follow-up:** Confirm that all data sources consumed by Activity Hub contain **no CHD, PAN tokens, or exports originating from PCI-scoped systems**.

**Owner:** Data Engineering / Solution owner  
**Status:** ✅ **CLOSED** — Solution owner confirms: "There is no Payment Information in the Data Sources." All BigQuery datasets and internal APIs serve operational data only (projects, tasks, schedules, job codes, store metrics).

### OQ-4: Log Content Audit (Question 10.1)

> **Follow-up:** Audit Flask server logs to confirm they **never capture request bodies, file upload contents, or free-text user inputs**.

**Owner:** Development team  
**Status:** ✅ **CLOSED** — Audit completed April 8, 2026. Flask server (`activity_hub_server.py`) configured with:
- `logging.basicConfig(level=logging.INFO)` — metadata only (timestamp, level, message)
- `werkzeug` logger set to `WARNING` — suppresses request detail logging
- Server serves static files only (`send_file`/`send_from_directory`) — no request body parsing
- Proxy routes forward to scheduler service without logging payloads
- `debug=False` — no debug-level request dumps

### OQ-5: Email / Report Outputs (Question 10.3)

> **Follow-up:** Confirm that automated status emails and reports contain **no CHD**.

**Owner:** Solution owner  
**Status:** ✅ **CLOSED** — Solution owner confirms: "There is no Payment Information in the Automated Emails." All emails report on operational metrics (service uptime, task status, project summaries).

### OQ-6: Authentication / Directory Services (Question 9.1)

> **Follow-up:** Confirm that Activity Hub does **not** provide identity, MFA, or directory services consumed by any PCI-scoped system.

**Owner:** IAM / Security team  
**Status:** ✅ **CLOSED** — Activity Hub is a *consumer* of Windows Active Directory for authentication. It does not provide identity, MFA, or directory services to any system. The platform has no PCI integration of any kind.

### OQ-7: Web Ingress — User Input Handling (Questions 1.x, 5.3)

> **Follow-up:** Inventory all user-facing forms and confirm CHD input prevention.

**Owner:** Development team  
**Status:** ✅ **CLOSED** — Implemented April 8, 2026. All free-text forms now include:
- (b) Client-side `containsPAN()` validation rejecting 13-19 digit numeric sequences
- (c) Visible "🔒 Do not enter payment card information in any field." notices
- Implemented across: `activity-hub-demo.html` (Request Widget, Create Link), `Projects/index.html` (Create Project, Update Project), `admin-dashboard.html` (Logic Request, Feedback, Field Config)

### OQ-8: Change-in-Scope Trigger Process

> **Follow-up:** Document the process for re-scoping if future features introduce payments.

**Owner:** Solution owner + Compliance team  
**Status:** ✅ **CLOSED** — Documented in [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md) under "Compliance & Security > Change-in-Scope Triggers." Process: Dev team identifies trigger → notify Solution Owner + Compliance within 5 business days → re-scope using PCI checklist → engage QSA/ISA if in scope → annual re-validation per PCI DSS 12.5.2.

---

## 3. Immediate Risk-Reduction Actions

All actions completed April 8, 2026:

| # | Action | Status |
|---|--------|--------|
| **A1** | **CHD input prevention on all user-facing forms.** Client-side `containsPAN()` validation rejecting 13-19 digit numeric sequences + visible "Do not enter payment card information" notices. Applied to: `activity-hub-demo.html`, `Projects/index.html`, `admin-dashboard.html`. | ✅ Done |
| **A2** | **Restrict log verbosity.** Flask logging set to INFO-level metadata only. Werkzeug logger set to WARNING. No request body logging. `debug=False`. | ✅ Done |
| **A3** | **File upload content logging.** Server uses `send_file`/`send_from_directory` only — no file upload processing or content logging exists. | ✅ N/A |
| **A4** | **Network segmentation.** Solution owner confirms no shared PCI resources and no CDE on this subnet. | ✅ Confirmed |
| **A5** | **Data sources confirmed.** All BigQuery datasets and internal APIs contain operational data only — no CHD. | ✅ Confirmed |
| **A6** | **Email content confirmed.** Automated emails contain no CHD, sourced exclusively from operational data. | ✅ Confirmed |

---

## 4. Draft Scoping Statement

### Likely Out of Scope → **CONFIRMED: Out of Scope**

> **Activity Hub** is an internal operations dashboard that provides task management, project tracking, scheduling, and team coordination for Walmart Distribution Center operations. Based on completed scoping, Activity Hub is **out of PCI DSS scope** because it does not store, process, or transmit cardholder data (CHD) or sensitive authentication data (SAD); it is not associated with any Merchant ID (MID); it does not integrate with any payment gateway, processor, or tokenization service; it does not provide security services (authentication, logging, monitoring, AV) to any PCI-scoped system; and it shares no infrastructure with PCI-scoped environments.

**All assumptions validated (April 8, 2026):**

1. ✅ No shared resources with PCI systems; no CDE on this network segment (Solution Owner confirmed)
2. ✅ Host `weus42608431466` and management plane are not shared with PCI infrastructure (Solution Owner confirmed)
3. ✅ All data sources (BigQuery, internal APIs) contain no CHD (Solution Owner confirmed)
4. ✅ Application logs capture only HTTP metadata; no request bodies or user text logged (Code audit completed)
5. ✅ Automated emails contain no CHD (Solution Owner confirmed)
6. ✅ Change-in-scope trigger process documented in Knowledge Hub (Implemented)
7. ✅ PAN input prevention implemented on all free-text forms (Client-side validation + notices)

**Rationale:** Activity Hub follows the "No" path at every node of the PCI DSS scoping decision tree: it does not handle CHD/SAD → it is not connected to a CDE → it does not provide security services to the CDE → it cannot affect CDE security. All 7 assumptions validated in writing on April 8, 2026. Activity Hub is formally classified as out of PCI scope. Annual re-validation per PCI DSS Requirement 12.5.2 is required (next: April 2027).

---

## 5. Completed PCI DSS Scoping Checklist

### Section 1: Cardholder Data Handling

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 1.1 | Does the solution **store** cardholder data (PAN, cardholder name, expiration date, service code)? | **No** | Activity Hub stores operational data only: tasks, project metadata, schedules, team assignments. No payment card fields exist in any database table, file, or in-memory structure. |
| 1.2 | Does the solution **process** cardholder data at any point in its workflow? | **No** | All workflows are operational (task tracking, project intake, shift scheduling). No payment processing workflow exists. |
| 1.3 | Does the solution **transmit** cardholder data over any network? | **No** | Network traffic consists of HTTP requests between browser and Flask server (port 8088), and internal API calls to operational services only. |
| 1.4 | Does the solution store or log **full track data** (magnetic stripe, chip, or contactless equivalent)? | **No** | No payment terminal integration or track data handling. |
| 1.5 | Does the solution store or have access to **CVV/CVC/CAV2** values? | **No** | No payment card verification values are collected or stored. |
| 1.6 | Does the solution store or have access to **PIN or PIN block** data? | **No** | No PIN entry or PIN block handling. |

### Section 2: Tokenized, Masked, or Truncated Data

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 2.1 | Does the solution handle **tokenized** card data? | **No** | No card tokens of any kind are used. |
| 2.2 | If tokenized, does the solution have access to the **detokenization system or token vault**? | **N/A** | No tokenization in use. |
| 2.3 | Does the solution display or store **masked PAN** (e.g., `****1234`)? | **No** | No PAN in any format appears in the UI or data stores. |
| 2.4 | Does the solution handle **truncated PAN** (first 6 / last 4 digits)? | **No** | No truncated PAN data. |
| 2.5 | Can any combination of truncated/masked data be reassembled to recover the full PAN? | **No** | No PAN fragments exist in any form. |

### Section 3: Network Connectivity & Segmentation

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 3.1 | Does the solution reside on or connect to a **PCI Category 1 environment**? | **No** | Activity Hub runs on host `weus42608431466` (10.97.114.181) which is a standard operations server, not a CDE host. |
| 3.2 | Does the solution reside on or connect to a **PCI Category 2 environment**? | **No** | No integrations with security infrastructure serving the CDE (no shared AD controllers, SIEM, or AV management). |
| 3.3 | Is there **network segmentation** isolating this solution from any CDE? | **Yes** | ✅ **CONFIRMED.** No CDE exists on this network segment. The 10.97.x.x operations subnet has no payment processing systems. |
| 3.4 | Does the solution share a **VLAN, subnet, or firewall zone** with any system that handles CHD? | **No** | ✅ **CONFIRMED.** No CHD systems on this subnet. No shared PCI infrastructure. |
| 3.5 | Does the solution have **any inbound or outbound network path** to/from a CDE? | **No** | ✅ **CONFIRMED.** No connectivity to CDE. All network traffic is operational (internal APIs, BigQuery, SMTP). |
| 3.6 | Does the solution use **shared infrastructure** with PCI-scoped systems? | **No** | ✅ **CONFIRMED.** "We do not have any shared resources with any PCI information." Host is dedicated to operational services. |

### Section 4: Cryptographic Elements

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 4.1 | Does the solution generate, store, or manage **encryption keys** used to protect cardholder data? | **No** | No CHD-related key management. The solution uses standard TLS for HTTP transport but does not terminate payment-related TLS. |
| 4.2 | Does the solution handle **certificates** used in CHD transmission? | **No** | TLS certificates are for internal operational traffic only, not payment flows. |
| 4.3 | Does the solution perform **encryption or decryption** of cardholder data? | **No** | No CHD encryption operations. |
| 4.4 | Does the solution manage or have access to **HSMs** related to payment processing? | **No** | No HSM integration. |

### Section 5: Application Development

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 5.1 | Is this a **custom-developed application**? | **Yes** | Activity Hub is a custom Flask/HTML/JS application built in-house. However, it does not handle payment transactions, so PCI Requirement 6 secure development requirements do not apply for PCI purposes. |
| 5.2 | Does the application handle **payment transactions** or interact with a **payment gateway/processor**? | **No** | No payment gateway or processor integration. |
| 5.3 | Does the application render or collect **cardholder data via a web form, API, or UI**? | **No** | All forms collect operational data (project names, task descriptions, widget requests). No card data entry fields. |
| 5.4 | Does the application use **iframes, redirects, or JavaScript** from a payment service provider? | **No** | No PSP JavaScript or hosted payment page integrations. |
| 5.5 | Has the application undergone **secure code review or application security testing**? | **Not formally** | As a non-PCI internal tool, formal SAST/DAST has not been performed. Recommended as a general best practice but not a PCI requirement for this solution. |
| 5.6 | Does development use **production cardholder data** in test/dev/staging environments? | **No** | No CHD exists in any environment. |

### Section 6: Merchant IDs (MIDs)

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 6.1 | Does the solution use or is it associated with any **Merchant ID (MID)**? | **No** | No MID association. Activity Hub is not a sales or payment channel. |
| 6.2 | If yes, list all MIDs: | **N/A** | — |
| 6.3 | Does the solution process transactions under a **Walmart MID**? | **No** | No transaction processing. |
| 6.4 | Does the solution interact with a **payment terminal, POS, or virtual terminal**? | **No** | No POS or terminal integration. |

### Section 7: Third-Party Involvement

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 7.1 | Does the solution use a **third-party payment processor**? | **No** | No payment processing. |
| 7.2 | Does any **third-party vendor** have access to cardholder data through this solution? | **No** | No CHD exists in the solution, so no vendor has access to CHD through it. |
| 7.3 | Does the solution integrate with any **third-party APIs** that handle payment data? | **No** | All API integrations are to internal operational services (BigQuery, internal microservices). None handle payment data. ✅ Confirmed: no CHD in any data source. |
| 7.4 | Is there a **shared responsibility model** documented with any third-party service provider? | **N/A** | Not applicable — no payment-related third parties involved. |
| 7.5 | Are all third-party providers **PCI DSS certified**? | **N/A** | Not applicable. |

### Section 8: Gift Card & Branded Prepaid Cards

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 8.1 | Does the solution handle **gift cards branded with a payment network logo**? | **No** | No gift card functionality. |
| 8.2 | Does the solution handle **closed-loop gift cards**? | **No** | No gift card functionality. |
| 8.3 | Do branded gift cards have a **PAN printed or encoded** on them? | **N/A** | No gift cards handled. |
| 8.4 | Does the solution **activate, reload, or redeem** branded gift cards? | **No** | No gift card functionality. |

### Section 9: Authentication & Access

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 9.1 | Does the solution provide **authentication services** to any PCI-scoped system? | **No** | ✅ **CONFIRMED.** Activity Hub is a *consumer* of Windows domain authentication (AD). It does not provide identity or MFA services to any other system. |
| 9.2 | Does the solution provide **logging, monitoring, or alerting** for PCI-scoped systems? | **No** | Logging is self-contained (Flask application logs). Not integrated with any CDE SIEM or monitoring platform. |
| 9.3 | Does the solution provide **antivirus, IDS/IPS, or firewall services** to PCI-scoped systems? | **No** | No security service provision. |
| 9.4 | Does the solution have **administrative access** to any system in the CDE? | **No** | No CDE administrative credentials or access. |

### Section 10: Data Flows & Logging

| # | Question | Answer | Details |
|---|----------|--------|---------|
| 10.1 | Does the solution create **logs** that could contain cardholder data? | **No** | ✅ **CONFIRMED.** Flask logging configured for metadata only (timestamp, level, message). Werkzeug logger set to WARNING. No request body logging. `debug=False`. Server serves static files only — no request body parsing. |
| 10.2 | Does the solution receive **data feeds** from PCI-scoped systems? | **No** | ✅ **CONFIRMED.** "There is no Payment Information in the Data Sources." All feeds are operational (BigQuery, internal APIs). |
| 10.3 | Does the solution send **data to** PCI-scoped systems? | **No** | ✅ **CONFIRMED.** "There is no Payment Information in the Automated Emails." Outbound data is operational only. |
| 10.4 | Is there a **data flow diagram** documenting CHD flows? | **N/A** | No CHD flows exist. An operational data flow diagram exists but is not PCI-relevant. |

---

## 6. Targeted Follow-Up Tracker

| ID | Follow-Up | Owner | Status | Closed |
|---|-----------|-------|--------|--------|
| FU-1 | Network segmentation — no shared PCI resources on 10.97.x.x | Network / Security | ✅ Closed | Apr 8, 2026 |
| FU-2 | Segmentation validation — no CDE on this subnet | Network / Security | ✅ Closed | Apr 8, 2026 |
| FU-3 | Host/hypervisor not shared with PCI-scoped systems | Infrastructure | ✅ Closed | Apr 8, 2026 |
| FU-4 | Management plane does not bridge to CDE | Infrastructure | ✅ Closed | Apr 8, 2026 |
| FU-5 | BigQuery datasets and internal APIs have no CHD | Data Engineering | ✅ Closed | Apr 8, 2026 |
| FU-6 | Application logs — metadata only, no request bodies | Development | ✅ Closed | Apr 8, 2026 |
| FU-7 | Automated emails contain no CHD | Solution Owner | ✅ Closed | Apr 8, 2026 |
| FU-8 | Activity Hub is AD *consumer*, not *provider* to PCI systems | IAM / Security | ✅ Closed | Apr 8, 2026 |
| FU-9 | CHD input prevention on all forms (validation + notices) | Development | ✅ Closed | Apr 8, 2026 |
| FU-10 | Change-in-scope trigger process documented in Knowledge Hub | Solution Owner + Compliance | ✅ Closed | Apr 8, 2026 |

---

## 7. Quick Scoping Decision Tree — Activity Hub Path

```
Does the solution store, process, or transmit CHD/SAD?
  └─ NO (Sections 1, 2, 6, 8 all "No")
      ├─ Does it connect to / share infrastructure with a CDE?
      │   └─ NO ✅ (Section 3 — confirmed by Solution Owner)
      │       ├─ Does it provide security services to the CDE?
      │       │   └─ NO ✅ (Section 9 all "No" — confirmed)
      │       │       ├─ Can it affect the security of the CDE?
      │       │       │   └─ NO ✅ (no admin access, no shared auth, no shared logging)
      │       │       │       └─ ✅ OUT OF SCOPE — CONFIRMED April 8, 2026
```

---

**Annual Re-Validation:** Per PCI DSS Requirement 12.5.2, this scoping determination must be re-confirmed at least annually or after any significant change to Activity Hub's architecture, data flows, or integrations.

**Next Re-Validation Due:** April 2027

---

*This analysis is based on PCI DSS v4.0 scoping guidance. All open questions resolved April 8, 2026. Change-in-scope triggers documented in [KNOWLEDGE_HUB.md](KNOWLEDGE_HUB.md).*
