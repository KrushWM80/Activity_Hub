# Projects in Activity Hub - DONE & DO List

**Date Created**: March 16, 2026  
**Feature Status**: Planning Phase  
**Last Updated**: End of Day, March 16

---

## ✅ DONE (What We've Accomplished)

- [x] **Feature Concept Definition** - Defined the Projects section requirement for users to manage Projects they Own or Follow
- [x] **Architecture Review** - Verified that Data-Bridge is available in Admin for data aggregation
- [x] **System Integration Identified** - Confirmed Data-Bridge will source all necessary project data
- [x] **Scope Definition** - Outlined key features needed:
  - Project ownership & following
  - Project metrics (testing, validation)
  - Store selection & validation tools
  - Template-based presentations for meetings/forums
- [x] **Planning Session Complete** - Documented requirements and created implementation roadmap

---

## 📋 DO - Tomorrow's Tasks

### **PHASE 1: DATA STRUCTURE & BACKEND (Priority: CRITICAL)**

#### Data-Bridge Setup
- [ ] **Define Projects Data Schema**
  - Create `projects-schema.json` in `Admin/Data-Bridge/Schemas/`
  - Define project fields: ID, Name, Owner, Status, Metrics, Stores Involved, Created Date, Last Updated
  - Include relationship fields: owner_user_id, follower_user_ids, store_ids
  
- [ ] **Create Projects Data Mapping**
  - Create `projects-mappings.json` in `Admin/Data-Bridge/Mappings/`
  - Map source data fields to canonical schema fields
  - Include transformation rules (status normalization, date formatting)

- [ ] **Add Projects Transformations**
  - Add project-specific transformation functions to `Platform/Data-Bridge/Transformations/transformations.js`
  - Examples: normalize_project_status(), normalize_dates(), calculate_metrics()

- [ ] **Add Projects Validators**
  - Add validation rules to `Platform/Data-Bridge/Transformations/validators.js`
  - Validate required fields, data types, date ranges
  - Validate relationships (owner exists, stores exist)

#### BigQuery Data Query
- [ ] **Design BigQuery Query for Projects**
  - Query projects data from warehouse
  - Filter by user ownership or following status
  - Include associated metrics table joins
  - Determine data refresh frequency (real-time vs. daily)

- [ ] **Test Data Extraction**
  - Run sample query against BigQuery
  - Validate returned fields match schema
  - Check for null/missing data issues

---

### **PHASE 2: ADMIN INTERFACE (Priority: HIGH)**

#### Admin Dashboard Enhancement
- [ ] **Create Admin Data-Bridge Project Configuration UI**
  - Add Projects to the Admin/Data-Bridge dashboard
  - Allow viewing of uploaded project data
  - Create schema and mapping configuration panels

- [ ] **Add Admin Links for Projects**
  - Create navigation link in admin-dashboard.html to Projects configuration
  - Update dynamic-links.json with Projects management link
  - Configure role-based access (which admin roles can manage projects)

- [ ] **Create Projects Admin Documentation**
  - Write admin guide for managing projects data imports
  - Document schema fields and transformation rules
  - Create troubleshooting guide

---

### **PHASE 3: FRONT-END FOUNDATION (Priority: HIGH)**

#### Projects Interface Structure
- [ ] **Create Projects Landing Page**
  - File: `Interface/Projects/projects-hub.html`
  - Basic layout with tabs: "Owned", "Following", "All"
  - Navigation integration with main Activity Hub

- [ ] **Create Projects API Interface Layer**
  - File: `Interface/Projects/projects-api.js`
  - Functions to fetch owned projects
  - Functions to fetch following projects
  - Functions to get project metrics
  - Functions to fetch stores for a project

- [ ] **Build Projects Data Display Component**
  - File: `Interface/Projects/projects-display.js`
  - Card-based project listing layout
  - Sort/filter functionality (by status, store, date)
  - Search functionality for projects

- [ ] **Create Project Detail View**
  - File: `Interface/Projects/project-detail.html`
  - Show full project information
  - Display associated metrics
  - Show store details and selection tools
  - Display meeting/forum templates

