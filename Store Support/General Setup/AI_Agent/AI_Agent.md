# 🤖 AI Agent Implementation & Policy Guide

**Last Updated:** January 23, 2026  
**Purpose:** Comprehensive guide for AI Agent development, governance, and compliance at Walmart, incorporating learnings from Projects in Stores Dashboard

---

## 🎯 Overview

This document serves as a central resource for building, deploying, and governing AI Agents at Walmart. It combines Walmart's AI governance policies with practical learnings from the Projects in Stores Dashboard (Sparky AI Agent) implementation.

**Key Topics:**
- AI Agent architecture and design patterns
- Walmart AI governance and compliance requirements
- Implementation best practices from Sparky AI
- Integration strategies with enterprise systems
- Security, monitoring, and operational considerations

---

## 📚 Core AI Governance Policies at Walmart

### 1. Global Artificial Intelligence, Machine Learning, and Automated Decisioning Policy (DC-DG-06)
- **Purpose:** Establishes global standards for responsible AI/ML development and deployment
- **Scope:** All AI, ML, and automated decisioning systems
- **Access:** [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)
- **Key Requirements:**
  - AI development lifecycle requirements
  - Risk assessment and mitigation
  - Model governance and monitoring
  - Ethical AI principles
  - Automated decisioning safeguards

### 2. Generative Artificial Intelligence (GenAI) Usage Standard (DC-DG-06-02)
- **Purpose:** Specific standards for GenAI tools (ChatGPT, Claude, Copilot, etc.)
- **Scope:** All generative AI applications
- **Key Requirements:**
  - Approved GenAI tools and platforms
  - Data privacy and confidentiality requirements
  - Prompt engineering best practices
  - Output validation and review
  - Prohibited use cases

### 3. AI Governance Risk Awareness Guideline (DC-DG-US-06-00-01)
- **Purpose:** Risk awareness and mitigation for AI projects
- **Key Requirements:**
  - Common AI risks (bias, fairness, transparency)
  - Risk identification framework
  - Mitigation strategies
  - Testing and validation approaches

---

## 🏗️ AI Agent Architecture

### Design Pattern: Sparky AI Agent (Proven Implementation)

The Projects in Stores Dashboard implements a production-ready AI Agent (Sparky) that demonstrates key architectural patterns:

```
┌──────────────────────────────────────────────────┐
│           Frontend (User Interface)               │
│  - Query Input                                    │
│  - Context Management                            │
│  - Result Display                                │
└────────────────┬─────────────────────────────────┘
                 │ HTTP/REST API
                 │ POST /api/ai/query
                 │
┌────────────────▼─────────────────────────────────┐
│        AI Agent Service (ai_agent.py)             │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Query Processor                             │ │
│  │ - Process natural language query            │ │
│  │ - Extract intent and entities               │ │
│  │ - Context awareness                         │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Search Engine                               │ │
│  │ - Search up to 100 matching results         │ │
│  │ - Semantic matching on titles/descriptions  │ │
│  │ - Rank by relevance                         │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Auto-Apply Logic                            │ │
│  │ - Single match → Automatically apply        │ │
│  │ - Multiple matches → Ask for clarification  │ │
│  │ - No matches → Suggest alternatives         │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Response Generator                          │ │
│  │ - Mock responses (production default)       │ │
│  │ - OpenAI GPT-4 (optional)                   │ │
│  │ - Azure OpenAI (optional)                   │ │
│  └─────────────────────────────────────────────┘ │
└────────────────┬─────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐   ┌──────▼────────┐
│  Database    │   │  AI Models    │
│  Service     │   │  (optional)   │
│              │   │               │
│ - BigQuery   │   │ - OpenAI      │
│ - SQL        │   │ - Azure OAI   │
│ - Filters    │   │ - Mock Resp   │
└──────────────┘   └───────────────┘
```

### Key Components

#### 1. Query Processor
**Learning from Sparky:** Natural language queries are processed through multiple stages:

```python
AIAgent (Sparky Implementation)
├── Query processor (_process_query)
│   └── Extract intent and entities
├── Context extractor (_extract_context)
│   └── Understand filter state and scope
├── Project search
│   └── Search up to 100 titles for matches
├── Auto-apply logic
│   └── Only when 1 unique match found
├── Multi-match handler
│   └── Shows list, asks for clarification
├── Mock responses (production default)
│   └── Emoji-rich, context-aware responses
└── Help system (lists all capabilities)
    └── Guides users on available queries
```

