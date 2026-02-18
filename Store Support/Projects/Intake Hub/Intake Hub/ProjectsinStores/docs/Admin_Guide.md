# Projects in Stores Dashboard - Admin Guide

## Overview

This guide explains how to manage the Feedback & Fix Approval system for the Projects in Stores Dashboard. When users submit feedback about issues they encounter, an AI-powered system analyzes the problem, investigates the codebase, and proposes specific fixes. Administrators review and approve these fixes before they're implemented.

---

## Getting Started

### Accessing the Admin Dashboard

1. **URL**: Navigate to `http://localhost:8001/admin` (or your server's hostname)
2. **Login Credentials**:
   - Username: `kendall.rush` | Password: `admin2026`
   - Username: `admin` | Password: `copilot123`

### Dashboard Layout

Once logged in, you'll see:
- **Header**: "🔧 Projects in Stores - Admin Dashboard" with logout button
- **Pending Fixes Section**: Cards for each fix awaiting review
- **Action History Section**: Log of all approved/denied fixes

---

## Understanding Fix Cards

Each pending fix displays:

### Header Information
- **Fix ID**: Unique identifier (e.g., `FIX-001`)
- **Fix Type Badge**: 
  - **🚀 AUTO-FIX READY** (green) - System has generated specific code changes that will be applied automatically when approved
  - **🛠️ MANUAL IMPLEMENTATION** (yellow) - Analysis provided but requires manual code changes
- **Category**: Type of issue (e.g., "filter_issue", "display_bug")
- **Priority**: HIGH, MEDIUM, or LOW
- **⚠️ NEEDS AI REVIEW Badge**: Appears when AI flags complex issues requiring careful review

### Details
| Field | Description |
|-------|-------------|
| **Description** | Summary of the reported issue |
| **Root Cause** | AI's analysis of what caused the problem |
| **Proposed Fix** | The specific code change to resolve the issue |
| **Investigation Notes** | Step-by-step analysis the AI performed |
| **Files Analyzed** | List of code files the AI examined |
| **File to Modify** | The specific file that will be changed |

### Code Changes
- **Current Code**: The existing code that will be replaced (shown in red/highlighted)
- **New Code**: The proposed replacement code (shown in green/highlighted)

---

## Taking Action on Fixes

### Understanding Fix Types

#### 🚀 AUTO-FIX READY
These fixes have specific code changes ready to apply:
- You'll see the exact **old code** that will be removed
- You'll see the exact **new code** that will replace it
- When approved, the change is **automatically applied** to the codebase
- The server may need a restart for backend changes to take effect

#### 🛠️ MANUAL IMPLEMENTATION  
These fixes require human intervention:
- The AI provides **root cause analysis** and **suggested resolution**
- No automatic code changes will be made when approved
- Approving acknowledges the issue and moves it to history
- You'll need to implement the fix manually or ask the development team

---

### ✅ Approve & Auto-Implement (for AUTO-FIX)
Click when:
- The analysis correctly identifies the root cause
- The proposed code change is appropriate
- You've verified the fix makes sense technically

**What happens**: The code change is automatically applied to the specified file.

### ✅ Acknowledge Issue (for MANUAL)
Click when:
- The analysis is helpful and accurate
- You want to track that this issue was reviewed
- You'll implement the fix manually or forward to development

**What happens**: The fix is marked as acknowledged and moved to history. No code changes are made.

### ❌ Deny
Click **Deny** when:
- The analysis is incorrect
- The proposed fix wouldn't solve the problem
- The change could cause other issues

**What happens**: The fix is marked as denied and moved to history. No code changes are made.

### ⏸️ Hold
Click **Hold** when:
- You need more time to review
- You want to consult with someone else
- The fix requires additional investigation

**What happens**: The fix remains in the pending queue with "On Hold" status.

---

## Auto-Fix Patterns

The AI system automatically generates code fixes for these common issues:

| Issue Pattern | What Triggers It | Auto-Fix Generated |
|---------------|------------------|-------------------|
| **Filter State Conflict** | "showed 0 results" + filter/division mentions | Clears search box when dropdown filters applied |
| **Source Filter Issue** | "Realty/Operations showed 0 results" | Adds source_filter handling to frontend |
| **Owner Search** | "owned by X" + "not found" | Adds owner search capability to AI agent |
| **Duplicate Content** | "repeated", "duplicate", "same thing" | Adds deduplication logic |
| **Performance/Slow** | "slow", "loading", "freeze" | Adds loading indicator |

Issues that don't match these patterns will be flagged as **🛠️ MANUAL IMPLEMENTATION**.

---

## Fix Categories

| Category | Description | Common Causes |
|----------|-------------|---------------|
| `filter_issue` | Problems with search/filter functionality | Conflicting filters, incorrect query logic |
| `display_bug` | UI rendering issues | CSS problems, JavaScript errors |
| `data_issue` | Incorrect data shown | Database query errors, mapping issues |
| `performance` | Slow loading or response times | Inefficient queries, missing indexes |
| `feature_request` | New functionality requests | User suggestions for improvements |

---

## Priority Levels

| Priority | Response Time | Description |
|----------|--------------|-------------|
| **HIGH** | Same day | Critical issues affecting core functionality |
| **MEDIUM** | 1-2 days | Notable issues but workarounds exist |
| **LOW** | 1 week | Minor issues or enhancements |

---

## Workflow Summary

```
┌─────────────────┐
│  User Reports   │
│    Feedback     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Analyzes   │
│  & Investigates │
│   Codebase      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────────┐ ┌───────────┐
│🚀AUTO-FIX │ │🛠️ MANUAL  │
│  READY    │ │   IMPL    │
└─────┬─────┘ └─────┬─────┘
      │             │
      ▼             ▼
┌─────────────────────────┐
│   Admin Reviews in      │
│   Dashboard             │
│   - Root Cause          │
│   - Code Diff (if auto) │
│   - Resolution          │
└────────────┬────────────┘
             │
        ┌────┴────┐
        │         │
        ▼         ▼
   ┌───────┐ ┌───────┐
   │Approve│ │ Deny  │
   └───┬───┘ └───┬───┘
       │         │
       ▼         ▼
┌───────────┐ ┌───────┐
│ AUTO: Code│ │Logged │
│ Applied   │ │Only   │
│           │ │       │
│ MANUAL:   │ │       │
│ Tracked   │ │       │
└───────────┘ └───────┘
```

---

## Best Practices

### Before Approving
1. **Read the Investigation Notes** - Understand how the AI reached its conclusion
2. **Review both code blocks** - Ensure the change is appropriate
3. **Check for side effects** - Consider if the change might affect other features
4. **Verify the file path** - Confirm the correct file is being modified

### When to Flag for Further Review
- Changes to core functionality (database queries, authentication)
- Large code changes (more than 10-15 lines)
- Changes involving multiple files
- Fixes marked with "⚠️ NEEDS REVIEW"

### After Approving
- Test the affected feature in the main dashboard
- Monitor for any new feedback related to the same area
- Document any follow-up issues

---

## Troubleshooting

### "Fix application failed"
- The code may have changed since the analysis
- Contact the development team to manually apply

### "File not found"
- The target file may have been moved or renamed
- Deny the fix and request a new analysis

### Dashboard not loading
- Verify the backend server is running (`http://localhost:8001/api/health`)
- Check that you're using the correct URL

---

## Contact & Escalation

| Issue Type | Contact |
|------------|---------|
| Technical Questions | Development Team |
| Access Issues | System Administrator |
| Urgent Production Issues | On-call Support |

**Email for Feedback Analysis**: ATCteamsupport@walmart.com

---

## Quick Reference Card

```
┌────────────────────────────────────────┐
│         ADMIN QUICK REFERENCE          │
├────────────────────────────────────────┤
│ Dashboard URL: localhost:8001/admin    │
│                                        │
│ Fix Types:                             │
│   🚀 AUTO-FIX - Code applies on approve│
│   🛠️ MANUAL   - Requires human impl    │
│                                        │
│ Actions:                               │
│   ✅ Approve - Apply/Acknowledge fix   │
│   ❌ Deny    - Reject, no changes      │
│   ⏸️ Hold    - Keep for later review   │
│                                        │
│ Review Checklist:                      │
│   □ Check fix type (AUTO vs MANUAL)    │
│   □ Read investigation notes           │
│   □ Compare old vs new code (if AUTO)  │
│   □ Check file path is correct         │
│   □ Consider side effects              │
│   □ Look for NEEDS AI REVIEW badge     │
└────────────────────────────────────────┘
```

---

*Last Updated: January 21, 2026*
