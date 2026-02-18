# Walmart GCP Project Setup Process (Updated 2025)

**Created by**: Amit Kumar  
**Last Modified**: Apr 13, 2025  
**Source**: Walmart Internal Documentation

This document describes the current procedure for setting up a GCP project along with its related resources, including Active Directory (AD) groups, service accounts, and secrets.

---

## Step 1: Active Directory Group Creation

### Requirements
- **Naming Convention**: Must use `gcp-` prefix for proper GCP synchronization
- **Domain**: Must be created under **HomeOffice** domain
- **Synchronization Time**: Up to **48 hours** for full AD-to-GCP sync

### Process
1. Follow GCP AD group creation documentation
2. Create groups based on project needs:
   - **Development Group**: `gcp-[project]-[env]-dev` (e.g., `gcp-ng-ecm-nprd-dev`)
   - **Admin Group**: `gcp-[project]-[env]-admin` (e.g., `gcp-ng-ecm-nprd-admin`)

### ServiceNow Integration
- **URL**: https://walmartglobal.service-now.com/wm_sp?id=sc_cat_item_guide&table=sc_cat_item&sys_id=222d77a3db8a634832af7f698c9619dc&searchTerm=google%20group
- **Purpose**: Google Group management and service account additions to AD groups

### Example Groups Created
```
Development: gcp-ng-ecm-nprd-dev
Admin: gcp-ng-ecm-nprd-admin
```

---

## Step 2: BFD (Managed) Project Creation

### Managed Services
Walmart provides managed services for common data processing needs:

#### AFAAS (Airflow as a Service)
- **Purpose**: Managed Apache Airflow for workflow orchestration
- **Setup**: Follow internal documentation for AFAAS creation
- **Integration**: Connects with GCP client projects

#### DPAAS (Dataproc as a Service)  
- **Purpose**: Managed Hadoop/Spark clusters
- **Setup**: Follow internal documentation for DPAAS creation
- **Integration**: Provides compute resources for data processing

### Project Details Template
```yaml
# Example project configuration
DPAAS:
  cluster_type: "managed"
  compute_profile: "standard"
  auto_scaling: true

AFAAS:
  workflow_type: "managed"  
  scheduler: "airflow"
  integration: "gcp_native"
```

---

## Step 3: GCP Client Project Setup

### Repository-Based Management
- **Repository**: https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions
- **Process**: Fork → Create YAML → Push → Automated Pipeline

### Project Creation Workflow

#### 1. Fork Repository
```bash
# Fork the central repository
git clone https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions
cd gcp_project_definitions
git checkout -b feature/new-project-[project-name]
```

#### 2. Create YAML Configuration
**File Location**: Must follow proper nesting structure
```
gcp_project_definitions/
└── organizations/
    └── walmart.com/
        └── international/
            └── prod/
                └── finance/
                    └── GGGR/
                        └── ecm/
                            └── [project-name].yaml
```

#### 3. YAML File Structure
```yaml
# File: [project-name].yaml
# Note: project_name and filename must match exactly

project_name: "gcp-ng-ecm-nprd"
billing_account: "012345-67890A-BCDEF1" 
organization_id: "123456789012"

# Project nesting path
organization_path: "organizations/walmart.com/international/prod/finance/GGGR/ecm/"

# Labels for cost tracking and governance
labels:
  cost-center: "CC-FINANCE-001"
  business-unit: "finance"
  team: "ecm"
  environment: "non-production"
  created-by: "automated-pipeline"

# Service accounts (automatically created)
service_accounts:
  - name: "ecm-etl-sa"
    display_name: "ECM ETL Service Account"
    roles:
      - "roles/bigquery.dataEditor"
      - "roles/storage.objectAdmin"
      - "roles/dataproc.worker"
  
  - name: "ecm-app-sa"  
    display_name: "ECM Application Service Account"
    roles:
      - "roles/bigquery.dataViewer"
      - "roles/storage.objectViewer"

# AD Groups integration
ad_groups:
  - name: "gcp-ng-ecm-nprd-dev"
    role: "roles/editor"
    members: []  # Populated via AD sync
    
  - name: "gcp-ng-ecm-nprd-admin"
    role: "roles/owner" 
    members: []  # Populated via AD sync

# APIs to enable
enabled_apis:
  - "compute.googleapis.com"
  - "bigquery.googleapis.com" 
  - "storage.googleapis.com"
  - "dataproc.googleapis.com"
  - "composer.googleapis.com"  # For AFAAS integration
```

#### 4. Validation Requirements
- **File Naming**: YAML filename must exactly match `project_name` field
- **Nesting**: Must follow organizational hierarchy structure
- **Conventions**: Follow Walmart naming conventions for successful validation
- **Review**: PR requires approval from Cloud Enablement team

#### 5. Automated Pipeline
```mermaid
graph LR
    A[Push to origin/main] --> B[Automated Pipeline Triggered]
    B --> C[YAML Validation]
    C --> D[Project Creation]
    D --> E[Service Account Creation]
    E --> F[IAM Role Assignment]
    F --> G[API Enablement]
    G --> H[Notification Sent]
```

---

## Step 4: Service Account Creation (Automated)

### Automatic Creation Process
- **Trigger**: Part of GCP project creation pipeline
- **Definition**: Specified in YAML `service_accounts` field
- **Timing**: Created immediately after project initialization

