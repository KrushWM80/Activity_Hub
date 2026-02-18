# APM Request Records

This document tracks all APM (Application Portfolio Management) requests for Activity Hub and related applications.

## Request Process Overview

**APM Support Portal**: `wmlink/apm`

**Support Team**: APM Team  
**Business Hours**: 08:00 to 15:00 CST  
**Response SLA**: 48 hours  
**Process**: Requests are processed during regular business days in the order received

---

## APM Record Onboarding Process

This is the complete path to production for Application 03 - APM Setup.

### Prerequisites

⚠️ **Important**: If the application owner has any outstanding certification tasks, the request will not be approved until these tasks are completed.

💡 **Recommendation**: Seek assistance from your application's architect when completing onboarding and assessment information.

### Step 1: Submit Onboarding Service Request

**Action**: Submit an onboarding service request at **Anything APM Service Request**

**Outcome**: 
- Once the RITM# is fully approved (see approval details below), you will receive an APM#
- ⚠️ You are **not yet ready** to proceed with the SSP at this stage

**Current Status for Activity Hub**:
- ✅ Request submitted: REQ65303447
- ⏳ RITM: RITM77170687 - Waiting for Approval

### Step 2: Complete Data Classification Assessment (DCA)

**Action**: Visit the **Application Hub** → Click **My Pending Assessments** (center of screen)

**Assessment**: Data Classification Assessment (DCA)

**Purpose**: Initial determination of Data Category and Data Classification

⚠️ **Critical Note**: 
- Once PCI, FINC, and SOX data categories are added, they **cannot be removed** with subsequent DCA retakes
- These categories can only be removed during the SSP review process

**Status for Activity Hub**: Pending Step 1 approval

### Step 3: Complete Additional Assessments

**Triggered Automatically**: Upon completion of the DCA, the system will initiate:

1. **PCI Assessment** (ServiceNow)
2. **RISK Assessment** (ServiceNow)
3. **Enterprise Privacy Risk Assessment (EPRA)** (One Trust) - *if applicable based on DCA results*

**Status for Activity Hub**: Pending Step 1 & 2 completion

### Step 4: SSP (Security Services Portal) Submission

**Prerequisites**:
- ✅ Data Classification Assessment (DCA) completed
- ✅ PCI Assessment completed
- ✅ Record is Certified

**Action**: Initiate SSP at **wmlink/ssp**

**Status for Activity Hub**: Pending all previous steps

---

## Assessment Requirements Summary

| Assessment | Trigger | Platform | Status |
|------------|---------|----------|--------|
| **Data Classification Assessment (DCA)** | Manual - Step 2 | Application Hub | Pending |
| **PCI Assessment** | Auto after DCA | ServiceNow | Pending |
| **RISK Assessment** | Auto after DCA | ServiceNow | Pending |
| **Enterprise Privacy Risk Assessment (EPRA)** | Auto after DCA (if applicable) | One Trust | TBD |
| **SSP (Security Services Portal)** | After DCA & PCI certified | wmlink/ssp | Pending |

---

## Active Requests

### REQ65303447 - Activity Hub Production Deployment

**Request ID**: REQ65303447  
**RITM**: RITM77170687  
**Status**: ⏳ Waiting for Approval  
**Submitted**: January 2026  
**Application**: Activity Hub

#### Request Details

This is the production deployment request for Activity Hub, transitioning from Pre-Production-Pilot to Production status.

---

## Application Profile: Activity Hub

### Core Information

| Field | Value |
|-------|-------|
| **Application Name** | Activity Hub |
| **Application Owner** | Kendall Rush (krush) |
| **Business Owner** | Kendall Rush (krush) |
| **Status** | Pre-Production-Pilot |
| **User Type** | Walmart Associates |
| **Supported Users** | 50,000+ Walmart Enterprise employees |

### Business Details

| Field | Value |
|-------|-------|
| **Tech Support Group** | Store Systems AMP Platform |
| **Team Rosters Product ID** | 6426 |
| **TR Product ID + Name** | 6426 = Activity Hub |
| **Team Rosters Pillar** | Business Groups - Walmart US |
| **Team Rosters Pillar Owner** | Hari Vasudev (h0v000y) |
| **Market/Country** | United States |
| **Brand/Store-Front** | Walmart |
| **Critical Business Service** | Store Ops |

### Technical Architecture

| Field | Value |
|-------|-------|
| **Platform** | Microsoft Azure |
| **Install Type** | On Premise |
| **Application Type** | Homegrown |
| **Architecture Type** | Web Based |
| **App Function** | Information Management - Content Management Systems |
| **App Function Category** | Content Management – N/A (SF) |
| **Technology Stack** | React 18+, Node.js microservices, Enterprise-grade cloud infrastructure |
| **Security Compliance** | SOC 2 Type II, End-to-end encryption |

### AI/ML & External Services

| Field | Value |
|-------|-------|
| **Creates/Uses AI or ML** | ✅ Yes |
| **Managed by External Party** | ❌ No |
| **Commercialized to External Clients** | ❌ No |
| **Opt-In for Data Scanning Access** | ✅ Yes |

### Integrations

| Field | Value |
|-------|-------|
| **Consumed by Other Applications** | ✅ Yes |

