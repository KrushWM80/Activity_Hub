# Copilot Prompt for PowerPoint: Executive Proposal Generation

## Overview
This document provides a comprehensive prompt for using GitHub Copilot or AI assistants to generate a PowerPoint presentation from the Executive Proposal markdown content. Use this prompt to automate the creation of professional, branded presentations.

---

## Complete Copilot Prompt

### Main Prompt

```
Create a PowerPoint presentation for the "Activity Hub: Store Operations Unified Platform" Executive Proposal with the following specifications:

**Presentation Details:**
- Total Slides: 20 slides
- Theme: Walmart branded (Blue #004890, Yellow #FCC810, White, Dark Gray #323232)
- Font: Bogle (fallback: Arial, Calibri)
- Layout: Professional executive format with consistent structure

**Slide-by-Slide Content:**

**SLIDE 1: Title Slide**
- Title: "Activity Hub"
- Subtitle: "Store Operations Unified Platform"
- Bottom text: "Executive Proposal | [Date] | [Your Name]"
- Background: Walmart Blue gradient
- Walmart spark logo (top right corner)

**SLIDE 2: Executive Summary**
- Title: "Executive Summary"
- 4 bullet points:
  • Unified platform consolidating 16 tools
  • $3.1M annual benefit, $699K investment
  • 1,319% ROI, 2-month break-even
  • Enhanced efficiency & user experience
- Bottom right: "Investment: $699K | Benefit: $3.1M"

**SLIDE 3: The Challenge**
- Title: "The Challenge: Fragmented Operations"
- Split layout:
  LEFT: "Current State" (red accent)
    • 16 disconnected platforms
    • Multiple logins required
    • Inconsistent interfaces
    • Training complexity
  RIGHT: Pain points with icons
    • Time Loss: 45 min/day per user
    • Errors: Inconsistent data entry
    • Frustration: Tool switching overhead
    • Cost: $3.1M annual impact

**SLIDE 4: The Solution (Interactive Overview)**
- Title: "Activity Hub: Unified Solution"
- Center: Large "Activity Hub" graphic/diagram
- 8 clickable solution boxes arranged around center:
  1. Reporting (top)
  2. Store Tools (top right)
  3. Intake (right)
  4. Governance (bottom right)
  5. Schedule Events (bottom)
  6. Integration (bottom left)
  7. Management (left)
  8. AI & Automation (top left)
- Note: "Click each box for detailed breakdown"
- Hyperlinks to detail slides 7a-7g

**DETAIL SLIDES (7a-7g): Solution Component Details**

**SLIDE 7a: Reporting Tools**
- Title: "Solution Component: Reporting"
- 3 integrated tools:
  1. Tableau - Enterprise analytics & visualization
  2. Power BI - Microsoft reporting suite
  3. Looker - Cloud-native analytics
- Benefits: Unified dashboards, real-time insights, consistent metrics
- Current users: 2,500 associates
- Annual benefit: $850K

**SLIDE 7b: Store Tools**
- Title: "Solution Component: Store Tools"
- 4 integrated tools:
  1. Field Assist - Store operations support
  2. Store OPS - Daily operations management
  3. Spark - Associate platform
  4. Store Wire - Communication hub
- Benefits: Single interface, streamlined workflows, reduced training
- Current users: 8,500 associates
- Annual benefit: $1.2M

**SLIDE 7c: Intake Systems**
- Title: "Solution Component: Intake"
- 2 integrated tools:
  1. ServiceNow - IT service management
  2. Intake - Request management
- Benefits: Automated routing, faster resolution, improved tracking
- Current users: 1,200 associates
- Annual benefit: $400K

**SLIDE 7d: Governance & Compliance**
- Title: "Solution Component: Governance"
- 2 integrated tools:
  1. SSP (Solution Security Plan) - Security compliance
  2. One Walmart - Corporate policies
- Benefits: Automated compliance, risk mitigation, audit readiness
- Current users: 800 associates
- Annual benefit: $350K

**SLIDE 7e: Scheduling**
- Title: "Solution Component: Schedule Events"
- 1 integrated tool:
  1. Schedule Events - Calendar & event management
- Benefits: Unified calendar, automated reminders, conflict prevention
- Current users: 3,000 associates
- Annual benefit: $250K

**SLIDE 7f: System Integration**
- Title: "Solution Component: Integration"
- 3 integrated tools:
  1. My APM (Application Portfolio Mgmt) - App lifecycle
  2. Teams - Collaboration platform
  3. Outlook - Email & calendar
- Benefits: Seamless data flow, reduced duplication, API-driven
- Current users: 5,000 associates
- Annual benefit: $650K

**SLIDE 7g: Management & AI**
- Title: "Solution Component: Management & AI"
- 2 integrated tools:
  1. My Facilities - Facility management
  2. Copilot - AI assistance & automation
- Benefits: Predictive maintenance, AI-powered insights, intelligent automation
- Current users: 1,500 associates
- Annual benefit: $400K

**SLIDE 8: Platform Architecture**
- Title: "Technical Architecture"
- 3-tier diagram:
  TOP: "User Layer" - Single sign-on, unified interface
  MIDDLE: "Integration Layer" - APIs, data sync, security
  BOTTOM: "Platform Layer" - 16 integrated systems
- Key features: Azure cloud, microservices, RESTful APIs
- Security: SSO, OAuth2, encryption, audit logging

**SLIDE 9: User Experience**
- Title: "Transformative User Experience"
- Before/After comparison:
  BEFORE:
    • 16 separate logins
    • 45 minutes daily tool switching
    • Inconsistent interfaces
    • Training: 3 weeks
  AFTER:
    • Single login
    • Instant access
    • Unified interface
    • Training: 3 days
- Center: Screenshot mockup of Activity Hub dashboard

**SLIDE 10: Financial Overview**
- Title: "Financial Model"
- Large metric boxes:
  • Investment: $699K (3-year total)
  • Annual Benefit: $3.1M
  • ROI: 1,319%
  • Break-Even: 2 months
  • 3-Year Net Benefit: $8.7M
- Bottom: Small print breakdown

**SLIDE 11: Investment Breakdown**
- Title: "3-Year Investment: $699K"
- Pie chart showing:
  • Development: $400K (57%)
  • Azure Infrastructure: $150K (21%)
  • Licenses: $99K (14%)
  • Training: $50K (7%)
- Timeline bar: Year 1: $350K | Year 2: $200K | Year 3: $149K

**SLIDE 12: Annual Benefits**
- Title: "Annual Benefits: $3.1M"
- Bar chart showing:
  1. Time Savings: $1.8M (58%)
  2. Error Reduction: $650K (21%)
  3. Training Efficiency: $350K (11%)
  4. License Consolidation: $300K (10%)
- Total: $3.1M per year

**SLIDE 13: Implementation Roadmap**
- Title: "18-Month Implementation Plan"
- Timeline with 4 phases:
  PHASE 1 (Months 1-3): Foundation
    • Architecture design
    • Azure setup
    • SSO integration
  PHASE 2 (Months 4-9): Core Build
    • Platform development
    • API integrations (8 tools)
    • Testing & validation
  PHASE 3 (Months 10-15): Rollout
    • Pilot with 500 users
    • Training program
    • Full deployment
  PHASE 4 (Months 16-18): Optimization
    • Performance tuning
    • User feedback
    • Feature enhancements

**SLIDE 14: Risk Mitigation**
- Title: "Risk Management Strategy"
- Risk matrix with 4 risks:
  1. Integration Complexity (MEDIUM)
     Mitigation: Phased API integration, dedicated integration team
  2. User Adoption (LOW)
     Mitigation: Training program, change champions, 24/7 support
  3. Security Compliance (LOW)
     Mitigation: SSP approval, penetration testing, regular audits
  4. Performance Issues (MEDIUM)
     Mitigation: Azure autoscaling, load testing, CDN deployment

**SLIDE 15: Success Metrics**
- Title: "Measuring Success"
- KPI dashboard layout with 6 metrics:
  1. User Adoption: 95% within 6 months
  2. Login Reduction: From 16 to 1 (100%)
  3. Time Savings: 45 min/day per user
  4. Error Rate: -40% decrease
  5. Training Time: -70% reduction
  6. User Satisfaction: 4.5/5 stars

**SLIDE 16: User Testimonials**
- Title: "Early Feedback (Pilot Results)"
- 3 quote boxes with photos/avatars:
  Quote 1: "Activity Hub saves me 30+ minutes every day. Game changer!" - Store Manager, Store #1234
  Quote 2: "Finally, one place for everything. No more juggling 10 tools." - Department Manager, Region 5
  Quote 3: "Training new associates is so much easier now." - Training Coordinator, Market 42
- Bottom: Pilot satisfaction: 4.7/5 stars (500 users)

**SLIDE 17: Competitive Analysis**
- Title: "Why Build vs. Buy?"
- Comparison table:
  | Factor | Build (Activity Hub) | Buy (Vendors) |
  |--------|---------------------|---------------|
  | Cost | $699K | $2-3M |
  | Customization | Full control | Limited |
  | Walmart Integration | Native | Complex |
  | Timeline | 18 months | 24+ months |
  | Ownership | Complete | Vendor-dependent |
- Recommendation: Build delivers superior value

**SLIDE 18: Next Steps**
- Title: "Recommended Actions"
- Numbered action items with owners:
  1. Approve $699K budget (CFO - Week 1)
  2. Assign project team (CTO - Week 2)
  3. Initiate Azure setup (IT - Week 3)
  4. Begin SSP process (Security - Week 4)
  5. Kick off development (PM - Month 2)
- Timeline: Decision needed by [Date]

**SLIDE 19: Q&A Preparation**
- Title: "Anticipated Questions"
- FAQ format:
  Q: Why not use existing vendor solutions?
  A: Custom solution provides better integration, lower cost, faster deployment
  
  Q: What if users resist change?
  A: Comprehensive training, change management program, 24/7 support
  
  Q: How do we ensure security?
  A: SSP approval, regular audits, Azure security features, encryption
  
  Q: Can we scale beyond 10K users?
  A: Azure autoscaling supports 50K+ users with no architecture changes

**SLIDE 20: Call to Action**
- Title: "Invest in Efficiency"
- Large centered text:
  "Transform Store Operations"
  "Unify 16 Tools into One Platform"
  "Deliver $3.1M Annual Value"
- Bottom: Contact information
  [Your Name] | [Title]
  [Email] | [Phone]
  "Ready to discuss next steps"

**Design Guidelines:**
- Consistent header/footer on all slides (slide numbers, date, confidential marking)
- Use Walmart blue (#004890) for headers and accents
- White backgrounds with subtle gradients
- Sans-serif fonts (Bogle, Arial, Calibri)
- Icons and graphics where applicable (use Walmart icon library)
- Animations: Simple fade/wipe transitions between slides
- Hyperlinks: Slide 4 boxes link to corresponding detail slides (7a-7g)
- Each detail slide has "Back to Overview" button linking to Slide 4

**Data Visualizations:**
- Use bar charts, pie charts, and timeline graphics
- Walmart brand colors for all charts
- Clear labels and legends
- High contrast for accessibility

**Additional Notes:**
- All dollar figures are annual unless specified
- Include slide notes with talking points for presenter
- Export as .pptx format
- Test all hyperlinks before presenting
- Include appendix slides with detailed calculations if needed
```

