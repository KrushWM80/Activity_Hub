# Zorro Project - Setup Action Plan
**Start Date:** March 3, 2026

---

## 📋 Executive Summary

The Zorro Project is **60% ready** to run. It has excellent code and documentation, but needs:

1. **Network access** to install Python packages (BLOCKING)
2. **FFmpeg** system tool installation
3. **API keys** from the Retina GenAI team
4. **Python packages** installation (30-45 minutes)

**Estimated time to full launch:** 2 days (depends on network & API key approval)

---

## ✅ What's Already Done

- ✅ Knowledge Base & Mapping reviewed (810-line document)
- ✅ Architecture documented and verified
- ✅ All source code present and organized
- ✅ Configuration templates ready
- ✅ Test suite prepared
- ✅ Created comprehensive setup docs:
  - ZORRO_SETUP_REVIEW.md (detailed review)
  - SETUP_SUMMARY.md (timeline & next steps)
  - DEPENDENCY_MATRIX.md (complete dependency mapping)
  - verify_setup.py (automated verification)

---

## 🎯 Action Items (In Priority Order)

### CRITICAL: Unblock Network Access

**Current Issue:** PyPI is blocked on Walmart network

**Action 1: Contact IT** (Do this FIRST - TODAY)
- [ ] Open ticket with IT Help Desk
- [ ] Request: PyPI access for `pip` package manager
- [ ] Provide: This URL list for whitelisting:
  - `pypi.org`
  - `pypi.python.org`
  - `files.pythonhosted.org`
  - `cdn.jsdelivr.net` (for some packages)
- [ ] Alternative: Ask if corporate proxy available
- [ ] Submit today, expect response within 24-48 hours

**Contact Info:**
- Email: IT Help Desk / ServiceNow
- Slack: #help-general or #it-support
- Subject: "Request PyPI access for Python development"

**Action 2: Test Network Access**
Once IT responds, test with:
```powershell
pip install pytest
```

If this works, PyPI is unblocked. ✅

**Action 3: Contact #help-genai-media-studio** (Parallel with IT)
- [ ] Message: "We're implementing Zorro; what's the approved way to install Python packages on Walmart network?"
- [ ] Ask: "Is there a pre-built Python environment or package mirror?"
- [ ] This may have a faster solution

---

### HIGH: Get API Credentials

**Action 4: Get WALMART_SSO_TOKEN** (Start NOW, runs in parallel)
- [ ] Join Slack channel: #help-genai-media-studio
- [ ] Send message:
  ```
  Hi team,
  We're setting up the Zorro project on this system.
  Can you provide a WALMART_SSO_TOKEN for video generation API access?
  Project: Zorro-001
  Use case: Testing video generation pipeline
  ```
- [ ] Expected response time: 2-4 hours (or next business day)
- [ ] Store token in `.env` file (see Step 5 below)

---

### MEDIUM: Install System Tools

**Action 5: Install FFmpeg** (Can do anytime)
```powershell
# Option A: Using Chocolatey (recommended)
choco install ffmpeg

# Option B: If Chocolatey not available
# 1. Download from: https://ffmpeg.org/download.html
# 2. Extract to: C:\ffmpeg
# 3. Add to PATH:
$env:Path += ";C:\ffmpeg\bin"
```

Verify:
```powershell
ffmpeg -version
```

Should show version info. ✅

---

### HIGH: Install Python Packages (Once Network Unblocked)

**Action 6: Install from requirements.txt**
```powershell
# Navigate to project
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Zorro"

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Install all packages (30-45 minutes)
pip install -r requirements.txt

# Verify installation
python verify_setup.py
```

Expected output:
```
✅ ALL CHECKS PASSED - System is ready for Zorro!
```

---

### MEDIUM: Configure Environment

**Action 7: Create .env file**
```powershell
# Copy template
Copy-Item .env.example .env

# Open in editor
notepad .env
```

