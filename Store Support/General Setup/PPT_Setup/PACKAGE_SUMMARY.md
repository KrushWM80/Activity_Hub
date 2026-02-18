# PPT Setup Package Summary

## Overview
Complete toolkit for generating PowerPoint presentations programmatically, specifically configured for Walmart's environment and the Activity Hub Executive Proposal.

---

## Files in This Package

### 1. **README.md** (Start Here)
Main documentation covering:
- Quick start guide
- Installation instructions for Walmart environment
- How to generate the Executive Proposal presentation
- Quick reference commands

### 2. **activity_hub_proposal.py** (Main Script)
Python script (600+ lines) that generates:
- 24-slide PowerPoint presentation
- 20 main slides + 7 detail slides
- Complete Activity Hub Executive Proposal
- Walmart branding and formatting

**Usage:**
```powershell
python "General Setup\PPT_Setup\activity_hub_proposal.py"
```

### 3. **INSTALLATION_COMMANDS.md** (Command Reference)
Complete command reference including:
- All installation methods
- Verification commands
- Troubleshooting commands
- Proxy configuration
- Virtual environment setup
- Batch installation script

### 4. **TROUBLESHOOTING.md** (Problem Solving)
Detailed solutions for:
- 403 MediaTypeBlocked errors (Walmart network blocks)
- Proxy connection issues
- SSL certificate errors
- Dependency conflicts
- Import errors
- Permission issues
- 10 common problems with step-by-step solutions

### 5. **COPILOT_PROMPT_FOR_POWERPOINT.md** (AI Guide)
AI-assisted presentation creation:
- Complete Copilot prompt for generating presentations
- Slide-by-slide specifications
- Alternative generation methods
- Customization tips for different audiences
- Template prompts for individual slides

---

## Installation Status

### ✅ Successfully Installed
- python-pptx 1.0.2
- XlsxWriter 3.2.9
- Pillow (already present)
- lxml (already present)
- typing-extensions (already present)

### Installation Method Used
Manual wheel file installation due to Walmart network restrictions:
1. Downloaded `.whl` files on personal device
2. Transferred to work machine
3. Installed locally with `--no-deps` flag

---

## Quick Start Guide

### 1. Verify Installation
```powershell
python -c "import pptx; print('✓ Version:', pptx.__version__)"
```

### 2. Generate Presentation
```powershell
python "General Setup\PPT_Setup\activity_hub_proposal.py"
```

### 3. Open and Customize
- File created: `Activity_Hub_Executive_Proposal.pptx`
- Open in PowerPoint
- Add hyperlinks (Slide 4 → detail slides)
- Replace logo placeholder
- Add charts/graphics
- Customize with your information

---

## Key Features

### Presentation Content
- **Slide 1:** Title slide with Walmart branding
- **Slide 2:** Executive summary (4 key points)
- **Slide 3:** The challenge (split layout)
- **Slide 4:** Solution overview (interactive with 8 components)
- **Slides 7a-7g:** Detail slides for each solution component
- **Slide 8:** Platform architecture
- **Slide 9:** User experience (before/after)
- **Slides 10-12:** Financial model and breakdown
- **Slide 13:** Implementation roadmap (18 months, 4 phases)
- **Slide 14:** Risk mitigation
- **Slide 15:** Success metrics
- **Slide 16:** User testimonials
- **Slide 17:** Competitive analysis (build vs buy)
- **Slide 18:** Next steps and action items
- **Slide 19:** Q&A preparation
- **Slide 20:** Call to action

