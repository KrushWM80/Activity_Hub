# Azure Management Groups & Access Levels Explained

## Your Situation

**Resource Group**: `amp2-prod-cosmos-rg`
**Parent Management Group**: `gtp-v2-cosmos-prod`
**Subscription**: `sp-pl-cosmos-prod-000`

---

## 🎯 What Is a Management Group?

A **Management Group** is a container that holds multiple subscriptions and applies policies across them.

### **Hierarchy:**
```
Management Group (gtp-v2-cosmos-prod)
    └── Subscription (sp-pl-cosmos-prod-000)
        └── Resource Group (amp2-prod-cosmos-rg)
            └── Resources (Static Web App, etc.)
```

### **Why They Matter:**
- Apply organization-wide policies
- Control access across multiple subscriptions
- Enforce compliance requirements
- Manage billing and governance

---

## 🔐 Access Levels You Might Have

### **Level 1: Management Group Level**
Permission granted at `gtp-v2-cosmos-prod` level

**If you have access here:**
- ✅ Can affect entire management group
- ✅ Can create subscriptions
- ✅ Can manage all subscriptions under it
- ⚠️ Rarely given to individual developers
- 👤 Usually: Management group admins only

### **Level 2: Subscription Level**
Permission granted at `sp-pl-cosmos-prod-000` level

**If you have access here:**
- ✅ Can create resources in any resource group
- ✅ Can manage billing
- ✅ Can create resource groups
- ⚠️ Sometimes restricted in production
- 👤 Usually: Subscription owners, leads

### **Level 3: Resource Group Level**
Permission granted at `amp2-prod-cosmos-rg` level

**If you have access here:**
- ✅ Can create resources (like Static Web Apps)
- ✅ Limited to this resource group only
- ✅ Most common for developers
- ✅ Good security model
- 👤 Usually: Developers on the team

### **Level 4: Resource Level**
Permission granted on specific resource

**If you have access here:**
- ✅ Can only manage that specific resource
- ✅ Very restricted
- ⚠️ Limited for development
- 👤 Usually: Specific operational teams

---

## ✅ What Access Level Do You Need for Static Web App?

### **Minimum Required Access:**

**Option A: Resource Group Level (RECOMMENDED)**
- Location: `amp2-prod-cosmos-rg`
- Role: **Contributor** or **Owner**
- Permission: `Microsoft.Web/StaticSites/write`
- Scope: Just this resource group
- ✅ Best practice for team developers

**Option B: Subscription Level**
- Location: `sp-pl-cosmos-prod-000`
- Role: **Contributor** or **Owner**
- Permission: `Microsoft.Web/StaticSites/write`
- Scope: All resource groups in subscription
- ⚠️ More permissions than you need

**Option C: Management Group Level**
- Location: `gtp-v2-cosmos-prod`
- Role: **Contributor** or **Owner**
- Permission: `Microsoft.Web/StaticSites/write`
- Scope: All subscriptions in group
- ❌ Excessive for this task
- ⚠️ Requires escalation approval

---

## 📋 Recommended Action Plan

### **Step 1: Check Your Current Access**

1. [ ] Go to Azure Portal: https://portal.azure.com
2. [ ] Navigate to: `amp2-prod-cosmos-rg` resource group
3. [ ] Click "Access control (IAM)" tab
4. [ ] Click "Check access" (top right)
5. [ ] Enter your email address
6. [ ] See what role/access you have

### **Step 2: What You Should Find**

You should see one of these:

**GOOD - Has Access:**
- [ ] Role: "Owner"
- [ ] Role: "Contributor"
- [ ] Role: "Static Sites Contributor"
- [ ] Role: Custom role with `Microsoft.Web/StaticSites/write`

**BAD - Doesn't Have Access:**
- [ ] Role: "Reader"
- [ ] Role: "Viewer"
- [ ] (Not listed - no permissions)

### **Step 3: If You Have Access (Owner/Contributor)**

Then the error is strange. Try these:

1. [ ] Refresh Azure Portal (F5)
2. [ ] Clear browser cache
3. [ ] Log out and back in
4. [ ] Try in private/incognito browser
5. [ ] Try again to create Static Web App

**If still fails**: Contact your Azure admin - there may be policy restrictions

### **Step 4: If You DON'T Have Access**

You need to request access. Here's what to request:

---

## 📧 What to Ask Your Admin For

### **Request Template:**

```
Subject: Access Request - Azure Static Web App Creation

Hi [Admin Name / Cloud Team],

I need to create an Azure Static Web App in the following location:
- Management Group: gtp-v2-cosmos-prod
- Subscription: sp-pl-cosmos-prod-000
- Resource Group: amp2-prod-cosmos-rg

Currently, I'm getting this error:
"You cannot perform this action without all of the following 
permissions (Microsoft.Web/StaticSites/write)"

Please grant me the minimum required access:

**Recommended:** 
- Role: Contributor or Owner
- Scope: Resource Group level (amp2-prod-cosmos-rg)
- Permission: Microsoft.Web/StaticSites/write

This is for [brief description of project/purpose].

My email: [your email]
Employee ID/Username: [your username]

Thank you,
[Your Name]
```

---

