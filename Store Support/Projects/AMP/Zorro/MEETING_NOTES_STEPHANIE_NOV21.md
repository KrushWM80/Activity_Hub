# Meeting Notes - Stephanie Tsai (PM, GenAI Media Studio)
## November 21, 2025

---

## 🎯 Meeting Objectives

1. ✅ Confirm GenAI Media Studio can meet our video generation needs
2. ✅ Address Stephanie's questions about audio descriptions and sample content
3. ✅ Get approval for API access
4. ✅ Understand timeline and next steps

**Important Note from Oskar (Nov 21):**
- Production API endpoint: `https://retina-ds-genai-backend.prod.k8s.walmart.net/docs`
- Authentication implementation in progress
- Limit sharing of APIs until authentication is complete
- Keep endpoint confidential during development phase

---

## 📋 KEY TALKING POINTS

### 1. PROJECT OVERVIEW (2 minutes)

**What We're Building:**
- Automated video generation system called "Zorro"
- Converts text-based store communications into short, engaging videos
- Supplement to daily messages on OneWalmart homepage

**Current Volume:**
- 100-150 videos per week
- 5,200-7,800 videos annually
- 8-10 seconds per video

**Why Videos:**
- Text messages get ~30% read rate
- Videos projected 70%+ engagement
- Visual learners (60% of associates) benefit
- Faster comprehension (10-sec video vs 5-min read)

**Status:**
- 96% complete (all code built and tested)
- Just needs API access to go live

---

### 2. SAMPLE CONTENT EXAMPLES (from OneWalmart)

**Type 1: Action Required - Pricing Updates**
```
Title: "Event 1 Prices Going Even Lower"
Message: Tab files drop overnight, hard markdowns Sunday Nov 16
Action: Change prices by 6am Sunday, use WAS cards

Video Concept:
- 10-second visual walkthrough
- Show: Tab file → Price change → WAS card placement
- Text overlay: "By 6am Sunday" + key steps
- Style: Clear, instructional, fast-paced
```

**Type 2: Recognition**
```
Title: "Thank You for Black Friday Success!"
Message: Great customer service during first event

Video Concept:
- 8-second celebration
- Show: Associates helping customers, teamwork
- Text overlay: "Thank You Team!" + specific achievement
- Style: Upbeat, appreciative, energetic
```

**Type 3: Training/Reminder**
```
Title: "Maintain Pricing Integrity This Weekend"
Message: Don't take store-initiated markdowns on Black Friday items

Video Concept:
- 10-second reminder
- Show: Pricing scanner → correct process → checkmark
- Text overlay: "No store markdowns" + icon
- Style: Clear, professional, important
```

**Type 4: Operational Update**
```
Title: "Update Aisle Locations as You Condense"
Message: Maintain online availability by updating locations

Video Concept:
- 8-second process demo
- Show: Moving items → updating location → online visible
- Text overlay: "Update = Online availability"
- Style: Practical, step-by-step, helpful
```

---

### 3. ADDRESSING STEPHANIE'S QUESTIONS

#### Q: "Have you tried using GenAI Media Studio? Does it satisfy your needs?"

**Answer:**
- ✅ YES - We tested the web UI manually and quality is excellent
- ✅ Google Veo models produce exactly the style we need
- ✅ Duration (4-8 seconds) is perfect for our use case
- ✅ Aspect ratios (16:9, 9:16, 1:1) cover all our devices

**Our Need:**
- We need **API access** (not just web UI) because:
  - Automating 100-150 videos/week
  - Integrating with our existing message system
  - Can't manually generate that volume via web UI
  - Need programmatic generation + batch processing

#### Q: "We don't have audio descriptions"

**Answer:**
- ✅ **NOT A BLOCKER** - We handle that!
- Our system (Zorro) adds accessibility features **after** you generate the video:
  - WebVTT captions (auto-generated from video + text)
  - Audio descriptions (text-to-speech)
  - Text transcripts
  - WCAG AAA compliance validation

**How It Works:**
```
Your API generates video (10 sec MP4)
         ↓
We receive the video file
         ↓
We add captions, audio, transcripts
         ↓
Complete accessible package ready for associates
```

**Legal Requirement:**
- ADA compliance mandatory for associate communications
- We've built the accessibility layer specifically for this
- Your platform generates core video, we handle compliance

---

### 4. TECHNICAL REQUIREMENTS

**What We Need from Media Studio API:**

1. **Video Generation Endpoint**
   - Base URL: `https://retina-ds-genai-backend.prod.k8s.walmart.net`
   - Documentation: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs
   - POST request with text prompt
   - Return video file (MP4)
   - 8-10 second duration
   - 16:9 aspect ratio (primary)

