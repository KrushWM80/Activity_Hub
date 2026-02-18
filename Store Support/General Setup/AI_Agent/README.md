# 🤖 Walmart AI Policy & Governance

**Last Updated:** November 25, 2025  
**Purpose:** Central resource for AI/ML compliance, ethical AI use, and GenAI governance at Walmart

---

## 🎯 Overview

Walmart has comprehensive policies governing the use of Artificial Intelligence (AI), Machine Learning (ML), and Generative AI (GenAI). **All AI/ML solutions must comply with these policies** and complete required assessments before production deployment.

This guide provides quick access to AI policies, standards, support contacts, and compliance resources.

---

## 📚 Key AI Policies & Standards

### Core AI Governance Policies

1. **Global Artificial Intelligence, Machine Learning, and Automated Decisioning Policy (DC-DG-06)**
   - **Purpose:** Establishes global standards for responsible AI/ML development and deployment
   - **Scope:** All AI, ML, and automated decisioning systems
   - **Access:** [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)
   - **What it covers:**
     - AI development lifecycle requirements
     - Risk assessment and mitigation
     - Model governance and monitoring
     - Ethical AI principles
     - Automated decisioning safeguards

2. **Generative Artificial Intelligence (GenAI) Usage Standard (DC-DG-06-02)**
   - **Purpose:** Specific standards for GenAI tools (ChatGPT, Claude, Copilot, etc.)
   - **Scope:** All generative AI applications
   - **Access:** [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)
   - **What it covers:**
     - Approved GenAI tools and platforms
     - Data privacy and confidentiality requirements
     - Prompt engineering best practices
     - Output validation and review
     - Prohibited use cases

3. **AI Governance Standard for Audio, Image and Video Content Generation (DC-DG-US-06-01)**
   - **Purpose:** Governance for AI-generated multimedia content
   - **Scope:** AI systems generating audio, images, or video
   - **Access:** [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)
   - **What it covers:**
     - Content generation standards
     - Disclosure requirements (AI-generated labels)
     - Copyright and IP considerations
     - Deepfake prevention
     - Quality and accuracy standards

4. **AI Governance Risk Awareness Guideline (DC-DG-US-06-00-01)**
   - **Purpose:** Risk awareness and mitigation for AI projects
   - **Scope:** All AI/ML initiatives
   - **Access:** [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)
   - **What it covers:**
     - Common AI risks (bias, fairness, transparency)
     - Risk identification framework
     - Mitigation strategies
     - Testing and validation approaches

---

## 🔗 Key Resources & Portals

### Primary AI Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| **Walmart AI Portal** | [ai.walmart.com](https://ai.walmart.com) | Central hub for AI tools, resources, and initiatives |
| **AI Governance Microlearning Hub** | [wmlink/AICompliance](wmlink/AICompliance) | Training modules and compliance guidance |
| **Data Governance Library** | [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary) | All AI policies and standards |
| **Global Tech Policy** | [wmlink/policy](wmlink/policy) | Comprehensive technology policies |

---

## 📞 Support Contacts

### AI-Related Questions

| Topic | Contact | Purpose |
|-------|---------|---------|
| **AI.walmart.com Portal** | [HelpwithAI@walmart.com](mailto:HelpwithAI@walmart.com) | Questions about ai.walmart.com platform |
| **AI Policy & Compliance** | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) | Global AI Policy questions, AI Compliance Assessments, ethical AI use |
| **GenAI Legal Review** | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) | Legal review for GenAI applications |
| **Enterprise Privacy Risk Assessment** | Privacy Team (via APM/SSP) | EPRA for AI projects handling sensitive data |

---

## 📋 Required AI Compliance Assessments

If your solution uses AI, ML, or GenAI, you may need to complete one or more of these assessments:

### 1. AI Compliance Assessment
**When Required:**
- All AI/ML models used in production
- Automated decisioning systems
- Any system using predictive analytics

**What's Assessed:**
- Model purpose and use case
- Data sources and quality
- Bias and fairness testing
- Model explainability
- Monitoring and governance

**How to Initiate:**
- Contact: [ModelReview@walmart.com](mailto:ModelReview@walmart.com)
- Submit via AI governance portal (if available)
- Include in APM/SSP process

---

### 2. Enterprise Privacy Risk Assessment (EPRA)
**When Required:**
- AI/ML systems processing PII (Personally Identifiable Information)
- Systems with privacy implications
- Triggered automatically during APM process if data classification includes PII

**What's Assessed:**
- Data collection and usage
- User consent mechanisms
- Data retention and deletion
- Privacy controls
- Third-party data sharing

**How to Initiate:**
- Triggered automatically via APM Data Classification Assessment (DCA)
- Complete via OneTrust platform
- Part of SSP process

