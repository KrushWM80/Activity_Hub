# Walmart BigQuery IAM and Access Control Guide

## Repository Information
- **Source**: https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions.git
- **Created by**: Chris Daniels
- **Last modified by**: Mike Stuker (Mar 19, 2020)

## BigQuery IAM Overview

BigQuery uses Identity and Access Management (IAM) to control access to three types of resources:
1. **Organizations** - Top-level Walmart GCP organization
2. **Projects** - Individual GCP projects (wmt-edw-prod, wmt-edw-dev, etc.)
3. **Datasets** - Data containers within projects

### Resource Hierarchy
```
Organization (Walmart)
└── Projects (wmt-edw-prod, wmt-edw-dev)
    └── Datasets (*_TABLES, *_VM, *_SECURE)
        └── Tables/Views (inherit dataset permissions)
```

## IAM Roles Matrix

### Project-Level IAM Roles

| IAM Role | Permission | Scope | Usage |
|----------|------------|-------|--------|
| `bigquery.dataViewer` | View all datasets in project | Application/Workload Project | Read-only access to all project data |
| `bigquery.dataEditor` | View/edit all datasets in project | Application/Workload Project | Full data manipulation within project |
| `bigquery.dataOwner` | Create/view/edit all datasets | Application/Workload Project | Complete dataset management |
| `bigquery.metadataViewer` | See dataset tree and structures | BigQuery EDW Project | Browse schema without data access |
| `bigquery.user` | Query BigQuery | Application/Workload Project | Basic query execution rights |
| `bigquery.jobUser` | Create and see BigQuery jobs | Application/Workload Project | Job management permissions |
| `bigquery.admin` | Admin BigQuery | Warehouse Solutions DBA only | Full administrative control |

### Dataset-Level Controls

| Dataset Control | Equivalent IAM | Scope | Usage |
|-----------------|---------------|-------|--------|
| `READER` | Dataset-level `bigquery.dataViewer` | BigQuery EDW Project | Read access to specific dataset |
| `WRITER` | Dataset-level `bigquery.dataEditor` | BigQuery EDW Project | Write access to specific dataset |
| `OWNER` | Dataset-level `bigquery.dataOwner` | Warehouse Solutions DBA only | Dataset ownership and control |

## Walmart Access Control Model

### Dataset Access Rights by Type

| Dataset Type | Access Level | Target Users | Purpose |
|--------------|--------------|-------------|----------|
| `<DOMAIN>_TABLES` | **WRITER** | ETL processes, data engineers | Raw data ingestion and processing |
| `<DOMAIN>_VM` | **READER** | All authorized users | Business views and analytics |
| `<DOMAIN>_SECURE` | **READER** | Specific authorized users only | Sensitive data with restricted access |

### Access Control Examples

#### US Walmart Merchant Business (US_WM_MB)
```
US_WM_MB_TABLES → WRITER access → gcp-prod-us-wm-mb-writer
US_WM_MB_VM     → READER access → gcp-prod-us-walmart-reader
US_WM_MB_SECURE → READER access → gcp-prod-us-wm-mb-secure
```

#### HR Domain (Multiple Roles/Objects)
```
HR_PAYROLL_TABLES → WRITER access → gcp-prod-hr-payroll-writer
HR_PAYROLL_VM     → READER access → gcp-prod-hr-payroll-reader
HR_PAYROLL_SECURE → READER access → gcp-prod-hr-payroll-secure

HR_BENEFITS_TABLES → WRITER access → gcp-prod-hr-benefits-writer
HR_BENEFITS_VM     → READER access → gcp-prod-hr-benefits-reader
HR_BENEFITS_SECURE → READER access → gcp-prod-hr-benefits-secure
```

## Permission Inheritance Model

### Hierarchy Rules
1. **Tables and Views** inherit permissions from parent dataset
2. **Datasets** inherit project-level permissions where applicable
3. **Union of Permissions** - Users get combined permissions from all assigned roles

### Permission Calculation
```
Effective Permission = Project IAM Role ∪ Dataset Control ∪ Group Membership
```

## Implementation Guidelines

### For Application/Workload Projects
- Grant **project-level** IAM roles for broad access patterns
- Use `bigquery.user` + `bigquery.jobUser` for basic query access
- Apply `bigquery.dataViewer` for read-only application access
- Apply `bigquery.dataEditor` for ETL and data processing applications

### For BigQuery EDW Projects (wmt-edw-*)
- Use **dataset-level** controls for granular access
- Grant `bigquery.metadataViewer` for schema browsing
- Apply dataset READER/WRITER controls based on data sensitivity

## Access Control Considerations

### Key Limitations
1. **No Object-Level Permissions**: Cannot manage permissions on individual tables/views
2. **Dataset Granularity**: Minimum permission boundary is at dataset level
3. **Multiple Datasets Required**: Complex access patterns require multiple datasets per domain

### Best Practices
1. **Separation of Concerns**: Use separate datasets for different access levels
2. **Principle of Least Privilege**: Grant minimum required access
3. **Group-Based Access**: Always use Google Groups, never individual users
4. **Regular Audits**: Review and validate permissions quarterly

## Sensitive Data Access via _SECURE Datasets

### Purpose
`_SECURE` datasets facilitate access control for sensitive data by:
- Providing restricted views of sensitive columns
- Requiring explicit approval for access
- Maintaining audit trails for compliance
- Supporting data masking and anonymization

### Implementation Pattern
```sql
-- Example: _SECURE dataset view with row-level security
CREATE VIEW `wmt-edw-prod.US_WM_MB_SECURE.customer_pii` AS
SELECT 
  customer_id,
  CASE 
    WHEN @user_email IN ('authorized_analyst@walmart.com') 
    THEN customer_ssn 
    ELSE 'REDACTED' 
  END as customer_ssn,
  customer_name
FROM `wmt-edw-prod.US_WM_MB_TABLES.customers`
WHERE region = 'US';
```

## Reference Links
- **Access Control Documentation**: https://cloud.google.com/bigquery/docs/access-control
- **IAM Roles Reference**: https://cloud.google.com/bigquery/docs/access-control#bigquery-roles
- **Dataset Permissions**: https://cloud.google.com/bigquery/docs/dataset-access-controls