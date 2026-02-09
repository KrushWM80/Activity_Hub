# Notification System Enhancement: Base Notifications & User Preferences
**Date:** January 14, 2026  
**Context:** Addendum to ARCHITECTURE-IMPACT-ANALYSIS.md  
**Focus:** Base Notifications, User Preferences, Multi-Channel Messaging

---

## 1. BASE NOTIFICATIONS (System Standard)

### Concept
Base Notifications are **pre-configured, standardized notification templates** that every user should receive by default because they're operationally critical. These are NOT optional—they represent mandatory communications for workflow continuity.

Unlike custom rules (which admins create), Base Notifications are:
- ✓ Built into the system
- ✓ Required for all users
- ✓ System-managed (not admin-created)
- ✓ Tied to core business processes
- ✓ Cannot be disabled (only delivery channel can change)

### Base Notification Categories

```
1. PROJECT LIFECYCLE NOTIFICATIONS
   ├─ Project Created (you're assigned)
   ├─ Project Status Changed (impacts your stores/team)
   ├─ Project Delayed/At Risk (you're owner/stakeholder)
   ├─ Project Completed
   └─ Project Cancelled

2. TASK & WORK ASSIGNMENT NOTIFICATIONS
   ├─ New Task Assigned to You
   ├─ Task Due Soon (24 hours before)
   ├─ Task Overdue (past due date)
   ├─ Task Reassigned to You
   └─ Task Completed by Team

3. URGENT/ESCALATION NOTIFICATIONS
   ├─ Project Critical Issue Detected
   ├─ Project SLA Violation
   ├─ High Priority Update from Manager
   └─ Escalation from Direct Report

4. COMPLIANCE & AUDIT NOTIFICATIONS
   ├─ Audit Started (you're in scope)
   ├─ Compliance Review Required
   ├─ Data Access Requested (HR audit)
   └─ Role Change Detected (SOX notification)

5. ORGANIZATIONAL CHANGE NOTIFICATIONS
   ├─ Manager Changed
   ├─ Org Unit Restructured
   ├─ New Team Member Added
   └─ Team Member Left

6. SYSTEM & MAINTENANCE NOTIFICATIONS
   ├─ Scheduled Maintenance Alert
   ├─ System Issue Detected
   ├─ Password Expiration (30 days)
   └─ System Update Available
```

### Base Notification Database Schema

```sql
CREATE TABLE base_notifications (
    id SERIAL PRIMARY KEY,
    notification_code VARCHAR(100) UNIQUE NOT NULL,
    -- e.g., "PROJECT_STATUS_CHANGED", "TASK_ASSIGNED"
    
    name VARCHAR(255) NOT NULL,
    -- e.g., "Project Status Changed"
    
    description TEXT,
    -- What triggers this, why user receives it
    
    category VARCHAR(50) NOT NULL,
    -- PROJECT_LIFECYCLE, TASK_WORK, URGENT, COMPLIANCE, ORG_CHANGE, SYSTEM
    
    trigger_event VARCHAR(100) NOT NULL,
    -- Database event/system event that triggers
    
    is_mandatory BOOLEAN DEFAULT TRUE,
    -- Cannot be disabled, only channel changed
    
    default_channels JSON NOT NULL,
    -- ["email", "in_app", "teams"]
    
    priority_level VARCHAR(50),
    -- CRITICAL, HIGH, MEDIUM, LOW
    
    delivery_timing VARCHAR(50),
    -- IMMEDIATE, BATCH_HOURLY, BATCH_DAILY
    
    template_id INT REFERENCES notification_templates(id),
    -- Reference to email/message template
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE base_notification_user_delivery_settings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    base_notification_id INT REFERENCES base_notifications(id),
    
    -- User can only customize DELIVERY, not disable
    enabled_channels JSON DEFAULT '["email", "in_app", "teams"]',
    -- User can choose: which channels to receive on
    
    mute_until TIMESTAMP,
    -- Snooze for 1 hour, 4 hours, 1 day, etc.
    
    delivery_preference VARCHAR(50),
    -- IMMEDIATE, BATCHED_HOURLY, BATCHED_DAILY
    
    customize_time_window_start TIME,
    customize_time_window_end TIME,
    -- "Don't send between 9 PM - 7 AM"
    
    do_not_disturb_enabled BOOLEAN DEFAULT FALSE,
    do_not_disturb_start_time TIME,
    do_not_disturb_end_time TIME,
    
    last_received_at TIMESTAMP,
    times_received_count INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, base_notification_id)
);

CREATE TABLE base_notification_executions (
    id SERIAL PRIMARY KEY,
    base_notification_id INT REFERENCES base_notifications(id),
    trigger_event_id VARCHAR(255),
    -- Which event triggered this
    
    user_id INT REFERENCES users(id),
    -- Who should receive
    
    related_project_id INT REFERENCES projects(id),
    related_task_id INT,
    related_resource_id VARCHAR(255),
    
    scheduled_send_at TIMESTAMP,
    sent_at TIMESTAMP,
    status VARCHAR(50),
    -- PENDING, SENT, FAILED, SNOOZED
    
    channels_sent JSON,
    -- ["email", "teams"] (actually sent via)
    
    delivery_log JSON,
    -- { "email": {...}, "teams": {...} }
    
    user_interaction VARCHAR(50),
    -- CLICKED, ARCHIVED, SNOOZED, IGNORED
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Base Notification Examples

```
EXAMPLE 1: PROJECT_STATUS_CHANGED
═══════════════════════════════════════════

