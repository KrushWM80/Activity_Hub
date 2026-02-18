# Visual Organizational Chart
## Store Operations Acceleration & Support — Data, Analytics & Platform Organization

---

## LEADERSHIP STRUCTURE

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              Juan Galarraga                                 │
│    SVP, Store Operations Acceleration & Support             │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬───────────────┬─────────────────┐
        │               │               │               │                 │
        ▼               ▼               ▼               ▼                 ▼
┌───────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────────────┐
│  VP #1        │ │  VP #2     │ │  VP #3     │ │  VP #4     │ │    VP #5        │
│               │ │            │ │            │ │            │ │                 │
│ Data Platform │ │   Store    │ │Home Office │ │ Analytics  │ │   Governance    │
│   & Eng       │ │  Analytics │ │ Analytics  │ │Capabilities│ │   Strategy &    │
│               │ │ & Products │ │ & Activity │ │& Data Sci  │ │ Transformation  │
│               │ │            │ │    Hub ⭐   │ │            │ │                 │
│               │ │            │ │            │ │            │ │    (Optional)   │
│  70-80 FTEs   │ │ 90-110 FTE │ │ 85-100 FTE │ │ 45-55 FTE  │ │   15-20 FTEs    │
└───────────────┘ └────────────┘ └────────────┘ └────────────┘ └─────────────────┘
```

---

## VP #1: DATA PLATFORM & ENGINEERING (70-80 FTEs)

```
┌─────────────────────────────────────────────────────┐
│         VP Data Platform & Engineering              │
│              Christopher Nuta (TBD)                 │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌────────────────────┐  ┌───────────────────────┐
│ Senior Director    │  │ Senior Director       │
│ Data Engineering   │  │ Platform Operations   │
│                    │  │                       │
│    40-45 FTEs      │  │     30-35 FTEs        │
└─────────┬──────────┘  └──────────┬────────────┘
          │                        │
    ┌─────┴─────┐           ┌──────┴──────┐
    ▼           ▼           ▼             ▼
┌─────────┐ ┌─────────┐ ┌────────┐ ┌──────────┐
│Director │ │Director │ │Director│ │ Director │
│  Data   │ │  Data   │ │  SRE & │ │   API    │
│Pipelines│ │Integra- │ │Reliab. │ │ Services │
│         │ │  tion   │ │        │ │          │
│ 20-25   │ │ 15-20   │ │ 10-15  │ │  8-10    │
└─────────┘ └─────────┘ └────────┘ └──────────┘

TEAMS:
├─ Data Pipelines: ETL/ELT, orchestration, scheduling
├─ Data Integration: Source system connectivity, APIs
├─ SRE & Reliability: 99.9% uptime, incident response
└─ API Services: Self-service data APIs, developer experience
```

---

## VP #2: STORE ANALYTICS & PRODUCTS (90-110 FTEs)

```
┌─────────────────────────────────────────────────────┐
│       VP Store Analytics & Products                 │
│                   (TBD)                             │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌────────────┐ ┌──────────┐ ┌──────────────┐
│Senior Dir  │ │Senior Dir│ │ Senior Dir   │
│    OMP     │ │MyWalmart │ │Store Ops     │
│            │ │ Analytics│ │  Analytics   │
│ 45-50 FTE  │ │20-25 FTE │ │  25-35 FTE   │
└─────┬──────┘ └────┬─────┘ └──────┬───────┘
      │             │               │
  ┌───┼───┐         │         ┌─────┴─────┐
  ▼   ▼   ▼         ▼         ▼           ▼
┌───┐┌───┐┌───┐  ┌─────┐  ┌──────┐  ┌──────┐
│Dir││Dir││Dir│  │ Dir │  │ Dir  │  │ Mgr  │
│PM ││Eng││Ana│  │Mobi-│  │Labor │  │Field │
│   ││   ││   │  │le Pr│  │& Exe │  │Supp. │
│4-5││15 ││10 │  │oduct│  │cution│  │      │
└───┘└───┘└───┘  └─────┘  └──────┘  └──────┘