**Action 8: Edit `.env` with your credentials**
```dotenv
# CRITICAL - Get these from Retina GenAI team
WALMART_SSO_TOKEN=<paste-token-here>

# Internal network - MUST be false
WALMART_SSL_VERIFY=false

# Use passthrough - recommended for Walmart network
LLM_PROVIDER=passthrough

# Optional - for development testing
DEBUG=false
LOG_LEVEL=INFO
```

---

### LOW: Start Application & Test

**Action 9: Launch Streamlit App**
```powershell
cd "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Zorro"
streamlit run app.py
```

Browser should open to: `http://localhost:8501`

**Action 10: Test Core Features**
- [ ] Navigate to "Design Studio"
- [ ] Under "Preloaded Templates", select "Example Character"
- [ ] Click "View in Design Editor"
- [ ] Try creating a simple video prompt
- [ ] Generate test video (if API working)

---

### OPTIONAL: Run Full Test Suite

**Action 11: Execute Tests**
```powershell
pytest -v
```

This validates all components. Expect output showing:
- Test discovery
- Test execution
- Pass/fail summary

---

## 📅 Timeline

| Day | Actions | Estimated Time | Blocking? |
|-----|---------|-----------------|-----------|
| **Today (Day 1)** | 1. Contact IT for PyPI<br>2. Contact #help-genai-media-studio<br>3. Request API token<br>4. Install FFmpeg | ~30 min actual work | Waiting on IT |
| **Day 2** | 5. Install Python packages (once network OK)<br>6. Create .env file<br>7. Add API token | ~1 hour | Network access |
| **Day 3** | 8. Start application<br>9. Test features<br>10. (Optional) Run tests | ~30 min | API token |
| **TOTAL** | **Full Launch** | **~2 hours actual work** | **2 days real time** |

---

## 🚀 Quick Command Cheat Sheet

### Setup Commands
```powershell
# Activate environment
& ".\.venv\Scripts\Activate.ps1"

# Install dependencies (after network unblocked)
pip install -r requirements.txt

# Verify setup
python verify_setup.py

# Configure environment
notepad .env

# Start application
streamlit run app.py

# Run tests
pytest -v
```

### Troubleshooting Commands
```powershell
# Check Python version
python --version

# Check specific package
python -c "import streamlit; print('✓ Installed')"

# Check FFmpeg
ffmpeg -version

# View environment variables
Get-Content .env

# Kill Streamlit (if stuck)
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process -Force
```

---

## 📞 Support Contacts

### Network Access (PyPI)
- **Channel:** ServiceNow or IT Help Desk
- **Time:** 24-48 hours typical response
- **What to request:** PyPI domain whitelisting

### Zorro Setup Issues
- **Channel:** #help-genai-media-studio on Slack
- **Response time:** 2-4 hours
- **What to ask:** "Approved way to install Python packages"

### API Credentials
- **Channel:** #help-genai-media-studio on Slack
- **Response time:** 2-4 hours
- **What to request:** `WALMART_SSO_TOKEN` for video API

### General Troubleshooting
- **Knowledge Base:** [docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md](docs/KNOWLEDGE_BASE_AND_DEPENDENCY_MAP.md)
- **Common Issues:** Search "Common Pitfalls & Solutions" section
- **Setup Guide:** [ZORRO_SETUP_REVIEW.md](ZORRO_SETUP_REVIEW.md)

---

## ✨ Success Criteria

You'll know setup is successful when:

1. ✅ **Network**
   - `pip install pytest` completes successfully
   - No "Connection refused" errors

2. ✅ **Packages**
   - `python verify_setup.py` shows "✅ ALL CHECKS PASSED"
   - Only shows ✗ for Phase 2 packages (sqlalchemy, etc.)

3. ✅ **Environment**
   - `.env` file exists and has WALMART_SSO_TOKEN
   - No errors when sourcing .env

