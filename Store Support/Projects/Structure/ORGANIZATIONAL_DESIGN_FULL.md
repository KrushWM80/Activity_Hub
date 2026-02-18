# Store Operations Acceleration & Support  
## Data, Analytics & Platform Organization Design
**For Juan Galarraga's Organization**

---

## EXECUTIVE SUMMARY

This organizational design enables Juan Galarraga's Store Operations Acceleration and Support organization to execute three simultaneous mandates: maintain legacy platforms, modernize to standardized tools (OMP, MyWalmart, Activity Hub), and build new analytical capabilities—all without disrupting business operations.

**Key Design Decisions:**
- **Hybrid Platform-Product Model**: Central platform teams build infrastructure; business-aligned product teams deliver outcomes
- **Dual-Track Execution**: Separate "Run" and "Transform" teams to manage legacy while building new
- **Activity Hub as Strategic Platform**: Dedicated team to build unified analytics experience
- **Federated Governance**: Central standards with distributed execution
- **VP-Level Business Alignment**: VPs own either Stores or Home Office outcome delivery

**Organization Scale:**  
~250-350 FTEs across platform, product, data, and support functions

---

## ORGANIZATIONAL STRUCTURE

### Level 1: SVP — Juan Galarraga
**Role**: Senior Vice President, Store Operations Acceleration and Support

**Scope**: Overall P&L, strategy, stakeholder management, organizational health

---

### Level 2: Vice Presidents (4-5 VPs)

#### **VP #1: Data Platform & Engineering**  
*Owner: Core data infrastructure and platform capabilities*

**Responsibilities:**
- Data ingestion, integration, and pipeline orchestration
- Data warehouse (BigQuery) architecture and optimization  
- Platform reliability, performance, and SRE
- DevOps, infrastructure-as-code, CI/CD  
- API management and data services

**Why this role:**  
Separates foundational platform work from business-facing analytics. This VP ensures reliable, scalable infrastructure that all product teams depend on.

**Teams:**
- **Data Engineering Platform** (20-25)  
- **Data Integration & ETL** (15-20)  
- **Platform Operations & SRE** (10-15)  
- **API & Data Services** (8-10)

---

#### **VP #2: Store Analytics & Products**  
*Owner: All analytics products and platforms serving Stores/Field Operations*

**Responsibilities:**
- Ops Metrics Portal (OMP) product ownership
- MyWalmart mobile analytics features  
- Store labor, inventory, execution analytics
- Field operations reporting and dashboards
- Store performance metrics and KPIs
- Direct relationship with Store Operations stakeholders

**Why this role:**  
Stores have unique needs (mobile-first, real-time, operational). This VP ensures undivided focus on field requirements with accountability for business outcomes.

**Teams:**
- **OMP Product & Development** (25-30)  
- **MyWalmart Analytics** (15-18)  
- **Store Operations Analytics** (20-25)  
- **Field Enablement & Support** (12-15)

---

#### **VP #3: Home Office Analytics & Activity Hub**  
*Owner: All analytics products serving Home Office, including Activity Hub platform*

**Responsibilities:**
- Activity Hub platform strategy and development
- Merchandising, Planning, Supply Chain analytics
- Finance and Executive reporting  
- Enterprise self-service analytics capabilities
- Cross-functional Home Office insights

**Why this role:**  
Home Office users need sophisticated analytical depth and cross-functional visibility. Activity Hub is strategic—requires VP-level ownership to drive adoption and integration.

**Teams:**
- **Activity Hub Platform** (20-25) — *Strategic*
- **Merchandising & Planning Analytics** (18-22)  
- **Finance & Supply Chain Analytics** (18-22)  
- **Executive Reporting & Insights** (12-15)

---

#### **VP #4: Analytics Capabilities & Data Science**  
*Owner: Horizontal capabilities that serve all business areas*

**Responsibilities:**
- Data science and machine learning  
- Analytics engineering (DBT, semantic layers, metrics)  
- Advanced analytics and predictive modeling  
- Visualization standards and best practices
- Self-service enablement tools and frameworks

