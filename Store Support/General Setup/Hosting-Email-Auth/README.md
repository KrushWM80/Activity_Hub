# Hosting, Email & Authentication Learnings

This folder contains key learnings and reusable patterns for **local hosting, email automation, and authentication** — drawn from multiple Activity Hub projects.

---

## 📋 Contents

1. **[USER_AUTHENTICATION.md](./USER_AUTHENTICATION.md)** - Login/Auth implementation patterns
2. **[LOCAL_HOSTING_SETUP.md](./LOCAL_HOSTING_SETUP.md)** - How to set up and run the local server
3. **[EMAIL_NOTIFICATIONS.md](./EMAIL_NOTIFICATIONS.md)** - Email integration for user notifications
4. **[SCHEDULED_EMAIL_AUTOMATION.md](./SCHEDULED_EMAIL_AUTOMATION.md)** - Automated scheduled emails via Task Scheduler + Outlook COM
5. **[DATA_PERSISTENCE.md](./DATA_PERSISTENCE.md)** - How users, sessions, and requests are managed
6. **[WORKFLOW_PATTERNS.md](./WORKFLOW_PATTERNS.md)** - Multi-step approval workflows for web apps
7. **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common issues and solutions

---

## 🚀 Quick Overview

### The Use Case
The Job Code Teaming Dashboard demonstrates a real-world application that:
- ✅ Requires user login with role-based access (Admin/User)
- ✅ Hosts a local web server accessible via browser
- ✅ Manages user sessions and permissions
- ✅ Implements multi-step workflows (Registration → Approval → Request → Export)
- ✅ Could integrate email notifications for approvals/rejections

### Key Components
```
Dashboard (Frontend)
    ↓
Python FastAPI Server (Backend)
    ↓
JSON Files (Users, Sessions, Requests)
    ↓
Data Sources (Excel, CSV)
```

---

## 💡 When to Use These Learnings

| Need | Reference |
|------|-----------|
| Create a dashboard that requires login | [USER_AUTHENTICATION.md](./USER_AUTHENTICATION.md) |
| Host a local web app on your computer | [LOCAL_HOSTING_SETUP.md](./LOCAL_HOSTING_SETUP.md) |
| Share access via VPN/network | [LOCAL_HOSTING_SETUP.md](./LOCAL_HOSTING_SETUP.md) |
| Send emails when events happen | [EMAIL_NOTIFICATIONS.md](./EMAIL_NOTIFICATIONS.md) |
| Build a multi-role approval system | [WORKFLOW_PATTERNS.md](./WORKFLOW_PATTERNS.md) |
| Manage user accounts & sessions | [DATA_PERSISTENCE.md](./DATA_PERSISTENCE.md) |
| Fix server/login issues | [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) |

---

## 🔗 Source Project

**Original Implementation:** `C:\Users\krush\Documents\VSCode\Store Support\Projects\JobCodes-teaming\Teaming\dashboard`

Key files:
- `backend/main.py` - FastAPI server with auth logic
- `frontend/JobCodeTeamingDashboard.html` - Web interface
- `start.ps1` / `start_server.bat` - Startup scripts
- `data/` - User accounts, sessions, requests

---

## 📚 Related Resources

See also in Spark-Playground/General Setup:
- **[Local Hosting/](../Local%20Hosting/)** - Additional hosting methods and network sharing
- **[AI_Policy/](../AI_Policy/)** - Security and compliance considerations

---

## ⚠️ Important Notes

1. **Default Credentials**: Dashboard uses `admin`/`admin123` by default - **change immediately in production**
2. **Local-Only by Default**: Server runs on localhost - see [LOCAL_HOSTING_SETUP.md](./LOCAL_HOSTING_SETUP.md) for network access
3. **Data Files**: JSON files in `data/` folder store everything - back these up!
4. **Python Requirements**: FastAPI, Uvicorn, Pandas, Openpyxl required
5. **Email Not Yet Implemented**: Learnings document the pattern; actual email integration needs SMTP configuration

---

## 🎯 Next Steps

1. Read [LOCAL_HOSTING_SETUP.md](./LOCAL_HOSTING_SETUP.md) to understand server architecture
2. Study [USER_AUTHENTICATION.md](./USER_AUTHENTICATION.md) for login implementation
3. Review [WORKFLOW_PATTERNS.md](./WORKFLOW_PATTERNS.md) if building approval systems
4. Refer to [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) if you encounter issues
