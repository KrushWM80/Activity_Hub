# Store Support GCP Project Setup - Next Steps Roadmap

**Current Date**: November 4, 2025  
**Project**: Store Support (`wmt-storesupport-prod`)  
**Status**: Documentation Complete → Ready for Implementation

---

## 🎯 Implementation Roadmap

### Phase 1: Active Directory Setup (Week 1-2)
**⏱️ Timeline: 1-48 hours** (includes AD sync time)

#### Step 1.1: Create AD Groups
Submit ServiceNow requests to create three AD groups:

**Request Template - ServiceNow URL:**
https://walmartglobal.service-now.com/wm_sp?id=sc_cat_item_guide&table=sc_cat_item&sys_id=222d77a3db8a634832af7f698c9619dc

**Groups to Create:**

1. **Admin Group**
   - **Name**: `gcp-storesupport-prod-admin`
   - **Domain**: HomeOffice
   - **Type**: Security Group
   - **Description**: Store Support administrators with full project access
   - **Members**: [Your team leads and senior engineers]

2. **Developer Group**
   - **Name**: `gcp-storesupport-prod-dev`
   - **Domain**: HomeOffice
   - **Type**: Security Group
   - **Description**: Store Support developers with development access
   - **Members**: [Your developers and engineers]

3. **Analyst Group**
   - **Name**: `gcp-storesupport-prod-analyst`
   - **Domain**: HomeOffice
   - **Type**: Security Group
   - **Description**: Store Support analysts with BigQuery access
   - **Members**: [Your analysts and business users]

#### ✅ Deliverables for Phase 1:
- [ ] ServiceNow tickets created for all 3 groups
- [ ] Groups created and visible in Active Directory
- [ ] Group members assigned
- [ ] (Wait 48 hours for full AD-to-GCP sync)
- [ ] Confirm groups appear in GCP Console

---

### Phase 2: GCP Project Configuration (Week 3)
**⏱️ Timeline: 2-3 days**

#### Step 2.1: Access the YAML Configuration Repository

```bash
# Clone the Walmart GCP project definitions repository
git clone https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions
cd gcp_project_definitions
git checkout -b feature/storesupport-prod
```

#### Step 2.2: Create Your Project YAML File

**File Location**: Follow Walmart's organizational hierarchy
```
gcp_project_definitions/
└── organizations/
    └── walmart.com/
        └── store-operations/              # Adjust per your org
            └── prod/
                └── support-services/       # Adjust per your org
                    └── wmt-storesupport-prod.yaml
```

**Use the template from**: `store-support-config.md` in this repository

#### Step 2.3: Fill in Required Values

Before submitting, populate these values:

```yaml
project_name: "wmt-storesupport-prod"
billing_account: "YOUR-BILLING-ACCOUNT-ID"  # Get from Walmart Finance
organization_id: "123456789012"              # Get from GCP console
organization_path: "organizations/walmart.com/store-operations/prod/support-services/"

labels:
  cost-center: "CC-STORESUPPORT-001"        # Your cost center
  business-unit: "store-operations"
  team: "store-support"
  environment: "production"
```

**Where to find these values:**
- **Billing Account**: Contact Walmart GCP Finance team
- **Organization ID**: Available in GCP Cloud Console → Settings
- **Cost Center**: Provided by your Finance contact
- **Organizational Path**: Confirm with GCP Admin (Allen Still or infrastructure team)

#### Step 2.4: Submit PR to gcp_project_definitions

```bash
# Add your YAML file
git add organizations/walmart.com/.../wmt-storesupport-prod.yaml

# Commit with descriptive message
git commit -m "feat: Add Store Support GCP project configuration (wmt-storesupport-prod)

- Project ID: wmt-storesupport-prod
- Team: Store Support
- Purpose: Software and product development for store support teams
- Service Accounts: ETL, Application, Analytics
- AD Groups: Admin, Dev, Analyst
- Billing: [Cost Center]"

# Push to your branch
git push origin feature/storesupport-prod
```

#### Step 2.5: Create Pull Request
- Go to: https://gecgithub01.walmart.com/Public-Cloud/gcp_project_definitions
- Create PR from your branch to main
- Add description: See commit message details
- Add reviewers: GCP Infrastructure team / Allen Still
- Link any related tickets/work orders

#### ✅ Deliverables for Phase 2:
- [ ] YAML configuration file created with all required fields
- [ ] All values verified and correct
- [ ] PR submitted to gcp_project_definitions
- [ ] PR reviewed and approved by infrastructure team
- [ ] PR merged to main branch

---

### Phase 3: Project Creation & Service Accounts (Week 4)
**⏱️ Timeline: 1-2 days** (automated by CI/CD pipeline)

#### Step 3.1: Monitor Pipeline Execution
Once your PR is merged, Walmart's automated pipeline will:
- ✅ Validate YAML configuration
- ✅ Create GCP project: `wmt-storesupport-prod`
- ✅ Configure IAM bindings
- ✅ Create service accounts:
  - `storesupport-etl-sa`
  - `storesupport-app-sa`
  - `storesupport-analytics-sa`