**Best Practice:** Always implement a mock response system first, then layer on real AI/ML models. This provides:
- Fast development and testing
- Fallback if AI service is unavailable
- Cost control (no API calls during dev)
- Context-aware responses without external APIs

#### 2. Data Integration
**Learning from Sparky:** AI agents need tight integration with data systems:

```
AI Agent ← → Database Service ← → BigQuery
  ├── Real-time filter state
  ├── Search context
  ├── Historical queries
  └── User preferences
```

**Key Requirements:**
- Fast query execution (< 100ms for search)
- Caching for common queries
- Filter state management
- Context passing between components

#### 3. Response Generation Options

**Option 1: Mock Responses (Recommended for MVP)**
- ✅ No external dependencies
- ✅ Fast (< 100ms)
- ✅ Cost-free
- ✅ Emoji-rich and contextual
- ✅ Perfect for development/testing

**Option 2: OpenAI GPT-4**
- ✅ Advanced natural language understanding
- ✅ Context-aware responses
- ⚠️ Requires API key and cost
- ⚠️ Need OPENAI_API_KEY environment variable
- ⚠️ May have latency (200-500ms typical)

**Option 3: Azure OpenAI**
- ✅ Enterprise-grade security
- ✅ Compliance with Walmart policies
- ✅ No data sent to OpenAI
- ⚠️ Requires Azure setup
- ⚠️ Additional cost

**Production Sparky Implementation:**
```python
# Start with mock, layer on OpenAI
OPENAI_API_KEY=sk-...     # Only if using real OpenAI
OPENAI_MODEL=gpt-4        # GPT-4 or GPT-3.5-turbo
```

---

## 💻 Implementation Patterns from Sparky

### Pattern 1: Contextual Query Processing

```python
# Sparky's approach to handling queries
def process_ai_query(query: str, context: dict):
    """
    Process natural language query with contextual awareness
    
    Args:
        query: User's natural language query (e.g., "Sidekick")
        context: Current filter state and scope
        
    Returns:
        - Single match: Automatically apply filter + response
        - Multiple matches: Show list + ask clarification
        - No matches: Suggest alternatives + help
    """
    # 1. Extract intent and entities
    intent = extract_intent(query)
    entities = extract_entities(query)
    
    # 2. Search database with context
    matches = search_projects(query, limit=100, context=context)
    
    # 3. Apply auto-logic
    if len(matches) == 1:
        return {
            "action": "auto_apply",
            "filter": matches[0],
            "response": f"Found it! 🎯 Filtering to {matches[0]}"
        }
    elif len(matches) > 1:
        return {
            "action": "clarify",
            "suggestions": matches[:10],  # Top 10
            "response": f"Found {len(matches)} matches. Which one?"
        }
    else:
        return {
            "action": "suggest",
            "alternatives": suggest_alternatives(query),
            "response": "No exact match found. Try these instead?"
        }
```

### Pattern 2: Filter State Management

**Learning:** AI agents need to understand and maintain filter state:

```
User Interaction Flow:
1. User opens dashboard (no filters)
2. User applies Division filter = "EAST"
3. User asks Sparky: "Show me sidekick projects"
4. Sparky applies filters in context of DIVISION=EAST
5. Results only show sidekick projects in EAST division
```

**Implementation:**
- Frontend maintains current filter state
- Pass filter state to AI agent with each query
- AI agent respects existing filters
- AI agent can suggest additional filters

### Pattern 3: Mock Response Strategy

**Sparky's Mock Responses (Production):**
```python
MOCK_RESPONSES = {
    "single_match": "Found it! 🎯 Filtering to {project_name}",
    "multiple_matches": "Found {count} matches. Which one did you mean?",
    "no_match": "Hmm, couldn't find '{query}'. Try 'Help' for suggestions",
    "help": "I can search for projects by name, type, or team. What are you looking for?"
}
```

**Key Benefits:**
- Response time: < 100ms
- No API dependency
- Graceful error handling
- User-friendly formatting
- Emoji enhancement

---

## � Feedback Loops & Continuous Improvement

### Why AI Agents Need Feedback Loops

AI agents require continuous feedback to improve:
- **Learn from errors:** Track when responses don't match user intent
- **Identify gaps:** Find missing features or capabilities
- **Detect patterns:** Recognize recurring issues
- **Measure effectiveness:** Validate improvements worked
- **Build trust:** Show users their input drives improvements

