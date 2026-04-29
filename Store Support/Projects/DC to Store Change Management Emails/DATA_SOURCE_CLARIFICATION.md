# Data Source Clarification - PC-07 Launch

## Current State (April 29, 2026)

### ⚠️ TEST DATA IN USE

The email pipeline is currently using **SYNTHETIC/FAKE TEST DATA**:

```
Snapshot Files (Testing):
- snapshots_local/manager_snapshot_2026-04-17.json → FAKE test data
- snapshots_local/manager_snapshot_2026-05-01.json → FAKE test data

Data Source: create_synthetic_snapshots.py (generates fake managers)
```

### Test Data Details

**Fake Stores (Test Only):**
- Facility #100 - Rogers, AR
- Facility #103 - Bentonville, AR
- Facility #108 - Fort Smith, AR
- Facility #121 - Little Rock, AR
- Facility #123 - Hot Springs, AR
- Facility #125 - Texarkana, AR
- Facility #130 - Pine Bluff, AR
- Facility #136 - Fayetteville, AR

**Fake Manager Names (Test Only):**
- JAMES RICHARDSON, LISA ANDERSON, MARK STEPHENS, PATRICIA LOPEZ, etc.

---

## May 1, 2026 Production - REAL DATA

### Real Data Flow

**05:00 AM - Snapshot Generation:**
```
sdl_scraper.py (Playwright automation)
  ↓
  Logs into SDL (Store Directory Lookup)
  ↓
  Exports real manager data from Walmart SDL system
  ↓
  Saves to: snapshots_local/manager_snapshot_2026-05-01.json
```

**Real Data Will Include:**
- ✅ REAL store numbers from Walmart system
- ✅ REAL manager names from SDL
- ✅ REAL location names and markets
- ✅ REAL role assignments (Store Manager, Market Manager, Region Manager)

**06:00 AM - PayCycle Execution:**
```
send_paycycle_production_email_generic.py (with TEST_MODE=False)
  ↓
  Loads real snapshots from May 1
  ↓
  Compares with April 17 real snapshots
  ↓
  Detects REAL manager changes
  ↓
  Routes to affected DC leadership
  ↓
  Sends from: atcteamsupport@walmart.com
  ↓
  To: atcteamsupport@walmart.com
  ↓
  BCC: Affected DC GMs/AGMs + monitoring team
```

---

## Status Summary

| Component | Current Status | May 1 Status |
|-----------|--------|---|
| Snapshots | FAKE (test) | REAL (from SDL) |
| Manager Names | Synthetic | Real |
| Store Numbers | Test values | Real Walmart stores |
| Email Recipients | You only (TEST_MODE) | DC leadership (PROD MODE) |
| Data Source | create_synthetic_snapshots.py | sdl_scraper.py |

---

## Important Notes

1. **Testing Phase (April 29):** Use fake data to verify email formatting, routing logic, and delivery
2. **Production Phase (May 1):** Real SDL data replaces test data automatically
3. **No Manual Changes Needed:** When SDL scraper runs May 1 @ 05:00 AM, it will create real snapshots
4. **Fallback Logic:** If SDL scraper fails, daily_check_smart.py will retry for 7 days

---

## Verification Checklist for May 1

- [ ] sdl_scraper.py runs at 05:00 AM and creates real snapshot
- [ ] Real snapshot contains actual Walmart manager data
- [ ] send_paycycle_production_email_generic.py runs at 06:00 AM with real data
- [ ] Email routed to correct DC leadership based on real changes
- [ ] atcteamsupport@walmart.com receives email with real facility data
- [ ] Kristine Torres, Matthew Farnworth, Kendall Rush see in BCC
- [ ] No synthetic/test data appears in production email
