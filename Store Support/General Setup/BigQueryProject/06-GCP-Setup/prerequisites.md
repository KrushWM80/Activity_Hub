# Prerequisites for GCP Project Setup

## Required Access and Permissions

### Google Cloud Platform Access
- [ ] **GCP Organization Admin Role**: Must have `roles/resourcemanager.organizationAdmin`
- [ ] **Billing Account User**: Access to `roles/billing.user` on Walmart billing accounts
- [ ] **Project Creator**: `roles/resourcemanager.projectCreator` permission
- [ ] **Security Admin**: `roles/iam.securityAdmin` for IAM configuration
- [ ] **Network Admin**: `roles/compute.networkAdmin` for VPC setup

### Walmart Internal Systems
- [ ] **ServiceNow Access**: For cloud resource requests and approvals
- [ ] **Active Directory Integration**: Verify Google Workspace sync is configured
- [ ] **VPN Access**: Corporate network access for configuration
- [ ] **Budget System Access**: Access to financial planning systems

## Required Training and Certifications

### Mandatory Training
- [ ] **Walmart Cloud Security Training**: Complete internal security training
- [ ] **GCP Fundamentals**: Complete Google Cloud basics course
- [ ] **Data Classification Training**: Understand Walmart data handling requirements
- [ ] **Incident Response Training**: Know escalation procedures

### Recommended Certifications
- [ ] **Google Cloud Associate Cloud Engineer**: Basic GCP operational knowledge
- [ ] **Google Cloud Professional Cloud Architect**: For complex architecture decisions
- [ ] **Walmart Cloud Governance Certification**: Internal governance processes

## Technical Requirements

### Workstation Setup
- [ ] **gcloud CLI**: Install and configure Google Cloud SDK
- [ ] **kubectl**: Kubernetes command-line tool (if using GKE)
- [ ] **Terraform**: Infrastructure as Code tool (if using IaC)
- [ ] **Git**: Version control system access
- [ ] **VPN Client**: Walmart corporate VPN software

### Network Requirements
- [ ] **Corporate Network Access**: On-site or VPN connection to Walmart network
- [ ] **Internet Access**: Unrestricted access to Google Cloud APIs
- [ ] **DNS Resolution**: Ability to resolve Google Cloud domains
- [ ] **Firewall Rules**: Corporate firewall allows GCP API traffic

## Documentation and Resources

### Required Documentation
- [ ] **Network Architecture Diagrams**: Current Walmart network topology
- [ ] **Security Policies**: Walmart cloud security standards
- [ ] **Compliance Requirements**: Applicable regulatory frameworks
- [ ] **Naming Conventions**: Walmart resource naming standards

### Reference Materials
- [ ] **Walmart Cloud Playbook**: Internal cloud adoption guidelines
- [ ] **GCP Best Practices**: Google Cloud architecture framework
- [ ] **Security Baseline**: Walmart security configuration templates
- [ ] **Cost Management Policies**: Budget and spending guidelines

## Team Information Requirements

### Development Team Details
- [ ] **Team Roster**: List of all team members requiring access
- [ ] **Roles and Responsibilities**: Define each team member's role
- [ ] **Contact Information**: Email, phone, and Slack channels
- [ ] **Manager Approval**: Supervisor sign-off on project scope

### Project Specifications
- [ ] **Application Type**: Web app, API, data processing, etc.
- [ ] **Data Classification**: Confidential, internal, public
- [ ] **User Base**: Internal users, customers, partners
- [ ] **Performance Requirements**: SLA, throughput, latency needs
- [ ] **Compliance Scope**: PCI, SOX, GDPR, CCPA requirements

## Approval Process

### Required Approvals
- [ ] **IT Security Approval**: Security team review and sign-off
- [ ] **Finance Approval**: Budget allocation and cost center assignment
- [ ] **Architecture Review**: Enterprise architecture team approval
- [ ] **Legal Review**: Data handling and privacy compliance review
- [ ] **Business Sponsor**: Business unit leader approval

### Documentation Checklist
- [ ] **Project Charter**: Business justification and objectives
- [ ] **Risk Assessment**: Security and operational risk analysis
- [ ] **Cost-Benefit Analysis**: ROI and total cost of ownership
- [ ] **Timeline**: Project milestones and delivery dates
- [ ] **Success Criteria**: Measurable project success metrics

## Pre-Setup Validation

### Access Validation
- [ ] **Test GCP Console Access**: Verify login to Google Cloud Console
- [ ] **Billing Account Verification**: Confirm billing account permissions
- [ ] **API Access Test**: Verify ability to enable GCP APIs
- [ ] **Service Account Creation**: Test service account creation permissions

### Tool Configuration
- [ ] **gcloud Configuration**: Set up local gcloud configuration
- [ ] **Authentication Test**: Verify application default credentials
- [ ] **Network Connectivity**: Test connectivity to GCP APIs
- [ ] **CLI Tools**: Verify all required command-line tools are installed

## Emergency Preparedness

### Backup Plans
- [ ] **Alternative Contacts**: Identify backup team members with access
- [ ] **Escalation Procedures**: Document when and how to escalate issues
- [ ] **Recovery Procedures**: Plan for configuration rollback if needed
- [ ] **Support Channels**: Know how to contact Google Cloud support

### Risk Mitigation
- [ ] **Change Management**: Follow Walmart change control processes
- [ ] **Testing Environment**: Set up isolated testing environment first
- [ ] **Rollback Plan**: Prepare rollback procedures for each configuration step
- [ ] **Communication Plan**: Notify stakeholders of setup activities