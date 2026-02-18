# Projects in Stores Dashboard - Admin Quick Reference

## Access
| Item | Value |
|------|-------|
| **URL** | `http://localhost:8001/admin` |
| **Login** | `kendall.rush` / `admin2026` |
| **Backup** | `admin` / `copilot123` |

---

## Actions at a Glance

| Button | When to Use | Result |
|--------|-------------|--------|
| ✅ **Approve** | Fix is correct and safe | Code auto-applies |
| ❌ **Deny** | Fix is wrong or risky | No changes made |
| ⏸️ **Hold** | Need more time/info | Stays in queue |

---

## Review Checklist

Before approving any fix:

- [ ] Read the **Investigation Notes** - understand how AI reached conclusion
- [ ] Compare **Current Code** vs **New Code** - verify the change is correct
- [ ] Check **File to Modify** - confirm correct file is targeted
- [ ] Look for **⚠️ NEEDS REVIEW** badge - extra caution required
- [ ] Consider side effects - could this break something else?

---

## Priority Response Times

| Priority | Target |
|----------|--------|
| 🔴 HIGH | Same day |
| 🟡 MEDIUM | 1-2 days |
| 🟢 LOW | 1 week |

---

## Common Categories

| Category | Typical Issues |
|----------|----------------|
| `filter_issue` | Search/dropdown not working correctly |
| `display_bug` | UI not rendering properly |
| `data_issue` | Wrong data showing |

---

## When to Escalate

Contact development team if:
- Change involves authentication/security
- Multiple files need modification
- Code change is 15+ lines
- You're unsure about the impact

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't login | Clear cookies, try backup credentials |
| Fix failed to apply | Code may have changed; contact dev team |
| Dashboard not loading | Check server at `localhost:8001/api/health` |

---

**Support Email**: ATCteamsupport@walmart.com