- ✅ Assign AD groups to project roles
- ✅ Enable required APIs
- ✅ Configure billing

**Monitor at**: GCP Cloud Console → My Projects

#### Step 3.2: Verify Project Creation
Check that these appear in GCP:
```
✓ Project ID: wmt-storesupport-prod
✓ Service Accounts (3):
  - storesupport-etl-sa@wmt-storesupport-prod.iam.gserviceaccount.com
  - storesupport-app-sa@wmt-storesupport-prod.iam.gserviceaccount.com
  - storesupport-analytics-sa@wmt-storesupport-prod.iam.gserviceaccount.com
✓ AD Group IAM Bindings:
  - gcp-storesupport-prod-admin → Owner
  - gcp-storesupport-prod-dev → Editor
  - gcp-storesupport-prod-analyst → BigQuery User
✓ APIs Enabled (13 required APIs)
✓ VPC Network: storesupport-vpc
```

#### ✅ Deliverables for Phase 3:
- [ ] GCP project created successfully
- [ ] All service accounts visible in GCP console
- [ ] AD groups synchronized and assigned to roles
- [ ] Required APIs enabled
- [ ] VPC and subnets created

---

### Phase 4: Secret and Credential Generation (Week 4-5)
**⏱️ Timeline: 1-2 days**

#### Step 4.1: Generate Service Account JSON Keys

For each service account, create JSON keys:

```bash
# For ETL service account
gcloud iam service-accounts keys create storesupport-etl-sa-key.json \
  --iam-account=storesupport-etl-sa@wmt-storesupport-prod.iam.gserviceaccount.com \
  --project=wmt-storesupport-prod

# For Application service account
gcloud iam service-accounts keys create storesupport-app-sa-key.json \
  --iam-account=storesupport-app-sa@wmt-storesupport-prod.iam.gserviceaccount.com \
  --project=wmt-storesupport-prod

# For Analytics service account
gcloud iam service-accounts keys create storesupport-analytics-sa-key.json \
  --iam-account=storesupport-analytics-sa@wmt-storesupport-prod.iam.gserviceaccount.com \
  --project=wmt-storesupport-prod
```

#### Step 4.2: Store Secrets Securely

**Option A: GCP Secret Manager** (Recommended)
```bash
# Store each JSON key in Secret Manager
gcloud secrets create storesupport-etl-sa-key \
  --data-file=storesupport-etl-sa-key.json \
  --project=wmt-storesupport-prod

gcloud secrets create storesupport-app-sa-key \
  --data-file=storesupport-app-sa-key.json \
  --project=wmt-storesupport-prod

gcloud secrets create storesupport-analytics-sa-key \
  --data-file=storesupport-analytics-sa-key.json \
  --project=wmt-storesupport-prod
```

**Option B: Walmart Secrets Management** (If required by policy)
- Follow internal Walmart secrets management procedures
- Store in AFAAS/DPAAS secret stores
- Document access procedures

#### ✅ Deliverables for Phase 4:
- [ ] All JSON keys created for each service account
- [ ] Keys stored securely (Secret Manager or equivalent)
- [ ] Access controls configured for secret retrieval
- [ ] Team members have access to retrieve secrets as needed
- [ ] Key rotation policy documented

---

### Phase 5: BigQuery & Data Setup (Week 5-6)
**⏱️ Timeline: 2-3 days**

#### Step 5.1: Create BigQuery Datasets

```bash
# Create TABLES dataset (writable by developers)
bq mk --dataset \
  --description="Store Support development tables and raw data" \
  --location=US \
  --project_id=wmt-storesupport-prod \
  STORE_SUPPORT_TABLES

# Create VM dataset (viewable by analysts)
bq mk --dataset \
  --description="Store Support virtual machines and processed data" \
  --location=US \
  --project_id=wmt-storesupport-prod \
  STORE_SUPPORT_VM

# Create SECURE dataset (restricted access)
bq mk --dataset \
  --description="Store Support secure and sensitive data" \
  --location=US \
  --project_id=wmt-storesupport-prod \
  STORE_SUPPORT_SECURE
```

#### Step 5.2: Configure BigQuery IAM

```bash
# Give developer group write access to TABLES dataset
bq update --set_iam_policy=<(jq -n \
  --arg admin 'serviceAccount:storesupport-dev@wmt-storesupport-prod.iam.gserviceaccount.com' \
  '{bindings: [{role: "roles/bigquery.dataEditor", members: [$admin]}]}') \
  wmt-storesupport-prod:STORE_SUPPORT_TABLES

# Give analyst group read access to VM dataset
# (configured via AD group in project)
```

#### ✅ Deliverables for Phase 5:
- [ ] STORE_SUPPORT_TABLES dataset created
- [ ] STORE_SUPPORT_VM dataset created
- [ ] STORE_SUPPORT_SECURE dataset created
- [ ] IAM bindings configured for each dataset
- [ ] Team members can query appropriate datasets