KEY PRODUCTS:
├─ Ops Metrics Portal (OMP): Primary Store analytics platform
├─ MyWalmart Mobile: Field visualization for associates
└─ Store Operations Analytics: Labor, inventory, execution insights
```

---

## VP #3: HOME OFFICE ANALYTICS & ACTIVITY HUB ⭐ (85-100 FTEs)

```
┌─────────────────────────────────────────────────────────┐
│    VP Home Office Analytics & Activity Hub             │
│                      (TBD)                              │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
┌──────────────┐ ┌────────────┐ ┌────────────────┐
│Senior Dir    │ │Senior Dir  │ │ Senior Dir     │
│ Activity Hub │ │Merchandi-  │ │ Finance &      │
│   ⭐⭐⭐       │ │sing & Plan.│ │ Supply Chain   │
│  30-35 FTE   │ │ 25-30 FTE  │ │   30-35 FTE    │
└──────┬───────┘ └─────┬──────┘ └────────┬───────┘
       │               │                 │
  ┌────┼────┬──────┐   │           ┌─────┴─────┐
  ▼    ▼    ▼      ▼   ▼           ▼           ▼
┌───┐┌───┐┌───┐ ┌────┐┌───┐     ┌─────┐   ┌────────┐
│Dir││Dir││Dir│ │Mgr ││Dir│     │ Dir │   │  Dir   │
│PM ││Eng││Ana│ │UX &││Mer│     │Fin. │   │  Exec  │
│   ││   ││   │ │Des.││Ana│     │ Ana.│   │  Rpt   │
│3-4││12 ││4-5│ │2-3 ││18 │     │18-22│   │  12-15 │
└───┘└───┘└───┘ └────┘└───┘     └─────┘   └────────┘

★ ACTIVITY HUB: STRATEGIC PLATFORM ★
Purpose: Unified analytics for Home Office
Goal: Consolidate Tableau, PowerBI, manual reports
Target: 5,000+ MAU by end of Phase 3
Investment: 30-35 FTEs dedicated to platform success
```

---

## VP #4: ANALYTICS CAPABILITIES & DATA SCIENCE (45-55 FTEs)

```
┌─────────────────────────────────────────────────────┐
│   VP Analytics Capabilities & Data Science          │
│                    (TBD)                            │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌────────────────────┐  ┌──────────────────┐
│ Senior Director    │  │ Senior Director  │
│ Data Science & ML  │  │Analytics Eng.    │
│                    │  │                  │
│    25-30 FTEs      │  │    20-25 FTEs    │
└─────────┬──────────┘  └──────────┬───────┘
          │                        │
    ┌─────┴─────┐           ┌──────┴──────┐
    ▼           ▼           ▼             ▼
┌─────────┐ ┌─────────┐ ┌────────┐ ┌──────────┐
│Director │ │Principal│ │Director│ │ Director │
│Predict. │ │   Data  │ │Metrics │ │    BI    │
│Analytic │ │Scientist│ │Semantic│ │Platforms │
│         │ │         │ │ Layer  │ │          │
│ 15-20   │ │  10-12  │ │ 18-22  │ │  10-12   │
└─────────┘ └─────────┘ └────────┘ └──────────┘

HORIZONTAL CAPABILITIES:
├─ Data Science: ML models, predictive analytics
├─ Analytics Engineering: DBT, semantic layer, metrics
└─ Visualization: Standards, best practices, enablement
```

---

## VP #5: GOVERNANCE, STRATEGY & TRANSFORMATION (15-20 FTEs)

```
┌─────────────────────────────────────────────────────┐
│  VP Governance, Strategy & Transformation           │
│                   (Optional)                        │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌────────────┐ ┌──────────┐ ┌──────────────┐
│Senior Dir  │ │Senior Dir│ │ Senior Dir   │
│   Data     │ │Portfolio │ │  Change &    │
│ Governance │ │   Mgmt   │ │  Adoption    │
│            │ │          │ │              │
│ 10-12 FTE  │ │ 8-10 FTE │ │   5-8 FTE    │
└─────┬──────┘ └────┬─────┘ └──────┬───────┘
      │             │               │
      ▼             ▼               ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Director │  │ Director │  │  Change  │
│   Data   │  │ Program  │  │ Managers │
│ Quality  │  │   Mgmt   │  │ Training │
│          │  │          │  │          │
│  10-12   │  │  8-10    │  │   5-8    │
└──────────┘  └──────────┘  └──────────┘