---

## Alternative: Simplified Prompt for Quick Generation

If the full prompt is too long, use this condensed version:

```
Create a 20-slide PowerPoint presentation for "Activity Hub: Store Operations Unified Platform" with:
- Walmart branding (Blue #004890, Yellow #FCC810)
- Font: Bogle/Arial
- Content from Executive_Proposal_Presentation_Outline.md
- Include: Title, Executive Summary, Challenge, Solution (8 components with 7 detail slides 7a-7g), Architecture, UX, Financial (Investment $699K, Benefits $3.1M, ROI 1,319%), Implementation roadmap, Risks, Metrics, Testimonials, Competitive analysis, Next steps, Q&A, Call to action
- Make Slide 4 interactive with hyperlinks to detail slides 7a-7g
- Use charts for financials and timeline
- Professional executive format
```

---

## Step-by-Step Instructions

### Method 1: Using GitHub Copilot in PowerPoint

1. **Open PowerPoint** and create a new blank presentation

2. **Use Copilot in PowerPoint:**
   - Click on the Copilot icon in the ribbon
   - Or press `Alt + Q` and search for "Copilot"

3. **Paste the main prompt** above into Copilot

4. **Let Copilot generate** the initial presentation structure

5. **Review and refine:**
   - Check all slides match the specification
   - Verify hyperlinks work (Slide 4 to detail slides)
   - Adjust colors to exact Walmart brand values
   - Add images, icons, and graphics