### Feedback Loop Architecture (from Code Puppy)

The Projects in Stores Dashboard implements a production-ready feedback loop:

```
USER FEEDBACK
    ↓
[Feedback Widget] ← User clicks "?" button
    │
    ├─ Category: UI, AI, Data, Performance, Other
    ├─ Rating: 1-5 stars with emojis 😞 😄 🤩
    ├─ Comments: Detailed feedback text
    └─ Context: Current filters, URL, browser
    ↓
POST /api/feedback
    ↓
[Backend Storage]
    │
    ├─ Save to database
    ├─ Send email notification
    └─ Queue for analysis
    ↓
[AI Analysis] (Optional/Future)
    │
    ├─ Extract root cause
    ├─ Match against known patterns
    ├─ Propose fix
    └─ Assess priority/risk
    ↓
[Admin Dashboard]
    │
    ├─ Review proposed fix
    ├─ Approve / Deny / Hold
    └─ View code diff
    ↓
[Auto-Fix Execution]
    │
    ├─ Apply code changes
    ├─ Restart service
    └─ Log change
    ↓
[Monitoring]
    │
    ├─ Track repeat reports (should ↓)
    ├─ Monitor satisfaction (should ↑)
    ├─ Measure fix effectiveness
    └─ Identify new patterns
    ↓
[Iteration]
    └─ Improve AI agent based on learnings
```

### Implementation: Feedback Widget (Frontend)

