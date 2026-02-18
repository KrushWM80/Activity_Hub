# Transitioning from Shared to Independent GCP Project

## Current Situation Assessment

### Current State
- **Peer Contact**: Allen Still (GCP Project Admin)
- **Current Access**: Using a client under Allen's project
- **Available Resources**: 
  - Allen's working YAML configuration
  - Allen's approved SSP (System Security Plan)
- **Goal**: Build independent project foundation

### Transition Strategy
Move from shared dependency to independent project ownership while leveraging proven configurations.

---

## Phase 1: Knowledge Transfer and Resource Gathering

### 1.1 Collect Allen's Project Configuration
- [ ] **Request YAML File**: Get copy of Allen's project YAML from gcp_project_definitions
- [ ] **Document Project Structure**: Record Allen's organizational nesting path
- [ ] **SSP Documentation**: Obtain copy of approved SSP for reference
- [ ] **Service Account Patterns**: Document Allen's service account configurations
- [ ] **IAM Role Mappings**: Record how Allen structured permissions

### 1.2 Analyze Current Usage Patterns
- [ ] **Client Configuration**: Document how your current client is configured under Allen's project
- [ ] **Resource Dependencies**: Identify shared resources you currently use
- [ ] **Data Access Patterns**: Map current BigQuery datasets and permissions
- [ ] **Application Integrations**: List applications currently using Allen's service accounts
- [ ] **Cost Analysis**: Review current usage and costs under Allen's project

### 1.3 Plan Independent Architecture
- [ ] **New Project Scope**: Define what your independent project will include
- [ ] **Resource Migration**: Plan what needs to move from Allen's project
- [ ] **Data Migration**: Identify datasets that need to be replicated or moved
- [ ] **Service Continuity**: Plan to minimize disruption during transition

---

## Phase 2: Prepare Your Independent Project Configuration

### 2.1 Adapt Allen's YAML Configuration
```yaml
# Store Support GCP Project Configuration
# File: wmt-storesupport-prod.yaml

project_name: "wmt-storesupport-prod"  # Official Store Support project name
billing_account: "012345-67890A-BCDEF1"  # Store Support cost center billing
organization_id: "123456789012"  # Same as Allen's

# Adapt Allen's nesting path for Store Support team
organization_path: "organizations/walmart.com/[store-operations]/prod/[support-services]/"

labels:
  cost-center: "CC-STORESUPPORT-001"  # Store Support cost center
  business-unit: "store-operations"    # Store operations business unit
  team: "store-support"               # Store Support team identifier
  environment: "production"
  created-by: "automated-pipeline"
  migrated-from: "allens-project"     # Track migration source

# Store Support service accounts
service_accounts:
  - name: "storesupport-etl-sa"
    display_name: "Store Support ETL Service Account"
    roles:
      - "roles/bigquery.dataEditor"
      - "roles/storage.objectAdmin"
      # Copy roles that work well for Allen
  
  - name: "storesupport-app-sa"  
    display_name: "Store Support Application Service Account"
    roles:
      - "roles/bigquery.dataViewer"
      - "roles/storage.objectViewer"

# Store Support AD groups pattern
ad_groups:
  - name: "gcp-storesupport-prod-dev"
    role: "roles/editor"
    members: []
    
  - name: "gcp-storesupport-prod-admin"
    role: "roles/owner"
    members: []

# Use Allen's proven API list as starting point
enabled_apis:
  - "compute.googleapis.com"
  - "bigquery.googleapis.com" 
  - "storage.googleapis.com"
  # Add others from Allen's working configuration
```

### 2.2 Customize SSP for Your Project
- [ ] **Copy Allen's SSP Structure**: Use his approved format as template
- [ ] **Update Project Details**: Change project name, team, and scope
- [ ] **Maintain Compliance Elements**: Keep security controls that Allen got approved
- [ ] **Add Your Specifics**: Include your team's specific use cases and data
- [ ] **Review with Security Team**: Get preliminary review before formal submission

### 2.3 Plan AD Groups
```
# Store Support AD groups following Allen's proven pattern
Development: gcp-storesupport-prod-dev
Admin: gcp-storesupport-prod-admin

# If Allen has specialized groups, consider similar ones for Store Support:
BigQuery: gcp-storesupport-bq-users
Storage: gcp-storesupport-storage-users
```

---

## Phase 3: Parallel Setup (Minimize Disruption)

### 3.1 Create Your AD Groups
- [ ] **Submit ServiceNow Requests**: Create AD groups following Allen's proven pattern
- [ ] **Use HomeOffice Domain**: Same as Allen's for consistency
- [ ] **Wait for Sync**: Allow 48 hours for AD-to-GCP synchronization
- [ ] **Add Initial Members**: Include yourself and key team members