6. **Add speaker notes:**
   - Include talking points for each slide
   - Reference specific data points
   - Add transition cues

### Method 2: Using Python Script with python-pptx

If you have `python-pptx` installed, create a Python script:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Initialize presentation
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Define Walmart colors
WALMART_BLUE = RGBColor(0, 72, 144)
WALMART_YELLOW = RGBColor(252, 200, 16)
WHITE = RGBColor(255, 255, 255)
DARK_GRAY = RGBColor(50, 50, 50)

# Slide 1: Title Slide
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
# Add title, subtitle, branding...

# Slide 2: Executive Summary
slide2 = prs.slides.add_slide(prs.slide_layouts[1])  # Title and content
title2 = slide2.shapes.title
title2.text = "Executive Summary"
# Add bullet points...

# Continue for all 20 slides...

# Save presentation
prs.save('Activity_Hub_Executive_Proposal.pptx')
```

### Method 3: Using Markdown-to-PowerPoint Converters

1. **Use Pandoc:**
```bash
pandoc Executive_Proposal_Presentation_Outline.md -o Activity_Hub_Proposal.pptx
```

2. **Customize the output:**
   - Apply Walmart theme
   - Add hyperlinks manually
   - Insert charts and graphics

### Method 4: Manual Creation with AI Assistance

1. **Create slides manually** in PowerPoint

2. **Use Copilot for each slide:**
   - "Create content for executive summary slide with 4 key points about Activity Hub"
   - "Generate financial chart showing $699K investment and $3.1M benefit"
   - "Design timeline graphic for 18-month implementation plan"

3. **Use Designer** (PowerPoint feature):
   - Let PowerPoint suggest layouts for each slide
   - Choose designs that match Walmart branding

---

## Content Source Files

Reference these files when creating the presentation:

1. **Main content:**
   - `General Setup/Production_Path/Executive_Proposal_Presentation_Outline.md`
   - Contains all slide content, speaker notes, and structure

2. **Detailed specifications:**
   - `General Setup/Production_Path/Executive_Proposal_Figma_Specs.md`
   - Pixel-perfect layout specifications, coordinates, animations

3. **Full narrative:**
   - `General Setup/Production_Path/Executive_Proposal.md`
   - Complete business case with all details and calculations

---

## Validation Checklist

After generating the presentation, verify:

- [ ] Total slide count: 20 main slides + 7 detail slides (7a-7g) = 27 total
- [ ] Walmart branding applied (colors, fonts, logo)
- [ ] All financial figures accurate ($699K, $3.1M, 1,319%)
- [ ] Hyperlinks work (Slide 4 to detail slides, back buttons)
- [ ] Charts and graphics are clear and branded
- [ ] Speaker notes included for all slides
- [ ] No spelling or grammar errors
- [ ] Animations are subtle and professional
- [ ] File exports as .pptx format
- [ ] Slide numbers and footers consistent
- [ ] All 16 platforms mentioned across detail slides
- [ ] 8 solution boxes on Slide 4 with correct labels

---

## Customization Tips

### For Different Audiences:

**Executive Leadership (C-Suite):**
- Focus on slides: 1, 2, 4, 10, 11, 12, 13, 18, 20
- Emphasize: ROI, strategic value, competitive advantage
- Duration: 15 minutes

**Technical Teams:**
- Focus on slides: 1, 3, 4, 7a-7g, 8, 13, 14
- Emphasize: Architecture, integration, implementation
- Duration: 30 minutes

**Financial Stakeholders:**
- Focus on slides: 1, 2, 10, 11, 12, 15, 17, 18
- Emphasize: Investment, benefits, ROI, risk mitigation
- Duration: 20 minutes

### For Different Timelines:

**Quick Pitch (5 minutes):**
- Slides: 1, 2, 4, 10, 20
- Hit the highlights and financials

**Standard Presentation (20 minutes):**
- All main slides (1-20)
- Skip detail slides unless questions arise

**Deep Dive (45 minutes):**
- All slides including detail slides (7a-7g)
- Allow time for Q&A on each section

---

## Troubleshooting

### Issue: Copilot doesn't generate full presentation
**Solution:** Break the prompt into sections, generate 5 slides at a time

### Issue: Hyperlinks don't work
**Solution:** Manually add hyperlinks in PowerPoint:
1. Select text/shape on Slide 4
2. Right-click → Hyperlink
3. Select "Place in This Document"
4. Choose target slide (7a-7g)

### Issue: Charts don't match brand colors
**Solution:** 
1. Click on chart
2. Chart Design → Change Colors
3. Create custom color scheme with Walmart colors

### Issue: Fonts not available (Bogle)
**Solution:** 
1. Use Arial or Calibri as fallback
2. Or install Bogle font from Walmart brand resources
3. Download from: [Walmart Brand Portal]

---

## AI Prompt Templates

### For Individual Slides

**For financial slides:**
```
Create a PowerPoint slide showing the financial breakdown for Activity Hub:
- Investment: $699K over 3 years
- Annual benefit: $3.1M
- ROI: 1,319%
- Break-even: 2 months
Use bar chart with Walmart blue (#004890) and yellow (#FCC810)
```

**For architecture diagrams:**
```
Create a technical architecture diagram slide showing:
- Top layer: User Interface (single login)
- Middle layer: Integration APIs
- Bottom layer: 16 integrated platforms
Use 3-tier design with Walmart branding
```

**For timeline slides:**
```
Create an 18-month implementation timeline with 4 phases:
Phase 1 (Months 1-3): Foundation
Phase 2 (Months 4-9): Core Build
Phase 3 (Months 10-15): Rollout
Phase 4 (Months 16-18): Optimization
Use Walmart blue timeline bar with milestones
```

---

## Export and Sharing

### Final Steps:

1. **Review with stakeholders** before finalizing

2. **Export versions:**
   - .pptx (editable PowerPoint)
   - .pdf (for distribution)
   - .odp (OpenOffice compatibility if needed)

3. **Share via:**
   - Email with password protection
   - SharePoint/OneDrive with access controls
   - USB drive for offline presentations

4. **Backup:**
   - Save to multiple locations
   - Version control (v1.0, v1.1, etc.)
   - Keep source markdown files

---

## Additional Resources

- **Walmart Brand Guidelines:** [Internal Brand Portal]
- **PowerPoint Templates:** [Walmart Template Library]
- **Icon Library:** [Walmart Digital Assets]
- **Copilot Documentation:** https://support.microsoft.com/copilot
- **python-pptx Documentation:** https://python-pptx.readthedocs.io/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-03 | Initial prompt created |

---

## Python Script Generated by Copilot

Copilot has generated a complete Python script that creates the full 20-slide presentation. The script is saved as `activity_hub_proposal.py` in this folder.

### Running the Script

**Prerequisites:**
```powershell
# Install python-pptx (see README.md for installation help)
pip install python-pptx
```

**Run the script:**
```powershell
python activity_hub_proposal.py
```

**Output:**
- File: `Activity_Hub_Executive_Proposal.pptx`
- Contains all 20 main slides + 7 detail slides (7a-7g)
- Walmart branded with colors, fonts, and layouts

**Post-Generation Tasks:**
1. Open the file in PowerPoint
2. Add hyperlinks to Slide 4 solution boxes (link to detail slides 7a-7g)
3. Add back buttons on detail slides (link to Slide 4)
4. Replace logo placeholder with actual Walmart spark logo
5. Add charts/graphics as needed
6. Review and customize formatting
7. Add any images or icons
8. Test all navigation

### Script Features

The generated script includes:
- **Walmart branding:** Blue (#004890), Yellow (#FCC810), proper fonts
- **20 main slides:** Title, Executive Summary, Challenge, Solution Overview, Architecture, UX, Financials, Implementation, Risks, Metrics, Testimonials, Competitive Analysis, Next Steps, Q&A, Call to Action
- **7 detail slides (7a-7g):** Reporting, Store Tools, Intake, Governance, Schedule Events, Integration, Management & AI
- **Professional layouts:** Split columns, bullet points, metric boxes, tables
- **Placeholder elements:** Logo, charts, hyperlinks (to be added manually)
- **Speaker notes ready:** Add your talking points in PowerPoint

### Customization Tips

After generating, you can customize:
- Replace `[Your Name]`, `[Date]`, `[Email]`, `[Phone]` with actual information
- Add real Walmart spark logo (top right on title slide)
- Insert charts for financial data (Slides 11-12)
- Add timeline graphics (Slide 13)
- Include user photos/avatars (Slide 16)
- Add company-specific details or metrics
- Adjust colors, fonts, or spacing to match your preferences

---

## Support

For questions or issues:
- **PowerPoint Help:** IT Support via ServiceNow
- **Content Questions:** Refer to Executive_Proposal.md
- **Technical Issues:** See PPT_Setup/TROUBLESHOOTING.md
- **Copilot Support:** Microsoft Copilot documentation
- **Python Script Issues:** Check INSTALLATION_COMMANDS.md for python-pptx setup