**Key Features:**
- Always-visible button (prominent, non-intrusive)
- Multi-step form (don't overwhelm with all questions at once)
- Emoji ratings (more engaging than numeric scales)
- Context capture (current state, URL, browser)
- Graceful degradation (thank user even if backend fails)

**Code Example:**
```javascript
// Step 1: Capture
<button onclick="openFeedback()">? Send Feedback</button>

// Step 2: Multi-step form
<form id="feedback-form">
    <!-- Step 1: Category -->
    <div id="step1">
        <p>What area would you like feedback on?</p>
        <input type="radio" name="category" value="Dashboard UI"> UI
        <input type="radio" name="category" value="AI Assistant"> AI
        <input type="radio" name="category" value="Data Quality"> Data
        <input type="radio" name="category" value="Performance"> Performance
        <button onclick="nextStep()">Next</button>
    </div>
    
    <!-- Step 2: Rating & Comments -->
    <div id="step2" style="display:none;">
        <p>How would you rate this?</p>
        <input type="radio" name="rating" value="5"> 🤩 Excellent
        <input type="radio" name="rating" value="4"> 😄 Great
        <input type="radio" name="rating" value="3"> 😊 Good
        <input type="radio" name="rating" value="2"> 😐 Fair
        <input type="radio" name="rating" value="1"> 😞 Poor
        
        <textarea placeholder="Your feedback..."></textarea>
        <button type="submit">Submit</button>
    </div>
</form>

// Step 3: Submit with context
async function submitFeedback() {
    const data = {
        category: document.querySelector('input[name="category"]:checked').value,
        rating: parseInt(document.querySelector('input[name="rating"]:checked').value),
        comments: document.querySelector('textarea').value,
        timestamp: new Date().toISOString(),
        user_context: {
            current_filters: selectedFilters,
            url: window.location.href,
            projects_displayed: allData.length
        }
    };
    
    const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    // Graceful degradation
    alert('Thank you for your feedback!');
}
```

### Implementation: Feedback API (Backend)

**Endpoint:** `POST /api/feedback`

```python
class FeedbackSubmission(BaseModel):
    category: str  # UI, AI, Data, Performance, Other
    rating: int    # 1-5
    comments: str  # Detailed feedback
    timestamp: str  # ISO format
    user_context: dict  # Current state

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackSubmission):
    # 1. Validate
    if len(feedback.comments) < 10:
        raise ValueError("Comments must be at least 10 characters")
    
    # 2. Store
    feedback_record = {
        "feedback_id": generate_id(),
        "timestamp": feedback.timestamp,
        "category": feedback.category,
        "rating": feedback.rating,
        "comments": feedback.comments,
        "user_context": feedback.user_context,
        "status": "received"
    }
    db.feedback.insert_one(feedback_record)
    
    # 3. Notify team (email)
    send_email(
        to="team@example.com",
        subject=f"New {feedback.category} Feedback: Rating {feedback.rating}/5",
        body=f"Comments: {feedback.comments}"
    )
    
    # 4. Queue for analysis (if using AI)
    await queue_for_analysis(feedback_record)
    
    return {"status": "success", "feedback_id": feedback_record["feedback_id"]}
```

### Common Patterns to Auto-Fix

| Issue | Trigger Words | Fix |
|-------|---------------|-----|
| **Filter Conflict** | "0 results", "filter shows nothing" | Clear search when filter applied |
| **Duplicate Data** | "duplicate entries", "same item twice" | Add deduplication logic |
| **Performance** | "slow", "loading", "freeze" | Add caching, optimize queries |
| **Data Accuracy** | "wrong count", "missing data" | Verify data source, add validation |
| **UI Bug** | "button missing", "text cut off" | Fix responsive CSS, check layout |

### Measuring Effectiveness

**Metrics to Track:**
```
Feedback Analytics Dashboard:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Feedback: 47
Avg Rating: 4.3/5 (↑ 0.4 this month)
Repeat Reports (same issue): 2 (95% decrease after fix)
User Satisfaction Post-Fix: 92%
Fixes Implemented This Month: 8
Avg Time to Fix: 12 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Key Indicators:**
- ↓ Repeat reports = Fix is working
- ↑ User satisfaction = Fix is valuable
- ↓ Fix time = Process is improving
- ↑ Fix approval rate = Team trusts analysis

### Feedback Loop Checklist

- [ ] Add feedback button to UI (always visible)
- [ ] Design multi-step feedback form
- [ ] Implement `/api/feedback` endpoint
- [ ] Set up feedback database table
- [ ] Send email notifications
- [ ] Review feedback manually (Week 1)
- [ ] Identify patterns (Week 2)
- [ ] Generate auto-fixes (Week 3)
- [ ] Build admin dashboard (Week 4)
- [ ] Set up metrics tracking (Week 5)
- [ ] Monitor effectiveness (ongoing)

### Reference Documentation

For detailed implementation patterns, templates, and best practices, see:
- **Full Guide:** `Feedback_Loop/FEEDBACK_LOOP_IMPLEMENTATION.md`
- **Quick Reference:** `Feedback_Loop/QUICK_REFERENCE.md`
- **Real Implementation:** Code Puppy project (code_puppy_standalone.html)

---

## �🔗 Key Resources & Support

### Primary AI Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| **Walmart AI Portal** | [ai.walmart.com](https://ai.walmart.com) | Central hub for AI tools and resources |
| **Data Governance Library** | [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary) | All AI policies and standards |
| **AI Governance Microlearning** | [wmlink/AICompliance](wmlink/AICompliance) | Training and compliance guidance |

### Support Contacts

| Topic | Contact | Purpose |
|-------|---------|---------|
| **AI Portal Questions** | [HelpwithAI@walmart.com](mailto:HelpwithAI@walmart.com) | ai.walmart.com platform support |
| **AI Policy & Compliance** | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) | Policy questions, compliance assessments |
| **GenAI Legal Review** | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) | Legal review for GenAI applications |
| **Enterprise Privacy** | Privacy Team (APM/SSP) | EPRA for AI projects with PII |

---

## 📋 Required AI Compliance Assessments

### 1. AI Compliance Assessment
**When Required:**
- All AI/ML models in production
- Automated decisioning systems
- Any system using predictive analytics

**What's Assessed:**
- Model purpose and use case
- Data sources and quality
- Bias and fairness testing
- Model explainability
- Monitoring and governance

**Contact:** [ModelReview@walmart.com](mailto:ModelReview@walmart.com)

### 2. Enterprise Privacy Risk Assessment (EPRA)
**When Required:**
- AI/ML systems processing PII (Personally Identifiable Information)
- Systems with privacy implications

**How to Initiate:**
- Triggered automatically via APM Data Classification Assessment (DCA)
- Complete via OneTrust platform

### 3. GenAI Legal Review
**When Required:**
- Applications using generative AI (ChatGPT, Claude, Copilot, etc.)
- AI-generated content in customer-facing applications

**Contact:** [ModelReview@walmart.com](mailto:ModelReview@walmart.com)

---

## ✅ AI Agent Development Checklist

### Phase 1: Planning & Design
- [ ] Review all applicable AI policies (DC-DG-06 series)
- [ ] Complete AI Governance Microlearning: [wmlink/AICompliance](wmlink/AICompliance)
- [ ] Identify which assessments are required
- [ ] Plan timeline with 2-4 weeks buffer for AI assessments
- [ ] Contact ModelReview@walmart.com for early guidance
- [ ] Define AI agent use cases and scope
- [ ] Identify data sources and ensure data quality

### Phase 2: Development
- [ ] Start with mock response implementation
- [ ] Implement context and filter state management
- [ ] Build query processor and search engine
- [ ] Test query understanding and matching
- [ ] Implement auto-apply logic
- [ ] Add multi-match clarification flow
- [ ] Implement help/guidance system
- [ ] Test bias and fairness aspects
- [ ] Document model training data sources
- [ ] Establish explainability mechanisms
- [ ] Create monitoring plan

### Phase 3: Integration & Testing
- [ ] Integrate with database/data service
- [ ] Test API performance (target < 100ms queries)
- [ ] Implement caching where needed
- [ ] Set up logging and monitoring
- [ ] Performance benchmark testing
- [ ] Test with real user queries
- [ ] Validate response accuracy

### Phase 4: Compliance Assessments
- [ ] Complete AI Compliance Assessment
- [ ] Complete EPRA (if PII data involved)
- [ ] Complete GenAI Legal Review (if using GenAI)
- [ ] Address all findings and recommendations
- [ ] Document assessment completion in APM/SSP

### Phase 5: Production Deployment
- [ ] Implement all required AI governance controls
- [ ] Establish ongoing model monitoring
- [ ] Set up bias and drift detection
- [ ] Create model retraining procedures
- [ ] Document AI disclosure requirements
- [ ] Security hardening (authentication, CORS, etc.)
- [ ] Rate limiting and request logging
- [ ] HTTPS and encryption setup

### Phase 6: Ongoing Operations
- [ ] Monitor AI agent performance continuously
- [ ] Track query patterns and usage
- [ ] Conduct regular bias audits
- [ ] Monitor response accuracy
- [ ] Retrain/improve models as needed
- [ ] Update assessments for significant changes
- [ ] Complete annual AI compliance reviews

---

## 🔑 AI Agent Best Practices

### Architecture Best Practices
1. **Start with Mock Responses** - Proven pattern from Sparky
   - Faster development
   - Lower cost
   - Reliable fallback
   - Foundation for adding real AI later

2. **Maintain Context & Filter State** - Critical for accuracy
   - Always pass current filter state to AI agent
   - Respect existing user context
   - Allow AI to suggest context-aware options

3. **Implement Graceful Degradation** - Handle all cases
   - Single match: Auto-apply
   - Multiple matches: Ask for clarification
   - No matches: Suggest alternatives
   - No AI service: Fall back to mock responses

4. **Performance is Critical** - Target < 100ms response times
   - Implement caching
   - Optimize database queries
   - Consider async processing
   - Monitor query performance

5. **Monitoring & Logging** - Essential for production
   - Log all AI queries and responses
   - Track response accuracy
   - Monitor API performance
   - Alert on failures or anomalies

### Ethical AI Principles
1. **Fairness** - AI systems must not discriminate
2. **Transparency** - AI decisions must be explainable
3. **Accountability** - Clear ownership and responsibility
4. **Privacy** - Protect customer and associate data
5. **Safety** - AI systems must be secure and reliable
6. **Human Oversight** - Humans in the loop for critical decisions

### Prohibited Use Cases ❌
- Discriminatory practices based on protected classes
- Surveillance without consent and legal basis
- Manipulative or deceptive practices
- High-stakes decisions without human oversight
- Sharing confidential Walmart data with external AI tools (without approval)

### Approved Use Cases ✅
- Productivity enhancement (coding assistance, documentation)
- Data analysis and insights
- Search and navigation assistance
- Customer experience improvements
- Operational efficiency
- Internal process automation

---

## 🏭 Implementation: Sparky AI Architecture

### Technology Stack

**Frontend:**
- Vanilla HTML/CSS/JavaScript (no frameworks)
- Fetch API for HTTP requests
- Responsive UI with minimize/maximize
- Zero build requirements

**Backend:**
- Python 3.10+
- FastAPI 0.109 (modern, fast, async-ready)
- Uvicorn ASGI server (port 8000)
- Pydantic for data validation

**Data Layer:**
- Google BigQuery (1,280,356+ records)
- Database Service (database.py)
- SQL query builder
- Filter translation
- Result transformation

**AI Layer:**
- Mock responses (default, production-ready)
- Optional: OpenAI GPT-4
- Optional: Azure OpenAI (enterprise)

### API Endpoints for AI Agent

```
POST /api/ai/query
├── Body: { "query": "user input", "context": {...} }
├── Processing:
│   ├── Extract intent
│   ├── Search projects (up to 100)
│   ├── Apply auto-logic
│   └── Generate response
├── Response Time: < 100ms
└── Response: { "action": "auto_apply|clarify|suggest", "data": {...} }
```

### Configuration

```env
# Optional - Mock responses work by default
OPENAI_API_KEY=sk-...          # For real OpenAI
OPENAI_MODEL=gpt-4              # GPT-4 or GPT-3.5-turbo

# Optional - For Azure OpenAI
AZURE_OPENAI_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_DEPLOYMENT=...
```

### Performance Characteristics (Production Data)
- Query processing: < 100ms
- Database search: ~200-300ms
- Mock responses: < 50ms
- OpenAI API: 200-500ms (optional)
- Caching hit: < 10ms

---

## 🔒 Security Considerations

### Current Security (Development)
- ⚠️ No authentication
- ⚠️ CORS open
- Environment variables for secrets
- Service account for BigQuery

### Production Requirements
- [ ] Add authentication middleware (JWT)
- [ ] Restrict CORS to specific domains
- [ ] Use secret manager for credentials
- [ ] Enable rate limiting
- [ ] Add request logging and auditing
- [ ] Implement caching securely
- [ ] Use HTTPS only
- [ ] Validate all user inputs
- [ ] API key rotation policy

---

## 📞 Quick Reference: AI Agent Support

| Question | Contact |
|----------|---------|
| Architecture/design help | Internal tech team |
| AI policy questions | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) |
| Compliance assessment | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) |
| ai.walmart.com access | [HelpwithAI@walmart.com](mailto:HelpwithAI@walmart.com) |
| Privacy (EPRA) questions | Privacy Team via OneTrust/APM |
| GenAI legal review | [ModelReview@walmart.com](mailto:ModelReview@walmart.com) |

---

## 📚 Additional Resources

### Learning Resources
- **AI Governance Microlearning Hub:** [wmlink/AICompliance](wmlink/AICompliance)
- **Walmart AI Portal:** [ai.walmart.com](https://ai.walmart.com)
- **Technology Policies:** [wmlink/policy](wmlink/policy)
- **Data Governance Library:** [wmlink/DataGovernanceLibrary](wmlink/DataGovernanceLibrary)

### Reference Implementations
- **Sparky AI (Projects in Stores):** C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores
  - Production-ready AI agent for search/navigation
  - FastAPI backend with mock responses
  - BigQuery integration
  - Contextual query processing

---

## 🎓 Training Path for AI Agents

### Required Training
1. **AI Governance Microlearning Hub** - Complete all modules
2. **Technology Compliance Policy** - Review data governance
3. **AI Ethics Framework** - Understand Walmart's ethical AI principles
4. **Prompt Engineering** (if using GenAI) - Best practices
5. **Model Monitoring** - Ongoing operations

### Recommended Certifications
- Responsible AI practitioner
- Machine learning fundamentals
- Data privacy and compliance
- AI security and risk management

---

## 🔄 AI Governance Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PLAN: Review policies, identify assessments              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. DESIGN: AI agent architecture, use cases                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. DEVELOP: Mock → Real AI, test, monitor                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ASSESS: Complete compliance, EPRA, GenAI review          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. APPROVE: Obtain all required approvals (APM/SSP)         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. DEPLOY: Production setup with governance controls        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. MONITOR: Continuous monitoring, bias audits              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. REVIEW: Annual compliance, model retraining              │
└─────────────────────────────────────────────────────────────┘
```

---

**Version:** 1.0  
**Last Updated:** January 23, 2026  
**Status:** Production Ready  
**Based on:** Sparky AI Agent (Projects in Stores Dashboard) implementation  
**Next Review:** January 23, 2027

**Questions?** Contact:
- **AI Policy:** [ModelReview@walmart.com](mailto:ModelReview@walmart.com)
- **AI Portal:** [HelpwithAI@walmart.com](mailto:HelpwithAI@walmart.com)