Base Notification Configuration:
{
  "notification_code": "PROJECT_STATUS_CHANGED",
  "name": "Project Status Changed",
  "category": "PROJECT_LIFECYCLE",
  "trigger_event": "project.status_updated",
  "is_mandatory": true,
  "default_channels": ["email", "in_app", "teams"],
  "priority_level": "HIGH",
  "delivery_timing": "IMMEDIATE",
  "template": {
    "subject": "Project Status Update: {{project.name}}",
    "body": "Project {{project.name}} status changed from {{old_status}} to {{new_status}}"
  }
}

User Override (John Doe):
{
  "user_id": 123,
  "enabled_channels": ["in_app", "teams"],  // Removed "email"
  "delivery_preference": "BATCHED_HOURLY",  // Group emails
  "do_not_disturb_enabled": true,
  "do_not_disturb_start": "21:00",
  "do_not_disturb_end": "07:00"
}

Result: John receives notifications via Teams + In-App, batched hourly, never between 9 PM - 7 AM


EXAMPLE 2: TASK_DUE_SOON
═══════════════════════════════════════════

Base Notification Configuration:
{
  "notification_code": "TASK_DUE_SOON",
  "name": "Task Due Within 24 Hours",
  "category": "TASK_WORK",
  "trigger_event": "task.due_within_24h",
  "is_mandatory": true,
  "default_channels": ["in_app", "teams"],
  "priority_level": "MEDIUM",
  "delivery_timing": "IMMEDIATE",
  "template": {
    "subject": "Reminder: Task Due Tomorrow",
    "body": "Your task '{{task.title}}' is due on {{task.due_date}}"
  }
}

User Override (Jane Smith):
{
  "user_id": 456,
  "enabled_channels": ["teams"],  // Only Teams, removed in_app
  "mute_until": "2026-01-15T14:00:00Z"  // Snooze for rest of day
}