### Technical Specifications
- **Colors:** Walmart Blue (#004890), Yellow (#FCC810), White, Dark Gray
- **Fonts:** Bogle (fallback: Arial, Calibri)
- **Layouts:** Professional executive format
- **Dimensions:** 10" × 7.5" (standard PowerPoint)
- **Total Slides:** 24 (20 main + 7 detail)

### Branding Elements
- Walmart spark logo placeholder (top right on title slide)
- Consistent color scheme throughout
- Professional typography and sizing
- Clean layouts with proper spacing
- Walmart brand compliance

---

## Walmart-Specific Considerations

### Network Restrictions
- **Problem:** PyPI downloads blocked (403 MediaTypeBlocked)
- **Solution:** Manual wheel file installation
- **Workaround:** Download externally, transfer files, install locally

### Proxy Configuration
```powershell
$env:HTTP_PROXY = "http://proxy.wal-mart.com:8080"
$env:HTTPS_PROXY = "http://proxy.wal-mart.com:8080"
```

### Artifactory (Currently Not Working)
- Connection resets when attempting to use Walmart Artifactory
- Manual installation is more reliable

---

## Use Cases

### 1. Executive Proposals
Generate the Activity Hub proposal or similar executive presentations.

### 2. Custom Presentations
Modify the script to create other Walmart-branded presentations:
- Quarterly business reviews
- Project proposals
- Status reports
- Training materials

### 3. Automated Reporting
Generate presentations from data:
- Pull data from databases
- Create charts and graphs
- Populate slides automatically
- Schedule regular report generation

### 4. Batch Processing
Create multiple presentations:
- Personalized presentations for different audiences
- Regional or market-specific versions
- A/B testing different messaging

---

## Customization Guide

### Modify the Script
The `activity_hub_proposal.py` script is well-structured and easy to customize:

**Change colors:**
```python
WALMART_BLUE = RGBColor(0, 72, 144)  # Modify RGB values
```

**Add new slides:**
```python
# Use helper functions
add_bullet_slide(prs, "Title", ["Bullet 1", "Bullet 2"])
add_split_slide(prs, "Title", "Left Title", left_bullets, "Right Title", right_bullets)
```

**Modify layouts:**
```python
# Adjust positioning (in inches)
left = Inches(1)
top = Inches(2)
width = Inches(8)
height = Inches(1)
```

**Change fonts:**
```python
p.font.size = Pt(24)  # Change size
p.font.bold = True    # Bold text
p.font.color.rgb = WALMART_BLUE  # Change color
```

---

## Best Practices

### Development
- Test changes incrementally
- Keep backup copies of working scripts
- Use version control for script modifications
- Comment your code for maintainability

### Presentation Generation
- Always review generated presentations in PowerPoint
- Test hyperlinks and navigation
- Verify all data and metrics are current
- Proof read all content
- Check for consistent branding

### File Management
- Use descriptive filenames with dates
- Store templates separately from generated files
- Keep source scripts in version control
- Document any customizations made

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Can't install python-pptx | Use manual wheel file installation |
| 403 MediaTypeBlocked | Download .whl files externally and transfer |
| Module not found after install | Verify Python environment matches pip |
| Import error: DLL load failed | Install Visual C++ Redistributables |
| Presentation won't open | Check file permissions, close PowerPoint |
| Slides look wrong | Verify Walmart fonts installed, check color values |
| Script errors | Check Python version (3.8+), verify all imports |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## Support Resources

### Internal Walmart
- **IT Support:** ServiceNow Portal
- **Email:** IT.Support@walmart.com
- **Reference:** "Python Package Installation - Network Access Required"

### External Resources
- **python-pptx Docs:** https://python-pptx.readthedocs.io/
- **GitHub Issues:** https://github.com/scanny/python-pptx/issues
- **Stack Overflow:** Tag questions with `python-pptx`

---

## Related Documentation

### In This Repository
- **Executive Proposal:** `../Production_Path/Executive_Proposal.md`
- **Presentation Outline:** `../Production_Path/Executive_Proposal_Presentation_Outline.md`
- **Figma Specs:** `../Production_Path/Executive_Proposal_Figma_Specs.md`

### External Links
- **Walmart Brand Portal:** [Internal link]
- **Python at Walmart:** [Internal wiki]
- **Artifactory:** https://artifacts.walmart.com/

---

## Future Enhancements

### Potential Additions
- [ ] Template system for multiple presentation types
- [ ] Data integration (pull from databases/APIs)
- [ ] Chart generation from data files
- [ ] Image and logo insertion automation
- [ ] Batch generation scripts for multiple presentations
- [ ] PowerPoint template (.potx) export
- [ ] PDF export functionality
- [ ] Presenter notes automation

### Known Limitations
- Hyperlinks must be added manually in PowerPoint
- Complex charts require PowerPoint chart tools
- Some animations need manual configuration
- Logo must be inserted manually (placeholder provided)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-02 | Initial documentation and setup guides |
| 1.1.0 | 2025-12-03 | Added activity_hub_proposal.py script |
| 1.2.0 | 2025-12-04 | Consolidated documentation, added package summary |

---

## License & Credits

### python-pptx
- **License:** MIT License
- **Author:** Steve Canny
- **Repository:** https://github.com/scanny/python-pptx

### Activity Hub Script
- **Created:** December 2025
- **Purpose:** Walmart Activity Hub Executive Proposal
- **Customization:** Walmart branding and content

---

## Contact

For questions or issues with this package:
1. Check README.md for quick start
2. Review TROUBLESHOOTING.md for common issues
3. Consult INSTALLATION_COMMANDS.md for command reference
4. Submit ServiceNow ticket for IT/network issues
5. Refer to python-pptx documentation for API questions
