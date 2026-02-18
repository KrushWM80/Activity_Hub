# Local Hosting Guide

Choose the right hosting method for your local projects.

---

## 🎯 Start Here: Which Method Do You Need?

| I need to... | Use This Method |
|--------------|-----------------|
| Serve a dashboard/webpage | [Continuous Server](#method-2-continuous-server) |
| Send automated emails/reports | [Scheduled Automation](#method-1-scheduled-automation) |
| Create an API | [Continuous Server](#method-2-continuous-server) |
| Run tasks hourly/daily | [Scheduled Automation](#method-1-scheduled-automation) |
| Show real-time data | [Continuous Server](#method-2-continuous-server) |
| Sync data periodically | [Scheduled Automation](#method-1-scheduled-automation) |
| **Share with team on VPN** | [Network Sharing Guide](./NETWORK_SHARING.md) |

**📖 Not sure?** → Read the [Decision Guide](./DECISION_GUIDE.md)

---

## Method 1: Scheduled Automation

**Best for:** Background tasks, reports, emails, data sync

```
Task Scheduler → Runs Script → Produces Output → Script Exits
```

- Runs on schedule (hourly, daily, etc.)
- Uses resources only when executing
- No web interface needed
- Team receives output via email/files

**📁 Template:** [Scheduled Automation System/](./Scheduled%20Automation%20System/)

**🔗 Real Example:** DC to Store Change Management Emails
- Location: `C:\Users\krush\Documents\VSCode\Store Support\Projects\DC to Store Change Management Emails`
- Runs hourly, detects changes, sends emails

---

## Method 2: Continuous Server

**Best for:** Dashboards, APIs, web applications

```
System Boots → Server Starts → Always Running → Users Access via URL
```

- Runs 24/7, always available
- Serves web pages/APIs
- Team accesses via browser
- Uses constant resources

**📁 Template:** [Continous Running Server - HTTP Port/](./Continous%20Running%20Server%20-%20HTTP%20Port/)

**🔗 Real Example:** Projects in Stores Dashboard
- Location: `C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores`
- FastAPI on port 8001
- VPN Access: http://10.97.105.88:8001

---

## Quick Comparison

| Aspect | Scheduled Automation | Continuous Server |
|--------|---------------------|-------------------|
| **Runs** | On schedule, then exits | Always running |
| **Team Access** | Via email/files | Via URL in browser |
| **Memory** | Only when executing | Constant |
| **Network Port** | Not needed | Required (e.g., 8001) |
| **Best For** | Reports, emails, sync | Dashboards, APIs |

---

## Documentation

| File | Purpose |
|------|---------|
| [DECISION_GUIDE.md](./DECISION_GUIDE.md) | Detailed decision tree and comparison |
| [QUICKSTART.md](./QUICKSTART.md) | Quick setup instructions |
| [**NETWORK_SHARING.md**](./NETWORK_SHARING.md) | **Share dashboards with team via VPN** |
| [Scheduled Automation System/](./Scheduled%20Automation%20System/) | Template for scheduled tasks |
| [Continous Running Server/](./Continous%20Running%20Server%20-%20HTTP%20Port/) | Template for web servers |

---

## Working Examples

### 1. Scheduled Automation: DC to Store Change Management Emails
**Path:** `C:\Users\krush\Documents\VSCode\Store Support\Projects\DC to Store Change Management Emails`

| Aspect | Detail |
|--------|--------|
| Schedule | Every hour via Task Scheduler |
| Purpose | Detect manager changes, send emails |
| Key Files | `setup_hourly_task.bat`, `daily_check.py` |
| Output | Email notifications |

### 2. Continuous Server: Projects in Stores Dashboard  
**Path:** `C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores`

| Aspect | Detail |
|--------|--------|
| Schedule | Always running (24/7) |
| Purpose | Interactive dashboard |
| Key Files | `backend/main.py`, `create_startup_shortcut.ps1` |
| Access | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8001` |

### 3. Continuous Server: Job Code Teaming Dashboard
**Path:** `C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard`

| Aspect | Detail |
|--------|--------|
| Schedule | Always running (24/7) |
| Purpose | Job code teaming management |
| Key Files | `backend/main.py`, `start.ps1` |
| Access | `http://LEUS62315243171.homeoffice.Wal-Mart.com:8080` |

---

## 🌐 Network Sharing

**Want to share your dashboard with teammates?** See [NETWORK_SHARING.md](./NETWORK_SHARING.md)

Quick reference - your permanent hostname:
```
http://LEUS62315243171.homeoffice.Wal-Mart.com:<PORT>
```

Use different ports for different services (8080, 8081, 8000, etc.)