Result: Jane receives next task-due notification via Teams only, after snooze expires
```

---

## 2. USER NOTIFICATION PREFERENCES UI

### 2.1 Preference Settings Page Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ NOTIFICATION PREFERENCES                            [Settings ⚙️] │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ Tab Navigation:                                                   │
│ [Base Notifications] [Custom Rules] [Channels] [Do Not Disturb]  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Base Notifications Tab

```
┌──────────────────────────────────────────────────────────────┐
│ BASE NOTIFICATIONS (Required • System-Managed)               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🔴 PROJECT LIFECYCLE (4 notifications)                      │
│ ├─ ☑ Project Created                                        │
│ │  Channels: [☑Email] [☑Teams] [☑In-App]                  │
│ │  Delivery: ⊙ Immediate ○ Batched                         │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ ├─ ☑ Project Status Changed                                │
│ │  Channels: [☑Email] [☑Teams] [☑In-App]                  │
│ │  Delivery: ⊙ Immediate ○ Batched                         │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ ├─ ☑ Project Delayed                                       │
│ │  Channels: [☑Email] [☑Teams] [☑In-App]                  │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ └─ ☑ Project Completed                                     │
│    Channels: [☐Email] [☑Teams] [☑In-App]                  │
│    [Customize ⏱] [Snooze 1h ⏸]                            │
│                                                              │
│ 🟡 TASK & WORK ASSIGNMENT (3 notifications)                │
│ ├─ ☑ New Task Assigned                                     │
│ │  Channels: [☑Email] [☑Teams] [☑In-App]                  │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ ├─ ☑ Task Due Soon (24h)                                   │
│ │  Channels: [☐Email] [☑Teams] [☑In-App]                  │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ └─ ☑ Task Overdue                                          │
│    Channels: [☑Email] [☑Teams] [☑In-App]                  │
│    [Customize ⏱] [Snooze 1h ⏸]                            │
│                                                              │
│ 🔴 URGENT & ESCALATION (2 notifications)                   │
│ ├─ ☑ Critical Issue Detected                               │
│ │  Channels: [☑Email] [☑Teams] [☑In-App]                  │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ └─ ☑ Manager Escalation                                    │
│    Channels: [☑Email] [☑Teams] [☑In-App]                  │
│    [Customize ⏱] [Snooze 1h ⏸]                            │
│                                                              │
│ ⚪ COMPLIANCE & SYSTEM (3 notifications)                    │
│ ├─ ☑ Audit Notification                                    │
│ │  Channels: [☑Email] [☐Teams] [☑In-App]                  │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ ├─ ☑ Role Change Detected (SOX)                            │
│ │  Channels: [☑Email] [☐Teams] [☑In-App]                  │
│ │  [Customize ⏱] [Snooze 1h ⏸]                            │
│ │                                                           │
│ └─ ☑ System Maintenance Alert                              │
│    Channels: [☑Email] [☑Teams] [☑In-App]                  │
│    [Customize ⏱] [Snooze 1h ⏸]                            │
│                                                              │
│ Legend: 🔴 = Critical  🟡 = Important  ⚪ = Informational   │
│                                                              │
│ NOTE: These notifications are required. You cannot           │
│ disable them, but you can change delivery channels           │
│ and timing.                                                  │
│                                                              │
│                                    [Reset to Defaults] [Save]│
└──────────────────────────────────────────────────────────────┘
```

### 2.3 Channels Tab

```
┌──────────────────────────────────────────────────────────────┐
│ NOTIFICATION CHANNELS                                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ PRIMARY CHANNEL (Default for all notifications)             │
│ ┌────────────────────────────────────────┐                 │
│ │ Select your primary channel:           │                 │
│ │ ○ Email (john.doe@walmart.com)        │                 │
│ │ ◉ Microsoft Teams                      │                 │
│ │ ○ Slack (if enabled for your team)    │                 │
│ │ ○ In-App Notification                  │                 │
│ │                                        │                 │
│ │ Teams Details:                         │                 │
│ │ ├─ Account: john.doe@microsoft.com    │                 │
│ │ ├─ Status: Connected ✓                 │                 │
│ │ ├─ DM or Channel: [v] Direct Message   │                 │
│ │ └─ Last notification: 2 min ago        │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ SECONDARY CHANNELS (Choose additional)                      │
│ ┌────────────────────────────────────────┐                 │
│ │ ☑ Email                                 │                 │
│ │ ☑ In-App Notification                   │                 │
│ │ ☐ Slack                                 │                 │
│ │ ☐ SMS (if enabled)                      │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ CHANNEL CONFIGURATION                                       │
│ ┌────────────────────────────────────────┐                 │
│ │ Email:                                  │                 │
│ │ ├─ Address: john.doe@walmart.com       │                 │
│ │ ├─ Batch sending: ○ Immediate          │                 │
│ │ │                 ◉ Every Hour         │                 │
│ │ │                 ○ Daily at 8 AM     │                 │
│ │ └─ [Send Test Email]                   │                 │
│ │                                        │                 │
│ │ Microsoft Teams:                        │                 │
│ │ ├─ Connected: ✓                         │                 │
│ │ ├─ Send to: ◉ Direct Message            │                 │
│ │ │           ○ Channel: #projects       │                 │
│ │ ├─ @Mention me: ☑ On critical only     │                 │
│ │ └─ [Send Test Message]                  │                 │
│ │                                        │                 │
│ │ Slack:                                  │                 │
│ │ ├─ Connected: ✗ (Not connected)         │                 │
│ │ ├─ Status: Available for team          │                 │
│ │ └─ [Connect to Slack]                   │                 │
│ │                                        │                 │
│ │ In-App:                                 │                 │
│ │ ├─ Notification Center: ☑ Enabled      │                 │
│ │ ├─ Sound: ☑ On                         │                 │
│ │ ├─ Desktop notification: ☑ On          │                 │
│ │ └─ Badge count: ☑ Show unread count    │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│                                    [Reset] [Save Changes]    │
└──────────────────────────────────────────────────────────────┘
```

### 2.4 Notification Type & Consistency Tab

```
┌──────────────────────────────────────────────────────────────┐
│ NOTIFICATION TYPE & CONSISTENCY PREFERENCES                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ NOTIFICATION DETAIL LEVEL                                   │
│ ┌────────────────────────────────────────┐                 │
│ │ How detailed should notification be?   │                 │
│ │                                        │                 │
│ │ ○ Summary Only                         │                 │
│ │   "Task assigned to you"               │                 │
│ │                                        │                 │
│ │ ◉ Summary + Key Details                │                 │
│ │   "Task assigned: Review Q1 Budget"    │                 │
│ │   "Due: Jan 20, Priority: High"       │                 │
│ │                                        │                 │
│ │ ○ Full Details                         │                 │
│ │   Includes description, attachments    │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ MENTION PREFERENCES                                         │
│ ┌────────────────────────────────────────┐                 │
│ │ When should notifications mention me?  │                 │
│ │                                        │                 │
│ │ ☐ Always @mention                      │                 │
│ │ ◉ Critical only @mention               │                 │
│ │   (urgent/escalation notifications)    │                 │
│ │ ☐ Never @mention                       │                 │
│ │                                        │                 │
│ │ Mention Format: [v] @john.doe          │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ FREQUENCY CONTROL (Avoid Notification Fatigue)             │
│ ┌────────────────────────────────────────┐                 │
│ │ Maximum notifications per day:         │                 │
│ │ ○ No limit                              │                 │
│ │ ◉ Intelligent batching                 │                 │
│ │   (Related notifications grouped)      │                 │
│ │ ○ Limit to [___] per day               │                 │
│ │ ○ Digest mode (1 summary per day)      │                 │
│ │                                        │                 │
│ │ How to handle exceeding limit:         │                 │
│ │ ⊙ Queue for next batch period          │                 │
│ │ ○ Show in inbox only (no alert)        │                 │
│ │ ○ Low priority = skip, medium+ = queue │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ GROUPING PREFERENCES                                        │
│ ┌────────────────────────────────────────┐                 │
│ │ How should related notifications       │                 │
│ │ be combined?                           │                 │
│ │                                        │                 │
│ │ ☑ Group by Project                     │                 │
│ │ ☑ Group by Priority                    │                 │
│ │ ☑ Group by Sender/Owner                │                 │
│ │ ☑ Group by Date                        │                 │
│ │                                        │                 │
│ │ Example (with grouping enabled):       │                 │
│ │ "Project Q1 Initiative (5 updates):    │                 │
│ │ ├─ Status changed to POC              │                 │
│ │ ├─ 3 new tasks assigned                │                 │
│ │ └─ Budget approved"                    │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│                                    [Reset] [Save Changes]    │
└──────────────────────────────────────────────────────────────┘
```

### 2.5 Do Not Disturb Tab

```
┌──────────────────────────────────────────────────────────────┐
│ DO NOT DISTURB & QUIET HOURS                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ DO NOT DISTURB SCHEDULE                                     │
│ ┌────────────────────────────────────────┐                 │
│ │ Enable Do Not Disturb:                 │                 │
│ │ ☑ Use schedule below                   │                 │
│ │                                        │                 │
│ │ Daily Schedule:                        │                 │
│ │ ├─ Start: 21:00 (9 PM)                 │                 │
│ │ ├─ End:   07:00 (7 AM)                 │                 │
│ │ └─ Timezone: America/Chicago           │                 │
│ │                                        │                 │
│ │ Which days apply?                      │                 │
│ │ ☑ Mon ☑ Tue ☑ Wed ☑ Thu               │                 │
│ │ ☑ Fri ☐ Sat ☐ Sun                     │                 │
│ │                                        │                 │
│ │ During Do Not Disturb:                 │                 │
│ │ ⊙ Deliver, but mute sound/badges      │                 │
│ │ ○ Queue until Do Not Disturb ends     │                 │
│ │ ○ Only CRITICAL can break through      │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ QUICK QUIET HOURS (Temporary)                              │
│ ┌────────────────────────────────────────┐                 │
│ │ Quick Snooze Buttons:                  │                 │
│ │ [Mute 1 hour] [Mute 4 hours]          │                 │
│ │ [Mute until 5 PM] [Mute until 9 AM]   │                 │
│ │ [Mute until tomorrow]                  │                 │
│ │                                        │                 │
│ │ Currently Active:                      │                 │
│ │ "Snoozed until 5:00 PM today"          │                 │
│ │ [Cancel Snooze]                        │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ PRIORITY BREAKTHROUGH                                       │
│ ┌────────────────────────────────────────┐                 │
│ │ Critical notifications during quiet    │                 │
│ │ hours can still alert if:              │                 │
│ │                                        │                 │
│ │ ☑ Escalation from my manager           │                 │
│ │ ☑ CRITICAL priority project issue      │                 │
│ │ ☑ Direct @mention in Teams/Slack       │                 │
│ │ ☑ More than 3 similar in 1 hour        │                 │
│ │ ☐ Any notification                     │                 │
│ │                                        │                 │
│ │ When breakthrough happens:             │                 │
│ │ ⊙ Sound only, no badge count          │                 │
│ │ ○ Full alert                           │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│ MEETING DETECTION (Calendar-Aware)                         │
│ ┌────────────────────────────────────────┐                 │
│ │ ☑ Detect meetings on calendar          │                 │
│ │   Reduce notifications during:         │                 │
│ │   ○ All meetings                        │                 │
│ │   ◉ Only 1:1 or large meetings        │                 │
│ │                                        │                 │
│ │ Integration: [Connect Outlook]         │                 │
│ │                                        │                 │
│ └────────────────────────────────────────┘                 │
│                                                              │
│                                    [Reset] [Save Changes]    │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. MULTI-CHANNEL MESSAGING ARCHITECTURE

