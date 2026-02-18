# ☁️ Step 5: Azure Cloud Setup (Post-SSP)

**Timeline:** 1-2 weeks  
**Owner:** Application Owner / Cloud Infrastructure Team  
**Prerequisites:** Step 4 completed (SSP Approved)

---

## 🎯 Overview

After receiving SSP approval, you can proceed with Azure cloud infrastructure setup for your production deployment. This step covers Azure account setup, resource provisioning, and deployment configuration specific to Walmart's Azure environment.

**Key Output:** Production-ready Azure infrastructure with proper permissions, security, and governance

---

## 🔧 ServiceNow for Azure Requests

Azure subscriptions and resources at Walmart are requested through ServiceNow. For detailed instructions on:
- Requesting Azure subscriptions via ServiceNow
- Submitting resource provisioning requests
- Tracking your Azure requests
- Referencing your APM/SSP in requests

**See:** [ServiceNow Guide for Azure Setup](./ServiceNow_Guide.md)

---

## 📁 Azure Setup Guides in This Folder

### 1. **Azure_Account_Setup_Guide.md**
Complete guide for creating an Azure account, understanding subscriptions, and setting up resource groups.

**Covers:**
- Creating Azure account
- Understanding Subscription IDs
- Creating Resource Groups
- Security best practices
- Multi-Factor Authentication setup

**Start here if:** You don't have an Azure account yet

---

### 2. **Azure_HTML_Publishing_Guide.md**
High-level overview of publishing HTML applications to Azure with different hosting options.

**Covers:**
- Azure hosting options comparison (Static Web Apps, App Service, Storage + CDN, Containers)
- Step-by-step deployment workflow
- Continuous deployment setup
- Custom domain configuration
- Monitoring and maintenance

**Start here if:** You want to understand your Azure hosting options

---

### 3. **Azure_Permission_Error_Resolution.md**
Troubleshooting guide for permission errors when trying to create Azure resources.

**Covers:**
- Understanding permission errors
- How to request access from admins
- Different solution options
- Sample email templates
- Checking current access levels

**Start here if:** You're getting permission errors in Azure Portal

---

### 4. **Azure_Management_Groups_AccessLevels.md**
Detailed explanation of Azure management groups, access levels, and role-based access control (RBAC).

**Covers:**
- Management group hierarchy
- Access level requirements for Static Web Apps
- Role types (Owner, Contributor, Reader)
- How to check current permissions
- What to request from admins

**Start here if:** You need to understand Azure permissions and management groups

---

## 🎯 Quick Start Guide

### For New Azure Users:
1. Read: `Azure_Account_Setup_Guide.md`
2. Create your Azure account and resource group
3. Read: `Azure_HTML_Publishing_Guide.md`
4. Deploy your HTML application

### For Existing Azure Users with Permission Issues:
1. Read: `Azure_Permission_Error_Resolution.md`
2. Check your current access level
3. Read: `Azure_Management_Groups_AccessLevels.md` for details
4. Request appropriate permissions from admin

---

## 📊 Your Current Azure Setup

**Document your Azure details here:**

### Account Information:
- Azure Account Email: ________________
- Subscription Name: `sp-pl-cosmos-prod-000`
- Subscription ID: `0a461000-1765-46fb-bc3a-c05b598e50e4`
- Management Group: `gtp-v2-cosmos-prod`

### Resource Group:
- Resource Group Name: `amp2-prod-cosmos-rg`
- Region: ________________
- Current Access Level: ________________

### Static Web App Details:
- App Name: ________________
- Public URL: ________________
- Deployment Status: ________________
- Created Date: ________________

---

## 🔑 Key Azure Concepts

### Subscription
- Unique identifier for billing and resource management
- You have: `0a461000-1765-46fb-bc3a-c05b598e50e4`
- Links to your billing account

### Resource Group
- Container for organizing related Azure resources
- You're using: `amp2-prod-cosmos-rg`
- All resources in a group can be managed together

### Management Group
- Organizes multiple subscriptions
- Applies policies across subscriptions
- You're under: `gtp-v2-cosmos-prod` (production)

### Static Web App
- Hosting service for static HTML/CSS/JavaScript
- Automatic HTTPS and global CDN
- Built-in CI/CD from GitHub

---

## 📞 Support Contacts

### Azure Support:
- Azure Portal: https://portal.azure.com
- Azure Documentation: https://learn.microsoft.com/azure/
- Azure Pricing Calculator: https://azure.microsoft.com/pricing/calculator/