## 🔍 Understanding the Roles

### **Role: Owner**
```
✅ Can create resources
✅ Can delete resources
✅ Can manage access/permissions
✅ Can manage billing
❌ Too much power for most developers
```

### **Role: Contributor** (RECOMMENDED)
```
✅ Can create resources
✅ Can delete resources
✅ Cannot manage access/permissions
✅ Cannot manage billing
✅ Good balance for developers
```

### **Role: Static Sites Contributor** (BEST IF AVAILABLE)
```
✅ Can create Static Web Apps
✅ Can update Static Web Apps
✅ Cannot create other resources
✅ Most limited/secure
✅ Ask for this if available
```

### **Role: Reader**
```
❌ Can view resources only
❌ Cannot create anything
❌ Cannot delete anything
```

---

## ⚠️ Special Considerations with Management Groups

### **Production Management Group Restrictions**

Since this is under `gtp-v2-cosmos-prod` (production), there may be:

1. **Policy Restrictions**
   - Certain resource types blocked entirely
   - Certain regions restricted
   - Certain configurations required

2. **Approval Requirements**
   - Need manager approval
   - Need security team review
   - Need compliance review

3. **Access Controls**
   - Even with "Owner" role, policies may prevent creation
   - Managed at management group level
   - Cannot bypass with individual permissions

### **What This Means**

Even if you get "Contributor" access, you might STILL get errors if:
- [ ] Management group policy blocks Static Web Apps
- [ ] Your organization prefers different services
- [ ] Production resources have different requirements

**Solution**: Ask your admin if Static Web Apps are allowed in production group

---

## 🎯 Specific Questions to Ask Your Admin

1. **"Is Azure Static Web Apps allowed in the `gtp-v2-cosmos-prod` management group?"**
   - If NO: You need different resource group
   - If YES: Continue with access request

2. **"What is the minimum role needed to create Static Web Apps in `amp2-prod-cosmos-rg`?"**
   - They'll tell you: Owner, Contributor, or custom role

3. **"Are there policies that might block Static Web App creation?"**
   - They can check management group policies

4. **"What is the approval process for new resources in production?"**
   - May need tickets, approvals, etc.

---

## 🔄 Possible Outcomes

### **Outcome 1: They Grant You Access**
- [ ] You get "Contributor" or "Owner" role
- [ ] Try creating Static Web App again
- [ ] Should work

### **Outcome 2: Policy Blocks It**
- [ ] Even with access, policies prevent creation
- [ ] They need to add exception OR
- [ ] You need different resource group

### **Outcome 3: Not Allowed in Production**
- [ ] Static Web Apps not approved for prod
- [ ] Need to use App Service instead, OR
- [ ] Need to use test subscription

### **Outcome 4: Requires Approval Process**
- [ ] Cannot self-serve create
- [ ] Must submit change request
- [ ] Wait for approval
- [ ] Then IT creates it for you

---

## 💡 What You Should Do RIGHT NOW

### **Immediate Action (Today):**

1. [ ] Go to Azure Portal
2. [ ] Check your current access level (Access control IAM)
3. [ ] Take screenshot of your current role
4. [ ] Note if you see any policy restrictions

### **Next Action (Within 24 hours):**

Contact your team lead/manager and ask:

**"I'm trying to create a Static Web App in our production 
subscription (sp-pl-cosmos-prod-000). Can you help me 
understand what access level I need and if there are any 
policies that would prevent this?"**

### **Then:**

Based on their answer, either:
- [ ] They grant you access
- [ ] They point you to the right admin
- [ ] They tell you it's not allowed
- [ ] They create it for you

---

## 📊 Quick Reference: Access Levels

| Level | What It Lets You Do | What You Need | Timeline |
|-------|-------------------|--------------|----------|
| **Resource Group Contributor** | Create Static Web Apps | Ask team lead | 1 day |
| **Subscription Contributor** | Create in any resource group | Ask cloud team | 2-3 days |
| **Management Group Contributor** | Control everything | Director approval | 3-5 days |
| **Custom Role** | Specific permissions | IT to define | Varies |

---

## ⚡ Summary

**What you need to create Static Web App:**
```
Minimum: Contributor role at Resource Group level
         (amp2-prod-cosmos-rg)

Permission name: Microsoft.Web/StaticSites/write

Scope: amp2-prod-cosmos-rg (or higher subscription level)
```

**How to request it:**
```
1. Check current access via "Check access" in IAM
2. Ask your admin for Contributor role
3. Specify: Resource Group level minimum
4. Ask if Static Web Apps are allowed in this management group
```

**Likely timeline:**
```
- Same day: If you ask manager
- 1-2 days: If manager approves and forwards
- 3-5 days: If needs management group review
```

---

## Notes & Action Items

### Current Access Check:
- Checked IAM: [ ] Yes [ ] No
- Current Role: ________________
- Has write permission: [ ] Yes [ ] No

### Admin Request:
- Asked for access: [ ] Yes [ ] No
- Admin name: ________________
- Email sent: ________________
- Date requested: ________________
- Status: ________________

### Resolution:
- Access granted: [ ] Yes [ ] No
- Date granted: ________________
- Static Web App created: [ ] Yes [ ] No
