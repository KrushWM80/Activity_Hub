# General Setup Documentation

This is the central documentation hub for all setup, configuration, and deployment processes.

---

## 📁 Folder Structure

### **APM_Setup/**
Complete Application Portfolio Management (APM) onboarding documentation.

**Contains:**
- APM onboarding process guide
- Data Classification Assessment (DCA) steps
- Security and compliance requirements
- ServiceNow integration
- Support contacts

**Start here for:** APM record creation, assessments, SSP initiation

**Service Ticket:** RITM74792480

---

### **Azure_Setup/**
Azure cloud platform setup and HTML application deployment guides.

**Contains:**
- Azure account creation guide
- Static Web App deployment instructions
- Permission and access control documentation
- Management groups and RBAC
- Troubleshooting guides

**Start here for:** Deploying HTML applications to Azure, resolving permission issues

**Current Setup:**
- Subscription: `sp-pl-cosmos-prod-000`
- Subscription ID: `0a461000-1765-46fb-bc3a-c05b598e50e4`
- Resource Group: `amp2-prod-cosmos-rg`
- Management Group: `gtp-v2-cosmos-prod`

---

### **Design/**
UI/UX design system, brand guidelines, and component specifications.

**Contains:**
- Brand extraction templates
- Color palettes and design tokens
- Widget specifications
- Shared components and icons
- Design system documentation

**Start here for:** Front-end development, UI consistency, brand compliance

---

### **Assessment/**
Software and environment assessment tools and documentation.

**Contains:**
- Software assessment tools
- Installation guides
- Requirements documentation
- Network workarounds
- Git setup scripts

**Start here for:** Environment setup, software installation, troubleshooting

---

## 🧩 Reusable UI Patterns

### **[Multi-Select Dropdown Filters](MULTI_SELECT_DROPDOWN_PATTERN.md)**
Complete copy-paste pattern for adding multi-select dropdown filters to any dashboard. Includes HTML structure, CSS, JavaScript (populate, label updates, event delegation IIFE, search input), API integration, and wiring. Originally built for TDA Insights — reusable across all projects.

---

## 🎯 Quick Start Guides

### For New Projects:

1. **Application Portfolio Management (APM)**
   - Navigate to `APM_Setup/README.md`
   - Follow the 4-step onboarding process
   - Complete DCA and assessments
   - Initiate SSP when certified

2. **Azure Deployment**
   - Navigate to `Azure_Setup/README.md`
   - Create/verify Azure account
   - Set up resource group
   - Deploy Static Web App

3. **Design Implementation**
   - Navigate to `Design/README.md`
   - Review design system
   - Use brand components
   - Follow widget specifications

---

## 📊 Current Project Status

### APM Status:
- [ ] Service Ticket Created: RITM74792480
- [ ] APM# Received: ________________
- [ ] DCA Completed: ________________
- [ ] Assessments Complete: ________________
- [ ] Certified: ________________
- [ ] SSP Initiated: ________________

### Azure Status:
- [ ] Account Set Up
- [ ] Permissions Verified
- [ ] Resource Group Access Confirmed
- [ ] Static Web App Created: ________________
- [ ] Application Deployed: ________________
- [ ] Public URL: ________________

### ServiceNow Status:
- [ ] Credentials Verified
- [ ] Required Items Identified
- [ ] Requests Submitted
- [ ] Tracking Active RITMs

---

## 🔗 Key Resources & Links

### Walmart Internal:
- **ServiceNow Portal**: https://walmartglobal.service-now.com/
- **Application Hub**: https://walmartglobal.service-now.com/apm?id=wm_application_hub
- **APM FAQ**: https://teams.wal-mart.com/sites/GBSConnect/SitePages/Frequently-Asked-Questions---APM-and-SOF.aspx
- **APM Overview**: https://teams.wal-mart.com/sites/GBSConnect/SitePages/What-Is-Application-Portfolio-Management-.aspx

### Azure:
- **Azure Portal**: https://portal.azure.com
- **Azure Documentation**: https://learn.microsoft.com/azure/
- **Static Web Apps**: https://learn.microsoft.com/azure/static-web-apps/

### Development:
- **Git Repository**: (if initialized in Assessment folder)
- **Code Puppy**: Installed version 0.0.249

---

## 📞 Support Contacts

### APM & Compliance:
- **APM Help**: apmmailbox@wal-mart.com
- **SSP Help**: Secrisk@wal-mart.com
- **Workplace Group**: https://walmart.workplace.com/groups/807323419664741/

### Cloud & Infrastructure:
- **Azure Admin**: ________________
- **Cloud Team**: ________________
- **IT Service Desk**: ________________

### Development Tools:
- **Code Puppy Support**: (see installation documentation)
- **Git Support**: (see Assessment/README_GIT.md)

---

## 🛠️ Development Environment

### Installed Tools:
- **Code Puppy**: v0.0.249 (interactive mode available)
- **Python**: (virtual environment in .venv-1/)
- **Git**: (initialized in Assessment folder)
- **PowerShell**: Windows PowerShell v5.1

### Configuration Files:
- `main.py`: Main application entry point
- `requirements.txt`: Python dependencies
- `setup.py`: Setup configuration

---

## ✅ Master Checklist

### Initial Setup:
- [ ] Azure account created and configured
- [ ] APM onboarding request submitted
- [ ] ServiceNow access verified
- [ ] Development environment set up
- [ ] Code Puppy installed and tested
- [ ] Git repository initialized

### Ongoing Tasks:
- [ ] Complete APM assessments (DCA, PCI, RISK)
- [ ] Resolve Azure permission issues
- [ ] Deploy HTML application to Azure
- [ ] Track ServiceNow requests
- [ ] Implement design system components
- [ ] Monitor application in production

### Documentation:
- [ ] All setup guides reviewed
- [ ] Project details documented
- [ ] Support contacts saved
- [ ] Credentials secured
- [ ] Process improvements noted

---

## 📝 Notes & Action Items

### Current Priorities:
1. ________________
2. ________________
3. ________________

### Blockers:
- ________________
- ________________

### Next Steps:
- ________________
- ________________

### Lessons Learned:
_Document insights and best practices as you progress through setup_

---

## 🔄 Regular Maintenance

### Weekly:
- [ ] Check APM assessment status
- [ ] Review Azure resource usage and costs
- [ ] Monitor ServiceNow request statuses
- [ ] Update documentation with changes

### Monthly:
- [ ] Review and update support contacts
- [ ] Archive completed requests/tickets
- [ ] Update process documentation
- [ ] Review security and compliance status

---

## 📚 Related Documentation

- **Production Path**: See `Production_Path/README.md` - Complete production deployment workflow
- **Azure Guides**: See `Azure_Setup/README.md`
- **Design System**: See `Design/README.md`
- **Assessment Tools**: See `Assessment/` folder files
- **ServiceNow Guides**: See step-specific guides in `Production_Path/` folders (02-05)

---

*Last Updated: November 18, 2025*
