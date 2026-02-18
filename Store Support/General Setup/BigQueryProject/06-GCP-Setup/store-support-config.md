# Store Support GCP Project Configuration Template

## Project Specification

### Official Project Details
- **Project Name**: Store Support
- **Project ID**: `wmt-storesupport-prod`
- **Team**: Walmart Home Office Store Support
- **Purpose**: Enable software and product development for Walmart store support teams

---

## YAML Configuration Template

### File: `wmt-storesupport-prod.yaml`

```yaml
# Store Support GCP Project Configuration
# File: wmt-storesupport-prod.yaml
# Location: gcp_project_definitions/organizations/walmart.com/[store-operations]/prod/[support-services]/

project_name: "wmt-storesupport-prod"
billing_account: "[STORE-SUPPORT-BILLING-ACCOUNT]"  # To be filled with actual billing account
organization_id: "123456789012"  # Walmart organization ID

# Organizational hierarchy - adapt based on Store Support's department structure
organization_path: "organizations/walmart.com/store-operations/prod/support-services/"

# Project labels for governance and cost tracking
labels:
  cost-center: "CC-STORESUPPORT-001"     # Store Support cost center
  business-unit: "store-operations"       # Store operations business unit
  team: "store-support"                   # Store Support team
  environment: "production"               # Production environment
  purpose: "software-product-development" # Development enablement
  created-by: "automated-pipeline"        # Creation method
  template-source: "allen-still-project"  # Source template reference

# Service accounts for Store Support operations
service_accounts:
  - name: "storesupport-etl-sa"
    display_name: "Store Support ETL Service Account"
    description: "Service account for Store Support data processing and ETL operations"
    roles:
      - "roles/bigquery.dataEditor"
      - "roles/storage.objectAdmin"
      - "roles/dataproc.worker"
      - "roles/composer.worker"  # If using AFAAS
  
  - name: "storesupport-app-sa"  
    display_name: "Store Support Application Service Account"
    description: "Service account for Store Support applications and services"
    roles:
      - "roles/bigquery.dataViewer"
      - "roles/storage.objectViewer"
      - "roles/cloudsql.client"
      - "roles/monitoring.metricWriter"
  
  - name: "storesupport-analytics-sa"
    display_name: "Store Support Analytics Service Account"  
    description: "Service account for Store Support analytics and reporting"
    roles:
      - "roles/bigquery.dataViewer"
      - "roles/storage.objectViewer"
      - "roles/bigquery.jobUser"

# AD Groups for Store Support team access management
ad_groups:
  - name: "gcp-storesupport-prod-admin"
    role: "roles/owner"
    description: "Store Support administrators with full project access"
    members: []  # Populated via AD sync
    
  - name: "gcp-storesupport-prod-dev"
    role: "roles/editor"
    description: "Store Support developers with development access"
    members: []  # Populated via AD sync
    
  - name: "gcp-storesupport-prod-analyst"
    role: "roles/bigquery.user"
    description: "Store Support analysts with BigQuery access"
    members: []  # Populated via AD sync

# APIs required for Store Support operations
enabled_apis:
  - "compute.googleapis.com"              # Compute resources
  - "bigquery.googleapis.com"             # Data analytics
  - "storage.googleapis.com"              # Cloud Storage
  - "cloudsql.googleapis.com"             # Managed databases
  - "dataproc.googleapis.com"             # Big data processing
  - "composer.googleapis.com"             # Workflow orchestration (AFAAS)
  - "monitoring.googleapis.com"           # Performance monitoring
  - "logging.googleapis.com"              # Centralized logging
  - "iam.googleapis.com"                  # Identity and access management
  - "cloudresourcemanager.googleapis.com" # Resource management
  - "secretmanager.googleapis.com"        # Secret management
  - "cloudfunctions.googleapis.com"       # Serverless functions
  - "run.googleapis.com"                  # Container runtime

# Network and security configuration
network_config:
  vpc_name: "storesupport-vpc"
  subnets:
    - name: "storesupport-app-subnet"
      cidr: "10.10.0.0/24"
      region: "us-central1"
    - name: "storesupport-data-subnet"  
      cidr: "10.10.1.0/24"
      region: "us-central1"

# Budget and cost controls
budget_config:
  monthly_limit: 5000  # $5,000 monthly budget
  alerts:
    - threshold: 0.5   # 50% alert
    - threshold: 0.8   # 80% alert  
    - threshold: 1.0   # 100% alert
```

