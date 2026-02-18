# PowerPoint Automation Setup

## Quick Start

This folder contains everything needed to generate PowerPoint presentations programmatically using python-pptx.

### What's Included
- **activity_hub_proposal.py** - Python script to generate the Executive Proposal presentation
- **INSTALLATION_COMMANDS.md** - Quick reference for all installation commands
- **TROUBLESHOOTING.md** - Solutions for common installation issues
- **COPILOT_PROMPT_FOR_POWERPOINT.md** - AI prompts for PowerPoint generation

---

## Installation (Walmart Environment)

### ⚠️ Known Issue
Walmart's network blocks direct pip installation due to security policies (403 MediaTypeBlocked error).

### ✅ Working Solution: Manual Install

**Step 1: Download wheel files** (on personal device/home network)
- python-pptx: https://pypi.org/project/python-pptx/#files
  - Download: `python_pptx-1.0.2-py3-none-any.whl`
- XlsxWriter: https://pypi.org/project/XlsxWriter/#files
  - Download: `xlsxwriter-3.2.9-py3-none-any.whl`

**Step 2: Transfer files** to your Walmart machine (USB, email, OneDrive)

**Step 3: Install locally**
```powershell
# Install python-pptx (without trying to download dependencies)
python -m pip install --no-deps C:\Users\[YourUsername]\Downloads\python_pptx-1.0.2-py3-none-any.whl

# Install XlsxWriter dependency
python -m pip install C:\Users\[YourUsername]\Downloads\xlsxwriter-3.2.9-py3-none-any.whl

# Verify installation
python -c "import pptx; print('✓ python-pptx version:', pptx.__version__)"
```

Expected output: `✓ python-pptx version: 1.0.2`

**Note:** Pillow, lxml, and typing-extensions are typically already installed in Walmart Python environments.

---

## Generating the Executive Proposal Presentation

Once python-pptx is installed, generate the Activity Hub presentation:

```powershell
# Run the generator script
python "General Setup\PPT_Setup\activity_hub_proposal.py"

# Output: Activity_Hub_Executive_Proposal.pptx (24 slides)
```

**What gets generated:**
- 20 main slides covering the complete executive proposal
- 7 detail slides (7a-7g) for solution components
- Walmart branding (colors, fonts, layouts)
- Professional formatting and structure

**After generation:**
1. Open in PowerPoint
2. Add hyperlinks on Slide 4 (solution boxes → detail slides)
3. Replace "[Walmart Spark Logo]" with actual logo
4. Add charts/graphics where noted
5. Customize with your name, date, contact info

---

## Quick Reference

### Generate Presentation
```powershell
python "General Setup\PPT_Setup\activity_hub_proposal.py"
```

### Test Installation
```powershell
python -c "import pptx; print('✓ Version:', pptx.__version__)"
```

### Common Issues
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions to:
- 403 MediaTypeBlocked errors
- Proxy connection issues
- SSL certificate errors
- Missing dependencies

### All Commands
See [INSTALLATION_COMMANDS.md](INSTALLATION_COMMANDS.md) for complete command reference.

### AI Generation
See [COPILOT_PROMPT_FOR_POWERPOINT.md](COPILOT_PROMPT_FOR_POWERPOINT.md) for using AI to create or modify presentations.

---

## Walmart Branding (Built into Script)

The activity_hub_proposal.py script uses these Walmart brand standards:

### Colors
- **Walmart Blue:** RGB(0, 72, 144) #004890
- **Walmart Yellow:** RGB(252, 200, 16) #FCC810
- **White:** RGB(255, 255, 255)
- **Dark Gray:** RGB(50, 50, 50)

### Typography
- **Primary Font:** Bogle (fallback: Arial, Calibri)
- **Title Size:** 44-60 pt
- **Body Text:** 18-24 pt

---

## Additional Resources

- **python-pptx Docs:** https://python-pptx.readthedocs.io/
- **API Reference:** https://python-pptx.readthedocs.io/en/latest/api/
- **GitHub:** https://github.com/scanny/python-pptx
- **Walmart IT Support:** ServiceNow Portal

---

## Package Information

- **Package:** python-pptx v1.0.2
- **Python:** 3.8+ required
- **License:** MIT
- **Dependencies:** Pillow, XlsxWriter, lxml, typing-extensions

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-02 | 1.0.0 | Initial setup documentation |
| 2025-12-03 | 1.1.0 | Added activity_hub_proposal.py script |
| 2025-12-04 | 1.2.0 | Consolidated and simplified documentation |