### Service Account Naming Convention
```
Format: <svc-acc-name>@<groupName(prefixed with gcp-)>.iam.gserviceaccount.com

Examples:
ecm-etl-sa@gcp-ng-ecm-nprd.iam.gserviceaccount.com
ecm-app-sa@gcp-ng-ecm-nprd.iam.gserviceaccount.com
```

### Cross-Team Access
- **Purpose**: Service accounts can be added to other teams' AD groups
- **Process**: Submit ServiceNow request for Google Group management
- **Use Case**: Grant access to shared resources across teams

### ServiceNow Request Process
1. **Access ServiceNow**: Use provided Google Group management link
2. **Select Action**: "Add member to Google Group"
3. **Specify Details**:
   - Service account email
   - Target AD group
   - Business justification
4. **Approval**: Follow standard approval workflow

---

## Step 5: Secret Generation and Application Integration

### JSON Key File Generation

#### Process
1. **Navigate**: GCP Console → IAM & Admin → Service Accounts
2. **Select**: Target service account
3. **Action**: Keys → Add Key → Create New Key
4. **Format**: JSON (recommended)
5. **Download**: Securely store the generated JSON file

#### Key File Structure
```json
{
  "type": "service_account",
  "project_id": "gcp-ng-ecm-nprd",
  "private_key_id": "key-id-12345",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "ecm-etl-sa@gcp-ng-ecm-nprd.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ecm-etl-sa%40gcp-ng-ecm-nprd.iam.gserviceaccount.com"
}
```

### Application Integration

#### Security Best Practices
1. **Secure Storage**: Store JSON keys in secure secret management systems
2. **Environment Variables**: Reference via environment variables, not hardcoded paths
3. **Rotation**: Implement regular key rotation (90-day maximum)
4. **Access Control**: Limit access to key files on a need-to-know basis

#### Integration Examples

**Python Application**:
```python
import os
from google.cloud import bigquery
from google.oauth2 import service_account

# Load credentials from secure location
credentials = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']
)

# Initialize client
client = bigquery.Client(credentials=credentials, project='gcp-ng-ecm-nprd')
```

**Docker Container**:
```dockerfile
# Dockerfile
COPY service-account-key.json /secrets/
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json

# Application startup
CMD ["python", "app.py"]
```

**Kubernetes Deployment**:
```yaml
# Secret containing service account key
apiVersion: v1
kind: Secret
metadata:
  name: gcp-service-account
type: Opaque
data:
  key.json: <base64-encoded-json-key>

---
# Pod using the secret
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    env:
    - name: GOOGLE_APPLICATION_CREDENTIALS
      value: "/var/secrets/google/key.json"
    volumeMounts:
    - name: google-cloud-key
      mountPath: /var/secrets/google
  volumes:
  - name: google-cloud-key
    secret:
      secretName: gcp-service-account
```

---

## Timeline and Dependencies

### Expected Duration
| Step | Duration | Dependencies |
|------|----------|--------------|
| 1. AD Group Creation | 1-48 hours | ServiceNow approval |
| 2. BFD Project Setup | 2-4 hours | AFAAS/DPAAS documentation |
| 3. GCP Client Project | 2-4 hours | Cloud enablement team approval |
| 4. Service Account Creation | Automatic | Step 3 completion |
| 5. Secret Generation | 15 minutes | Step 4 completion |
| **Total End-to-End** | **2-7 days** | All approvals and sync delays |

### Critical Path Items
- **AD Group Sync**: Can take up to 48 hours
- **YAML Validation**: Must pass automated checks
- **PR Approval**: Cloud enablement team review required
- **Service Account Propagation**: Usually within 1 hour

---

## Validation and Testing

### Post-Setup Verification
```bash
# 1. Verify AD group sync
adquery group -A gcp-ng-ecm-nprd-dev

# 2. Check Google Group membership  
gcloud identity groups memberships list --group-email="gcp-ng-ecm-nprd-dev@walmart.com"

# 3. Test service account authentication
gcloud auth activate-service-account --key-file=service-account-key.json
gcloud projects describe gcp-ng-ecm-nprd

# 4. Verify BigQuery access
bq ls --project_id=gcp-ng-ecm-nprd

# 5. Test cross-team resource access (if configured)
gsutil ls gs://shared-team-bucket/
```

### Common Issues and Solutions
| Issue | Symptoms | Resolution |
|-------|----------|------------|
| AD Group not syncing | Group not visible in GCP Console | Wait 48 hours, verify HomeOffice domain |
| YAML validation failure | PR build fails | Check naming convention and nesting |
| Service account creation failed | No SA visible after project creation | Verify YAML syntax in service_accounts section |
| Key generation not working | Cannot create JSON key | Check IAM permissions for key creation |

---

## Integration with Existing Walmart Systems

### AFAAS Integration
- **Airflow DAGs**: Can reference GCP service accounts for authentication
- **Workflow Orchestration**: Connects to GCP resources via service accounts
- **Monitoring**: Integrated with Walmart's workflow monitoring systems

### DPAAS Integration  
- **Data Processing**: Dataproc clusters can use project service accounts
- **Storage Access**: Unified access to GCS buckets and BigQuery datasets
- **Compute Scaling**: Auto-scaling based on project quotas and budgets

### Enterprise Monitoring
- **Cost Tracking**: Automatic integration with Walmart's cost management systems
- **Security Monitoring**: Service account usage tracked in security systems
- **Compliance**: Automated compliance checks for created resources