**Why this role:**  
Capabilities like data science and analytics engineering are leveraged across Stores and Home Office. Centralizing them avoids duplication and builds deep expertise.

**Teams:**
- **Data Science & ML** (15-20)  
- **Analytics Engineering** (18-22)  
- **Visualization & BI Platforms** (10-12)  
- **Self-Service Enablement** (8-10)

---

#### **VP #5: Governance, Strategy & Transformation (Optional)**  
*Owner: Standards, governance, portfolio management, and modernization program*

**Responsibilities:**
- Data governance and quality  
- Metric definitions and semantic standards  
- Portfolio prioritization across maintain/modernize/innovate  
- Change management and adoption programs  
- Vendor management and technology strategy

**Why this role:**  
The "triple mandate" requires active management. This VP ensures standards are enforced, priorities are balanced, and legacy-to-modern transition is coordinated.

**Alternative:** If not a separate VP, distribute these responsibilities:
- Data Governance → VP Data Platform  
- Portfolio Management → Direct to Juan  
- Transformation Program → Shared across VPs with PMO support

**Teams:**
- **Data Governance & Quality** (10-12)  
- **Portfolio & Program Management** (8-10)  
- **Change Management & Adoption** (6-8)  
- **Architecture & Standards** (8-10)

---

## TEAM-LEVEL STRUCTURE: Example Deep-Dive

### **Activity Hub Platform Team** (Reports to VP Home Office Analytics)

**Senior Director, Activity Hub**  
├─ **Director, Product Management** (3-4 PMs)  
├─ **Director, Engineering** (12-15 engineers)  
│   ├─ Frontend Squad (4-5)  
│   ├─ Backend/API Squad (4-5)  
│   ├─ Integration Squad (3-4)  
├─ **Director, Analytics & Data** (4-5 analytics engineers)  
└─ **Manager, UX & Design** (2-3 designers)

**Charter:**  
Build and operate Activity Hub as the unified analytics platform for Home Office. Integrate data from multiple sources (Merchandising, Operations, Finance) to create apples-to-apples comparisons with consistent metrics and definitions.

**Key Metrics:**  
- Monthly Active Users (MAU)  
- Dashboards/reports migrated from legacy tools  
- Data source integrations completed  
- User satisfaction (NPS)

---

### **OMP Product & Development Team** (Reports to VP Store Analytics)

**Senior Director, Ops Metrics Portal**  
├─ **Director, Product Management** (4-5 PMs)  
├─ **Director, Engineering** (15-18 engineers)  
│   ├─ Store Ops Squad (5-6)  
│   ├─ Labor & Scheduling Squad (5-6)  
│   ├─ Platform Services Squad (4-5)  
├─ **Director, Analytics** (10-12 analysts)  
└─ **Manager, Field Support** (5-6 support specialists)

**Charter:**  
Own OMP as the primary analytics platform for Store Operations. Deliver real-time operational metrics, labor management insights, and execution tracking to field leaders.

---

## INTERACTION MODEL: How Teams Work Together

### **Platform → Product Dependency Flow**

```
Data Platform & Engineering (VP #1)
        ↓ provides infrastructure
Store Analytics (VP #2) + Home Office Analytics (VP #3)
        ↓ consumes platform services
        ↓ builds business-specific products
Business Stakeholders (Directors/Senior Directors)
```

### **Cross-VP Collaboration Mechanisms**

1. **Weekly Platform Council**  
   - All VPs + key Senior Directors  
   - Review platform health, resolve dependencies, prioritize shared work  

