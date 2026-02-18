# 🔗 BigQuery Integration Hub
## Centralized BigQuery Resources for All Walmart Projects

**Last Updated:** November 24, 2025  
**Purpose:** Master repository for BigQuery connection tools, scripts, documentation, and best practices for Walmart data projects

---

## 📚 Folder Organization

### 📖 [01-Getting-Started](./01-Getting-Started/)
**Start here for all BigQuery projects**
- Main README and overview documentation
- Quick start guides and tutorials
- BigQuery REST API setup guides
- Complete export instructions
- Live data setup guides
- Real data setup documentation

**Key Files:**
- `README.md` - Main BigQuery integration overview
- `BIGQUERY_REST_SETUP.md` - REST API configuration
- `COMPLETE_BIGQUERY_EXPORT.md` - Data export guide
- `LIVE_DATA_SETUP_INSTRUCTIONS.md` - Live data connection setup
- `REAL_DATA_SETUP.md` - Production data access guide
- `GCLOUD_INSTALLATION_GUIDE.md` - Google Cloud SDK installation

---

### 🔐 [02-Authentication](./02-Authentication/)
**Authentication & connection setup**
- Google Cloud SDK installation scripts
- Authentication configuration tools
- Direct BigQuery connection scripts

**Key Files:**
- `install_gcloud.ps1` - Automated gcloud SDK installation
- `setup_gcloud_auth.ps1` - Authentication setup wizard
- `connect_direct_bigquery.ps1` - Direct PowerShell connection

---

### 📊 [03-Data-Access](./03-Data-Access/)
**Core data access Python modules**
- BigQuery connection services
- Data fetching and export tools
- REST API services

**Key Files:**
- `connect_bigquery.py` - Primary Python BigQuery connector
- `bigquery_service.py` - Service wrapper for BigQuery operations
- `bigquery_rest_service.py` - REST API service layer
- `fetch_live_data.py` - Live data fetching utilities
- `export_real_bigquery_data.py` - Production data export tools

---

### 🎯 [04-AMP-Specific](./04-AMP-Specific/)
**AMP (Application Activity Management Plan) project files**
- Complete AMP BigQuery integration SQL
- AMP data processing scripts
- Tableau integration for AMP data
- Trigger generators for automated data pipelines
- Monitoring dashboards

**Key Files:**
- `amp_bigquery_complete_integration.py` - Generates complete BigQuery integration SQL
- `amp_bigquery_enhanced_multisource_system_20251028_080418.sql` - Latest AMP BigQuery system
- `amp_bigquery_trigger_generator.py` - Creates automated data pipeline triggers
- `amp_bigquery_tableau_integration.py` - Tableau integration for AMP data
- `amp_enhanced_monitoring_dashboard_20251028_075101.sql` - AMP monitoring dashboard
- `csv_bigquery_comparison.py` - Compare CSV data with BigQuery results

---

### 🚀 [05-Deployment](./05-Deployment/)
**Deployment automation & orchestration**
- Phase-based deployment scripts
- Complete system deployment automation
- Live data setup automation
- Data export automation

**Key Files:**
- `deploy_bigquery_phase1.ps1` - Phase 1 deployment (foundation)
- `deploy_bigquery_complete.ps1` - Complete BigQuery deployment
- `deploy_amp_trigger_20251028_072802.sh` - AMP trigger deployment
- `deploy_enhanced_multisource_trigger_20251028_080418.sh` - Enhanced trigger deployment
- `setup_live_data.ps1` - Live data connection automation
- `export-complete-data.ps1` - Complete data export automation

---

### ☁️ [06-GCP-Setup](./06-GCP-Setup/)
**Google Cloud Platform project setup & configuration**
- Comprehensive GCP project setup guides
- Walmart-specific GCP processes (2025)
- IAM and security configuration
- Network setup and VPC configuration
- Cost management and monitoring
- Collaboration guides and checklists

**Key Documentation:**
- `NEXT_STEPS.md` - 📋 START HERE: 7-phase implementation roadmap
- `walmart-gcp-process-2025.md` - 🆕 Current Walmart GCP Process (April 2025)
- `gcp-project-setup-checklist.md` - Complete setup checklist
- `bigquery-iam-guide.md` - BigQuery IAM and access control
- `store-support-config.md` - Store Support project configuration template
- `allen-collaboration-checklist.md` - Quick action plan for peer collaboration
- `peer-collaboration-guide.md` - Transitioning from shared to independent project
- `security-compliance.md` - Security and compliance requirements
- `monitoring-logging.md` - Monitoring and logging setup
- `cost-management.md` - Cost management and budgeting
- `network-setup.md` - Network configuration and VPC setup
- `prerequisites.md` - Required prerequisites and access
- `templates/` - Configuration templates and Terraform scripts

