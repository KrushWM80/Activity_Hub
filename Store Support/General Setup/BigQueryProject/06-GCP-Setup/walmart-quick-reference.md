# Walmart GCP Setup Quick Reference Card

## 🚀 Essential Steps (In Order)

### Step 1: ServiceNow Requests
```
URL: wmlink/adgroup
Action: Create Active Directory Group
Groups needed:
├── gcp-[app]-admin
├── gcp-[app]-writer  
├── gcp-[app]-reader
└── gcp-[app]-user
```

### Step 2: YAML Pull Request
```
Repository: gcp_project_definitions
File: [project-name].yaml
Reviewers: @cloud-gov-network
Wait for: Auto-creation of project + service accounts
```

### Step 3: BigQuery Dataset Setup
```
Datasets to create:
├── [PROJECT]_TABLES (writer access)
├── [PROJECT]_VM (reader access)
└── [PROJECT]_SECURE (secure access)
```

### Step 4: Assign Permissions
```bash
# Add groups to datasets
bq update --dataset \
  --add_binding role=roles/bigquery.dataEditor,members=group:gcp-prod-[dataset]-writer \
  wmt-edw-prod:[DATASET]_TABLES

bq update --dataset \
  --add_binding role=roles/bigquery.dataViewer,members=group:gcp-prod-[dataset]-reader \
  wmt-edw-prod:[DATASET]_VM
```

---

## ⚡ Critical Commands

### Validate Google Group Creation
```bash
# Check if AD group exists
adquery group -A gcp-[group-name]

# View Google Groups
https://groups.google.com/a/walmart.com/
```

### BigQuery Validation
```bash
# Compare dev vs prod permissions
bq show wmt-edw-dev:[DATASET];bq show wmt-edw-prod:[DATASET]

# List all datasets
bq ls wmt-edw-prod
```

### Service Account Key Generation
```bash
# Generate key file for service account
gcloud iam service-accounts keys create keyfile.json \
  --iam-account=[SA-NAME]@[PROJECT].iam.gserviceaccount.com
```

---

## 📋 Required Information

### For ServiceNow AD Group Request
- **On Behalf Of**: Yourself (or MJSTUKE for BQ Admin)
- **Domain**: HomeOffice  
- **Group Name**: Must start with `gcp-`
- **Owners**: Team manager + senior member
- **Data Classification**: Highly Sensitive (for secure groups)
- **Business Justification**: "[ROLE] access for [DATASET] in wmt-edw-[ENV]"

### For YAML PR
- **Project Name**: Follow naming convention
- **Billing Account**: Walmart billing account ID
- **Service Accounts**: List required SAs
- **Google Groups**: Reference created groups
- **Labels**: cost-center, business-unit, team, environment

---

## 🔍 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Google Group not syncing | Verify AD group exists with `adquery` |
| ServiceNow request rejected | Check data classification matches use case |
| YAML PR not approved | Ensure all groups exist and SSP approved |
| BigQuery access denied | Verify user in correct Google Group |
| Service account key expired | Regenerate key with 90-day rotation |

---

## 📞 Key Contacts

| Team | Contact | Purpose |
|------|---------|---------|
| Cloud Enablement | @cloud-gov-network | YAML PR approval |
| BigQuery Admin | j5mcclu, mjstuke | Dataset management |
| ServiceNow | wmlink/adgroup | AD Group creation |
| Security | Internal SOC | SSP amendments |

---

## 📊 BigQuery IAM Mapping (Step 2)

### Project-Level IAM Roles
| IAM Role | Scope | Use Case |
|----------|-------|----------|
| `bigquery.metadataViewer` | EDW Projects | Schema browsing only |
| `bigquery.user` + `bigquery.jobUser` | App Projects | Basic query execution |
| `bigquery.dataViewer` | App Projects | Read-only application access |
| `bigquery.dataEditor` | App Projects | ETL and data processing |
| `bigquery.admin` | DBA Only | Full administrative control |

### Dataset-Level Controls
| Group Suffix | Dataset Access | Dataset Role | Use Case |
|--------------|----------------|--------------|----------|
| `-writer` | `*_TABLES`, `*_VM` | WRITER | ETL, data loading |
| `-secure` | `*_SECURE`, `*_VM` | READER | Sensitive data access |
| `-reader` | `*_VM` (multiple) | READER | Business analytics |

### Access Pattern Examples
```
US_WM_MB_TABLES → WRITER → gcp-prod-us-wm-mb-writer
US_WM_MB_VM     → READER → gcp-prod-us-walmart-reader  
US_WM_MB_SECURE → READER → gcp-prod-us-wm-mb-secure
```

---

## 🕒 Typical Timeline
- **AD Group Creation**: 24-48 hours
- **Google Group Sync**: 1-4 hours after AD creation
- **YAML PR Review**: 1-3 business days
- **Project Creation**: Automatic after PR approval
- **End-to-End**: 3-7 business days

---

*💡 Tip: Create a spreadsheet to track multiple group requests - it gets overwhelming quickly!*