### 3.1 Supported Channels Overview

```
CHANNEL CAPABILITIES MATRIX
═══════════════════════════════════════════════════════════

                  Email    Teams    Slack    In-App   SMS
────────────────────────────────────────────────────────
Immediate Delivery  ✓✓      ✓✓✓     ✓✓      ✓✓✓     ✓
Batching           ✓✓✓     ✓       ✓       ✓       ✗
Rich Formatting    ✓✓      ✓✓✓     ✓✓      ✓✓✓     ✗
Attachments        ✓✓✓     ✓       ✓       ✓✓      ✗
Interactive        ✗       ✓✓✓     ✓✓      ✓✓✓     ✗
Buttons/Actions    ✗       ✓✓✓     ✓✓      ✓✓✓     ✗
Threading/Replies  ✗       ✓✓✓     ✓✓✓     ✓       ✗
Mentions           ✗       ✓✓✓     ✓✓✓     ✗       ✗
Read Receipts      ✗       ✓       ✗       ✓       ✗
Encryption         ✓✓      ✓✓✓     ✓✓      ✓✓      ✓✓✓
────────────────────────────────────────────────────────

Legend: ✓✓✓ = Excellent  ✓✓ = Good  ✓ = Basic  ✗ = Not Available

RECOMMENDED USE CASES:
- Email: Formal records, compliance, detailed info, batching
- Teams: Primary workplace communication, interactive actions
- Slack: Team coordination, informal notifications
- In-App: Quick alerts, critical/urgent, actions
- SMS: Ultra-critical, mobile, off-hours escalation
```

