# GCP Project Setup Checklist for Walmart Development Teams

## Overview
This checklist guides Walmart home office store support teams through setting up Google Cloud Platform (GCP) projects for software and product development teams.

---

## Phase 1: Pre-Setup Requirements ✅

### 1.1 Access and Permissions (2025 Updated Process)
- [ ] **GitHub Enterprise Access**: Access to https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions
- [ ] **ServiceNow Access**: Permissions for Google Group management requests
- [ ] **AFAAS/DPAAS Documentation**: Review managed services documentation
- [ ] **Organizational Nesting Knowledge**: Understand project hierarchy requirements
- [ ] **Cloud Enablement Team Contact**: Identify reviewers for YAML PR approval

### 1.2 Documentation and Approvals (2025 Updated Process)
- [ ] **Business Justification**: Document use case for GCP project
- [ ] **Project Nesting Path**: Determine correct organizational hierarchy
  - Example: `organizations/walmart.com/international/prod/finance/GGGR/ecm/`
- [ ] **Service Requirements**: Identify need for AFAAS and/or DPAAS
- [ ] **AD Group Planning**: Plan development and admin group names
- [ ] **Service Account Requirements**: Define needed service accounts and their roles
- [ ] **Budget Approval**: Secure cost center assignment and spending limits
- [ ] **Compliance Check**: Verify regulatory requirements (PCI, SOX, etc.)

### 1.3 Team Information
- [ ] **Development Team Contacts**: Collect team lead and developer contact information
- [ ] **Project Scope**: Define application type, data classification, and user base
- [ ] **Environment Requirements**: Determine dev, staging, and production needs
- [ ] **Integration Requirements**: Identify existing Walmart systems to integrate with

---

## Phase 2: Active Directory Group Creation (Step 1) 📋

### 2.1 AD Group Creation via ServiceNow
- [ ] **Follow Naming Convention**: Use `gcp-` prefix for all groups
- [ ] **Create Development Group**: `gcp-[project]-[env]-dev` (e.g., `gcp-ng-ecm-nprd-dev`)
- [ ] **Create Admin Group**: `gcp-[project]-[env]-admin` (e.g., `gcp-ng-ecm-nprd-admin`) 
- [ ] **Submit ServiceNow Requests**: Use Google Group management portal
  - URL: https://walmartglobal.service-now.com/wm_sp?id=sc_cat_item_guide&table=sc_cat_item&sys_id=222d77a3db8a634832af7f698c9619dc&searchTerm=google%20group
- [ ] **Ensure HomeOffice Domain**: Critical for GCP synchronization
- [ ] **Wait for Synchronization**: Allow up to 48 hours for AD-to-GCP sync
- [ ] **Validate Group Creation**: Verify groups appear in Google Groups console

### 2.2 BFD Managed Project Creation (Step 2)
- [ ] **Review AFAAS Requirements**: Determine if Airflow as a Service is needed
- [ ] **Review DPAAS Requirements**: Determine if Dataproc as a Service is needed
- [ ] **Follow AFAAS Documentation**: Complete managed Airflow setup if required
- [ ] **Follow DPAAS Documentation**: Complete managed Dataproc setup if required
- [ ] **Document Integration Points**: Record how managed services connect to client project

---

## Phase 3: GCP Client Project Setup (Step 3) 🏗️

### 3.1 Repository Management
- [ ] **Fork gcp_project_definitions**: Clone https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions
- [ ] **Create Feature Branch**: `git checkout -b feature/new-project-[project-name]`
- [ ] **Determine Nesting Path**: Follow organizational hierarchy
  - Example: `gcp_project_definitions/organizations/walmart.com/international/prod/finance/GGGR/ecm/`
- [ ] **Validate Path Structure**: Ensure correct departmental nesting

### 3.2 YAML Configuration Creation
- [ ] **Create Project YAML File**: Filename must match project_name exactly
- [ ] **Define Project Metadata**:
  - `project_name`: Must match YAML filename
  - `billing_account`: Walmart billing account ID
  - `organization_id`: Walmart organization ID
  - `organization_path`: Correct nesting hierarchy
- [ ] **Configure Labels**: Apply Walmart standardized labels
  - `cost-center`, `business-unit`, `team`, `environment`, `created-by`
- [ ] **Define Service Accounts**: Specify required service accounts with roles
- [ ] **Map AD Groups**: Reference created AD groups with appropriate roles
- [ ] **Enable Required APIs**: List all needed GCP APIs