4. ✅ **Application**
   - `streamlit run app.py` starts without errors
   - Browser opens to `http://localhost:8501`
   - Can navigate to Design Studio tab

5. ✅ **API**
   - (Optional) Can view sample AMP messages
   - (Optional) Can generate test video

---

## 🎯 Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Documentation reviewed | 100% | 100% | ✅ Done |
| Code reviewed | 100% | 100% | ✅ Done |
| Python packages | 100% | 46% | ⏳ Waiting for network |
| System tools | 100% | 0% | ⏳ Ready to install |
| API access | Yes | No | ⏳ Waiting for IT |
| **Ready to launch** | Yes | No | ⏳ 2 days away |

---

## 📝 Tracking Checklist

Copy this checklist and check off items as you complete them:

```
NETWORK & TOOLS:
☐ Day 1: Contact IT for PyPI access
☐ Day 1: Contact #help-genai-media-studio 
☐ Day 1: Install FFmpeg
☐ Day 1: Verify FFmpeg: ffmpeg -version
☐ Day 2: Test network access: pip install pytest
☐ Day 2: Confirm PyPI is unblocked

PACKAGES & ENVIRONMENT:
☐ Day 2: Install requirements: pip install -r requirements.txt
☐ Day 2: Verify packages: python verify_setup.py
☐ Day 2: Copy env template: Copy-Item .env.example .env
☐ Day 2: Request WALMART_SSO_TOKEN from team
☐ Day 3: Receive API token
☐ Day 3: Add token to .env file
☐ Day 3: Verify .env is complete

APPLICATION & TESTING:
☐ Day 3: Start app: streamlit run app.py
☐ Day 3: Test Design Studio tab loads
☐ Day 3: Test navigation works
☐ Day 3: (Optional) Generate test video
☐ Day 3: (Optional) Run pytest -v

FINAL:
☐ All items above complete
☐ No errors in application startup
☐ Documentation reviewed
☐ Ready for Phase 1 features
```

---

## 🔑 Key Files to Know

| File | Purpose | Status |
|------|---------|--------|
| `requirements.txt` | All Python dependencies | ✅ Ready |
| `.env.example` | Environment template | ✅ Ready |
| `.env` | Your actual secrets (create from example) | ❌ Create me |
| `verify_setup.py` | Automated setup checker | ✅ Ready |
| `app.py` | Main Streamlit application | ✅ Ready |
| `config/config.yaml` | Application configuration | ✅ Ready |
| `ZORRO_SETUP_REVIEW.md` | Detailed setup guide | ✅ Ready |
| `SETUP_SUMMARY.md` | Timeline and next steps | ✅ Ready |
| `DEPENDENCY_MATRIX.md` | Complete dependency map | ✅ Ready |

---

## Important Notes

1. **Network is the blocker** - Everything else can be done in parallel while waiting for IT
2. **Do IT and Slack requests TODAY** - These have the longest lead time
3. **FFmpeg can be installed anytime** - Independent of other steps
4. **PyTorch is large** - 2-3 GB download and install, plan for 45+ minutes
5. **Keep .env secret** - Don't commit to Git, contains API tokens
6. **SSL verification is required to be false** - Walmart uses internal certs

---

## Final Reminders

✅ **Before starting:**
- Ensure 20 GB free disk space (for PyTorch + packages)
- Have admin access (for FFmpeg and Python install)
- Know your Walmart network access level

✅ **While installing:**
- Be patient with PyTorch (large download)
- Don't interrupt pip installs mid-way
- Keep terminal window open

✅ **After launching:**
- Save any test videos before restarting
- Keep .env file secure
- Reference knowledge base for features

---

**Status:** Ready for Implementation  
**Total Work:** ~2 hours actual time  
**Total Calendar Time:** ~2 days (waiting for approvals)  
**Last Updated:** March 3, 2026

**Next Action:** Contact IT for PyPI access (TODAY) ➡️