### 3.2 Multi-Channel Delivery Pipeline

```
NOTIFICATION SENDING FLOW
═════════════════════════════════════════════════════════════

Notification Triggered
        │
        ↓
┌───────────────────────────────────┐
│ Determine Recipient Preferences   │
├───────────────────────────────────┤
│ • Primary channel?                │
│ • Secondary channels?             │
│ • Batching preference?            │
│ • Do Not Disturb active?          │
│ • Snoozed notifications?          │
└───────────────────────────────────┘
        │
        ↓
┌───────────────────────────────────────────────┐
│ Check Channel-Specific Rules                  │
├───────────────────────────────────────────────┤
│ IF Primary = Teams:                           │
│   ├─ DM or Channel notification?              │
│   ├─ @Mention?                                │
│   └─ Rich cards vs plain message?             │
│                                               │
│ IF Primary = Email:                           │
│   ├─ Immediate or batched?                    │
│   ├─ HTML or plain text?                      │
│   └─ Include attachments?                     │
│                                               │
│ IF Secondary channels queued:                 │
│   ├─ Fallback order?                          │
│   └─ Timing (same time, staggered)?           │
└───────────────────────────────────────────────┘
        │
        ↓
┌───────────────────────────────────────────────┐
│ Apply Delivery Rules                          │
├───────────────────────────────────────────────┤
│ IF Do Not Disturb Active:                     │
│   ├─ IF CRITICAL priority → deliver anyway   │
│   └─ IF normal → queue for after DND ends    │
│                                               │
│ IF Snoozed:                                   │
│   └─ Queue until snooze expires               │
│                                               │
│ IF Batching enabled:                          │
│   └─ Add to batch queue (1hr, daily, etc.)    │
│                                               │
│ Otherwise:                                    │
│   └─ Send immediately                         │
└───────────────────────────────────────────────┘
        │
        ├─────────────┬──────────────┬──────────┬───────┐
        ↓             ↓              ↓          ↓       ↓
       EMAIL        TEAMS          SLACK     IN-APP   SMS
        │             │              │          │       │
        ↓             ↓              ↓          ↓       ↓


CHANNEL HANDLERS:
═══════════════════════════════════════════════════════════

EMAIL HANDLER:
├─ Load template
├─ Render with data
├─ Apply styling/branding
├─ Add unsubscribe link
├─ Sign with DKIM
└─ Send via SES/SendGrid
   └─ Log delivery status

TEAMS HANDLER:
├─ Determine: DM vs Channel
├─ Build adaptive card (rich format)
├─ Add action buttons (View, Reply, Archive)
├─ Handle @mentions based on preference
├─ Send via Teams Bot API
└─ Log delivery + read receipt tracking

SLACK HANDLER:
├─ Determine: DM vs Channel
├─ Format Slack message blocks
├─ Add interactive elements (buttons)
├─ Handle thread replies
├─ Send via Slack Webhook/API
└─ Log delivery status

IN-APP HANDLER:
├─ Create notification object
├─ Store in user's notification center
├─ Send WebSocket to browser/app
├─ Show toast/banner
└─ Track: viewed, clicked, archived

SMS HANDLER:
├─ Shorten message (160 char limit)
├─ Add short URL
├─ Send via Twilio/AWS SNS
└─ Log delivery + read status
```