### 3.2 Submit Your Project YAML PR
- [ ] **Fork gcp_project_definitions**: Follow standard process
- [ ] **Place in Correct Hierarchy**: Use organizational path appropriate for your team
- [ ] **Reference Allen's Success**: Mention in PR description that configuration is based on Allen's proven setup
- [ ] **Include SSP Status**: Note that SSP is adapted from Allen's approved version

### 3.3 Coordinate with Allen During Transition
- [ ] **Maintain Current Access**: Keep using Allen's client during setup
- [ ] **Test New Project**: Validate your new project works before migration
- [ ] **Plan Migration Timeline**: Coordinate with Allen on when to switch over
- [ ] **Document Dependencies**: Identify any shared resources that need coordination

---

## Phase 4: Migration Execution

### 4.1 Data and Configuration Migration
```bash
# Example commands for migrating resources (customize based on your needs)

# Copy BigQuery datasets (if applicable)
bq mk --transfer_config \
  --project_id=wmt-storesupport-prod \
  --data_source=scheduled_query \
  --target_dataset=store_support_data \
  --display_name="Migration from Allen's project" \
  --params='{"query":"SELECT * FROM `allens-project.dataset.table`"}'

# Copy Cloud Storage data (if applicable)
gsutil -m cp -r gs://allens-bucket/store-support-data/* gs://wmt-storesupport-prod-bucket/

# Export/import service account keys
# (Generate new keys in your project, update applications)
```

### 4.2 Application Updates
- [ ] **Generate New Service Account Keys**: Create keys for your new service accounts
- [ ] **Update Application Configurations**: Point applications to your new project
- [ ] **Test Connectivity**: Verify applications work with new project
- [ ] **Update Environment Variables**: Change project IDs and service account references

### 4.3 Validation and Cutover
- [ ] **Parallel Testing**: Run applications against both projects temporarily
- [ ] **Performance Validation**: Ensure new project performs as expected
- [ ] **Cost Verification**: Confirm billing is routing to your cost center
- [ ] **Security Validation**: Verify all security controls are working
- [ ] **Team Training**: Ensure team knows how to use new project

---

## Phase 5: Post-Migration Cleanup

### 5.1 Remove Dependencies on Allen's Project
- [ ] **Remove Client Access**: Clean up your client configuration in Allen's project
- [ ] **Update Documentation**: Change all references from Allen's project to yours
- [ ] **Notify Stakeholders**: Inform all users about the new project details
- [ ] **Archive Old Configurations**: Safely store old configurations for reference

### 5.2 Optimize Your Independent Setup
- [ ] **Review Resource Usage**: Optimize based on actual usage patterns
- [ ] **Adjust IAM Permissions**: Fine-tune permissions based on your specific needs
- [ ] **Cost Optimization**: Implement cost controls appropriate for your budget
- [ ] **Monitoring Setup**: Configure monitoring and alerting for your project

### 5.3 Knowledge Documentation
- [ ] **Document Migration Process**: Record what worked well for future reference
- [ ] **Create Team Playbook**: Document how your team will manage the project
- [ ] **Acknowledge Allen's Help**: Formally thank Allen and document his contribution
- [ ] **Share Lessons Learned**: Help other teams who might need similar transitions

---

## Coordination with Allen Still

### Communication Plan
- [ ] **Initial Meeting**: Discuss timeline and approach with Allen
- [ ] **Resource Sharing**: Get copies of Allen's YAML and SSP configurations
- [ ] **Regular Check-ins**: Weekly status updates during transition
- [ ] **Migration Coordination**: Plan cutover timing to minimize disruption
- [ ] **Post-Migration**: Thank Allen and offer reciprocal help in future

### Questions to Ask Allen
1. **What worked well** in his project setup process?
2. **What challenges** did he encounter and how were they resolved?
3. **Which configurations** are most critical to get right?
4. **How long** did his approval process take?
5. **Any tips** for working with the cloud enablement team?

### Maintaining Relationship
- [ ] **Document Allen's Contribution**: Include acknowledgment in project documentation
- [ ] **Offer Reciprocal Help**: Be available to help Allen with future projects
- [ ] **Share Your Experience**: Document and share your migration experience
- [ ] **Build Network**: Use this as foundation for broader GCP community at Walmart

---

## Success Metrics

### Technical Success
- [ ] Independent project fully functional
- [ ] All applications migrated successfully
- [ ] No performance degradation
- [ ] Security controls properly implemented
- [ ] Cost tracking working correctly

### Process Success
- [ ] Smooth transition with minimal downtime
- [ ] Team fully trained on new project
- [ ] Documentation complete and accurate
- [ ] Good relationship maintained with Allen
- [ ] Knowledge captured for future teams

### Timeline Target
- **Week 1-2**: Knowledge transfer and configuration preparation
- **Week 3-4**: AD groups and project creation
- **Week 5-6**: Migration and testing
- **Week 7**: Cutover and cleanup

This approach leverages Allen's proven success while building your independent foundation for long-term success.