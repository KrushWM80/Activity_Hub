# Access Control System - Active Directory Integration

## 🔐 Overview
The Access Control system seamlessly integrates with Walmart Enterprise Active Directory to provide secure, scalable, and centrally managed user authentication and authorization for the Activity Hub platform.

## 🏢 Active Directory Integration Architecture

### Authentication Flow
```
User Login → AD Authentication → Group Membership Check → Role Assignment → Activity Hub Access
```

### Core Components
- **AD Group Mapping**: Direct mapping of AD security groups to Activity Hub roles
- **Single Sign-On (SSO)**: Seamless authentication using corporate credentials
- **Dynamic Authorization**: Real-time permission updates based on AD group changes
- **Audit Integration**: Complete audit trail linked to corporate identity management

## 📋 AD Group Structure

### Enterprise-Level Groups
These groups provide organization-wide access and are managed by Corporate IT:

#### **WMT_ActivityHub_Executives**
- **Purpose**: C-Level and VP access across all business units
- **Membership**: CEO, CFO, CTO, all VPs, and designated senior executives
- **Activity Hub Role**: C-Level Executive, Vice President
- **Managed By**: Corporate IT Security Team

#### **WMT_ActivityHub_Directors**
- **Purpose**: Senior and regular directors with department oversight
- **Membership**: All directors and senior directors across business units
- **Activity Hub Role**: Director, Senior Director
- **Managed By**: HR Business Partners with IT approval

#### **WMT_ActivityHub_Managers**
- **Purpose**: Team managers and supervisors
- **Membership**: All people managers across the organization
- **Activity Hub Role**: Manager
- **Managed By**: Department HR representatives

### Functional Groups
These groups provide access based on job function regardless of department:

#### **WMT_ActivityHub_ProjectManagers**
- **Purpose**: Professional project managers and coordinators
- **Membership**: Certified PMs, project coordinators, program managers
- **Activity Hub Role**: Project Manager
- **Managed By**: PMO (Project Management Office)

#### **WMT_ActivityHub_BusinessAnalysts**
- **Purpose**: Data analysts, business intelligence, and reporting specialists
- **Membership**: Business analysts, data scientists, BI developers
- **Activity Hub Role**: Business Analyst
- **Managed By**: Analytics Center of Excellence

#### **WMT_ActivityHub_TechnicalSpecialists**
- **Purpose**: IT professionals and system administrators
- **Membership**: System admins, developers, technical architects
- **Activity Hub Role**: Technical Specialist
- **Managed By**: Enterprise Technology Leadership

### Department-Specific Groups
Each department has its own access groups for department-specific permissions:

#### **Finance Department**
- **WMT_ActivityHub_Finance_Leadership**: Finance directors and above
- **WMT_ActivityHub_Finance_Managers**: Finance managers and team leads
- **WMT_ActivityHub_Finance_Analysts**: Financial analysts and specialists
- **WMT_ActivityHub_Finance_Users**: All finance department employees

#### **Operations Department**
- **WMT_ActivityHub_Ops_Leadership**: Operations directors and above
- **WMT_ActivityHub_Ops_Managers**: Operations managers and supervisors
- **WMT_ActivityHub_Ops_Coordinators**: Supply chain and logistics coordinators
- **WMT_ActivityHub_Ops_Users**: All operations department employees

#### **Technology Department**
- **WMT_ActivityHub_Tech_Leadership**: Technology directors and above
- **WMT_ActivityHub_Tech_Managers**: Engineering managers and team leads
- **WMT_ActivityHub_Tech_Developers**: Software developers and engineers
- **WMT_ActivityHub_Tech_Users**: All technology department employees

#### **Human Resources Department**
- **WMT_ActivityHub_HR_Leadership**: HR directors and above
- **WMT_ActivityHub_HR_BusinessPartners**: HR business partners and managers
- **WMT_ActivityHub_HR_Specialists**: HR specialists and coordinators
- **WMT_ActivityHub_HR_Users**: All HR department employees

### Administrative Groups
Special groups for Activity Hub system administration:

#### **WMT_ActivityHub_SuperAdmins**
- **Purpose**: Full system administration access
- **Membership**: Senior IT leaders and designated system owners
- **Managed By**: CTO office with security team approval

#### **WMT_ActivityHub_RoleAdmins**
- **Purpose**: Role and permission management access
- **Membership**: HR leaders and department heads
- **Managed By**: CHRO office with IT security approval

#### **WMT_ActivityHub_ContentAdmins**
- **Purpose**: Content and link management access
- **Membership**: Communications team and department liaisons
- **Managed By**: Corporate Communications with IT approval

## 🔄 Group Management Workflow

### New User Onboarding
```
1. HR creates employee record in Workday
2. Workday triggers AD account creation
3. Manager requests Activity Hub access via ServiceNow
4. IT adds user to appropriate AD groups
5. User gains automatic Activity Hub access on next login
```

### Role Changes
```
1. Employee role change in Workday (promotion/transfer)
2. Automated workflow updates AD group memberships
3. Activity Hub permissions automatically adjust
4. Manager and employee receive change notifications
```

### Access Removal
```
1. Employee departure/transfer triggers Workday workflow
2. AD groups automatically updated within 24 hours
3. Activity Hub access immediately revoked
4. Audit trail captures all access changes
```

## 🛠️ Technical Implementation