### 3.3 Channel Configuration Schema

```sql
CREATE TABLE notification_channels (
    id SERIAL PRIMARY KEY,
    
    channel_name VARCHAR(50) UNIQUE NOT NULL,
    -- 'email', 'teams', 'slack', 'in_app', 'sms'
    
    display_name VARCHAR(100),
    -- 'Microsoft Teams', 'Email', etc.
    
    is_enabled BOOLEAN DEFAULT TRUE,
    -- Can admins disable a channel globally?
    
    is_default BOOLEAN DEFAULT FALSE,
    -- Default channel for new users
    
    capabilities JSON,
    -- {"batch": true, "rich_format": true, "mentions": false}
    
    delivery_timeout_seconds INT,
    -- Max time to attempt delivery
    
    retry_strategy JSON,
    -- {"max_attempts": 3, "backoff_exponential": true}
    
    rate_limit_per_hour INT,
    -- Prevent spam
    
    cost_per_message DECIMAL,
    -- For budget tracking (if applicable)
    
    priority_ranking INT,
    -- Fallback order (1 = highest priority fallback)
    
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE user_channel_connections (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    channel_id INT REFERENCES notification_channels(id),
    
    external_account_id VARCHAR(500),
    -- user@email.com, slack_user_id, teams_id, etc.
    
    external_account_name VARCHAR(500),
    -- Display name on the external platform
    
    connection_status VARCHAR(50),
    -- 'connected', 'pending_auth', 'disconnected', 'error'
    
    last_verified_at TIMESTAMP,
    -- When we last tested the connection
    
    auth_token VARCHAR(500) ENCRYPTED,
    -- OAuth token or API key (encrypted at rest)
    
    metadata JSON,
    -- Platform-specific settings
    -- Teams: {"dm_enabled": true, "channel": "#projects"}
    -- Slack: {"workspace_id": "...", "dm_enabled": true}
    -- Email: {"smtp_verified": true, "bounce_count": 0}
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, channel_id)
);


CREATE TABLE notification_delivery_logs (
    id SERIAL PRIMARY KEY,
    notification_execution_id INT REFERENCES notification_executions(id),
    channel_id INT REFERENCES notification_channels(id),
    user_id INT REFERENCES users(id),
    
    destination VARCHAR(500),
    -- Recipient email, Teams ID, Slack ID, etc.
    
    message_body TEXT,
    -- What was actually sent
    
    status VARCHAR(50),
    -- 'sent', 'delivered', 'failed', 'bounced', 'read'
    
    attempt_number INT,
    error_message TEXT,
    
    external_message_id VARCHAR(500),
    -- Message ID from Teams, Slack, email provider
    
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    
    delivery_time_ms INT,
    -- How long delivery took
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 4. TEAMS & SLACK CHANNEL INFRASTRUCTURE

### 4.1 Platform Workspace Setup

The Activity Hub system itself needs Slack and Teams channels for operational coordination.

```
MICROSOFT TEAMS SETUP
═══════════════════════════════════════════════════════════

