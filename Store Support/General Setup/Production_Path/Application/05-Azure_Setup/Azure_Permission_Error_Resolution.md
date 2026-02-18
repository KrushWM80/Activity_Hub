# Azure Static Web App Permission Error: Resolution Guide

## Error Details
**Error Message**: "You cannot perform this action without all of the following permissions (Microsoft.Web/StaticSites/write)"

**Your Current Setup**:
- Subscription ID: `0a461000-1765-46fb-bc3a-c05b598e50e4`
- Subscription: `sp-pl-cosmos-prod-000`
- Resource Group: `amp2-prod-cosmos-rg`

---

## 🔍 What This Error Means

This error occurs when:
1. ❌ Your user account lacks write permissions for Static Web Apps
2. ❌ The subscription/resource group is restricted (enterprise/production)
3. ❌ Your role doesn't include `Microsoft.Web/StaticSites/write` permission
4. ❌ You're using a work/shared account with limited permissions

---

## ✅ Solution Options

### **Option 1: Use a Personal Azure Subscription (Recommended)**

If you have a personal Azure free account, use that instead:

1. [ ] Go to Azure Portal: https://portal.azure.com
2. [ ] Click your name (top right) → Switch directory
3. [ ] Select your personal account/subscription
4. [ ] Create Static Web App using your personal subscription
5. [ ] Deploy your HTML there

**Advantages:**
- Full permissions (owner)
- Free tier available
- No approval needed
- Complete control

---

### **Option 2: Request Permission from Admin**

If you need to use `sp-pl-cosmos-prod-000` subscription:

#### **What to Ask Your Admin For:**
Ask your Azure Administrator to grant you one of these roles:
- **Owner** - Full permissions (recommended for development)
- **Contributor** - Can create resources but not manage access
- **Specific Role** - "Static Sites Contributor" or similar

#### **How Admin Grants Access:**

Your admin needs to:
1. [ ] Go to Resource Group: `amp2-prod-cosmos-rg`
2. [ ] Click "Access control (IAM)" → "Add role assignment"
3. [ ] Role: Select "Contributor" or "Owner"
4. [ ] Member: Search for your email/username
5. [ ] Click "Review + assign"

#### **What to Tell Your Admin:**
```
Can you grant me [Owner/Contributor] role for the 
amp2-prod-cosmos-rg resource group in the 
sp-pl-cosmos-prod-000 subscription? 

I need Microsoft.Web/StaticSites/write permissions 
to create a Static Web App for [your project name].

My email: [your email]
```

---

### **Option 3: Create New Resource Group with Your Permissions**

If you want to stay in the same subscription but have limited access:

1. [ ] Contact your admin to grant you permission to **create resource groups**
2. [ ] Once granted, create a NEW resource group:
   - Name: `my-html-app-rg` (or similar)
   - Region: Same as `amp2-prod-cosmos-rg` for consistency
3. [ ] Use the NEW resource group for Static Web App
4. [ ] Admin can grant you permissions on that new group

---

### **Option 4: Request Dedicated Static Web App**

If this is for a business project:

1. [ ] Submit a request to your Azure administrator/team
2. [ ] Request: "Azure Static Web App for [project name]"
3. [ ] They create it with proper permissions
4. [ ] They grant you access
5. [ ] You get URL to deploy to

---

## 🔐 Understanding Azure Permissions

### **Common Roles and Permissions:**

| Role | Permissions | Can Create Static Web Apps? |
|------|-------------|---------------------------|
| **Owner** | Full control | ✅ YES |
| **Contributor** | Create resources | ✅ YES |
| **Developer** | Limited resources | ❌ MAYBE |
| **Reader** | View only | ❌ NO |
| **Custom Role** | Varies | ❓ DEPENDS |

---

## 📋 Recommended Path Forward

### **If This is a Personal Project:**
1. [ ] Create free personal Azure account
2. [ ] Create Static Web App there
3. [ ] Deploy your HTML
4. [ ] No permission issues

### **If This is for Work:**
1. [ ] Identify the correct subscription/resource group for your project
2. [ ] Contact your Azure admin or team lead
3. [ ] Request appropriate permissions
4. [ ] Once granted, deploy
5. [ ] Keep resources organized with proper naming

### **If You're Unsure:**
1. [ ] Ask your IT/Cloud team which subscription to use
2. [ ] Ask which resource group to use
3. [ ] Ask them to grant required permissions
4. [ ] Proceed once confirmed

