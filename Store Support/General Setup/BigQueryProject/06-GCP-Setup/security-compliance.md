# Security and Compliance Configuration

## Security Baseline Configuration

### Identity and Access Management (IAM)

#### Service Account Security
- [ ] **Minimal Permissions**: Apply principle of least privilege
- [ ] **Key Rotation**: Enable automatic service account key rotation (90 days)
- [ ] **Key Management**: Use Cloud KMS for service account keys
- [ ] **No Default Service Accounts**: Disable default compute service accounts

```yaml
# Service Account Policy Template
bindings:
  - members:
    - serviceAccount:app-service@project.iam.gserviceaccount.com
    role: roles/custom.applicationRunner
  condition:
    title: "Time-based access"
    expression: "request.time.getHours() >= 6 && request.time.getHours() <= 22"
```

#### User Access Controls
- [ ] **Multi-Factor Authentication**: Enforce MFA for all users
- [ ] **Session Management**: Set session timeout to 8 hours
- [ ] **IP Restrictions**: Limit access to Walmart office networks
- [ ] **Regular Access Reviews**: Monthly access audits

### Organization Policies

#### Mandatory Walmart Policies
```yaml
# org-policies.yaml
policies:
  compute.restrictLoadBalancerCreationForTypes:
    listPolicy:
      allowedValues:
        - "EXTERNAL_1_TO_1_NAT"
        - "INTERNAL_MANAGED"
  
  compute.requireOsLogin:
    booleanPolicy:
      enforced: true
  
  compute.restrictXpnProjectLienRemoval:
    booleanPolicy:
      enforced: true
  
  storage.uniformBucketLevelAccess:
    booleanPolicy:
      enforced: true
```

### Network Security

#### VPC Security Configuration
- [ ] **Private Google Access**: Enable for all subnets
- [ ] **VPC Flow Logs**: Enable for security monitoring
- [ ] **Private Service Connect**: Use for Google APIs access
- [ ] **Network Segmentation**: Implement defense in depth

#### Firewall Rules Template
```yaml
# firewall-rules.yaml
rules:
  - name: allow-health-checks
    direction: INGRESS
    sourceRanges:
      - 130.211.0.0/22
      - 35.191.0.0/16
    allowed:
      - IPProtocol: tcp
        ports: ["80", "443", "8080"]
  
  - name: deny-all-ingress
    direction: INGRESS
    priority: 65534
    action: DENY
    sourceRanges: ["0.0.0.0/0"]
```

## Data Protection and Encryption

### Encryption Standards

#### Encryption at Rest
- [ ] **Customer-Managed Encryption Keys (CMEK)**: Use Cloud KMS
- [ ] **Database Encryption**: Enable for Cloud SQL instances
- [ ] **Storage Encryption**: Default encryption for Cloud Storage
- [ ] **Compute Disk Encryption**: Encrypt all persistent disks

#### Cloud KMS Configuration
```yaml
# kms-config.yaml
keyRings:
  - name: walmart-app-keyring
    location: us-central1
    keys:
      - name: database-key
        purpose: ENCRYPT_DECRYPT
        algorithm: GOOGLE_SYMMETRIC_ENCRYPTION
        rotationPeriod: 7776000s  # 90 days
      - name: storage-key
        purpose: ENCRYPT_DECRYPT
        algorithm: GOOGLE_SYMMETRIC_ENCRYPTION
        rotationPeriod: 7776000s
```

### Data Classification and Handling

#### Data Classification Labels
- [ ] **Confidential**: Customer PII, payment data, trade secrets
- [ ] **Internal**: Employee data, internal processes
- [ ] **Public**: Marketing materials, public documentation
- [ ] **Restricted**: Legal documents, audit data

#### Data Loss Prevention (DLP)
```yaml
# dlp-config.yaml
inspectTemplates:
  - name: walmart-pii-detection
    inspectConfig:
      infoTypes:
        - name: CREDIT_CARD_NUMBER
        - name: US_SOCIAL_SECURITY_NUMBER
        - name: EMAIL_ADDRESS
        - name: PHONE_NUMBER
      minLikelihood: LIKELY
      limits:
        maxFindingsPerRequest: 100
```

## Compliance Framework Implementation

### PCI DSS Compliance (if applicable)

#### Network Requirements
- [ ] **Network Segmentation**: Isolate cardholder data environment
- [ ] **DMZ Implementation**: Deploy web applications in DMZ
- [ ] **Access Control Lists**: Restrict access to cardholder data
- [ ] **Regular Penetration Testing**: Schedule quarterly pen tests

#### Audit Requirements
```yaml
# pci-audit-config.yaml
auditLogs:
  - service: cloudresourcemanager.googleapis.com
    auditLogConfigs:
      - logType: ADMIN_READ
      - logType: DATA_READ
      - logType: DATA_WRITE
  
  - service: compute.googleapis.com
    auditLogConfigs:
      - logType: ADMIN_READ
      - logType: DATA_READ
      - logType: DATA_WRITE
```

### SOX Compliance

#### Change Management Controls
- [ ] **Infrastructure as Code**: Use Terraform for all changes
- [ ] **Approval Workflows**: Implement change approval process
- [ ] **Segregation of Duties**: Separate development and production access
- [ ] **Change Documentation**: Document all infrastructure changes