Workspace: Walmart Activity Hub

Team Structure:
├─ #general
│  └─ System announcements, platform updates
│
├─ #notifications
│  └─ Where Activity Hub sends critical alerts
│     (monitored by ops team)
│
├─ #projects-feed
│  └─ Real-time project updates stream
│
├─ #escalations
│  └─ High-priority escalations requiring immediate action
│
├─ #integrations
│  └─ Sync status, data connector logs, platform bridge alerts
│
├─ #admin
│  └─ Private channel for admins only
│     (notification rule changes, user access changes)
│
├─ #support
│  └─ User support, incident triage
│
├─ #compliance-audit
│  └─ Audit logs, SOX notifications, compliance events
│
└─ #dev-staging
   └─ Development/test environment notifications


SLACK WORKSPACE SETUP
═══════════════════════════════════════════════════════════

Workspace: walmart-activity-hub

Channel Structure:
├─ #general
│  └─ Company-wide announcements
│
├─ #activity-hub-notifications
│  └─ Critical platform alerts
│
├─ #projects
│  └─ Project updates and discussions
│
├─ #ops-team
│  └─ Operations team private channel
│
├─ #integration-status
│  └─ Data sync status, API health
│
├─ #alerts
│  └─ Automated alerts from monitoring
│
└─ #support
   └─ Support team channel
```

### 4.2 Bot Integration Architecture

```
TEAMS BOT
═════════════════════════════════════════════════════════════

Activity Hub Teams Bot
├─ Function: Send notifications, interactive messages
├─ Authentication: Microsoft Azure App Registration
├─ Endpoints:
│  ├─ POST /teams/send-notification/{user_id}
│  ├─ POST /teams/send-channel-message/{channel_id}
│  ├─ POST /teams/button-action (webhook for button clicks)
│  └─ POST /teams/mention-user
│
└─ Capabilities:
   ├─ Send rich Adaptive Cards
   ├─ Handle button clicks → Activity Hub actions
   ├─ @Mention users
   ├─ Create threaded replies
   └─ Update/delete messages


SLACK BOT
═════════════════════════════════════════════════════════════

Activity Hub Slack App
├─ Function: Send notifications, slash commands
├─ Authentication: OAuth 2.0
├─ Endpoints:
│  ├─ POST /slack/send-notification/{user_id}
│  ├─ POST /slack/send-channel-message/{channel_id}
│  ├─ POST /slack/events (webhook for interactions)
│  ├─ POST /slack/slash-commands (handle /activityhub)
│  └─ POST /slack/button-action
│
└─ Capabilities:
   ├─ Send formatted messages
   ├─ Handle button/dropdown interactions
   ├─ @Mention users
   ├─ Create threaded conversations
   ├─ Slash commands: /activityhub status, /activityhub help
   └─ App Home with quick links
```

### 4.3 Interactive Message Examples

```
TEAMS NOTIFICATION (Rich Adaptive Card)
═════════════════════════════════════════════════════════════

┌───────────────────────────────────────────────────┐
│                                                   │
│ 📋 Project Status Changed                        │
│                                                   │
│ Q1 Store Initiative Pilot → POC Phase            │
│                                                   │
│ Owner: John Doe                                  │
│ Status: POC (Proof of Concept)                   │
│ Stores Affected: 45 Northeast Region             │
│ Timeline: Jan 14 - Feb 28, 2026                  │
│ Priority: HIGH                                   │
│                                                   │
│ Description:                                     │
│ Project has entered POC phase. Teams have been  │
│ notified to set up Communication Activity in    │
│ AMP for store visits.                           │
│                                                   │
│ [View Project] [View Tasks] [More Details]      │
│                                                   │
│ 👤 John Doe  •  🕐 5 minutes ago  •  ⋮ (menu)   │
│                                                   │
└───────────────────────────────────────────────────┘


SLACK NOTIFICATION (Message Blocks)
═════════════════════════════════════════════════════════════