---

## 🎯 Immediate Next Steps

### **Step 1: Determine Subscription to Use**

- [ ] Is `sp-pl-cosmos-prod-000` the RIGHT subscription?
  - If YES → Request permissions (Option 2)
  - If NO → Use personal Azure account (Option 1)

### **Step 2: Verify Permissions**

Check your current permissions:
1. [ ] Go to Azure Portal
2. [ ] Go to Resource Group: `amp2-prod-cosmos-rg`
3. [ ] Click "Access control (IAM)"
4. [ ] Click "Check access" (top right)
5. [ ] Enter your email
6. [ ] See your current role/permissions

### **Step 3: Take Action**

Based on permissions:
- **If you have "Owner" or "Contributor"**: The error shouldn't occur. Try refreshing portal or reloading
- **If you have "Reader" only**: Request upgrade (Option 2)
- **If not listed**: You have no permissions. Request access (Option 2)

---

## 🔧 Troubleshooting Specific Scenarios

### **Scenario A: You Work at Walmart**

`sp-pl-cosmos-prod-000` looks like a corporate production subscription.

**Action**: 
1. [ ] Check with your team lead/manager
2. [ ] Verify this is the right subscription for your project
3. [ ] Contact your Azure administrator or Cloud Center of Excellence (CCOE)
4. [ ] They will grant appropriate permissions
5. [ ] Mention this is for a Static Web App deployment

**Typical Process**:
- [ ] Submit request through IT/Cloud ticketing system
- [ ] Wait for approval (usually 1-2 days)
- [ ] Admin grants permissions
- [ ] Retry creating Static Web App

---

### **Scenario B: You're Learning Azure**

If this is a learning project:

**Better Option**:
1. [ ] Create free personal Azure account
2. [ ] Use that for learning/testing
3. [ ] Keep work subscriptions for production
4. [ ] No permission issues
5. [ ] Complete control for experimenting

---

### **Scenario C: This is Production Code**

If this is production HTML:

**Proper Process**:
1. [ ] Define requirements with stakeholders
2. [ ] Request proper Azure resources through official channels
3. [ ] Get correct subscription and resource group
4. [ ] Have proper access management
5. [ ] Follow your organization's policies
6. [ ] Deploy with proper governance

---

## 📞 Sample Email to Your Azure Admin

If you need to request permissions, here's a template:

---

**Subject**: Request Azure Permissions - Static Web App Creation

**Body**:
```
Hi [Admin Name],

I need to create an Azure Static Web App for [project name] 
in our existing subscription: sp-pl-cosmos-prod-000, 
resource group: amp2-prod-cosmos-rg.

When attempting to create the resource, I'm getting this error:
"You cannot perform this action without all of the following 
permissions (Microsoft.Web/StaticSites/write)"

Could you please grant me [Owner/Contributor] role for the 
amp2-prod-cosmos-rg resource group?

My email: [your email]
Subscription ID: 0a461000-1765-46fb-bc3a-c05b598e50e4

Thank you,
[Your Name]
```

---

## 🛠️ Quick Checklist

- [ ] Subscription is the RIGHT one for this project
- [ ] Contacted admin if needed for permissions
- [ ] Know your current role in resource group
- [ ] Have plan to get required permissions
- [ ] Ready to retry once permissions granted
- [ ] Have personal Azure account as backup

---

## 📚 Additional Resources

- **Azure RBAC Overview**: https://learn.microsoft.com/azure/role-based-access-control/
- **Manage Access to Resources**: https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal
- **Static Web Apps Permissions**: https://learn.microsoft.com/azure/static-web-apps/

---

## Notes

### Your Current Situation:
- Subscription: `sp-pl-cosmos-prod-000`
- Resource Group: `amp2-prod-cosmos-rg`
- Missing Permission: `Microsoft.Web/StaticSites/write`

### Action Plan:
_Document your decision below_

- [ ] Using this subscription for a reason
- [ ] Contact admin for permissions
- [ ] Create new personal account instead
- [ ] Waiting for admin response
- [ ] Other: ________________

### Admin Contact Information:
- Name: ________________
- Email: ________________
- Team: ________________

### Status:
- Started: ________________
- Permissions Requested: ________________
- Permissions Granted: ________________
- Static Web App Created: ________________