### Access Control

| AD Group | Purpose |
|----------|---------|
| `tableau_home_office_all_type_a` | Tableau access for home office users |

---

## Application Description

The Walmart Enterprise Activity Hub is a comprehensive, customizable interface that revolutionizes how employees manage projects, tasks, and collaboration. Serving as a centralized command center, it personalizes the work experience through drag-and-drop dashboards with role-based templates tailored for executives, managers, project managers, and team members.

### Key Features

#### 🤖 Intelligent Task Management
- AI-powered task prioritization
- Smart recommendations
- Priority-based notification system
- Reduces information overload

#### 📊 Real-Time Project Analytics
- Project health visibility
- Timeline tracking
- Resource utilization monitoring

#### 🤝 Advanced Collaboration Tools
- Cross-functional communication
- Document sharing
- Team coordination

#### 🎯 Role-Based Dashboards
- Drag-and-drop customization
- Executive templates
- Manager templates
- Project manager templates
- Team member templates

---

## Business Value & ROI

### Time Savings by Role

| Role | Weekly Time Saved | Annual Impact |
|------|------------------|---------------|
| **Executives** | 2-3 hours | Strategic oversight improvement |
| **Managers** | 4-5 hours | Team performance optimization |
| **Project Managers** | 6-8 hours | Faster issue resolution |
| **Team Members** | 3-4 hours | Clearer priorities |

### Financial Impact

| Metric | Value |
|--------|-------|
| **Total Investment** | $3.4M |
| **Annual Benefits** | $27M |
| **ROI** | 694% |
| **Project Delivery Improvement** | 15% faster timelines |

---

## Request History

### REQ65303447 Timeline & Process Tracking

| Step | Date | Event | Status |
|------|------|-------|--------|
| **1** | January 2026 | Onboarding service request submitted (REQ65303447/RITM77170687) | ⏳ Waiting for Approval |
| **1** | TBD | APM Team review & approval | Pending |
| **1** | TBD | APM# assigned | Pending |
| **2** | TBD | Data Classification Assessment (DCA) | Pending |
| **3** | TBD | PCI Assessment (auto-triggered) | Pending |
| **3** | TBD | RISK Assessment (auto-triggered) | Pending |
| **3** | TBD | EPRA Assessment (if applicable) | TBD |
| **4** | TBD | Record Certification | Pending |
| **4** | TBD | SSP Submission (wmlink/ssp) | Pending |
| **5** | TBD | SSP Review & Approval | Pending |
| **6** | TBD | Production deployment | Pending |

---

## Related Documentation

- [Activity Hub README](../README.md)
- [AMP Data Analysis](../AMP_DATA_ANALYSIS.md)
### Immediate Actions (Step 1 - Current)

1. ⏳ **Monitor RITM77170687 Approval**
   - Check APM portal at `wmlink/apm` regularly
   - Response expected within 48 business hours
   - Wait for APM# assignment
   - **Do NOT proceed to SSP until Step 1 is complete**

2. 📋 **Prepare for Data Classification Assessment**
   - Review application data flows
   - Document PCI, FINC, and SOX data handling (if applicable)
   - Consult with application architect
   - Gather data classification documentation

### After Step 1 Approval

3. 📊 **Complete Application Hub Assessments**
   - Access Application Hub → My Pending Assessments
   - Complete Data Classification Assessment (DCA)
   - Wait for auto-triggered assessments (PCI, RISK, EPRA)
   - Track assessment completion status

4. 🔒 **SSP Submission & Review**
   - Verify DCA and PCI assessments are complete
   - Confirm record is Certified
   - Submit SSP at `wmlink/ssp`
   - Engage with Security Risk team for review
### APM Support

**Email**: apmmailbox@wal-mart.com  
**Portal**: wmlink/apm (Anything APM Service Request)  
**Business Hours**: Monday-Friday, 08:00-15:00 CST  
**SLA**: 48-hour response time  
**Purpose**: Onboarding requests, APM record management, general APM questions

### SSP (Security Services Portal) Support

**Email**: Secrisk@wal-mart.com  
**Portal**: wmlink/ssp  
**Help Page**: SSP Workplace  
**Purpose**: SSP submissions, security assessments, certification questions

### Application-Specific Support

**Tech Support Group**: Store Systems AMP Platform  
**Pillar Owner**: Hari Vasudev (h0v000y)  
**Application Owner**: Kendall Rush (krush)*
   - Execute production deployment plan
   - Notify all stakeholders
   - Update Team Rosters product status (6426)
   - Begin production monitoring
   - Update APM record status to Productiondocuments
   - Confirm stakeholder alignment

3. 🚀 **Post-Approval Actions**
   - Execute production deployment plan
   - Notify all stakeholders
   - Update Team Rosters product status
   - Begin production monitoring

---

## Support & Escalation

**Primary Contact**: APM Team  
**Portal**: wmlink/apm  
**Business Hours**: Monday-Friday, 08:00-15:00 CST  
**SLA**: 48-hour response time

For urgent issues outside business hours, escalate through Store Systems AMP Platform support channels.

---

**Last Updated**: January 14, 2026  
**Document Owner**: Kendall Rush (krush)  
**Version**: 1.0