2. **Bi-Weekly Product Review**  
   - Product VPs (#2, #3) + Juan  
   - Review business outcomes, feature launches, user feedback  

3. **Monthly Architecture Forum**  
   - Technical leaders across VPs  
   - Align on standards, review RFCs, approve major changes  

4. **Quarterly Business Review**  
   - All VPs + business stakeholder Directors  
   - Strategic alignment, priority setting, resource allocation

---

## RACI MATRIX: Triple Mandate Execution

| Responsibility | Platform VP | Store VP | Home Office VP | Capabilities VP | Governance VP |
|---|:---:|:---:|:---:|:---:|:---:|
| **MAINTAIN LEGACY** |  |  |  |  |  |
| Tableau/PowerBI uptime | C | R/A | R/A | C | I |
| Legacy report fixes | C | R/A | R/A | C | I |
| User support | I | A/R | A/R | C | C |
| **MODERNIZE PLATFORMS** |  |  |  |  |  |
| OMP development | C | R/A | I | C | I |
| Activity Hub development | C | I | R/A | C | I |
| Data migration | R/A | C | C | C | I |
| Platform standards | R/A | C | C | C | A |
| **INNOVATE NEW** |  |  |  |  |  |
| Data science models | C | C | C | R/A | I |
| Advanced analytics | C | C | C | R/A | I |
| Self-service tools | C | C | C | R/A | A |
| **GOVERNANCE** |  |  |  |  |  |
| Metric definitions | C | C | C | C | R/A |
| Data quality | R/A | C | C | C | A |
| Access control | R/A | C | C | C | A |

**Legend:**  
- **R** = Responsible (does the work)  
- **A** = Accountable (owns the outcome)  
- **C** = Consulted (provides input)  
- **I** = Informed (kept in the loop)

---

## GOVERNANCE FRAMEWORK

### **Decision Rights**

#### **Level 1: Strategic (SVP — Juan)**
- Overall org strategy and priorities  
- Resource allocation across VPs  
- Major platform investments (e.g., Activity Hub go/no-go)  
- Senior leadership hiring  

#### **Level 2: Portfolio (VPs)**
- Team structure and headcount within VP area  
- Feature prioritization for their domain  
- Technology choices within guardrails  
- Director-level hiring  

#### **Level 3: Execution (Senior Directors / Directors)**
- Sprint planning and delivery execution  
- Day-to-day prioritization  
- Team-level hiring  
- Technical implementation decisions  

### **Standards Governance**

**Data Governance Council** (meets bi-weekly)  
- **Chair:** VP Governance (or VP Data Platform if no separate governance VP)  
- **Members:** Senior Director from each VP area + key business stakeholders  
- **Scope:**  
  - Approve metric definitions  
  - Set data quality standards  
  - Resolve data ownership conflicts  
  - Approve schema changes impacting multiple teams  

**Architecture Review Board** (meets monthly)  
- **Chair:** SVP-level technical leader or VP Data Platform  
- **Members:** Senior Directors of Engineering from each VP area  
- **Scope:**  
  - Review RFCs for major system changes  
  - Approve technology choices  
  - Ensure platform consistency  
  - Resolve cross-team technical dependencies  

---

## WORK INTAKE & PRIORITIZATION

### **Three-Track Portfolio Management**

#### **Track 1: RUN (Maintain Legacy)**  
**Allocation:** 30-40% of capacity  
**Owner:** Each product VP for their domain  
**Examples:**  
- Tableau dashboard fixes  
- PowerBI report updates  
- Data refresh issues  
- User support tickets  

**Decision Process:**  
- VPs own prioritization within their domain  
- SLA-driven (severity 1 = immediate, severity 2 = 1 week, etc.)  
- Weekly review of backlog health  

#### **Track 2: TRANSFORM (Modernize)**  
**Allocation:** 40-50% of capacity  
**Owner:** Shared across product VPs, coordinated by governance/PMO  
**Examples:**  
- OMP feature development  
- Activity Hub buildout  
- Tableau → Activity Hub migrations  
- Data model standardization  

**Decision Process:**  
- Quarterly roadmap planning  
- Monthly release planning  
- Business value scoring: Impact × Urgency × Strategic Fit  
- Cross-VP dependencies managed via Platform Council  

#### **Track 3: INNOVATE (Build New)**  
**Allocation:** 10-20% of capacity  
**Owner:** VP Capabilities + product VPs co-own  
**Examples:**  
- Predictive analytics models  
- New data science use cases  
- Advanced visualization experiments  
- Self-service tool enhancements  

**Decision Process:**  
- Innovation pipeline reviewed quarterly  
- Business sponsors required for new initiatives  
- Stage-gate funding: Discover → Validate → Scale  
- "Fail fast" culture: kill projects that don't show promise  

---

## BUSINESS STAKEHOLDER ENGAGEMENT

### **How Directors/Senior Directors in Operations Engage**

**Store Operations Directors** engage with:  
1. **VP Store Analytics** as primary business partner  
2. **Senior Director, OMP** for product-specific needs  
3. **Director, Store Operations Analytics** for day-to-day requests  

**Merchandising/Planning Directors** engage with:  
1. **VP Home Office Analytics** as primary business partner  
2. **Senior Director, Activity Hub** for platform features  
3. **Director, Merchandising Analytics** for day-to-day requests  

### **Engagement Mechanisms**

**Monthly Business Partner Review**  
- VP + business stakeholder senior directors  
- Review priorities, upcoming releases, blockers  
- Adjust roadmap based on business need  

**Quarterly Strategy Alignment**  
- Juan + all VPs + key business stakeholders  
- Strategic priorities for next quarter  
- Major feature launches and dependencies  

**Embedded Analysts**  
- Analytics teams have "homes" in business functions  
- Report to analytics VP but sit with business teams  
- Translate business needs into technical requirements  

---

## TRANSITION PLAN: Current State → Future State

### **Phase 1: Foundation (Months 0-6)**

**Objectives:**  
✓ Establish VP structure and hire key leaders  
✓ Stand up Activity Hub core team  
✓ Stabilize legacy platforms  
✓ Begin data platform modernization  

**Key Actions:**  
- Hire VPs for Data Platform, Store Analytics, Home Office Analytics  
- Recruit Senior Director for Activity Hub  
- Establish governance forums (Platform Council, ARB)  
- Audit legacy Tableau/PowerBI estate  
- Define initial metric standards  

**Staffing:**  
- Start with ~150 FTEs (assume 100-150 existing team)  
- Prioritize hiring platform and Activity Hub roles  
- 60% RUN / 30% TRANSFORM / 10% INNOVATE  

---

### **Phase 2: Scale (Months 7-18)**

**Objectives:**  
✓ Activity Hub MVP launched  
✓ OMP feature parity with legacy tools  
✓ 30% of Tableau/PowerBI reports migrated  
✓ Data science team operational  

**Key Actions:**  
- Launch Activity Hub to pilot users (Home Office)  
- Migrate high-value Tableau dashboards to Activity Hub  
- Build out data science team and deliver first models  
- Standardize semantic layer across all platforms  
- Begin decommissioning oldest Tableau workbooks  

**Staffing:**  
- Grow to ~250 FTEs  
- Hire for Analytics Engineering, Data Science, Activity Hub  
- 40% RUN / 45% TRANSFORM / 15% INNOVATE  

---

### **Phase 3: Optimize (Months 19-36)**

**Objectives:**  
✓ 70%+ of legacy tools migrated  
✓ Activity Hub as primary Home Office platform  
✓ OMP and MyWalmart fully adopted in Stores  
✓ Self-service analytics mature  
✓ Data science embedded in business workflows  

**Key Actions:**  
- Decommission Tableau and PowerBI infrastructure  
- Optimize platform costs and performance  
- Shift resources from maintenance to innovation  
- Establish COE (Center of Excellence) model for self-service  
- Expand data science to predictive/prescriptive use cases  

**Staffing:**  
- Stabilize at ~300-350 FTEs  
- Shift contractor mix: fewer maintenance, more product dev  
- 20% RUN / 40% TRANSFORM / 40% INNOVATE  

---

## TEAM CHARTERS: Examples

### **Data Engineering Platform Team**

**Mission:**  
Provide reliable, scalable, and secure data infrastructure that enables all analytics and data science work across the organization.

**Responsibilities:**  
- Design and operate data ingestion pipelines  
- Manage BigQuery data warehouse  
- Ensure 99.9% platform uptime  
- Provide self-service data APIs  
- Optimize query performance and costs  

**Key Metrics:**  
- Platform uptime (target: 99.9%)  
- Data pipeline SLA attainment (target: 95%)  
- Query performance (p95 latency)  
- Cost per TB processed  

**Interfaces:**  
- **Upstream:** Source systems, IT infrastructure  
- **Downstream:** All analytics teams, data scientists  
- **Governance:** Architecture Review Board, Data Governance Council  

---

### **Activity Hub Platform Team**

**Mission:**  
Build and operate Activity Hub as the unified analytics platform for Home Office, enabling consistent metrics and cross-functional insights.

**Responsibilities:**  
- Develop Activity Hub product roadmap  
- Engineer platform features and integrations  
- Migrate legacy Tableau/PowerBI reports  
- Design UX for cross-functional analytics  
- Support Home Office users  

**Key Metrics:**  
- Monthly Active Users (MAU)  
- Reports migrated from legacy tools  
- User satisfaction (NPS > 40)  
- Time-to-insight (user task completion time)  

**Interfaces:**  
- **Upstream:** Data Platform, Analytics Engineering  
- **Downstream:** Home Office Directors, Merchandising, Finance, Supply Chain  
- **Partners:** OMP team (shared standards), MyWalmart team (mobile patterns)  

---

## KEY SUCCESS FACTORS

### **What Makes This Design Work**

1. **VP-Level Business Alignment**  
   - Stores and Home Office have dedicated VPs who own outcomes  
   - Eliminates "no one owns this" problems  
   - Clear escalation path for business stakeholders  

2. **Platform Separation**  
   - Data Platform VP focuses on infrastructure reliability  
   - Product VPs focus on business outcomes  
   - Capabilities VP provides horizontal expertise  
   - Avoids "full stack" team anti-pattern at scale  

3. **Activity Hub Strategic Focus**  
   - Senior Director-level ownership ensures executive attention  
   - Dedicated team avoids "side project" risk  
   - Clear integration with broader platform strategy  

4. **Triple Mandate Discipline**  
   - Explicit RUN/TRANSFORM/INNOVATE tracks  
   - Portfolio management ensures balance  
   - Prevents "innovation theater" while legacy burns  

5. **Governance Without Bureaucracy**  
   - Forums have clear scope and decision rights  
   - Federated model empowers teams  
   - Standards enforced through platforms, not policies  

---

## RISKS & MITIGATIONS

### **Risk 1: Legacy Maintenance Overwhelms Transformation**

**Mitigation:**  
- Hard capacity caps on RUN track (e.g., 40% max)  
- Automated testing and monitoring to reduce manual toil  
- Ruthlessly deprecate low-value legacy reports  
- Communicate "sundown dates" for Tableau/PowerBI

---

### **Risk 2: Activity Hub Adoption Fails**

**Mitigation:**  
- Executive sponsorship from Juan and Home Office leaders  
- Migrate high-visibility executive dashboards first  
- Invest heavily in UX and performance  
- Embed Activity Hub team with business stakeholders  
- Celebrate migration wins publicly  

---

### **Risk 3: Platform and Product Teams Misaligned**

**Mitigation:**  
- Weekly Platform Council with all VPs  
- Shared OKRs across platform and product teams  
- Platform teams measure "customer" (product team) satisfaction  
- Rotate engineers between platform and product teams  

---

### **Risk 4: Talent Retention During Transition**

**Mitigation:**  
- Clear career paths from legacy to modern tech  
- Invest in upskilling (e.g., Tableau → Activity Hub)  
- Bonus structures tied to migration milestones  
- Communicate vision frequently: "We're building the future"  

---

### **Risk 5: Business Stakeholders Resist Change**

**Mitigation:**  
- Change management team dedicated to adoption  
- Pilot programs with friendly stakeholders  
- "No worse than legacy" performance guarantee  
- Executive communication from Juan on strategic rationale  
- Celebrate early wins and user testimonials  

---

## ORGANIZATIONAL PRINCIPLES (Revisited)

This design optimizes for:

✅ **Parallel Execution** — RUN/TRANSFORM/INNOVATE tracks with dedicated capacity  
✅ **Business Outcomes** — VPs own Stores and Home Office delivery  
✅ **Platform Leverage** — Activity Hub, OMP, MyWalmart as strategic platforms  
✅ **Metric Standardization** — Governance council enforces semantic consistency  
✅ **Scalability** — 250-350 FTEs supporting thousands of users  
✅ **Clarity** — Decision rights and RACI explicit  
✅ **Sustainability** — 3-5 year horizon with clear transition phases  

---

## APPENDIX: SAMPLE ORG CHART

```
Juan Galarraga (SVP)
│
├─ VP Data Platform & Engineering
│   ├─ Senior Director, Data Engineering
│   │   ├─ Director, Data Pipelines (20-25)
│   │   └─ Director, Data Integration (15-20)
│   ├─ Senior Director, Platform Operations
│   │   ├─ Director, SRE & Reliability (10-15)
│   │   └─ Director, API Services (8-10)
│
├─ VP Store Analytics & Products
│   ├─ Senior Director, Ops Metrics Portal
│   │   ├─ Director, Product Management (4-5 PMs)
│   │   ├─ Director, Engineering (15-18 engineers)
│   │   └─ Director, Analytics (10-12 analysts)
│   ├─ Senior Director, MyWalmart Analytics
│   │   ├─ Director, Mobile Product (15-18)
│   └─ Senior Director, Store Operations Analytics
│       ├─ Director, Labor & Execution (20-25)
│       └─ Manager, Field Support (12-15)
│
├─ VP Home Office Analytics & Activity Hub
│   ├─ Senior Director, Activity Hub ⭐
│   │   ├─ Director, Product Management (3-4 PMs)
│   │   ├─ Director, Engineering (12-15 engineers)
│   │   └─ Director, Analytics & Data (4-5)
│   ├─ Senior Director, Merchandising & Planning
│   │   ├─ Director, Merchandising Analytics (18-22)
│   └─ Senior Director, Finance & Supply Chain
│       ├─ Director, Finance Analytics (18-22)
│       └─ Director, Executive Reporting (12-15)
│
├─ VP Analytics Capabilities & Data Science
│   ├─ Senior Director, Data Science & ML
│   │   ├─ Director, Predictive Analytics (15-20)
│   │   └─ Director, Advanced Analytics (10-12)
│   ├─ Senior Director, Analytics Engineering
│   │   ├─ Director, Metrics & Semantic Layer (18-22)
│   │   └─ Director, BI Platforms (10-12)
│   └─ Senior Director, Enablement
│       └─ Director, Self-Service Tools (8-10)
│
└─ VP Governance, Strategy & Transformation (Optional)
    ├─ Senior Director, Data Governance
    │   └─ Director, Data Quality (10-12)
    ├─ Senior Director, Portfolio Management
    │   └─ Director, Program Management (8-10)
    └─ Senior Director, Change & Adoption
        └─ Director, Training & Enablement (6-8)
```

---

## FINAL RECOMMENDATIONS

### **For Juan Galarraga:**

1. **Hire VPs First** — VP Data Platform and VP Home Office Analytics are critical paths for Activity Hub success.

2. **Invest in Activity Hub** — This is the strategic differentiator. Give it Senior Director-level ownership and dedicated resources.

3. **Communicate the Vision** — The "triple mandate" is complex. Over-communicate why we're doing this and how we'll succeed.

4. **Empower VPs** — Give them decision authority and hold them accountable for outcomes, not activities.

5. **Celebrate Migrations** — Every Tableau dashboard retired is progress. Make it visible.

### **For the Organization:**

1. **Start Small, Scale Fast** — Phase 1 is about foundations. Don't try to hire 300 people on day one.

2. **Standards First** — Invest in metrics governance early. It's easier to prevent inconsistency than fix it later.

3. **Platform Thinking** — Activity Hub, OMP, and MyWalmart are platforms, not projects. Fund them accordingly.

4. **Fail Fast on Innovation** — Track 3 (Innovate) should have a high failure rate. That's healthy.

5. **Measure What Matters** — Track migration %, platform adoption, and user satisfaction relentlessly.

---

**This design is a starting point, not a finish line.**

Expect to refine team charters, adjust headcount, and evolve governance as the organization matures. The key is to start with clarity and iterate based on what you learn.

---

*Document Version: 1.0*  
*Date: January 2026*  
*Owner: Juan Galarraga Organization*  
*Next Review: Quarterly*