---

### 3. GenAI Legal Review
**When Required:**
- Applications using generative AI (ChatGPT, Claude, Copilot, etc.)
- AI-generated content used in customer-facing applications
- GenAI systems with IP or copyright considerations

**What's Assessed:**
- Legal compliance
- IP and copyright considerations
- Terms of service compliance
- Liability considerations
- Disclosure requirements

**How to Initiate:**
- Contact: [ModelReview@walmart.com](mailto:ModelReview@walmart.com)
- Submit early in project lifecycle
- Include in SSP documentation

---

## 🛤️ AI Solutions in Production Path

### When AI/ML is Part of Your Solution:

Your **Production Path timeline extends by 2-4 weeks** to accommodate AI-specific assessments:

```
Standard Path:     DQC → Team Rosters → APM → SSP → Azure (5-10 weeks)
AI/ML Solution:    DQC → Team Rosters → APM → AI Assessments → SSP → Azure (7-14 weeks)
```

### Integration with Production Path Steps:

#### **Step 3: APM Setup (Week 2-5)**
- [ ] Declare AI/ML usage in APM registration
- [ ] Document AI/ML models and purpose
- [ ] Complete Data Classification Assessment (triggers EPRA if PII)

#### **Between Step 3 & 4: AI Compliance Assessments (Week 5-7)**
- [ ] **AI Compliance Assessment** - Submit to ModelReview@walmart.com
- [ ] **EPRA** - Complete via OneTrust (if triggered)
- [ ] **GenAI Legal Review** - If using GenAI tools

#### **Step 4: SSP Process (Week 7-9)**
- [ ] Reference AI compliance assessment results in SSP
- [ ] Document AI/ML model governance
- [ ] Include AI-specific security controls
- [ ] Demonstrate bias and fairness testing

---

## ✅ AI Solution Compliance Checklist

Use this checklist to ensure AI compliance throughout your project:

### Phase 1: Planning & Design
- [ ] Review all applicable AI policies (DC-DG-06 series)
- [ ] Complete AI Governance Microlearning: [wmlink/AICompliance](wmlink/AICompliance)
- [ ] Identify which AI assessments are required
- [ ] Plan timeline with 2-4 weeks buffer for AI assessments
- [ ] Contact ModelReview@walmart.com early for guidance

### Phase 2: Development
- [ ] Implement bias and fairness testing
- [ ] Document model training data sources
- [ ] Establish model explainability mechanisms
- [ ] Create model monitoring plan
- [ ] Document AI ethics considerations

### Phase 3: Compliance Assessments
- [ ] Complete AI Compliance Assessment
- [ ] Complete EPRA (if PII data)
- [ ] Complete GenAI Legal Review (if applicable)
- [ ] Address all findings and recommendations
- [ ] Document assessment completion in APM/SSP

### Phase 4: Production Deployment
- [ ] Implement all required AI governance controls
- [ ] Establish ongoing model monitoring
- [ ] Set up bias and drift detection
- [ ] Create model retraining procedures
- [ ] Document AI disclosure requirements (if customer-facing)

### Phase 5: Ongoing Operations
- [ ] Monitor model performance continuously
- [ ] Conduct regular bias audits
- [ ] Retrain models as needed
- [ ] Update assessments for significant model changes
- [ ] Complete annual AI compliance reviews

---

## 🔑 Key AI Principles at Walmart

### Ethical AI Framework:

1. **Fairness** - AI systems must not discriminate
2. **Transparency** - AI decisions must be explainable
3. **Accountability** - Clear ownership and responsibility
4. **Privacy** - Protect customer and associate data
5. **Safety** - AI systems must be secure and reliable
6. **Human Oversight** - Humans in the loop for critical decisions

### Prohibited AI Use Cases:

❌ **DO NOT use AI for:**
- Discriminatory practices (hiring, promotions based on protected classes)
- Surveillance without consent and legal basis
- Manipulative or deceptive practices
- Systems without human oversight for high-stakes decisions
- Sharing confidential Walmart data with external AI tools (without approval)

✅ **Approved AI Use Cases (with proper compliance):**
- Productivity enhancement (coding assistance, documentation)
- Data analysis and insights
- Demand forecasting and optimization
- Customer experience improvements
- Operational efficiency
- Internal process automation

---

## 📖 AI Training & Resources

### Required Training:
- [ ] **AI Governance Microlearning Hub**: [wmlink/AICompliance](wmlink/AICompliance)
- [ ] Complete all modules before starting AI project
- [ ] Review annually for updates

### Additional Resources:
- **AI Best Practices** - Available on ai.walmart.com
- **GenAI Prompt Engineering** - Guidelines in GenAI Usage Standard
- **Model Development Guides** - Contact ModelReview@walmart.com
- **AI Use Case Examples** - Shared on ai.walmart.com