GOVERNANCE FUNCTIONS:
├─ Data Governance: Metric definitions, quality standards
├─ Portfolio Mgmt: RUN/TRANSFORM/INNOVATE balance
└─ Change Management: Training, adoption, communication
```

---

## FULL ORGANIZATION HEADCOUNT SUMMARY

```
┌────────────────────────────────────────────────────────────┐
│                 JUAN GALARRAGA (SVP)                       │
│                         1 FTE                              │
└────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼───┐          ┌───▼───┐         ┌───▼───┐
    │VP #1  │          │VP #2  │         │VP #3  │
    │  70-80│          │90-110 │         │85-100 │
    └───────┘          └───────┘         └───────┘
        │                  │                  │
    ┌───▼───┐          ┌───▼───┐         
    │VP #4  │          │VP #5  │         
    │ 45-55 │          │ 15-20 │         
    └───────┘          └───────┘         

TOTAL ORGANIZATION: 310-370 FTEs
TARGET STEADY STATE: ~335 FTEs
```

### **Breakdown by Management Level**

| Level | Count | Average Span | Total FTEs Managed |
|---|---:|---:|---:|
| **SVP** (Juan) | 1 | 4-5 VPs | 335 total org |
| **VP** | 4-5 | 3-4 Senior Directors each | 60-85 each |
| **Senior Director** | 12-15 | 2-4 Directors each | 20-35 each |
| **Director** | 35-45 | 3-6 Managers/leads each | 5-15 each |
| **Manager** | 60-80 | 5-8 ICs each | 5-8 each |
| **Individual Contributors** | 180-220 | n/a | n/a |

---

## TEAM INTERACTION MAP

```
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS STAKEHOLDERS                    │
│  Stores Directors | Merchandising | Finance | Supply Chain  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Requests & Requirements
                            ▼
              ┌─────────────────────────┐
              │   PRODUCT TEAMS         │
              │  (VP Store Analytics &  │
              │   VP Home Office Analyt)│
              └────────────┬────────────┘
                           │
                           │ Consumes Platform Services
                           ▼
              ┌─────────────────────────┐
              │   PLATFORM TEAMS        │
              │ (VP Data Platform & Eng)│
              └────────────┬────────────┘
                           │
                           │ Leverages Capabilities
                           ▼
              ┌─────────────────────────┐
              │  CAPABILITY TEAMS       │
              │ (VP Analytics Capabilit)│
              └────────────┬────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌───────────────┐                  ┌──────────────────┐
│  GOVERNANCE   │◄────Standards────►│   ALL TEAMS     │
│  (VP Gov/PMO) │                  │                 │
└───────────────┘                  └──────────────────┘
```

---

## RACI: WHO DOES WHAT

```
                    │ Platform │ Store  │ Home Office│ Capabil.│Govern.│
                    │   VP     │  VP    │    VP      │   VP    │  VP   │
────────────────────┼──────────┼────────┼────────────┼─────────┼───────┤
MAINTAIN LEGACY     │          │        │            │         │       │
├ Tableau uptime    │    C     │  R/A   │    R/A     │    C    │   I   │
├ User support      │    I     │  A/R   │    A/R     │    C    │   C   │
────────────────────┼──────────┼────────┼────────────┼─────────┼───────┤
MODERNIZE PLATFORMS │          │        │            │         │       │
├ OMP development   │    C     │  R/A   │     I      │    C    │   I   │
├ Activity Hub dev  │    C     │   I    │    R/A     │    C    │   I   │
├ Data migration    │   R/A    │   C    │     C      │    C    │   I   │
────────────────────┼──────────┼────────┼────────────┼─────────┼───────┤
INNOVATE NEW        │          │        │            │         │       │
├ Data science      │    C     │   C    │     C      │   R/A   │   I   │
├ Self-service      │    C     │   C    │     C      │   R/A   │   A   │
────────────────────┼──────────┼────────┼────────────┼─────────┼───────┤
GOVERNANCE          │          │        │            │         │       │
├ Metric defs       │    C     │   C    │     C      │    C    │  R/A  │
├ Data quality      │   R/A    │   C    │     C      │    C    │   A   │
────────────────────┴──────────┴────────┴────────────┴─────────┴───────┘