### Internal Support (if using corporate Azure):
- Cloud Team: ________________
- Admin Contact: ________________
- IT Ticket System: ________________

---

## ✅ Azure Setup Checklist

### Phase 1: Account & Access Setup (Week 1)
- [ ] Request Azure subscription (if not already available)
- [ ] Verify access to Azure Portal
- [ ] Join appropriate security groups
- [ ] Configure Azure CLI or PowerShell access
- [ ] Set up authentication (Azure AD integration)

### Phase 2: Resource Planning (Week 1)
- [ ] Define resource group structure
- [ ] Plan naming conventions (follow Walmart standards)
- [ ] Identify required Azure services
- [ ] Estimate costs and obtain budget approval
- [ ] Document architecture in Azure-specific terms

### Phase 3: Resource Provisioning (Week 1-2)
- [ ] Create resource groups
- [ ] Provision compute resources (VMs, App Services, Functions, etc.)
- [ ] Set up databases (Azure SQL, CosmosDB, etc.)
- [ ] Configure storage accounts
- [ ] Set up networking (VNets, subnets, NSGs)
- [ ] Configure load balancers or traffic managers (if needed)

### Phase 4: Security & Governance (Week 2)
- [ ] Apply Azure Policy compliance requirements
- [ ] Configure security groups and RBAC
- [ ] Enable Azure Security Center
- [ ] Set up Azure Monitor and Log Analytics
- [ ] Configure backup and disaster recovery
- [ ] Enable encryption (at rest and in transit)
- [ ] Set up Key Vault for secrets management

### Phase 5: Integration & Testing (Week 2)
- [ ] Connect to on-premises resources (if applicable)
- [ ] Configure service endpoints or private links
- [ ] Test network connectivity
- [ ] Validate security controls
- [ ] Test monitoring and alerting
- [ ] Perform security scanning

---

## 🔑 Key Azure Concepts for Walmart

### Naming Conventions
Follow Walmart's Azure naming standards:
- Resource Groups: `rg-[pillar]-[project]-[environment]`
- Storage Accounts: `st[pillar][project][env]`
- VMs: `vm-[pillar]-[project]-[function]-[env]`

### Required Tags
All Azure resources must be tagged:
- `CostCenter`: Budget code
- `Environment`: Dev/Test/Prod
- `Owner`: Technical owner email
- `Project`: Project name
- `DataClassification`: Based on APM DCA

---

## 🎯 Success Criteria

You've successfully completed Step 5 when:

- ✅ Azure subscription and access configured
- ✅ All resources provisioned and properly tagged
- ✅ Security controls implemented (matching SSP)
- ✅ Monitoring and logging configured
- ✅ Integration testing completed
- ✅ Security scanning passed
- ✅ Ready for production deployment

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Access denied to subscription | Request security group membership from Cloud Infrastructure team |
| Cannot create resources | Verify Azure Policy compliance and subscription limits |
| Naming validation errors | Follow Walmart naming conventions exactly |
| Cost approval delays | Submit budget request early with detailed estimates |
| Network connectivity issues | Verify NSG rules and VNet configuration |
| Missing required tags | Review and apply all mandatory resource tags |

---

## 💡 Best Practices

### Before You Start:
1. ✅ Ensure SSP is approved with all security controls documented
2. ✅ Have architecture diagram showing Azure components
3. ✅ Obtain budget approval for estimated Azure costs
4. ✅ Review Walmart Azure standards and policies

### During Setup:
1. ✅ Use Infrastructure as Code (ARM templates, Terraform)
2. ✅ Apply tags to ALL resources immediately
3. ✅ Enable monitoring and logging from day one
4. ✅ Follow naming conventions strictly
5. ✅ Document all resource IDs and configurations

### After Setup:
1. ✅ Set up cost alerts and budget monitoring
2. ✅ Schedule regular security reviews
3. ✅ Maintain documentation of any changes
4. ✅ Plan for disaster recovery testing

---

## 🚀 Next Steps

Once Azure infrastructure is ready:
- Deploy your application to production
- Complete go-live activities per deployment plan
- Perform post-deployment verification
- Begin ongoing compliance and monitoring (see Step 4 SSP Post-Approval Checklist)

---

**💡 Remember:** Your SSP defines the security controls that must be implemented in Azure. Ensure your Azure configuration matches what was approved in the SSP!

---

## 📝 Notes & Issues

### Current Status:
_Document your progress here_

### Issues Encountered:
_Track any problems and resolutions_

### Next Steps:
_What needs to be done next_