---

### **PHASE 4: METRICS & TOOLS (Priority: MEDIUM)**

#### Metrics Implementation
- [ ] **Define Metrics Schema**
  - What metrics to track (testing %, validation %, stores covered, etc.)
  - Where metrics data comes from (Data-Bridge table)
  - How often to refresh metrics

- [ ] **Create Metrics Display Component**
  - File: `Interface/Projects/projects-metrics.js`
  - Dashboard cards showing key metrics
  - Charts/visualizations for project health
  - Progress indicators for testing/validation

#### Store Selection & Validation
- [ ] **Build Store Selection Tool**
  - File: `Interface/Projects/store-selection-tool.js`
  - Interface to select/deselect stores
  - Bulk selection features
  - Store filtering (by region, district, etc.)

- [ ] **Create Validation Tools**
  - File: `Interface/Projects/validation-tools.js`
  - Data validation checks
  - Store readiness verification
  - Conflict detection

---

### **PHASE 5: TEMPLATES & PRESENTATIONS (Priority: MEDIUM)**

#### Template System Foundation
- [ ] **Define Template Structure**
  - Document what templates are needed (meetings, forums, status reports)
  - Decide on template storage location

- [ ] **Create Meeting Template Renderer**
  - File: `Interface/Projects/meeting-template.js`
  - Load template from configuration
  - Populate with live project data
  - Generate presentation view

- [ ] **Create Forum Template Renderer**
  - File: `Interface/Projects/forum-template.js`
  - Similar to meeting template but for forum discussions
  - Include comment/feedback sections

---

### **PHASE 6: INTEGRATION & TESTING (Priority: HIGH)**

#### Cross-Module Integration
- [ ] **Integrate with Main Activity Hub Navigation**
  - Add Projects tab/link to main landing page
  - Update nav links in For You page
  - Ensure authentication flows

- [ ] **Connect to Data-Bridge Data Flow**
  - Wire up API calls to fetch data from backend
  - Set up data caching strategy
  - Implement error handling for data unavailability

#### Testing Plan
- [ ] **Create Unit Tests**
  - Test transformation functions
  - Test validator functions
  - Test API interface layer

- [ ] **Create Integration Tests**
  - Test full data flow from BigQuery → Data-Bridge → UI
  - Test filtering/sorting functionality
  - Test permission/access controls

- [ ] **Create Manual Test Cases**
  - Test as different user roles (owner, follower, view-only)
  - Test with various data scenarios (empty, large datasets)
  - Test error conditions (no data, network failures)

---

## 📊 Implementation Timeline Estimate

**Week 1 (This Week)**
- Days 1-2: Data-Bridge setup, schema/mapping, transformations
- Days 2-3: BigQuery queries and testing
- Days 3-5: Basic UI framework and API layer

**Week 2**
- Days 1-2: Project detail view and metrics foundation
- Days 3-4: Store selection and validation tools
- Days 5: Template systems start

**Week 3+**
- Continue template development
- Full integration testing
- Performance optimization
- Documentation and deployment

---

## 🎯 Success Criteria

✓ Data successfully flows from BigQuery → Data-Bridge → Projects UI  
✓ Users can see projects they own  
✓ Users can see projects they follow  
✓ Project metrics display accurately  
✓ Store selection tools work correctly  
✓ Meeting/forum templates generate properly  
✓ All tests pass  
✓ Performance is acceptable (<2s page load)  

---

## 🔗 Related Documentation

- **Data-Bridge**: `Platform/Data-Bridge/README.md`
- **Admin Interface**: `Interface/Admin/README.md`
- **Role Management**: `Interface/Admin/ROLE_MANAGEMENT.md`
- **Access Control**: `Interface/Admin/ACCESS_CONTROL.md`

---

## 📝 Notes

- Start with Data-Bridge configuration tomorrow morning - this is the foundation
- Schema and mapping decisions today will affect all downstream work
- Consider data refresh frequency impacts on UI responsiveness
- Plan for role-based visibility of projects early