**Walmart 2025 GCP Process (5 Steps):**
1. **AD Group Creation** (ServiceNow, 1-48 hours)
2. **BFD Managed Services** (AFAAS/DPAAS setup)
3. **GCP Client Project** (YAML PR to gcp_project_definitions)
4. **Service Account Management** (Auto-created)
5. **Secret Generation** (JSON keys for applications)

---

### 💡 [07-Examples](./07-Examples/)
**Example data, test scripts, and reference implementations**
- Sample data files (CSV, JSON)
- Test scripts and validation tools
- Tableau schema extractors
- Reference data examples

**Key Files:**
- `Test-BigQuery.ps1` - PowerShell connection testing
- `real-amp-data.csv` - Real AMP data example
- `sample-real-data.csv` - Sample dataset for testing
- `live_amp_data.json` - Live AMP data JSON export
- `tableau_schema_extractor.py` - Extract Tableau flow schemas
- `tableau_schema_extracted.json` - Extracted schema reference
- `bigquery-complete-export.json` - Complete export example
- `bigquery-export.json` - Standard export example

---

## 🎯 Quick Start Guide

### For New BigQuery Projects

1. **📋 Start with GCP Setup**: Review `06-GCP-Setup/NEXT_STEPS.md` for the 7-phase implementation roadmap
2. **📚 Read Documentation**: Check `01-Getting-Started/README.md` for BigQuery-specific guidance
3. **🔐 Setup Authentication**: Follow `02-Authentication/install_gcloud.ps1` to install Google Cloud SDK
4. **📊 Access Data**: Use scripts in `03-Data-Access/` to connect to BigQuery
5. **🚀 Deploy**: Use deployment scripts in `05-Deployment/` for automation
6. **💡 Reference Examples**: Check `07-Examples/` for sample implementations

### For AMP-Specific Projects

1. Follow the general Quick Start above
2. Reference `04-AMP-Specific/` for AMP-specific SQL, scripts, and integrations
3. Use `amp_bigquery_enhanced_multisource_system_20251028_080418.sql` for the latest AMP system
4. Deploy using `05-Deployment/deploy_bigquery_complete.ps1`

---

## 🔧 Common Use Cases

### **Setting Up a New GCP Project**
→ Go to `06-GCP-Setup/NEXT_STEPS.md`

### **Connecting to BigQuery from Python**
→ Use `03-Data-Access/connect_bigquery.py`

### **Installing Google Cloud SDK**
→ Run `02-Authentication/install_gcloud.ps1`

### **Exporting BigQuery Data**
→ Use `03-Data-Access/export_real_bigquery_data.py`

### **Deploying AMP System**
→ Use `05-Deployment/deploy_bigquery_complete.ps1`

### **Testing BigQuery Connection**
→ Run `07-Examples/Test-BigQuery.ps1`

### **Setting Up Collaboration with Peers**
→ See `06-GCP-Setup/peer-collaboration-guide.md`

---

## 📊 Key Data Sources

### Walmart AMP Data
- **Table**: `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
- **Purpose**: Published AMP titles for store associates
- **Access**: Read-only via authenticated Google Cloud credentials
- **Dataset Size**: 75+ published titles per fiscal week

---

## 🔑 Best Practices

### Authentication
- Always use service accounts for automated processes
- Store credentials securely (never commit to Git)
- Rotate service account keys regularly
- Use least-privilege IAM roles

### Data Access
- Query only the data you need (avoid `SELECT *`)
- Use partitioned tables when possible
- Cache frequently accessed data
- Monitor query costs in GCP Console

### Deployment
- Test in development environment first
- Use phase-based deployment approach
- Document all configuration changes
- Monitor deployments for errors

### Cost Management
- Set up budget alerts
- Use query cost estimates before running
- Leverage BigQuery free tier
- Archive old data to Cloud Storage

---

## 📞 Support & Collaboration

### Internal Resources
- **Walmart Cloud Infrastructure Team** - For GCP project setup and access
- **Allen Still** - Peer collaboration for Store Support projects
- **BFD Managed Services** - For AFAAS/DPAAS setup

### Documentation
- All guides in `01-Getting-Started/` and `06-GCP-Setup/`
- Collaboration guides for working with peers
- Walmart-specific processes documented for 2025

---

## 🔄 Maintenance & Updates

This folder is the **central hub for all BigQuery work**. When working on any BigQuery project:

1. ✅ **Reference this folder first** for existing tools and patterns
2. ✅ **Update documentation** when you create new scripts or processes
3. ✅ **Add new examples** to `07-Examples/` for future reference
4. ✅ **Document lessons learned** in relevant README files
5. ✅ **Keep GCP setup guides current** with Walmart's latest processes

---

## 📝 Version History

- **November 24, 2025** - Consolidated and reorganized BigQuery folder structure
  - Created logical folder hierarchy (01-07)
  - Separated AMP-specific files
  - Consolidated GCP setup documentation
  - Removed duplicate nested folders
  - Created comprehensive master README

---

**💡 Remember:** This folder serves ALL BigQuery projects. Keep it organized, well-documented, and up-to-date for the entire team!