### Group Mapping Configuration
```json
{
  "ad_group_mappings": {
    "WMT_ActivityHub_Executives": {
      "activity_hub_roles": ["c-level-executive", "vice-president"],
      "additional_permissions": ["enterprise.view.all", "strategic.planning.access"],
      "department_overrides": true
    },
    "WMT_ActivityHub_Directors": {
      "activity_hub_roles": ["director", "senior-director"],
      "additional_permissions": ["department.management.full"],
      "department_overrides": true
    },
    "WMT_ActivityHub_Finance_Leadership": {
      "base_role_from": "WMT_ActivityHub_Directors",
      "additional_permissions": [
        "finance.sap.access",
        "finance.reporting.advanced",
        "finance.budget.management"
      ]
    }
  }
}
```

### Authentication Integration
- **Protocol**: SAML 2.0 with Walmart Enterprise Identity Provider
- **Session Management**: Integrated with corporate session timeout policies
- **Multi-Factor Authentication**: Leverages existing corporate MFA requirements
- **Certificate Management**: Uses Walmart Enterprise PKI infrastructure

### Real-Time Synchronization
- **Sync Frequency**: Every 15 minutes for group membership changes
- **Emergency Sync**: Immediate sync triggered for security-related changes
- **Conflict Resolution**: Automated resolution with fallback to most restrictive access
- **Monitoring**: Real-time alerts for sync failures or permission conflicts

## 📊 Access Control Analytics

### Security Metrics
- **Login Success/Failure Rates**: Monitor authentication patterns
- **Permission Escalation Attempts**: Track unusual access requests
- **Group Membership Changes**: Audit all AD group modifications
- **Session Analytics**: Monitor user session patterns and anomalies

### Compliance Reporting
- **SOX Compliance**: Role segregation and access certification reports
- **Quarterly Access Reviews**: Automated reports for management review
- **Audit Trail Export**: Complete access history for compliance teams
- **Risk Assessment**: Automated identification of excessive permissions

## 🔐 Security Features

### Access Controls
- **Principle of Least Privilege**: Users receive minimum necessary access
- **Time-Based Access**: Temporary access grants with automatic expiration
- **Location-Based Restrictions**: IP address and location validation
- **Device Management**: Integration with corporate device management policies

### Monitoring and Alerting
- **Suspicious Activity Detection**: Machine learning-based anomaly detection
- **Failed Login Monitoring**: Automated alerts for multiple failed attempts
- **Permission Changes**: Real-time notifications for access modifications
- **Compliance Violations**: Immediate alerts for policy violations

## 🛠️ Administrative Tools

### Group Management Interface
- **Visual Group Mapper**: Drag-and-drop interface for group-to-role mapping
- **Bulk Operations**: Mass group membership changes with approval workflow
- **Permission Testing**: Test user access before deploying changes
- **Rollback Capability**: Quick rollback of group mapping changes

### Access Request Portal
- **Self-Service Requests**: Users can request additional access
- **Manager Approval**: Automated workflow for access approvals
- **Emergency Access**: Fast-track process for critical business needs
- **Access Reviews**: Periodic review and certification of user access

## 📋 Configuration Files

### `access-groups.json` Structure
```json
{
  "ad_integration": {
    "domain": "corp.walmart.com",
    "ldap_servers": [
      "ldap://dc1.corp.walmart.com:389",
      "ldap://dc2.corp.walmart.com:389"
    ],
    "service_account": "WMT\\ActivityHub_ServiceAccount",
    "sync_frequency_minutes": 15,
    "emergency_sync_enabled": true
  },
  "group_mappings": [
    {
      "ad_group": "WMT_ActivityHub_Executives",
      "activity_hub_roles": ["c-level-executive"],
      "permissions": ["enterprise.view.all"],
      "department_specific": false,
      "priority": 1
    }
  ],
  "access_policies": {
    "session_timeout_minutes": 480,
    "concurrent_sessions_allowed": 3,
    "ip_restrictions": {
      "enabled": true,
      "allowed_ranges": ["10.0.0.0/8", "172.16.0.0/12"]
    }
  }
}
```

## 🔄 Maintenance and Support

### Regular Maintenance Tasks
- **Monthly Group Reviews**: Validate group memberships and mappings
- **Quarterly Access Audits**: Comprehensive review of all access grants
- **Annual Policy Reviews**: Update access policies and procedures
- **Security Updates**: Apply patches and security improvements

### Support Procedures
- **Access Issues**: Escalation path for access-related problems
- **Emergency Procedures**: After-hours support for critical access needs
- **Change Management**: Controlled process for modifying access controls
- **Documentation Updates**: Maintain current access control procedures

## 📞 Support and Contacts

### Access Control Team
- **Primary Contact**: Walmart Enterprise Security Team
- **Emergency Contact**: IT Security Operations Center (24/7)
- **Policy Questions**: Information Security Policy Team
- **Technical Issues**: Active Directory Support Team

### Request Channels
- **Standard Requests**: ServiceNow self-service portal
- **Emergency Requests**: Call IT Security Operations Center
- **Policy Exceptions**: Submit to Information Security Team
- **Bulk Changes**: Contact Enterprise Security for approval

---

## 🏢 Integration Points

### Walmart Enterprise Systems
- **Workday**: Employee lifecycle management and role changes
- **ServiceNow**: Access request and incident management
- **Splunk**: Security monitoring and log analysis
- **CyberArk**: Privileged access management integration

### Compliance and Governance
- **Identity Governance**: Integration with enterprise identity management
- **Risk Management**: Automated risk assessment and reporting
- **Audit Support**: Complete audit trail and compliance reporting
- **Policy Enforcement**: Automated enforcement of corporate access policies

---

**Access Control Status**: ✅ Architecture Complete - Ready for Implementation  
**Last Updated**: November 6, 2025  
**Version**: 1.0.0  
**Owner**: Kendall Rush (kendall.rush@walmart.com)

Secure your Activity Hub with enterprise-grade access control and seamless AD integration. 🔐