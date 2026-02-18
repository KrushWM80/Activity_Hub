# Local Hosting Decision Guide

## Which Method Should You Use?

Answer these questions to determine the best local hosting approach for your project.

---

## Quick Decision Tree

```
                    Does your project need to...
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
    Respond to web requests?            Run tasks automatically?
    (Dashboard, API, UI)                (Reports, emails, sync)
            │                                   │
            ▼                                   ▼
    ┌───────────────┐                   ┌───────────────┐
    │  CONTINUOUS   │                   │   SCHEDULED   │
    │    SERVER     │                   │  AUTOMATION   │
    │   (Method 2)  │                   │   (Method 1)  │
    └───────────────┘                   └───────────────┘
```

---

## Decision Questions

### Question 1: What does your project DO?

| If your project... | Use This Method |
|-------------------|-----------------|
| Serves a dashboard/webpage to users | **Continuous Server** |
| Provides an API for other systems | **Continuous Server** |
| Sends automated emails/reports | **Scheduled Automation** |
| Syncs data between systems | **Scheduled Automation** |
| Monitors for changes and alerts | **Scheduled Automation** |
| Processes files on a schedule | **Scheduled Automation** |

### Question 2: How do users interact with it?

| If users... | Use This Method |
|-------------|-----------------|
| Open a URL in their browser | **Continuous Server** |
| Receive emails/notifications | **Scheduled Automation** |
| Don't interact directly (automated) | **Scheduled Automation** |
| Need real-time data access | **Continuous Server** |
| Need data at specific times | **Scheduled Automation** |

### Question 3: When does it need to run?

| If it runs... | Use This Method |
|---------------|-----------------|
| 24/7 always available | **Continuous Server** |
| At specific times (hourly, daily) | **Scheduled Automation** |
| Only when triggered by an event | **Scheduled Automation** |
| Whenever a user wants to access it | **Continuous Server** |

### Question 4: What resources does it use?

| If it needs... | Use This Method |
|----------------|-----------------|
| Constant memory allocation | **Continuous Server** |
| Resources only when running | **Scheduled Automation** |
| Open network port | **Continuous Server** |
| No network port | **Scheduled Automation** |

---

## Method Comparison

| Aspect | Scheduled Automation | Continuous Server |
|--------|---------------------|-------------------|
| **Best For** | Background tasks, reports, emails | Dashboards, APIs, web UIs |
| **Runs** | On schedule, then exits | Always running |
| **Memory** | Only when executing | Constant |
| **Network Port** | Not required | Required |
| **Team Access** | Via email/files | Via URL |
| **Startup** | Task Scheduler | Startup shortcut/task |
| **Complexity** | Lower | Higher |
| **Admin Required** | Sometimes | Sometimes |

---

## Method 1: Scheduled Automation

### When to Use
✅ Automated reports that run daily/hourly  
✅ Email notifications on changes  
✅ Data sync between systems  
✅ File processing on schedule  
✅ Monitoring and alerting  
✅ Batch processing tasks  

### Real Example: DC to Store Change Management Emails
- Runs hourly via Task Scheduler
- Scrapes data, detects changes, sends emails
- No web interface needed
- Team receives emails, doesn't interact with system

### Key Files Needed
```
your-project/
├── main_script.py          # Your automation logic
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── setup_task.bat          # Creates scheduled task
└── README.md               # Documentation
```

📁 **Template Location:** `./Scheduled Automation System/`

---

## Method 2: Continuous Running Server

### When to Use
✅ Dashboards that team members access  
✅ APIs that other systems call  
✅ Real-time data displays  
✅ Interactive web applications  
✅ Always-available services  
✅ Multi-user web apps  

### Real Example: Intake Hub / Projects in Stores Dashboard
- FastAPI server on port 8001
- Team accesses via VPN at http://10.97.105.88:8001
- Must run 24/7 for availability
- Interactive dashboard with search, export, AI chat

### Key Files Needed
```
your-project/
├── backend/
│   ├── main.py             # FastAPI/Flask server
│   ├── requirements.txt    # Python dependencies
│   └── start_server.ps1    # Server startup script
├── frontend/
│   └── index.html          # Web interface
├── create_startup_shortcut.ps1   # Auto-start on login
├── setup_auto_startup.ps1        # Auto-start on boot (admin)
└── README.md               # Documentation
```

📁 **Template Location:** `./Continous Running Server - HTTP Port/`

---

## Hybrid Approach

Some projects may need **BOTH** methods:

**Example Scenario:**
- Dashboard shows real-time data (Continuous Server)
- Background job refreshes data every hour (Scheduled Automation)

**Implementation:**
1. Set up continuous server for the web interface
2. Add scheduled task to refresh/sync data periodically
3. Server serves cached/fresh data to users

---

## Decision Checklist

Before choosing, verify:

- [ ] What is the primary user interaction?
- [ ] How often does the process need to run?
- [ ] Does it need to be accessible via URL?
- [ ] What happens if it's not running? (Impact)
- [ ] Do I have admin access for scheduled tasks?
- [ ] Will I always be logged in (for startup shortcuts)?

---

## Quick Reference

### I need a dashboard → **Continuous Server**
### I need automated emails → **Scheduled Automation**
### I need an API → **Continuous Server**
### I need scheduled reports → **Scheduled Automation**
### I need real-time data → **Continuous Server**
### I need periodic sync → **Scheduled Automation**

---

## Next Steps

1. **Decided on Scheduled Automation?**
   → Go to `./Scheduled Automation System/README.md`

2. **Decided on Continuous Server?**
   → Go to `./Continous Running Server - HTTP Port/README.md`

3. **Need both?**
   → Start with Continuous Server, then add Scheduled tasks

---

## Support

- **Scheduled Automation Example:** `C:\Users\krush\Documents\VSCode\Store Support\Projects\DC to Store Change Management Emails`
- **Continuous Server Example:** `C:\Users\krush\Documents\VSCode\Intake Hub\ProjectsinStores`

Review these working implementations for detailed examples.