R = Responsible (does the work)
A = Accountable (owns the outcome)
C = Consulted (provides input)
I = Informed (kept in the loop)
```

---

## GOVERNANCE FORUMS

```
┌─────────────────────────────────────────────────────────────┐
│              QUARTERLY BUSINESS REVIEW                      │
│  Juan + All VPs + Business Stakeholder Directors            │
│  Purpose: Strategic alignment, roadmap, resource allocation │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
│   WEEKLY     │ │  BI-WEEKLY   │ │    MONTHLY      │
│  PLATFORM    │ │     DATA     │ │ ARCHITECTURE    │
│   COUNCIL    │ │  GOVERNANCE  │ │  REVIEW BOARD   │
│              │ │   COUNCIL    │ │                 │
│ All VPs      │ │ SD from each │ │ Tech leads from │
│ + Key SDs    │ │ VP + bizstk  │ │   all VPs       │
│              │ │              │ │                 │
│ Operations   │ │ Standards &  │ │ Technical       │
│ Coordination │ │ Metrics      │ │ Decisions       │
└──────────────┘ └──────────────┘ └─────────────────┘
```

---

## CAREER PATHS

```
INDIVIDUAL CONTRIBUTOR TRACK          MANAGEMENT TRACK
──────────────────────────           ────────────────────

IC7 - Principal                      L10 - SVP (Juan)
      (Staff+, Architecture)                │
      │                                     │
IC6 - Staff                          L9  - VP
      (Technical Leadership)               │
      │                                     │
IC5 - Senior                         L8  - Senior Director
      (Independent Execution)              │
      │                                     │
IC4 - Mid-Level                      L7  - Director
      (Solid Contributor)                  │
      │                                     │
IC3 - Junior                         L6  - Manager
      (Needs Guidance)                     │
      │                                     │
IC2 - Entry                          L5  - Team Lead
      (Learning)                           │

DUAL-TRACK: Can move between IC and Management
EXPERTISE: Deep specialists valued as much as managers
PROGRESSION: Clear criteria for each level
```

---

## COLLABORATION PATTERNS

### **Sprint Cycle (2-week sprints)**

```
Week 1                              Week 2
Mon Tue Wed Thu Fri                Mon Tue Wed Thu Fri
 │                                  │               │
 ▼                                  ▼               ▼
Sprint                         Mid-Sprint      Sprint End
Planning                         Check-in        Demo & Retro
 │                                  │               │
 └──────────────────────────────────┴───────────────┘
               Execute & Collaborate
```

### **Platform-Product Sync Pattern**

```
Product Team needs data feature
        │
        ▼
    Log request in Platform backlog
        │
        ▼
Weekly Platform Council prioritizes
        │
        ▼
Platform Team implements
        │
        ▼
Product Team validates
        │
        ▼
    Deploy to production
```

---

## TOOLS & SYSTEMS

```
┌─────────────────────────────────────────────────────────┐
│                   DATA PLATFORM                         │
│  BigQuery | GCP | DBT | Airflow | APIs                  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
┌────────────┐ ┌──────────┐ ┌──────────────┐
│    OMP     │ │ Activity │ │  MyWalmart   │
│  (Stores)  │ │   Hub    │ │   (Mobile)   │
│            │ │  (Home   │ │              │
│            │ │  Office) │ │              │
└────────────┘ └──────────┘ └──────────────┘
```

**Legacy (to be decommissioned):**
- Tableau
- PowerBI
- Manual PowerPoint processes

**Modern Stack:**
- **Data**: BigQuery, GCP, DBT, Airflow
- **Analytics**: Activity Hub, OMP, MyWalmart
- **ML**: Python, TensorFlow, MLOps platforms
- **Collaboration**: Jira, Confluence, Slack, GitHub

---

## SUMMARY: ORGANIZATION AT A GLANCE

| Dimension | Value |
|---|---|
| **Total FTEs (Steady State)** | 320-350 |
| **Number of VPs** | 4-5 |
| **Number of Senior Directors** | 12-15 |
| **Number of Directors** | 35-45 |
| **Number of Managers** | 60-80 |
| **Individual Contributors** | 180-220 |
| **Contractor Mix** | 25% at steady state |
| **Annual Cost (Steady State)** | $68M-76M |
| **Key Platforms** | Activity Hub, OMP, MyWalmart |
| **Users Served** | 5,000+ (thousands in field) |
| **Governance Forums** | 4 (Weekly, Bi-weekly, Monthly, Quarterly) |

---

*For detailed roles, responsibilities, and transition plans, see:*
- *[ORGANIZATIONAL_DESIGN_FULL.md](ORGANIZATIONAL_DESIGN_FULL.md)*
- *[STAFFING_AND_FINANCIALS.md](STAFFING_AND_FINANCIALS.md)*
- *[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)*