### 3.3 Automated Pipeline Execution  
- [ ] **Submit Pull Request**: Push YAML to origin/main branch
- [ ] **YAML Validation**: Ensure automated validation passes
- [ ] **Cloud Enablement Review**: Wait for team approval
- [ ] **Monitor Pipeline**: Track automated project creation process
- [ ] **Verify Project Creation**: Confirm project appears in GCP Console
- [ ] **Validate Service Accounts**: Check that service accounts were created automatically

---

---

## Phase 4: Service Account Management (Step 4) 🔐

### 4.1 Automated Service Account Creation
- [ ] **Verify Auto-Creation**: Confirm service accounts created via pipeline
- [ ] **Validate Naming Convention**: Check format `<svc-acc-name>@<groupName>.iam.gserviceaccount.com`
- [ ] **Review Assigned Roles**: Verify roles match YAML specification
- [ ] **Document Service Account Purpose**: Record intended use for each service account

### 4.2 Cross-Team Access Management
- [ ] **Identify Cross-Team Needs**: Determine if service accounts need access to other teams' resources
- [ ] **Submit ServiceNow Requests**: Use Google Group management portal to add service accounts to other AD groups
- [ ] **Provide Business Justification**: Document why cross-team access is needed
- [ ] **Track Approval Status**: Monitor ServiceNow ticket progress

---

## Phase 5: Secret Generation and Application Integration (Step 5) 🔑

### 5.1 JSON Key File Generation
- [ ] **Access Service Account Console**: Navigate to IAM & Admin → Service Accounts
- [ ] **Generate JSON Keys**: Create new keys for each service account
- [ ] **Download Securely**: Store JSON files in secure location immediately
- [ ] **Document Key Purpose**: Record which applications will use each key

### 5.2 Secure Integration Practices
- [ ] **Implement Secret Management**: Store keys in enterprise secret management system
- [ ] **Configure Environment Variables**: Reference keys via environment variables
- [ ] **Set Up Key Rotation**: Implement 90-day maximum rotation schedule
- [ ] **Apply Access Controls**: Limit key file access on need-to-know basis

### 5.3 Application Integration
- [ ] **Update Application Code**: Integrate service account authentication
- [ ] **Test Authentication**: Verify applications can authenticate with GCP
- [ ] **Configure Container Deployments**: Set up secure key mounting for containers
- [ ] **Document Integration**: Record how keys are used in each application

### 3.3 Security Policies
- [ ] **Enable 2FA**: Require multi-factor authentication
- [ ] **Set Session Timeouts**: Configure appropriate timeout periods
- [ ] **IP Allowlisting**: Restrict access to Walmart office networks
- [ ] **Audit Logging**: Enable admin activity and data access logs

---

## Phase 4: Network Configuration 🌐

### 4.1 VPC Setup
- [ ] **Create Custom VPC**: Design network architecture
- [ ] **Define Subnets**: Create subnets for different tiers
  - Web tier subnet
  - Application tier subnet
  - Database tier subnet
- [ ] **Configure IP Ranges**: Use RFC 1918 private ranges
- [ ] **Set Up Regional Distribution**: Deploy across multiple zones

### 4.2 Security Groups and Firewall Rules
- [ ] **Create Firewall Rules**:
  - Allow HTTP/HTTPS from load balancers
  - Allow SSH from bastion hosts only
  - Deny all other inbound traffic by default
- [ ] **Set Up Network Tags**: Tag instances for firewall targeting
- [ ] **Configure Health Check Rules**: Allow health check traffic

### 4.3 Connectivity
- [ ] **VPN Setup**: Configure site-to-site VPN to Walmart network
- [ ] **Private Google Access**: Enable for private subnet instances
- [ ] **Cloud NAT**: Set up for outbound internet access
- [ ] **DNS Configuration**: Set up private DNS zones

---

## Phase 5: Security and Compliance 🛡️

### 5.1 Data Protection
- [ ] **Enable Encryption at Rest**: Configure customer-managed encryption keys (CMEK)
- [ ] **Set Up Key Management**: Create and manage encryption keys in Cloud KMS
- [ ] **Data Classification**: Label resources based on data sensitivity
- [ ] **Backup Encryption**: Ensure backups are encrypted

### 5.2 Security Monitoring
- [ ] **Enable Security Command Center**: Configure security insights
- [ ] **Set Up Vulnerability Scanning**: Enable container and VM scanning
- [ ] **Configure Binary Authorization**: Set up container image policies
- [ ] **Enable Web Security Scanner**: For application security testing

### 5.3 Compliance Controls
- [ ] **PCI DSS Compliance** (if applicable):
  - Network segmentation
  - Access controls
  - Logging requirements
