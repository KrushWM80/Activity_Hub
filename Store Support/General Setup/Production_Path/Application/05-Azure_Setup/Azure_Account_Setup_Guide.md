# Creating an Azure Account: Complete Setup Guide

## Overview
This guide walks you through creating an Azure account, understanding subscription management, and setting up resource groups for your HTML application deployment.

---

## 🎯 What You'll Get After Setup

After completing this guide, you'll have:
- ✅ Azure Account
- ✅ Subscription ID
- ✅ Resource Group(s)
- ✅ Access to Azure Portal
- ✅ Ability to deploy services (Static Web Apps, etc.)

---

## 📚 Key Concepts Explained

### **Azure Account**
- Your login credentials (Microsoft account)
- Single entry point to all Azure services
- Can manage multiple subscriptions
- Similar to having an Amazon or Google account

### **Subscription ID**
- **What it is**: A unique identifier for your Azure subscription
- **Format**: UUID (e.g., `12345678-1234-1234-1234-123456789012`)
- **Purpose**: Links you to billing, resource usage, and service limits
- **How many**: You can have multiple subscriptions under one account
- **Usage**: Required when deploying resources via CLI or API
- **Important**: Your billing is tracked per subscription

### **Resource Group**
- **What it is**: Container that holds related Azure resources
- **Purpose**: Organize and manage resources together
- **Billing**: Track costs by resource group
- **Access Control**: Apply permissions to entire group
- **Deletion**: Deleting resource group deletes all resources in it
- **Best Practice**: Logical grouping (e.g., all resources for one project)

### **Example Structure**:
```
Azure Account (your login)
    ├── Subscription 1 (Free Tier)
    │   ├── Resource Group: "my-html-app-rg"
    │   │   ├── Static Web App: "my-html-app"
    │   │   └── Storage Account: "myappdata"
    │   └── Resource Group: "other-project-rg"
    │       └── App Service: "my-api"
    │
    └── Subscription 2 (Paid/Enterprise)
        ├── Resource Group: "production-rg"
        └── Resource Group: "testing-rg"
```

---

## ✅ Step-by-Step: Create Your Azure Account

### **Step 1: Go to Azure**

1. [ ] Open browser and go to https://azure.microsoft.com/
2. [ ] Click "Start free" button (top right)
3. [ ] You'll be directed to account creation page

---

### **Step 2: Sign In or Create Microsoft Account**

1. [ ] Enter your email address
2. [ ] If you have a Microsoft account (Outlook, Hotmail, etc.), sign in
3. [ ] If you don't have one, click "Create one" to make new account
4. [ ] Fill in:
   - [ ] First name
   - [ ] Last name
   - [ ] Email
   - [ ] Password (strong password recommended)
5. [ ] Complete security verification (email or phone)
6. [ ] Click "Next"

---

### **Step 3: Set Up Azure Free Account**

1. [ ] Click "Start free"
2. [ ] Agree to Microsoft Azure terms
3. [ ] You'll see the free account benefits:
   - 12 months free services
   - $200 free credit (30 days)
   - Always-free services
4. [ ] Click "Continue"

---

### **Step 4: Verify Identity**

Azure requires identity verification. Choose one method:

#### **Option A: Phone Verification** (Faster)
1. [ ] Select your country
2. [ ] Enter phone number
3. [ ] Receive SMS code
4. [ ] Enter code to verify
5. [ ] Click "Verify code"

#### **Option B: Card Verification**
1. [ ] Enter credit card details
2. [ ] Enter billing address
3. [ ] Confirm identity through charge check
4. [ ] Takes 24-48 hours

**Note**: Card is NOT charged - just verification

---

### **Step 5: Choose Your Free Account Details**

1. [ ] Review free services available
2. [ ] Agree to terms and conditions
3. [ ] Click "Sign up"
4. [ ] Wait for account provisioning (1-2 minutes)

---

### **Step 6: Access Your Azure Portal**

1. [ ] Once account is created, click "Go to Azure Portal"
2. [ ] Or go to https://portal.azure.com
3. [ ] Sign in with your Microsoft account
4. [ ] You should see the Azure Portal dashboard

---

## 🔍 Finding Your Subscription ID

Once you're in the Azure Portal, find your Subscription ID:

### **Method 1: Using Home Dashboard**
1. [ ] From Azure Portal home, click "Subscriptions" (left sidebar)
2. [ ] You'll see your subscription(s) listed
3. [ ] Copy the **Subscription ID** (the UUID)
4. [ ] Save this ID somewhere safe

### **Method 2: Using Quick Search**
1. [ ] Click search box at top of Portal
2. [ ] Type "Subscriptions"
3. [ ] Click "Subscriptions" from results
4. [ ] See your Subscription ID

### **Your Subscription ID will look like:**
```
12345678-9abc-def0-1234-567890abcdef
```

**Save this ID!** You'll need it for:
- Deploying resources via Azure CLI
- Billing and cost tracking
- API calls
- Team collaboration

---

## 📂 Creating Your First Resource Group

Resource Groups organize all your resources for a specific project.

### **Step 1: Open Resource Groups**

1. [ ] Go to Azure Portal: https://portal.azure.com
2. [ ] Search for "Resource groups" in search box
3. [ ] Click on "Resource groups" from results

### **Step 2: Create New Resource Group**

1. [ ] Click "+ Create" button
2. [ ] Fill in the following fields:

#### **Subscription**
- [ ] Select your subscription (should auto-select)
- [ ] This links the resource group to your subscription

#### **Resource group name**
- [ ] Enter descriptive name (e.g., "my-html-app-rg")
- [ ] Naming convention: `[project-name]-rg`
- [ ] Rules: Only alphanumeric, hyphens, underscores
- [ ] Cannot start with number or special character