---

### Phase 6: Testing & Validation (Week 6)
**⏱️ Timeline: 1-2 days**

#### Step 6.1: Connectivity Tests

```bash
# Test ETL service account access
gcloud auth activate-service-account \
  --key-file=storesupport-etl-sa-key.json \
  --project=wmt-storesupport-prod

# Test BigQuery access
bq query --use_legacy_sql=false \
  'SELECT COUNT(*) FROM `wmt-storesupport-prod.STORE_SUPPORT_TABLES.__TABLES__`'

# Test Cloud Storage access
gsutil ls gs://wmt-storesupport-prod-data/
```

#### Step 6.2: Application Testing
- Deploy test applications using service account credentials
- Verify ETL pipelines can read/write to BigQuery
- Confirm analytics dashboards can access data
- Test monitoring and logging

#### Step 6.3: Team Access Verification
- [ ] Admin team members can access GCP console
- [ ] Developer team members can deploy applications
- [ ] Analyst team members can query BigQuery datasets
- [ ] All audit logs are being collected

#### ✅ Deliverables for Phase 6:
- [ ] All connectivity tests passed
- [ ] Team members can access appropriate resources
- [ ] Monitoring and logging working correctly
- [ ] Cost tracking enabled and visible

---

### Phase 7: Production Readiness (Week 7)
**⏱️ Timeline: 1 week**

#### Step 7.1: Security & Compliance Review
- [ ] Review security compliance checklist (see `security-compliance.md`)
- [ ] Configure IAM conditions if needed
- [ ] Enable VPC Service Controls if required
- [ ] Document security procedures

#### Step 7.2: Documentation & Training
- [ ] Create team-specific runbooks
- [ ] Document application deployment procedures
- [ ] Train team on GCP tools and best practices
- [ ] Create incident response procedures

#### Step 7.3: Monitoring & Cost Controls
- [ ] Set up budget alerts (see `cost-management.md`)
- [ ] Configure monitoring dashboards (see `monitoring-logging.md`)
- [ ] Document cost allocation procedures
- [ ] Set up regular cost reviews

#### ✅ Deliverables for Phase 7:
- [ ] Security review completed
- [ ] Team trained on procedures
- [ ] Monitoring and alerting configured
- [ ] Cost controls in place
- [ ] Documentation complete

---

## 📊 Timeline Summary

| Phase | Task | Duration | Start | End |
|-------|------|----------|-------|-----|
| 1 | AD Setup | 1-2 weeks | Week 1 | Week 2 |
| 2 | YAML Config | 2-3 days | Week 3 | Week 3 |
| 3 | Project Creation | 1-2 days | Week 4 | Week 4 |
| 4 | Secrets Generation | 1-2 days | Week 4-5 | Week 5 |
| 5 | BigQuery Setup | 2-3 days | Week 5-6 | Week 6 |
| 6 | Testing | 1-2 days | Week 6 | Week 6 |
| 7 | Production Ready | 1 week | Week 7 | Week 7 |
| **TOTAL** | **Full Setup** | **~7 weeks** | | |

---

## 🎯 Immediate Action Items (Next 7 Days)

### This Week:
1. **[ ] Day 1-2**: Prepare ServiceNow AD group requests
   - Gather team member names for each group
   - Get manager approval
   - Submit 3 ServiceNow tickets

2. **[ ] Day 3-4**: Gather Required Information
   - Contact GCP Finance for billing account ID
   - Confirm organizational hierarchy with GCP admin
   - Get cost center from Finance

3. **[ ] Day 5-7**: Prepare YAML Configuration
   - Customize `store-support-config.md` template
   - Fill in all required fields
   - Get peer review from another GCP admin

### Next Week:
4. Clone `gcp_project_definitions` repository
5. Create YAML file in proper location
6. Submit PR with full documentation

---

## 📚 Key Reference Documents

- **Current Process**: `walmart-gcp-process-2025.md`
- **Configuration Template**: `store-support-config.md`
- **Security Guide**: `security-compliance.md`
- **BigQuery IAM**: `bigquery-iam-guide.md`
- **Monitoring Setup**: `monitoring-logging.md`
- **Cost Management**: `cost-management.md`

---

## 🤝 Support & Escalation

**For questions contact:**
- **GCP Infrastructure**: Allen Still (peer) or team
- **Walmart Cloud Services**: Internal Slack channel #gcp-support
- **ServiceNow**: Create ticket in GCP category

---

## ✅ Success Criteria

Your Store Support GCP project will be complete when:
1. ✅ GCP project `wmt-storesupport-prod` is created
2. ✅ All 3 service accounts are functional
3. ✅ AD groups are synced and assigned to roles
4. ✅ BigQuery datasets accessible to authorized teams
5. ✅ Monitoring and logging operational
6. ✅ Team members trained and able to deploy applications
7. ✅ Cost tracking and budgets in place

---

**Last Updated**: November 4, 2025  
**Status**: Ready for Implementation  
**Next Review**: After Phase 2 completion