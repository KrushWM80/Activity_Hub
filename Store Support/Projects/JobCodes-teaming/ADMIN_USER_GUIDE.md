# Job Codes Admin Panel - User Guide

**Last Updated**: April 29, 2026  
**Feature**: Manage consolidated job code requests with status updates and comments

---

## 📋 Quick Start

### Access the Admin Panel
1. Navigate to: **http://localhost:8080/Aligned**
2. Click **Admin** in the left navigation menu
3. Select **Job Code Requests** tab in the Administration panel

### What You'll See
A table with all pending, in-review, and approved job code requests:

| Column | What It Shows |
|--------|---------------|
| **Job Codes** | All job codes in the request (e.g., "1-0-040407, 1-0-040413, 1-0-40225, ...") |
| **Description** | The reason/details for the request (truncated to 50 characters) |
| **Status** | Current status with color: 🟡 Pending • 🔵 In Review • 🟢 Approved • 🔴 Rejected |
| **Requested By** | Name of the person who submitted the request |
| **Date** | When the request was submitted |
| **Actions** | "View" button to open the detail modal |

---

## 🔍 Viewing Request Details

### Open a Request
Click the **"View"** button on any row to open the detail modal.

### In the Detail Modal
You'll see:
- **Request Type**: Whether this is an update to existing codes or new codes
- **Requested By**: Full name of the requester
- **Date**: Submission date and time
- **Reason**: Full description of what they're requesting
- **Job Codes**: All codes displayed as blue badges (e.g., `1-0-040407`)

---

## ✏️ Editing & Managing Requests

### Changing Status

1. In the detail modal, find the **"Status"** dropdown
2. Select from:
   - **Pending** - Initial state
   - **In Review** - Being reviewed by team
   - **Approved** - Ready to implement
   - **Rejected** - Not approved
3. Click **"Save Changes"** button
4. You'll see a success notification: "Request status updated"
5. The admin table will refresh with the new status

### Adding Comments

1. Scroll to the **"Add Comment"** section
2. Type your comment in the text area (e.g., "Approved for implementation - verified all codes are valid")
3. Click **"Add Comment"** button
4. You'll see a success notification: "Comment added"
5. Your comment immediately appears in the **"Comments"** section below with:
   - Your name
   - The exact timestamp
   - Your comment text

### Viewing Comments & History

The modal displays:
- **Comments**: All comments added by admins with timestamps
- **Change History**: Every status change recorded with:
  - What changed (e.g., "status: pending → approved")
  - When it changed (timestamp)

---

## 📊 Common Workflows

### Workflow 1: Quick Approval
```
1. View request
2. Change status to "Approved"
3. Click "Save Changes"
4. Done! Status updates in table
```

### Workflow 2: Needs Review
```
1. View request
2. Add comment: "Needs clarification on job code 1-0-040225"
3. Leave status as "Pending" or change to "In Review"
4. Click "Save Changes"
5. Requester sees comment in their notification
```

### Workflow 3: Reject with Reason
```
1. View request
2. Add comment: "Cannot approve - job code 1-0-40225 doesn't exist in master list"
3. Change status to "Rejected"
4. Click "Save Changes"
5. Requester is notified of rejection and reason
```

---

## 💡 Tips & Best Practices

### ✅ DO
- ✅ Add comments explaining why you're changing status
- ✅ Use "In Review" status while investigating
- ✅ Reference specific job codes in comments if there are issues
- ✅ Review the complete history before making decisions
- ✅ Approve requests that meet all validation criteria

### ❌ DON'T
- ❌ Don't leave requests in "Pending" indefinitely - set a status
- ❌ Don't approve without verifying all job codes are valid
- ❌ Don't forget to add comments explaining rejections
- ❌ Don't assume requesters know why you changed status - add comments

---

## 🔐 Access Requirements

You must have one of these roles to access the Job Codes Admin Panel:
- **Admin - All Tabs** - Full access to all admin functions
- **Admin - Job Codes** - Full access to job codes management
- **Reviewer - Job Codes** - View-only access (cannot edit)

---

## 📝 Request Information Reference

### What is a "Consolidated Request"?
A consolidated request contains multiple job codes (1-300+) submitted as a **single request**. 

**Example**:
- Instead of 6 separate requests (one per job code)
- You get 1 request with all 6 codes listed
- Much cleaner to manage in the admin table!

### Status Definitions
| Status | Meaning | Next Action |
|--------|---------|-------------|
| **Pending** | New request, not reviewed yet | Review and decide approval |
| **In Review** | Being investigated/verified | Complete review, then approve/reject |
| **Approved** | Ready for implementation | Hand off to implementation team |
| **Rejected** | Not approved due to issues | Notify requester with reason |

---

## ❓ FAQ

**Q: Can I edit the job codes in a request?**  
A: No, job codes are set when the request is created. You can only change the status and add comments.

**Q: What happens when I change the status?**  
A: The change is recorded in the history with timestamp and your name. Requesters may receive notifications about the change.

**Q: Can I undo a status change?**  
A: Yes, just change it back. The change history shows all previous changes, so there's a complete audit trail.

**Q: Are comments permanent?**  
A: Yes, comments are saved permanently in the request. Everyone can see all comments added.

**Q: How many job codes can be in one request?**  
A: The system supports 1-300+ job codes per request. No limit enforced, but very large requests may need to be split for clarity.

**Q: What if I accidentally approve a request?**  
A: Change the status back to "Pending" and add a comment explaining it was an accidental approval.

---

## 🆘 Troubleshooting

### Problem: Status change not saving
**Solution**: 
1. Make sure you see a green success notification
2. Wait 2-3 seconds for the table to refresh
3. Close and reopen the modal to verify

### Problem: Can't see the Job Code Requests tab
**Solution**: 
1. Check your user role (must have Admin or Reviewer role for Job Codes)
2. Contact your system administrator if you need access

### Problem: Comment won't submit
**Solution**:
1. Make sure the comment text box is not empty
2. Try refreshing the page
3. Check the browser console for error messages

### Problem: Modal won't open when clicking "View"
**Solution**:
1. Try refreshing the page
2. Check browser console (F12) for JavaScript errors
3. Verify the request ID in the URL matches the request

---

## 📞 Support

If you encounter issues or have questions:
1. Check the FAQ section above
2. Contact the Job Codes Admin Support team
3. Reference the request ID when reporting issues

---

## 📚 Related Documentation

- **System Overview**: See [KNOWLEDGE_HUB.md](../../../Documentation/KNOWLEDGE_HUB.md#4-job-codes-teaming-dashboard)
- **Technical Details**: See [TECHNICAL_LEARNINGS.md](TECHNICAL_LEARNINGS.md)
- **How to Submit a Request**: [USER_GUIDE_SUBMISSION.md](USER_GUIDE_SUBMISSION.md) (coming soon)
