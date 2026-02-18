# Walmart-Specific GCP Setup Process

## ServiceNow Integration

### Creating Google Groups via ServiceNow
Walmart uses ServiceNow for Active Directory group creation, which automatically syncs to Google Groups.

#### Process Steps:
1. **Access ServiceNow**: Go to wmlink/adgroup
2. **Select Options**:
   - Production environment
   - "Create Active Directory Group"
3. **Fill Required Fields**:
   - **On Behalf Of**: Yourself (or MJSTUKE for BigQuery Admin Team)
   - **Production Active Directory Domain**: HomeOffice
   - **Group Name**: Must start with `gcp-` for auto-sync
   - **First/Second Owner**: Team managers with approval
   - **Members**: Add initial team members
   - **Resource Description**: "[READER|WRITER] access for [Dataset] in wmt-edw-[dev|prod]"
   - **Data Classification**: Choose appropriate level (Highly Sensitive for secure groups)

### Group Naming Standards

#### Required Prefix
- All groups must begin with `gcp-` for AD to Google Group sync

#### BigQuery Group Types
```
Writer Groups (Data Editor access):
gcp-[dev|prod]-[dataset_basename]-writer

Secure Groups (Viewer access to secure data):
gcp-[dev|prod]-[dataset_basename]-secure

Reader Groups (Viewer access to view models):
gcp-[dev|prod]-[domaingrouping]-reader
```

#### Application Groups
```
Administrative access:
gcp-[app]-admin

Write access:
gcp-[app]-writer

Read access:
gcp-[app]-reader

General user access:
gcp-[app]-user
```

## YAML Configuration Process

### Project Definition Repository
- **Repository**: `gcp_project_definitions`
- **Process**: Submit YAML pull request for new projects
- **Example**: `grs-omni-*` configuration files
- **Approval**: Cloud enablement team (@cloud-gov-network) approves PR

### YAML Structure Example
```yaml
project_name: "grs-omni-prod"
billing_account: "012345-67890A-BCDEF1"
organization_id: "123456789012"
labels:
  cost-center: "CC-RETAIL-001"
  business-unit: "grocery"
  team: "omni-channel"
  environment: "production"
service_accounts:
  - name: "grs-omni-app-sa"
    roles:
      - "roles/bigquery.dataViewer"
      - "roles/storage.objectViewer"
google_groups:
  - "gcp-omni-admin"
  - "gcp-omni-writer"
  - "gcp-omni-reader"
```

## BigQuery Dataset Structure

### Dataset Naming Convention
Walmart follows a specific dataset structure:

#### Core Dataset Types
1. **`[PREFIX]_TABLES`**: Raw data tables
   - Access: Writer groups (BigQuery Data Editor)
   - Purpose: Data ingestion and ETL processing

2. **`[PREFIX]_VM`**: View models
   - Access: Reader groups (BigQuery Data Viewer)
   - Purpose: Business logic and data transformation views

3. **`[PREFIX]_SECURE`**: Secure views
   - Access: Secure groups (BigQuery Data Viewer)
   - Purpose: Sensitive data with restricted access

#### Example Dataset Names
- `US_WM_MB_TABLES` - US Walmart Merchant Business tables
- `US_WM_MB_VM` - US Walmart Merchant Business view models
- `US_WM_MB_SECURE` - US Walmart Merchant Business secure views

### Access Control Matrix

| Group Type | Dataset Access | BigQuery Role | Purpose |
|------------|---------------|---------------|---------|
| `-writer` | `*_TABLES`, `*_VM` | `bigquery.dataEditor` | Data loading and processing |
| `-secure` | `*_SECURE`, `*_VM` | `bigquery.dataViewer` | Sensitive data access |
| `-reader` | `*_VM` (multiple) | `bigquery.dataViewer` | Business user access |

## Integration Points

### ETL and Data Processing
- **DataStage**: Version 11.7.1 (supports BigQuery)
- **Mainframe**: JCL changes for data connectivity
- **APIs**: RESTful interfaces for data ingestion

### Key File Generation
Service accounts require key files for:
- ETL processes (DataStage)
- Mainframe connectivity (JCL)
- API integrations
- Third-party tool connections

### Validation Commands

#### Verify Google Group Creation
```bash
# Web interface
https://groups.google.com/a/walmart.com/forum/#!overview

# Command line validation
adquery group -A {group_name}

# Check BigQuery permissions
bq show wmt-edw-dev:DATASET_NAME
bq show wmt-edw-prod:DATASET_NAME
```

## Special Access Groups

### Enterprise-Wide Groups
- **`gcp-edw-metadata-viewer`**: Metadata access to dev and prod
- **`gcp-edw-sandbox-user`**: Sandbox environment access
- **`gcp-edw-bq-storage-api-user`**: BigQuery Storage API access

### Domain-Specific Groups
- **`gcp-dev-us-walmart-reader`**: US Walmart non-secure data access
- **`gcp-dev-us-sams-reader`**: US Sam's Club data access
- **`gcp-dev-ww-reader`**: Worldwide data access

## Approval Matrix

### Required Approvals by Environment

| Environment | SSP Amendment | Security Review | Cloud Enablement |
|-------------|---------------|-----------------|------------------|
| **Production** | ✅ Required | ✅ Required | ✅ Required |
| **Development** | ❌ Not Required | ✅ Required | ✅ Required |
| **Sandbox** | ❌ Not Required | ⚠️ Limited | ✅ Required |

### Approval Contacts
- **Cloud Enablement**: @cloud-gov-network team
- **BigQuery Admin**: j5mcclu, mjstuke
- **Security**: Internal security team via ServiceNow
- **Compliance**: SOX/PCI teams as applicable

## Master Lists and Documentation

### Required Documentation Updates
1. **Google Group and Dataset Cross Reference Master List**
2. **Service Account inventory**
3. **Key file registry**
4. **Access approval audit trail**

### Regular Maintenance
- **Monthly**: Review Google Group memberships
- **Quarterly**: Audit dataset permissions
- **Semi-Annual**: Service account key rotation
- **Annual**: Complete access certification