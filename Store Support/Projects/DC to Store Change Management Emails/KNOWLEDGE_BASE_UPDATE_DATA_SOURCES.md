# Knowledge Base Update - Data Source & Test vs Production (April 29)

## Summary of Changes

Updated all documentation and code to clearly distinguish between:
1. **TEST DATA** (currently in use)
2. **PRODUCTION DATA** (starts May 1, 2026)

---

## Files Updated

### Documentation (4 files)
✅ `README.md` - Added "Data Source Information" section
✅ `QUICK_START_PAYCYCLE.md` - Added test data warning
✅ `DATA_SOURCE_CLARIFICATION.md` - NEW comprehensive guide
✅ `paycycle_tracking.json` - Added data source note in metadata

### Code (1 file)
✅ `create_synthetic_snapshots.py` - Added ⚠️ WARNING in docstring

---

## Key Points for Knowledge Base

### Current State (April 29, 2026)
- **Data Source:** `create_synthetic_snapshots.py` (FAKE test data)
- **Snapshots Used:**
  - `snapshots_local/manager_snapshot_2026-04-17.json` → SYNTHETIC
  - `snapshots_local/manager_snapshot_2026-05-01.json` → SYNTHETIC
- **Purpose:** Testing email pipeline, formatting, routing logic
- **Data Quality:** NOT for production decisions

### Manager Names Currently in Use (TEST ONLY)
```
JAMES RICHARDSON, LISA ANDERSON, MARK STEPHENS, PATRICIA LOPEZ,
ROBERT WILLIAMS, JENNIFER MARTINEZ, DAVID BROWN, SUSAN TAYLOR
```

### Fake Stores Currently in Use (TEST ONLY)
```
100 - Rogers, AR
103 - Bentonville, AR
108 - Fort Smith, AR
121 - Little Rock, AR
123 - Hot Springs, AR
125 - Texarkana, AR
130 - Pine Bluff, AR
136 - Fayetteville, AR
```

---

## May 1, 2026 - Production Data Flow

### 05:00 AM - SDL Scraper Execution
```python
sdl_scraper.py runs automatically
├─ Uses Playwright browser automation
├─ Authenticates to Walmart SDL system
├─ Exports REAL manager data
├─ Saves to: snapshots_local/manager_snapshot_2026-05-01.json
└─ Contains: Real store numbers, real manager names, real roles
```

### 06:00 AM - PayCycle Execution
```python
send_paycycle_production_email_generic.py 7 (with TEST_MODE=False)
├─ Loads REAL May 1 snapshot from SDL scraper
├─ Compares with REAL April 17 snapshot
├─ Detects REAL manager changes
├─ Routes to affected DC leadership
├─ From: atcteamsupport@walmart.com
├─ To: atcteamsupport@walmart.com
└─ BCC: Affected DCs + Kristine Torres + Matthew Farnworth + Kendall Rush
```

---

## Why This Matters

### Testing Phase (Now)
- ✅ Verify email formatting with fake data
- ✅ Test DC routing logic
- ✅ Confirm SMTP delivery works
- ✅ Validate recipient email addresses
- ✅ Practice monitoring and tracking

### Production Phase (May 1+)
- ✅ Automatic transition to real SDL data
- ✅ No code changes needed (automated)
- ✅ Email recipients see real manager changes
- ✅ DC leadership notified of actual staffing changes
- ✅ System tracks real business events

---

## Verification Checklist

- [ ] Documentation clearly states test vs production data
- [ ] Synthetic snapshots marked as FAKE
- [ ] SDL scraper scheduled for May 1 @ 05:00 AM
- [ ] PayCycle task scheduled for May 1 @ 06:00 AM
- [ ] TEST_MODE=False only in production (never in test)
- [ ] Email recipients list correct (atcteamsupport@walmart.com)
- [ ] BCC list includes all 3 team members
- [ ] No confusion between test data and real data

---

## Error Prevention

### ❌ Do NOT
- Use synthetic data for business decisions
- Assume test manager names are real
- Store test snapshots as backups (they'll be overwritten)
- Include test data in production reports

### ✅ DO
- Always check `DATA_SOURCE_CLARIFICATION.md` if uncertain
- Use real snapshots for all business analysis
- Archive production snapshots for compliance
- Review both test and production emails before May 1

---

## Communication

When discussing with stakeholders:
- "We're currently testing with synthetic data"
- "Production data starts May 1 from SDL system"
- "No business changes are based on test data"
- "Real manager changes will be detected on May 1"

