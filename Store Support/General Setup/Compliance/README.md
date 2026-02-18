# Compliance Reference - Index
**Location:** General Setup/Compliance/  
**Purpose:** Master reference for compliance standards and future projects

---

## Navigation Guide

### For Understanding Compliance (Start Here)

**📘 COMPLIANCE-STANDARDS-FRAMEWORK.md**
- **What:** Universal compliance framework for ANY project
- **Best For:** Learning how to determine what standards apply
- **Read Time:** 30-45 minutes
- **Sections:**
  - How to determine compliance requirements (decision tree)
  - PCI/SOX/SOC 2 frameworks explained
  - Third-party AI/DPA requirements
  - Implementation roadmap pattern
  - Critical controls checklist
  - Common mistakes to avoid

**📋 AI-POLICY.md**
- **What:** Enterprise AI usage policy
- **Best For:** Teams using AI/ML services
- **Read Time:** 20-30 minutes
- **Sections:**
  - Data classification requirements
  - DPA requirements checklist
  - Approved vendors (Azure OpenAI, Google Vertex AI)
  - Prohibited uses
  - Audit logging requirements

---

## Quick Reference - Compliance Decision Tree

**Use this to determine what applies to your project:**

```
Does your system handle payment card data?
├─ YES → PCI DSS ✅
│
└─ NO → Continue

Does your system handle financial data for SEC reporting?
├─ YES → SOX ✅
│
└─ NO → Continue

Is it enterprise-critical or 50+ users?
├─ YES → SOC 2 Type II ✅
│
└─ NO → Continue

Do you use third-party AI/APIs with company data?
├─ YES → DPA Required ✅
│
└─ NO → Minimal compliance needed
```

---

## Critical Controls - Required for ALL Systems

```
ALWAYS implement:
✅ Authentication (SSO or strong login)
✅ Encryption (at rest & in transit)
✅ Audit logging (who did what when)
✅ Access control (RBAC)
✅ Change management (code review)
✅ Incident response plan (documented)
```

---

## How to Use This Framework

### For NEW Projects

**Step 1:** Read COMPLIANCE-STANDARDS-FRAMEWORK.md
**Step 2:** Use Decision Tree (Section 4)
**Step 3:** Determine what applies to your project
**Step 4:** Document findings in Compliance Report
**Step 5:** If using AI → Review AI-POLICY.md

### If Using AI/ML Services

**Step 1:** Read AI-POLICY.md (5 min overview)
**Step 2:** Complete DPA Checklist (Section 5)
**Step 3:** Get legal approval before using vendor
**Step 4:** Implement audit logging
**Step 5:** Verify data classification

---

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Status:** ✅ Ready for use

