# Job Codes Dashboard - Access Guide

**Status: March 12, 2026**

---

## âœ… CURRENT SOLUTION: Use IP Address (WORKING NOW)

### ðŸ”— Access URL (IP-Based)
```
http://10.97.114.181:8080/static/index.html#
```

**This works NOW.** No DNS changes needed yet.

---

## ðŸ“‹ What's the Issue?

Your bookmarked URL uses a hostname that currently points to the **wrong IP**:

| Aspect | Current | Issue |
|--------|---------|-------|
| **Bookmarked URL** | `http://leus62315243171.homeoffice.wal-mart.com:8080/static/index.html#` | âœ— DNS points to 10.97.108.66 |
| **Actual Service Location** | `10.97.114.181:8080` | âœ“ Service IS running here |
| **DNS A Record** | Points to 10.97.108.66 | âœ— No service on this IP |

---

## ðŸ”§ PERMANENT FIX (Requires IT)

**Contact IT and request:**

> Please update the DNS A record for `leus62315243171.homeoffice.wal-mart.com` to point to `10.97.114.181` instead of `10.97.108.66`

**Why this fix?**
- Your bookmarked URL will work naturally
- No IP addresses to remember
- Properly aligned with actual server location

---

## ðŸš€ IMMEDIATE WORKAROUNDS

### Option 1: Update Bookmarks (Recommended)
Replace your bookmark with:
```
http://10.97.114.181:8080/static/index.html#
```

### Option 2: Create Hosts File Entry (This Machine Only)
Add this line to `C:\Windows\System32\drivers\etc\hosts`:
```
10.97.114.181 leus62315243171.homeoffice.wal-mart.com
```
*(Requires Administrator; only affects this machine)*

### Option 3: Wait for IT DNS Fix
- Service is running and accessible
- Once DNS is fixed, your original URL works

---

## ðŸ“ž IT Escalation Template

If you need to contact IT, use this information:

```
Subject: Update DNS A Record - Job Codes Dashboard

Details:
- Hostname: leus62315243171.homeoffice.wal-mart.com
- Current DNS: 10.97.108.66 (no service)
- Should be: 10.97.114.181 (service running)
- Application: Job Codes Dashboard
- Port: 8080

Impact: Users cannot access Job Codes Dashboard through hostname
Request: Update A record to point to correct IP
```

---

## âœ¨ Configuration Reference

See [config.py](./config.py) for detailed configuration options:
- Hostname vs IP switch
- Server settings
- File paths
- Email configuration

---

## ðŸ“Š Status Dashboard

Current Active Configuration:
```python
ACTIVE_CONNECTION = "IP"
ACCESS_URL = "http://10.97.114.181:8080/static/index.html#"
ACCESS_DESCRIPTION = "IP Address (Direct - No DNS)"
```

**Switch to hostname** in config.py once DNS is fixed.

---

**Last Updated:** March 12, 2026
**Service Status:** âœ… Running
**Access Status:** âœ… Available via IP