#### Access Controls
```yaml
# sox-rbac.yaml
roles:
  - name: sox-developer
    permissions:
      - compute.instances.list
      - compute.instances.get
      - logging.logs.list
    bindings:
      - members: ["group:developers@walmart.com"]
        conditions:
          - title: "Development environment only"
            expression: "resource.name.startsWith('projects/wmt-dev-')"
```

## Security Monitoring and Incident Response

### Security Command Center Setup

#### Asset Discovery
- [ ] **Asset Inventory**: Enable automatic asset discovery
- [ ] **Security Marks**: Apply security classification labels
- [ ] **Finding Sources**: Enable all security finding sources
- [ ] **Custom Detectors**: Configure Walmart-specific security rules

#### Security Findings Configuration
```yaml
# scc-config.yaml
notificationConfig:
  - name: walmart-security-notifications
    description: "Critical security findings"
    pubsubTopic: projects/wmt-security/topics/security-alerts
    filter: "severity=\"HIGH\" OR severity=\"CRITICAL\""
```

### Binary Authorization

#### Container Security Policy
```yaml
# binauthz-policy.yaml
admissionWhitelistPatterns:
  - namePattern: "gcr.io/wmt-trusted-images/*"
defaultAdmissionRule:
  requireAttestationsBy:
    - projects/wmt-security/attestors/security-attestor
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
```

### Vulnerability Management

#### Container Scanning
- [ ] **Enable Container Analysis API**: Scan all container images
- [ ] **Critical Vulnerability Alerts**: Alert on critical CVEs
- [ ] **Base Image Updates**: Regular base image patching
- [ ] **Policy Enforcement**: Block deployment of vulnerable images

#### VM Scanning
```yaml
# vm-scanning.yaml
osConfig:
  patchDeployments:
    - name: walmart-security-patches
      instanceFilter:
        labels:
          patch-group: "production"
      patchConfig:
        rebootConfig: REBOOT_IF_REQUIRED
        apt:
          type: UPGRADE
        yum:
          security: true
          minimal: true
```

## Incident Response Procedures

### Security Incident Response Plan

#### Immediate Response (0-15 minutes)
1. **Identify and Isolate**: Identify affected resources and isolate if possible
2. **Alert Team**: Notify Walmart Security Operations Center (SOC)
3. **Preserve Evidence**: Take snapshots of affected systems
4. **Initial Assessment**: Determine scope and potential impact

#### Investigation Phase (15 minutes - 4 hours)
1. **Forensic Analysis**: Analyze logs and system state
2. **Impact Assessment**: Determine data or system compromise
3. **Stakeholder Notification**: Notify business stakeholders
4. **Regulatory Assessment**: Determine if regulatory notification required

#### Recovery and Remediation (4+ hours)
1. **System Recovery**: Restore systems from clean backups
2. **Patch Vulnerabilities**: Apply security patches
3. **Access Review**: Review and revoke compromised access
4. **Monitoring Enhancement**: Improve detection capabilities

### Contact Information

#### Internal Contacts
- **Walmart SOC**: [Emergency Number] / [Email]
- **Legal Team**: [Contact Information]
- **PR/Communications**: [Contact Information]
- **Business Continuity**: [Contact Information]

#### External Contacts
- **Google Cloud Support**: [Enterprise Support Number]
- **Law Enforcement**: Local FBI Cyber Crime Unit
- **Regulatory Bodies**: PCI Council, State AGs (as applicable)

## Compliance Validation and Reporting

### Regular Assessments
- [ ] **Monthly**: Access reviews and privilege validation
- [ ] **Quarterly**: Vulnerability assessments and penetration testing
- [ ] **Semi-Annual**: Compliance audits (PCI, SOX)
- [ ] **Annual**: Security architecture review

### Reporting Templates
```yaml
# compliance-reports.yaml
reports:
  - name: monthly-access-review
    schedule: "0 0 1 * *"  # First day of each month
    recipients:
      - security-team@walmart.com
      - compliance-team@walmart.com
  
  - name: quarterly-vulnerability-summary
    schedule: "0 0 1 1,4,7,10 *"  # Quarterly
    recipients:
      - ciso@walmart.com
      - risk-management@walmart.com
```

## Audit Trail Requirements

### Logging Configuration
- [ ] **Admin Activity Logs**: All administrative actions
- [ ] **Data Access Logs**: All data read/write operations
- [ ] **System Event Logs**: All system-level events
- [ ] **Application Logs**: Application-specific audit events

### Log Retention Policies
- **Security Logs**: 7 years retention
- **Audit Logs**: 7 years retention (SOX requirement)
- **Application Logs**: 3 years retention
- **Debug Logs**: 90 days retention

### Log Export Configuration
```yaml
# log-export.yaml
sinks:
  - name: security-logs-to-bigquery
    destination: bigquery.googleapis.com/projects/wmt-security/datasets/audit_logs
    filter: 'protoPayload.serviceName="cloudresourcemanager.googleapis.com" OR protoPayload.serviceName="iam.googleapis.com"'
  
  - name: audit-logs-to-storage
    destination: storage.googleapis.com/wmt-audit-logs-bucket
    filter: 'logName:"cloudaudit.googleapis.com"'
```