#### **Region**
- [ ] Select region closest to your users
- [ ] Common choices: "East US", "West US", "Europe West"
- [ ] Same region = faster data transfer
- [ ] Doesn't lock you to one region for resources
- [ ] Different regions may have different pricing

### **Step 3: Review and Create**

1. [ ] Click "Review + create"
2. [ ] Review your settings
3. [ ] Click "Create"
4. [ ] Wait for creation (usually instant)

### **Step 4: Verify Resource Group Created**

1. [ ] You'll see "Deployment succeeded" notification
2. [ ] Click "Go to resource group"
3. [ ] You now have an empty resource group
4. [ ] Ready to deploy services!

---

## 💾 Important Information to Document

Create a document or use the section below to save this critical information:

### **Account Information**
- [ ] Email: ________________
- [ ] Microsoft Account: ________________
- [ ] Account Created Date: ________________

### **Subscription Information**
- [ ] Subscription Name: ________________
- [ ] **Subscription ID**: ________________
- [ ] Account Type: ☐ Free Tier  ☐ Paid  ☐ Enterprise
- [ ] Credit Amount: $________
- [ ] Credit Expiration Date: ________________

### **Resource Group Information**
- [ ] Resource Group Name: ________________
- [ ] Region: ________________
- [ ] Created Date: ________________
- [ ] Purpose: ________________

### **Access Details**
- [ ] Portal URL: https://portal.azure.com
- [ ] Username: ________________
- [ ] Password saved in: ☐ Password Manager  ☐ Secure location

---

## ⚠️ Important Security Notes

### **DO:**
- [ ] Use strong password (12+ characters, mixed case, numbers, symbols)
- [ ] Enable Multi-Factor Authentication (MFA) for your account
- [ ] Store Subscription ID securely but accessible
- [ ] Use resource groups to organize and control access
- [ ] Regularly review costs and usage

### **DON'T:**
- ❌ Share Subscription ID publicly
- ❌ Commit Subscription ID to GitHub or public repos
- ❌ Use weak or reused passwords
- ❌ Leave portal unattended without logging out
- ❌ Give full access to resources to untrusted parties

---

## 🔐 Enable Multi-Factor Authentication (Recommended)

### **Why MFA?**
- Extra security layer
- Prevents unauthorized access even if password compromised
- Required for many enterprise scenarios
- Free to enable

### **How to Enable:**

1. [ ] In Azure Portal, click your name (top right)
2. [ ] Click "View my account"
3. [ ] Click "Security info" (left sidebar)
4. [ ] Click "+ Add method"
5. [ ] Choose method:
   - [ ] Microsoft Authenticator app (recommended)
   - [ ] Phone verification (SMS or call)
   - [ ] Email verification
6. [ ] Follow prompts to set up
7. [ ] Test by logging out and back in

---

## 🎯 Next Steps After Account Creation

1. **Immediate**:
   - [ ] Save your Subscription ID securely
   - [ ] Write down your Resource Group name
   - [ ] Enable MFA for security

2. **Short Term**:
   - [ ] Create your Static Web App (in next guide)
   - [ ] Deploy your HTML application
   - [ ] Get your public URL

3. **Ongoing**:
   - [ ] Monitor costs in Azure Portal
   - [ ] Review resource usage monthly
   - [ ] Keep password secure
   - [ ] Update recovery information

---

## 📞 Troubleshooting

### **Problem: "Card verification failed"**
- Solution: Try different card or contact bank
- Alternative: Use phone verification instead
- Wait 24-48 hours if declined

### **Problem: "Cannot find Subscription ID"**
- Go to Subscriptions blade in portal
- Check all subscriptions listed
- Subscription ID is shown in list

### **Problem: "Cannot create Resource Group"**
- Ensure you selected correct subscription
- Check name doesn't contain invalid characters
- Try different region
- Refresh portal and retry

### **Problem: "Free tier account was suspended"**
- Check email for Microsoft notifications
- May have exceeded free credit limits
- Contact Azure Support
- Consider upgrading to paid

### **Problem: "Forgot password"**
- Go to https://account.live.com/password/reset
- Follow password recovery steps
- Can use email or phone verification

---

## 📖 Useful Azure Portal Features

### **Bookmarking Common Pages**
- Subscriptions: https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade
- Resource Groups: https://portal.azure.com/#blade/HubsExtension/BrowseResourceGroups
- Cost Analysis: https://portal.azure.com/#blade/Microsoft_Azure_Billing/CostAnalysisBlade

### **Azure Mobile App**
- Download "Azure" app on your phone
- Monitor resources on-the-go
- Receive alerts for issues
- Approve deployments remotely

### **Azure CLI**
- Command-line tool for Azure management
- Useful for automation and scripting
- Install from: https://learn.microsoft.com/cli/azure/install-azure-cli

---

## 📚 Additional Resources

- **Azure Free Account**: https://azure.microsoft.com/free/
- **Azure Portal**: https://portal.azure.com/
- **Account & Subscription Help**: https://support.microsoft.com/account-billing
- **Azure Pricing Calculator**: https://azure.microsoft.com/pricing/calculator/
- **Azure Documentation**: https://learn.microsoft.com/azure/

---

## Notes & Setup Progress

### Setup Checklist:
- [ ] Azure account created
- [ ] Identity verified
- [ ] Logged into Azure Portal
- [ ] Subscription ID saved
- [ ] Resource Group created
- [ ] MFA enabled (recommended)
- [ ] Password saved securely
- [ ] Billing information reviewed

### Date Completed: ________________

### Issues Encountered:
_Document any problems during setup_

### Next Action:
_When ready, proceed to: Azure_HTML_Publishing_Guide.md - Step 4_
