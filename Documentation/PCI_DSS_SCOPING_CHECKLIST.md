# PCI DSS Scoping Checklist

Use this checklist to determine whether a solution falls under PCI scope. Collect answers from the solution owner or technical team. Any **🔴 RED FLAG** answer automatically indicates PCI scope.

---

## Section 1: Cardholder Data Handling

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 1.1 | Does the solution **store** cardholder data (PAN, cardholder name, expiration date, service code)? | | |
| 1.2 | Does the solution **process** cardholder data at any point in its workflow? | | |
| 1.3 | Does the solution **transmit** cardholder data over any network? | | |
| 1.4 | Does the solution store or log **full track data** (magnetic stripe, chip, or contactless equivalent)? | | |
| 1.5 | Does the solution store or have access to **CVV/CVC/CAV2** values? | | |
| 1.6 | Does the solution store or have access to **PIN or PIN block** data? | | |

**Why these matter:** Any storage, processing, or transmission of cardholder data (CHD) or sensitive authentication data (SAD) places the solution squarely in PCI scope. Questions 1.4–1.6 are **🔴 RED FLAGS** — storing SAD post-authorization is explicitly prohibited by PCI DSS.

---

## Section 2: Tokenized, Masked, or Truncated Data

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 2.1 | Does the solution handle **tokenized** card data? | | |
| 2.2 | If tokenized, does the solution have access to the **detokenization system or token vault**? | | |
| 2.3 | Does the solution display or store **masked PAN** (e.g., `****1234`)? | | |
| 2.4 | Does the solution handle **truncated PAN** (first 6 / last 4 digits)? | | |
| 2.5 | Can any combination of truncated/masked data be reassembled to recover the full PAN? | | |

**Why these matter:** Tokens and masked data are generally out of scope, **unless** the system can detokenize or reassemble the full PAN. Question 2.2 is a **🔴 RED FLAG** — access to the token vault brings the solution into scope. Question 2.5 is also a **🔴 RED FLAG**.

---

## Section 3: Network Connectivity & Segmentation

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 3.1 | Does the solution reside on or connect to a **PCI Category 1 environment** (systems that directly store/process/transmit CHD)? | | |
| 3.2 | Does the solution reside on or connect to a **PCI Category 2 environment** (systems that provide security services to Cat 1, e.g., AD, DNS, logging, AV)? | | |
| 3.3 | Is there **network segmentation** isolating this solution from any cardholder data environment (CDE)? | | |
| 3.4 | Does the solution share a **VLAN, subnet, or firewall zone** with any system that handles CHD? | | |
| 3.5 | Does the solution have **any inbound or outbound network path** to/from a CDE? | | |
| 3.6 | Does the solution use **shared infrastructure** (servers, databases, load balancers) with PCI-scoped systems? | | |

**Why these matter:** "Connected-to" systems fall in scope even if they never touch CHD. If there is no validated segmentation between this solution and a CDE, it is in scope by default. Questions 3.1, 3.4, and 3.5 are **🔴 RED FLAGS**.

---

## Section 4: Cryptographic Elements

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 4.1 | Does the solution generate, store, or manage **encryption keys** used to protect cardholder data? | | |
| 4.2 | Does the solution handle **certificates** used in CHD transmission (e.g., TLS termination for payment traffic)? | | |
| 4.3 | Does the solution perform **encryption or decryption** of cardholder data? | | |
| 4.4 | Does the solution manage or have access to **Hardware Security Modules (HSMs)** related to payment processing? | | |

**Why these matter:** Key management systems and encryption/decryption endpoints are PCI Category 2 at minimum. Question 4.1 and 4.3 are **🔴 RED FLAGS** — they place the solution in scope as a security-providing system.

---

## Section 5: Application Development

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 5.1 | Is this a **custom-developed application** (not a COTS/vendor product)? | | |
| 5.2 | Does the application handle **payment transactions** or interact with a **payment gateway/processor**? | | |
| 5.3 | Does the application render or collect **cardholder data via a web form, API, or UI**? | | |
| 5.4 | Does the application use **iframes, redirects, or JavaScript** from a payment service provider? | | |
| 5.5 | Has the application undergone **secure code review or application security testing** (SAST/DAST)? | | |
| 5.6 | Does development use **production cardholder data** in test/dev/staging environments? | | |

**Why these matter:** Custom apps that touch payment flows must comply with PCI DSS Requirement 6 (secure development). Question 5.2 and 5.3 are **🔴 RED FLAGS**. Question 5.6 is a **🔴 RED FLAG** — production CHD in non-production environments extends PCI scope to those environments.

---

## Section 6: Merchant IDs (MIDs)

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 6.1 | Does the solution use or is it associated with any **Merchant ID (MID)**? | | |
| 6.2 | If yes, list all MIDs: | | |
| 6.3 | Does the solution process transactions under a **Walmart MID**? | | |
| 6.4 | Does the solution interact with a **payment terminal, POS, or virtual terminal**? | | |