2. **Authentication** (In Progress)
   - SSO implementation underway
   - Will limit API sharing until authentication complete
   - Secure within Walmart network (Kubernetes cluster)

3. **Rate Limits**
   - 100-150 requests per week (spread across 5 days)
   - ~30 videos per day average
   - Can batch if needed

4. **Status/Polling**
   - Check generation status
   - Estimated time: 2-5 minutes per video

**What We DON'T Need:**
- ❌ Audio descriptions from your API (we add them)
- ❌ Captions from your API (we generate them)
- ❌ Custom models or training
- ❌ High-resolution 4K (standard quality is fine)

---

### 5. BUSINESS JUSTIFICATION

**Cost Comparison:**

**Option A: Manual Production**
- 150 videos/week × 8 hours = 1,200 hours/week
- Requires 30 designers @ $1.3M-$2M annually
- ❌ Not feasible

**Option B: Automated with Media Studio**
- 150 videos/week × 2 minutes = 5 hours (automated)
- Cost: ~$780/year (API usage)
- ✅ Feasible and scalable

**Annual Savings: $1.3M - $2M**

**ROI:**
- Implementation cost: $85K (already spent - 96% done)
- Annual benefit: $690K (labor savings + improved engagement)
- Net ROI: $605K (710% return)

---

### 6. USE CASE FIT WITH MEDIA STUDIO

**Why We're Perfect for Your Platform:**

✅ **Internal Walmart Use** - Exactly what Studio is designed for  
✅ **Moderate Volume** - 100-150/week is reasonable, not excessive  
✅ **Clear Business Case** - Store communications (critical function)  
✅ **Scalable** - Could expand to other departments if successful  
✅ **API Consumer** - Demonstrates platform value beyond web UI  
✅ **Feedback Partner** - Can provide insights on API performance  

**How We Complement Studio:**
- We handle the "last mile" (accessibility, delivery, integration)
- You focus on core strength (high-quality video generation)
- Win-win: You get API usage data, we get automated videos

---

### 7. SAMPLE PROMPTS (Based on OneWalmart Messages)

**Example 1: Pricing Action**
```
Prompt: "A professional retail environment showing a Walmart 
associate using a handheld device to scan and update product 
prices, close-up of price tag changing, bright store lighting, 
efficient and organized, 4K quality"

Use Case: "Prices Going Lower" message
Duration: 8 seconds
Style: Clear, instructional, professional
```

**Example 2: Recognition**
```
Prompt: "Celebratory scene in a Walmart store, diverse team of 
associates giving high-fives and celebrating together, positive 
energy, bright lighting, joyful atmosphere, team achievement, 4K"

Use Case: "Thank You Black Friday Team" message
Duration: 8 seconds
Style: Upbeat, appreciative, energetic
```

**Example 3: Process Reminder**
```
Prompt: "Walmart associate organizing merchandise in aisle, 
using mobile device to update location, scanning items, well-lit 
store, organized shelving, professional retail environment, 4K"

Use Case: "Update Aisle Locations" message
Duration: 10 seconds
Style: Practical, step-by-step, helpful
```

---

### 8. ADDRESSING POTENTIAL CONCERNS

#### Concern: "Your volume might be too high"
**Response:**
- 30 videos/day average (spread across business hours)
- Can adjust schedule to off-peak times
- Can reduce volume if quotas are an issue
- Willing to start with pilot (25-50/week) and scale up

#### Concern: "API isn't ready for external consumers"
**Response:**
- We're internal (Walmart US Stores team)
- Not external/vendor access
- Can provide feedback to improve API
- Happy to be early adopter/beta tester

#### Concern: "Need approval from security/compliance"
**Response:**
- All data stays within Walmart network
- No PII in prompts (just general store scenarios)
- SSO authentication (already approved pattern)
- Can submit SSP if required

#### Concern: "Cost implications unclear"
**Response:**
- Willing to pay usage fees (budgeted $780/year)
- Can discuss chargeback model
- ROI justifies costs ($690K annual benefit)
- Open to pilot to prove value before full commitment

---

### 9. QUESTIONS TO ASK STEPHANIE

**Priority Questions:**

1. **Does our use case fit within Media Studio's intended scope?**
   - 100-150 videos/week for store communications
   - Automated via API (not manual web UI)

2. **What's the API access approval process?**
   - Documentation needed?
   - Timeline for approval?
   - Who makes final decision?

3. **Are there rate limits or quotas we should know about?**
   - Videos per day/week/month?
   - Concurrent requests?
   - Peak usage restrictions?