---

## 🚨 Common AI Compliance Issues & Solutions

| Issue | Solution |
|-------|----------|
| Using ChatGPT with confidential data | Use approved Walmart GenAI tools only; never share confidential data with external tools |
| Skipping AI Compliance Assessment | Contact ModelReview@walmart.com early; required for all AI/ML in production |
| Model bias not tested | Implement bias testing framework; document in AI Compliance Assessment |
| No model monitoring plan | Establish continuous monitoring; include drift detection and retraining triggers |
| Missing EPRA for PII data | Ensure APM DCA correctly identifies PII; complete EPRA via OneTrust |
| GenAI output used without review | Implement human review process; document in GenAI Legal Review |

---

## 📝 AI Documentation Requirements

For AI/ML solutions, maintain these additional documents:

### Required Documentation:
1. **Model Card** - Model purpose, training data, performance metrics
2. **Bias Testing Results** - Fairness analysis and mitigation
3. **Explainability Documentation** - How model decisions can be explained
4. **Data Lineage** - Training data sources and quality
5. **Monitoring Plan** - Ongoing model performance tracking
6. **Retraining Procedures** - When and how to retrain
7. **Incident Response** - What to do if model behaves unexpectedly

### Where to Store:
- Reference in APM record
- Attach to SSP submission
- Include in project documentation
- Share with ModelReview@walmart.com

---

## 🔄 AI Governance Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PLAN: Review policies, identify assessments needed       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. DEVELOP: Build with ethics in mind, test for bias        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. ASSESS: Complete AI Compliance, EPRA, GenAI reviews      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. APPROVE: Obtain all required approvals (APM/SSP)         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. DEPLOY: Implement with governance controls in place      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. MONITOR: Continuous monitoring, bias audits, retraining  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. REVIEW: Annual compliance review, update documentation   │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Best Practices for AI Compliance

### Before Starting Your AI Project:
1. ✅ Complete AI Governance Microlearning
2. ✅ Contact ModelReview@walmart.com for early guidance
3. ✅ Review all applicable policies
4. ✅ Plan realistic timeline (include assessment time)
5. ✅ Identify data sources and ensure data quality

### During Development:
1. ✅ Build explainability into models from the start
2. ✅ Test for bias at every stage
3. ✅ Document everything (data, decisions, testing)
4. ✅ Use approved tools and platforms only
5. ✅ Keep ModelReview team informed of progress

### Before Production:
1. ✅ Complete all required assessments
2. ✅ Implement all governance controls
3. ✅ Establish monitoring dashboards
4. ✅ Train team on AI policies
5. ✅ Document incident response procedures

### In Production:
1. ✅ Monitor continuously for drift and bias
2. ✅ Regular model performance reviews
3. ✅ Quick response to anomalies
4. ✅ Maintain documentation updates
5. ✅ Annual compliance reviews

---

## 📞 Quick Reference: Who to Contact

| Question About | Contact |
|----------------|---------|
| AI portal access or tools | [HelpwithAI@walmart.com](mailto:HelpwithAI@walmart.com) |
| Policy interpretation | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) |
| AI Compliance Assessment | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) |
| GenAI legal questions | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) |
| EPRA (privacy) | Privacy Team via OneTrust or APM |
| Training and resources | AI Governance Microlearning Hub |
| APM/SSP for AI solutions | APM: apmmailbox@wal-mart.com, SSP: Secrisk@wal-mart.com |

---

## 🎓 AI Compliance Training Path

### Required for All AI Projects:
1. **AI Governance Microlearning Hub** - [wmlink/AICompliance](wmlink/AICompliance)
2. **Technology and Data Compliance Policy** - [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)
3. **Project-specific guidance** - From ModelReview@walmart.com

### Recommended:
- Responsible AI principles training
- Bias and fairness in AI
- Model explainability techniques
- AI security and privacy
- GenAI best practices (if using GenAI)

---

## 🔄 Keeping This Guide Current

AI policy and governance is evolving rapidly. Stay current by:
- [ ] Reviewing ai.walmart.com monthly for updates
- [ ] Subscribing to AI policy updates
- [ ] Attending AI governance office hours
- [ ] Monitoring ModelReview@walmart.com communications
- [ ] Completing annual AI compliance refresher training

---

**💡 Remember:** AI compliance is not a blocker—it's a framework for building ethical, responsible, and effective AI solutions. Start early, engage with ModelReview team, and build compliance into your development process from day one.

**Questions?** Contact [ModelReview@walmart.com](mailto:ModelReview@walmart.com) - The AI governance team is here to help!