**Why these matter:** Each MID represents a payment processing relationship and is subject to PCI compliance validation. Any MID association is a **🔴 RED FLAG** for scoping.

---

## Section 7: Third-Party Involvement

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 7.1 | Does the solution use a **third-party payment processor** (e.g., Stripe, Adyen, FIS)? | | |
| 7.2 | Does any **third-party vendor** have access to cardholder data through this solution? | | |
| 7.3 | Does the solution integrate with any **third-party APIs** that handle payment data? | | |
| 7.4 | Is there a **shared responsibility model** documented with any third-party service provider? | | |
| 7.5 | Are all third-party providers **PCI DSS certified** (listed on Visa/Mastercard registries)? | | |

**Why these matter:** Third-party risk is a major PCI focus area. If a vendor touches CHD on your behalf, they must be validated as PCI compliant, and you must maintain oversight (Requirement 12.8). Question 7.2 without 7.5 is a **🔴 RED FLAG**.

---

## Section 8: Gift Card & Branded Prepaid Cards

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 8.1 | Does the solution handle **gift cards branded with a payment network logo** (Visa, Mastercard, Amex, Discover)? | | |
| 8.2 | Does the solution handle **closed-loop gift cards** (Walmart-only, no network branding)? | | |
| 8.3 | Do branded gift cards have a **PAN printed or encoded** on them? | | |
| 8.4 | Does the solution **activate, reload, or redeem** branded gift cards? | | |

**Why these matter:** Branded/open-loop gift cards carrying a PAN from a card network (Visa, MC, Amex, Discover) are treated as payment cards under PCI DSS. Questions 8.1 and 8.3 are **🔴 RED FLAGS**. Closed-loop cards (8.2) are generally out of scope unless they carry a network PAN.

---

## Section 9: Authentication & Access

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 9.1 | Does the solution provide **authentication services** (AD, LDAP, MFA) to any PCI-scoped system? | | |
| 9.2 | Does the solution provide **logging, monitoring, or alerting** for PCI-scoped systems? | | |
| 9.3 | Does the solution provide **antivirus, IDS/IPS, or firewall services** to PCI-scoped systems? | | |
| 9.4 | Does the solution have **administrative access** to any system in the CDE? | | |

**Why these matter:** Systems that provide security services to the CDE are PCI Category 2 ("security-impacting") and are in scope. Any "yes" here means the solution supports the security posture of the CDE.

---

## Section 10: Data Flows & Logging

| # | Question | Yes / No | Details |
|---|----------|----------|---------|
| 10.1 | Does the solution create **logs** that could contain cardholder data (even accidentally)? | | |
| 10.2 | Does the solution receive **data feeds** from PCI-scoped systems? | | |
| 10.3 | Does the solution send **data to** PCI-scoped systems? | | |
| 10.4 | Is there a **data flow diagram** documenting where CHD enters, moves, and exits? | | |

**Why these matter:** Accidental CHD in logs is one of the most common scoping oversights. If CHD leaks into logs, the logging infrastructure becomes in-scope. Question 10.1 is a **🔴 RED FLAG** if the answer is yes or uncertain.

---

## Quick Scoping Decision Tree

```
Does the solution store, process, or transmit CHD/SAD?
  ├─ YES → IN SCOPE (PCI Category 1)
  └─ NO
      ├─ Does it connect to / share infrastructure with a CDE?
      │   ├─ YES → IN SCOPE (Category 2 - Connected-to)
      │   └─ NO
      │       ├─ Does it provide security services to the CDE?
      │       │   ├─ YES → IN SCOPE (Category 2 - Security-impacting)
      │       │   └─ NO
      │       │       ├─ Can it affect the security of the CDE?
      │       │       │   ├─ YES → IN SCOPE (Category 3)
      │       │       │   └─ NO → OUT OF SCOPE
      │       │       └─
      │       └─
      └─
```

---

## 🔴 Red Flag Summary

If **any** of these are true, the solution is automatically in PCI scope:

| Red Flag | Questions |
|----------|-----------|
| Stores/processes/transmits CHD | 1.1, 1.2, 1.3 |
| Stores SAD (track data, CVV, PIN) | 1.4, 1.5, 1.6 |
| Access to token vault / detokenization | 2.2 |
| Can reassemble full PAN | 2.5 |
| Connected to CDE without segmentation | 3.1, 3.4, 3.5 |
| Manages encryption keys for CHD | 4.1, 4.3 |
| Processes payment transactions | 5.2, 5.3 |
| Production CHD in non-prod environments | 5.6 |
| Associated with a MID | 6.1 |
| Third-party accesses CHD without PCI cert | 7.2 without 7.5 |
| Handles branded gift cards with PAN | 8.1, 8.3 |
| CHD in logs | 10.1 |

---

*Checklist based on PCI DSS v4.0 scoping guidance. Consult your PCI QSA or ISA for final scoping determination.*