- [ ] **SOX Compliance**:
  - Change management controls
  - Access reviews
  - Audit trails
- [ ] **Data Residency**: Ensure data stays in approved regions

---

## Phase 6: Monitoring and Logging 📊

### 6.1 Cloud Monitoring Setup
- [ ] **Create Monitoring Workspace**: Set up centralized monitoring
- [ ] **Configure Alerting Policies**:
  - High CPU utilization
  - Memory usage thresholds
  - Disk space warnings
  - Application error rates
- [ ] **Set Up Dashboards**: Create operational dashboards
- [ ] **Configure Notification Channels**: Set up email, SMS, and Slack alerts

### 6.2 Logging Configuration
- [ ] **Enable Audit Logs**: Admin activity, data access, and system events
- [ ] **Set Up Log Retention**: Configure retention policies per Walmart requirements
- [ ] **Create Log Sinks**: Export logs to BigQuery or Cloud Storage for analysis
- [ ] **Configure Log-Based Metrics**: Create custom metrics from log data

### 6.3 Performance Monitoring
- [ ] **Enable Application Performance Monitoring**: Set up APM tools
- [ ] **Configure Uptime Checks**: Monitor application availability
- [ ] **Set Up SLI/SLO Monitoring**: Define and track service level objectives

---

## Phase 7: Cost Management 💰

### 7.1 Budget Controls
- [ ] **Set Up Budgets**: Create project-level budgets with alerts
- [ ] **Configure Billing Alerts**: Set up notifications at 50%, 80%, and 100% of budget
- [ ] **Apply Quota Limits**: Set resource quotas to prevent overspend
- [ ] **Enable Committed Use Discounts**: Apply for predictable workloads

### 7.2 Cost Optimization
- [ ] **Right-size Resources**: Use appropriate machine types
- [ ] **Configure Auto-scaling**: Set up horizontal pod autoscaling
- [ ] **Schedule Resources**: Shut down dev/test resources outside business hours
- [ ] **Enable Preemptible Instances**: Use for non-critical workloads

### 7.3 Cost Tracking
- [ ] **Set Up Cost Allocation**: Use labels for department/team tracking
- [ ] **Configure Export to BigQuery**: Enable detailed billing export
- [ ] **Create Cost Reports**: Set up regular cost analysis reports

---

## Phase 7.5: BigQuery Setup (Walmart Specific) 📊

### 7.5.1 BigQuery Access Rights and Roles (Step 2)
- [ ] **Reference gcp_project_definitions Repository**: Review https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions.git
- [ ] **Configure Project-Level IAM Roles**:
  - `bigquery.metadataViewer`: Schema browsing (EDW projects)
  - `bigquery.user` + `bigquery.jobUser`: Basic query access
  - `bigquery.dataViewer`: Read-only application access
  - `bigquery.dataEditor`: ETL and data processing
  - `bigquery.admin`: Warehouse Solutions DBA only
- [ ] **Configure Dataset-Level Controls**:
  - `READER`: Dataset-level bigquery.dataViewer
  - `WRITER`: Dataset-level bigquery.dataEditor  
  - `OWNER`: Dataset-level bigquery.dataOwner (DBA only)
- [ ] **Create Domain Datasets**:
  - `<DOMAIN>_TABLES`: WRITER access for ETL processes
  - `<DOMAIN>_VM`: READER access for all authorized users
  - `<DOMAIN>_SECURE`: READER access for specific users only

### 7.5.2 Google Groups and Dataset Permissions
- [ ] **Map Groups to IAM Roles**:
  - Writer groups → `bigquery.dataEditor` (project or dataset level)
  - Reader groups → `bigquery.dataViewer` (project or dataset level)  
  - Secure groups → Dataset READER control for _SECURE datasets
- [ ] **Apply Permission Inheritance Rules**:
  - Tables/Views inherit from parent dataset
  - Union of permissions from project IAM + dataset controls + group membership
- [ ] **Handle Complex Access Patterns**:
  - Create multiple datasets per domain for different access levels
  - Use separate datasets when object-level permissions needed (e.g., HR payroll vs benefits)
- [ ] **Update Dataset Permissions**: Use GUI "Share Dataset" or `bq update` command
- [ ] **Validate Effective Permissions**: Test combined project + dataset access

### 7.5.3 Special Access Groups
- [ ] **Metadata Viewer**: `gcp-edw-metadata-viewer` for DDL access without data viewing
- [ ] **Storage API Access**: `gcp-edw-bq-storage-api-user` for BigQuery Storage API usage
- [ ] **Domain Reader Groups**: Create broad access groups (e.g., `gcp-dev-us-walmart-reader`)