┌───────────────────────────────────────────────────┐
│                                                   │
│ 📋 Project Update                                │
│                                                   │
│ *Q1 Store Initiative: Status → POC*             │
│                                                   │
│ Owner: John Doe                                  │
│ Stores Affected: 45 (Northeast)                  │
│ Timeline: Jan 14 - Feb 28                        │
│                                                   │
│ [View Project]  [View Tasks]  [Acknowledge]      │
│                                                   │
│ :clock1: 5 min ago in #projects-feed             │
│                                                   │
└───────────────────────────────────────────────────┘


IN-APP NOTIFICATION (Toast)
═════════════════════════════════════════════════════════════

┌─────────────────────────────────────┐
│ 📋 Project Status Changed            │
│ Q1 Store Initiative → POC            │
│                                     │
│ [View] [Dismiss] [Snooze]          │
│                                     │
│ 5 min ago                    [×]    │
└─────────────────────────────────────┘
```

---

## 5. DATABASE ADDITIONS FOR MULTI-CHANNEL SUPPORT

### Additions to Core Schema

```sql
-- Extend notification_rules table
ALTER TABLE notification_rules ADD COLUMN (
    multi_channel_strategy VARCHAR(50),
    -- 'primary_only', 'primary_and_secondary', 'all_channels'
    
    channel_priority JSON,
    -- Ordered list: ["teams", "email", "in_app"]
    
    channel_specific_config JSON
    -- Per-channel customizations
);

-- Extend notification_executions table
ALTER TABLE notification_executions ADD COLUMN (
    channels_attempted JSON,
    -- Which channels we tried to send to
    
    channels_succeeded JSON,
    -- Which channels actually delivered
    
    fallback_used BOOLEAN,
    -- Did we fall back to secondary channel?
);

-- New table: Channel-specific templates
CREATE TABLE notification_templates_by_channel (
    id SERIAL PRIMARY KEY,
    template_id INT REFERENCES notification_templates(id),
    channel_id INT REFERENCES notification_channels(id),
    
    template_content TEXT,
    -- Channel-optimized content
    -- Email: full HTML
    -- Teams: JSON Adaptive Card
    -- Slack: JSON message blocks
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(template_id, channel_id)
);
```

---

## 6. IMPLEMENTATION PRIORITY

### Phase 1: Channels (Week 1-2)
```
✓ Multi-channel delivery pipeline
✓ Email, Teams, In-App, SMS handlers
✓ User channel connection management
✓ Delivery logging
```

### Phase 2: Base Notifications (Week 2-3)
```
✓ Base notification templates
✓ User delivery preferences per base notification
✓ Mandatory notification system
✓ UI for notification preferences (partial)
```

### Phase 3: User Preferences UI (Week 3-5)
```
✓ Base Notifications tab
✓ Channels tab with configuration
✓ Do Not Disturb scheduling
✓ Notification type preferences
✓ Consistency controls
✓ Snooze functionality
```

### Phase 4: Team/Slack Infrastructure (Week 5-6)
```
✓ Teams Bot setup + API integration
✓ Slack Bot setup + API integration
✓ Channel creation and management
✓ Interactive message formatting
```

### Phase 5: Integration (Week 6+)
```
✓ Connect notification engine to channels
✓ Connect preferences to delivery pipeline
✓ Connect base notifications to UI
✓ Testing + hardening
```

---

## 7. CRITICAL DECISIONS NEEDED

Before implementation, confirm:

1. **Primary vs. Secondary Channels**
   - Should Teams be mandatory primary? (recommended: YES)
   - Email as fallback? (recommended: YES)
   - Can users opt for Slack instead? (depends on team policy)

2. **Base Notifications List**
   - Confirm the 6 categories + examples provided are appropriate
   - Any others to add?
   - Any that should NOT be mandatory?

3. **User Preference Defaults**
   - New user gets all channels by default?
   - Or just primary + in-app?
   - Do Not Disturb defaults?

4. **Team/Slack Channels**
   - Which channels does ops team need?
   - Who has access to #admin channel?
   - Should #compliance-audit be read-only?

5. **Escalation Strategy**
   - If Teams fails → email?
   - If all fail → SMS?
   - Retry logic + timing?

6. **Rich Formatting**
   - Always use Adaptive Cards (Teams) or sometimes plain text?
   - Buttons on notifications? (View, Acknowledge, Reply?)
   - Interactive elements on all channels or just Teams/Slack?

---

**This document supplements the main ARCHITECTURE-IMPACT-ANALYSIS.md. Use both when designing the notification system.**