4. **What's the typical video generation time?**
   - Average: 2-5 minutes?
   - During peak hours?
   - SLA or guarantees?

5. **Are there costs associated with API usage?**
   - Per-video charges?
   - Chargeback to our department?
   - Any upfront costs?

6. **What's the timeline to receive API access?**
   - Days? Weeks?
   - Can we expedite given our readiness (96% complete)?

7. **Is there API documentation available?**
   - Request/response formats?
   - Authentication details?
   - Error handling?
   - Code examples?

8. **What support is available for API consumers?**
   - Technical support channel?
   - Best practices?
   - Troubleshooting resources?

9. **Can we start with a pilot program?**
   - Test with 25-50 videos/week first?
   - Validate quality and performance?
   - Then scale to full 100-150/week?

10. **Is there anything else you need from us?**
    - Additional documentation?
    - Security reviews?
    - Stakeholder approvals?

---

### 10. NEXT STEPS TO PROPOSE

**If Stephanie Approves:**

**Immediate (This Week):**
1. ✅ Provide any additional documentation requested
2. ✅ Complete any required approval forms/processes
3. ✅ Submit SSP if needed (we can do this quickly)

**Week of Nov 25-29:**
1. ✅ Receive SSO token and API documentation
2. ✅ Configure authentication in our system
3. ✅ Run test script (test_walmart_api.py is ready)
4. ✅ Generate first 5-10 test videos

**Week of Dec 2-6:**
1. ✅ Validate quality and performance
2. ✅ Complete end-to-end testing
3. ✅ Deploy to production environment
4. ✅ Start pilot with 25-50 videos/week

**Week of Dec 9-13:**
1. ✅ Scale to full 100-150 videos/week
2. ✅ Monitor performance and costs
3. ✅ Collect feedback from store associates
4. ✅ Share usage data and insights with Media Studio team

**If Additional Info Needed:**
- Provide sample prompts and expected outputs
- Share our technical architecture
- Demonstrate our accessibility features
- Schedule technical deep-dive if helpful

---

### 11. CLOSING STATEMENT

**Summary:**
- We've built a complete system (96% done) that just needs your API
- Use case: 100-150 store communication videos per week
- Sample content: OneWalmart messages (pricing, recognition, reminders)
- We handle accessibility (audio descriptions, captions) - not a blocker
- Strong business case: $690K annual benefit, 710% ROI
- Perfect fit for Media Studio's internal platform mission

**Value Proposition:**
- **For Us:** Access to high-quality video generation at scale
- **For Media Studio:** Real-world API usage, feedback, demonstration of platform value
- **For Walmart:** Better associate communications, cost savings, improved engagement

**Ask:**
API access to generate 100-150 videos/week for store communications. We're ready to go live as soon as we receive SSO token and documentation.

---

## 📞 MEETING PREP CHECKLIST

**Before Meeting:**
- [x] Review USE_CASE_FOR_STEPHANIE.md
- [x] Review sample OneWalmart messages
- [x] Prepare sample prompts
- [x] Review these talking points
- [ ] Have code repository link ready (if asked): https://gecgithub01.walmart.com/hrisaac/zorro
- [ ] Have director's availability for follow-up meeting (if needed)

**During Meeting:**
- [ ] Take notes on Stephanie's questions/concerns
- [ ] Note any action items assigned to us
- [ ] Confirm next steps and timeline
- [ ] Get contact info for technical questions

**After Meeting:**
- [ ] Send thank you email with summary
- [ ] Complete any requested action items
- [ ] Update project documentation
- [ ] Notify director of outcome

---

## 🎯 SUCCESS CRITERIA FOR THIS MEETING

**Minimum Success:**
- ✅ Stephanie understands our use case clearly
- ✅ We've addressed audio description concern
- ✅ She confirms we're in scope for API access
- ✅ Next steps are clear (even if approval pending)

**Ideal Success:**
- ✅ All of the above, PLUS:
- ✅ Approval granted in principle
- ✅ Timeline confirmed (expected API access date)
- ✅ Documentation and support resources identified
- ✅ Pilot program agreed upon

**Home Run:**
- ✅ Immediate API access approval
- ✅ SSO token process initiated this week
- ✅ Technical documentation shared
- ✅ Direct support contact provided
- ✅ Go-live date set for early December

---

**Prepared:** November 21, 2025  
**Meeting Date:** November 21, 2025  
**Attendees:** Robert Isaacs, Stephanie Tsai (PM, GenAI Media Studio), [Director if available]  
**Duration:** 30-45 minutes estimated