### 7.5.4 ETL and Integration Setup
- [ ] **DataStage Setup**: Configure DataStage DS ver 11.7.1 (supports BQ)
- [ ] **Mainframe Integration**: Set up JCL changes for mainframe connectivity
- [ ] **API Integration**: Configure API access for data ingestion
- [ ] **Create Stats and Log Tables**: Set up monitoring tables for every project

### 7.5.5 Cross-Reference and Documentation
- [ ] **Update Master List**: Maintain Google Group and Dataset Cross Reference Master List
- [ ] **Document Access Patterns**: Record which groups access which datasets
- [ ] **Document IAM Considerations**:
  - Note: Cannot manage permissions at object (table/view) level
  - Multiple datasets required for complex access patterns (e.g., HR roles)
  - Dataset WRITER access enables modifying object structure
- [ ] **Validate Cross-Environment**: Compare dev and prod dataset permissions
- [ ] **Reference Documentation**: Update links to https://cloud.google.com/bigquery/docs/access-control

---

## Phase 8: Development Environment Setup 🛠️

### 8.1 CI/CD Pipeline
- [ ] **Set Up Cloud Build**: Configure build triggers and workflows
- [ ] **Container Registry**: Set up private container registry
- [ ] **Deployment Automation**: Configure automated deployments
- [ ] **Environment Promotion**: Set up dev → staging → prod pipeline

### 8.2 Development Tools
- [ ] **Cloud Source Repositories**: Set up Git repositories
- [ ] **Cloud Code Integration**: Configure IDE extensions
- [ ] **Debugging Tools**: Set up Cloud Debugger and Profiler
- [ ] **Testing Infrastructure**: Configure test environments

### 8.3 Database Setup
- [ ] **Cloud SQL Configuration**: Set up managed databases
- [ ] **Backup Strategy**: Configure automated backups
- [ ] **High Availability**: Set up regional persistence
- [ ] **Security**: Configure private IP and encryption

---

## Phase 9: Documentation and Handoff 📝

### 9.1 Documentation Creation
- [ ] **Architecture Diagrams**: Create system architecture documentation
- [ ] **Runbooks**: Document operational procedures
- [ ] **Troubleshooting Guides**: Create problem resolution guides
- [ ] **Access Procedures**: Document how to request and manage access

### 9.2 Knowledge Transfer
- [ ] **Team Training**: Conduct GCP training sessions
- [ ] **Admin Training**: Train team leads on administrative tasks
- [ ] **Emergency Procedures**: Document incident response procedures
- [ ] **Support Contacts**: Provide escalation paths and contact information

### 9.3 Project Handoff
- [ ] **Access Review**: Verify all team members have appropriate access
- [ ] **Monitoring Validation**: Confirm all monitoring and alerts are working
- [ ] **Security Validation**: Verify security controls are in place
- [ ] **Final Documentation**: Complete all project documentation

---

## Phase 10: Post-Setup Tasks and Governance 🔄

### 10.1 Ongoing Maintenance
- [ ] **Monthly Access Reviews**: Review and audit user access
- [ ] **Quarterly Security Reviews**: Assess security posture
- [ ] **Cost Reviews**: Monthly budget and spend analysis
- [ ] **Compliance Audits**: Regular compliance assessments

### 10.2 Optimization
- [ ] **Performance Reviews**: Quarterly performance assessments
- [ ] **Cost Optimization**: Ongoing resource optimization
- [ ] **Security Updates**: Regular security patch management
- [ ] **Capacity Planning**: Proactive scaling planning

---

## Emergency Contacts and Escalation

### Walmart Internal Contacts
- **Cloud Infrastructure Team**: [Insert contact information]
- **Security Team**: [Insert contact information]
- **Network Operations**: [Insert contact information]
- **Compliance Team**: [Insert contact information]

### Google Cloud Support
- **Support Case Portal**: Google Cloud Console → Support
- **Emergency Contact**: [Insert Walmart's Google enterprise support contact]

---

## Validation Checklist

Before considering the setup complete, verify:
- [ ] All team members can access required resources
- [ ] Applications deploy successfully through CI/CD pipeline
- [ ] Monitoring and alerting are functioning correctly
- [ ] Security controls are properly configured
- [ ] Cost controls and budgets are in place
- [ ] Documentation is complete and accessible
- [ ] Backup and disaster recovery procedures are tested

---

**Document Version**: 1.0  
**Last Updated**: October 24, 2025  
**Next Review**: November 24, 2025  
**Owner**: Walmart Cloud Infrastructure Team