---

## AD Groups Creation Plan

### Required ServiceNow Requests

#### 1. Admin Group
```
Group Name: gcp-storesupport-prod-admin
Domain: HomeOffice
Purpose: Administrative access for Store Support GCP project
Members: Store Support team leads and senior engineers
Data Classification: Internal/Confidential (depending on data access)
```

#### 2. Developer Group  
```
Group Name: gcp-storesupport-prod-dev
Domain: HomeOffice
Purpose: Development access for Store Support GCP project
Members: Store Support developers and engineers
Data Classification: Internal
```

#### 3. Analyst Group
```
Group Name: gcp-storesupport-prod-analyst
Domain: HomeOffice  
Purpose: Analytics and BigQuery access for Store Support
Members: Store Support analysts and business users
Data Classification: Internal
```

### Specialized Groups (Optional)
```
# If needed based on Allen's pattern:
gcp-storesupport-bq-users     # BigQuery specific access
gcp-storesupport-storage-users # Cloud Storage specific access
gcp-storesupport-readonly      # Read-only access for stakeholders
```

---

## BigQuery Dataset Structure

### Proposed Store Support Datasets
```
# Following Walmart naming conventions:
STORE_SUPPORT_TABLES  → WRITER access → gcp-storesupport-prod-dev
STORE_SUPPORT_VM      → READER access → gcp-storesupport-prod-analyst  
STORE_SUPPORT_SECURE  → READER access → gcp-storesupport-prod-admin

# Additional datasets based on Store Support functions:
STORE_OPERATIONS_VM   → READER access → gcp-storesupport-prod-analyst
SUPPORT_METRICS_VM    → READER access → gcp-storesupport-prod-analyst
```

---

## Integration with Store Support Operations

### Use Cases for Store Support GCP Project
- **Store Performance Analytics**: BigQuery datasets for store metrics and KPIs
- **Support Ticket Analysis**: Data processing for support request patterns
- **Operational Reporting**: Dashboards and reports for store operations
- **Predictive Analytics**: Machine learning for support optimization
- **Data Integration**: ETL pipelines for store systems integration

### Applications and Workloads
- **Dashboard Applications**: Real-time store support dashboards
- **Analytics Tools**: Business intelligence and reporting tools
- **API Services**: Microservices for store support functions
- **Batch Processing**: Scheduled data processing and analysis jobs
- **Machine Learning**: Predictive models for store support optimization

---

## Migration Timeline for Store Support

### Phase 1: Setup (Week 1-2)
- [ ] Submit ServiceNow requests for AD groups
- [ ] Adapt Allen's YAML configuration for Store Support
- [ ] Submit PR to gcp_project_definitions repository
- [ ] Wait for cloud enablement team approval

### Phase 2: Configuration (Week 3-4)  
- [ ] Verify project creation and service accounts
- [ ] Generate JSON keys for service accounts
- [ ] Configure BigQuery datasets and permissions
- [ ] Set up initial monitoring and logging

### Phase 3: Migration (Week 5-6)
- [ ] Migrate applications from Allen's client to Store Support project
- [ ] Test all functionality in new project environment
- [ ] Update documentation and team training materials
- [ ] Validate security controls and compliance

### Phase 4: Production (Week 7)
- [ ] Complete cutover from Allen's project client
- [ ] Clean up old configurations and dependencies  
- [ ] Document lessons learned and best practices
- [ ] Establish ongoing project governance and maintenance

---

## Success Metrics for Store Support Project

### Technical Metrics
- [ ] All Store Support applications successfully migrated
- [ ] BigQuery datasets accessible to appropriate teams
- [ ] Service accounts functioning correctly for all use cases
- [ ] Monitoring and alerting operational
- [ ] Cost tracking aligned with Store Support budget

### Operational Metrics
- [ ] Store Support team trained on new GCP project
- [ ] Documentation complete and accessible
- [ ] Security controls validated and compliant
- [ ] Integration with existing Store Support systems verified
- [ ] Performance meets or exceeds current capabilities

This configuration provides Store Support with a robust, secure, and scalable GCP foundation for software and product development initiatives.