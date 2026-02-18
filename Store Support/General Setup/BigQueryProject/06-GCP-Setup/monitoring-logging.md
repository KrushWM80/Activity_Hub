# Monitoring and Logging Setup Guide

## Cloud Monitoring Configuration

### Workspace Setup

#### Create Monitoring Workspace
```bash
# Create monitoring workspace
gcloud alpha monitoring workspaces create \
  --workspace-name="walmart-monitoring-workspace" \
  --description="Centralized monitoring for Walmart GCP projects"
```

#### Workspace Configuration
- [ ] **Multi-Project Monitoring**: Include all related projects
- [ ] **Metrics Scope**: Define scope for cross-project monitoring
- [ ] **Notification Channels**: Configure email, SMS, and Slack channels
- [ ] **Uptime Checks**: Set up external monitoring for critical endpoints

### Alert Policies

#### Infrastructure Alerts
```yaml
# infrastructure-alerts.yaml
alertPolicies:
  - displayName: "High CPU Utilization"
    conditions:
      - displayName: "CPU usage above 80%"
        conditionThreshold:
          filter: 'resource.type="gce_instance"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 0.8
          duration: 300s
    notificationChannels:
      - "projects/wmt-monitoring/notificationChannels/email-alerts"
    alertStrategy:
      autoClose: 86400s  # 24 hours

  - displayName: "Memory Usage Critical"
    conditions:
      - displayName: "Memory usage above 90%"
        conditionThreshold:
          filter: 'resource.type="gce_instance" AND metric.type="compute.googleapis.com/instance/memory/utilization"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 0.9
          duration: 180s
    severity: CRITICAL

  - displayName: "Disk Space Warning"
    conditions:
      - displayName: "Disk usage above 85%"
        conditionThreshold:
          filter: 'resource.type="gce_instance" AND metric.type="compute.googleapis.com/instance/disk/utilization"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 0.85
          duration: 300s
```

#### Application Performance Alerts
```yaml
# application-alerts.yaml
alertPolicies:
  - displayName: "High Error Rate"
    conditions:
      - displayName: "Error rate above 5%"
        conditionThreshold:
          filter: 'resource.type="gae_app" AND metric.type="appengine.googleapis.com/http/server/response_count"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 0.05
          duration: 300s
    severity: HIGH

  - displayName: "Response Time Degradation"
    conditions:
      - displayName: "95th percentile latency above 2 seconds"
        conditionThreshold:
          filter: 'metric.type="loadbalancing.googleapis.com/https/request_duration"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 2000  # milliseconds
          duration: 600s

  - displayName: "Low Availability"
    conditions:
      - displayName: "Uptime check failure"
        conditionAbsent:
          filter: 'metric.type="monitoring.googleapis.com/uptime_check/check_passed"'
          duration: 300s
    severity: CRITICAL
```

### Custom Dashboards

#### Infrastructure Dashboard
```yaml
# infrastructure-dashboard.yaml
dashboard:
  displayName: "Walmart Infrastructure Overview"
  mosaicLayout:
    tiles:
      - width: 6
        height: 4
        widget:
          title: "CPU Utilization by Instance"
          xyChart:
            dataSets:
              - timeSeriesQuery:
                  filter: 'resource.type="gce_instance"'
                  unitOverride: "1"
                plotType: LINE
            yAxis:
              scale: LINEAR
      
      - width: 6
        height: 4
        widget:
          title: "Memory Usage"
          xyChart:
            dataSets:
              - timeSeriesQuery:
                  filter: 'metric.type="compute.googleapis.com/instance/memory/utilization"'
                plotType: STACKED_AREA

      - width: 12
        height: 4
        widget:
          title: "Network Traffic"
          xyChart:
            dataSets:
              - timeSeriesQuery:
                  filter: 'metric.type="compute.googleapis.com/instance/network/received_bytes_count"'
                plotType: LINE
```

#### Application Dashboard
```yaml
# application-dashboard.yaml
dashboard:
  displayName: "Application Performance Monitoring"
  mosaicLayout:
    tiles:
      - widget:
          title: "Request Rate"
          scorecard:
            timeSeriesQuery:
              filter: 'metric.type="loadbalancing.googleapis.com/https/request_count"'
            sparkChartView:
              sparkChartType: SPARK_LINE

      - widget:
          title: "Error Rate"
          scorecard:
            timeSeriesQuery:
              filter: 'metric.type="logging.googleapis.com/user/error_count"'
            gaugeView:
              lowerBound: 0
              upperBound: 10

      - widget:
          title: "Response Time Distribution"
          xyChart:
            dataSets:
              - timeSeriesQuery:
                  filter: 'metric.type="loadbalancing.googleapis.com/https/request_duration"'
                plotType: STACKED_BAR
```

## Logging Configuration

### Cloud Logging Setup

#### Log Router Configuration
```yaml
# log-routing.yaml
sinks:
  - name: "security-logs-to-bigquery"
    destination: "bigquery.googleapis.com/projects/wmt-security-logs/datasets/security_audit"
    filter: |
      protoPayload.serviceName="cloudresourcemanager.googleapis.com"
      OR protoPayload.serviceName="iam.googleapis.com"
      OR protoPayload.serviceName="compute.googleapis.com"
      OR severity>=ERROR
    exclusions:
      - name: "exclude-health-checks"
        filter: 'httpRequest.userAgent="GoogleHC/1.0"'

  - name: "application-logs-to-storage"
    destination: "storage.googleapis.com/wmt-app-logs"
    filter: |
      resource.type="gae_app"
      OR resource.type="k8s_container"
      OR resource.type="cloud_function"
    
  - name: "audit-logs-long-term"
    destination: "storage.googleapis.com/wmt-audit-archive"
    filter: 'logName:"/logs/cloudaudit.googleapis.com"'
```

#### Log-Based Metrics
```yaml
# log-metrics.yaml
metrics:
  - name: "error_count_by_service"
    description: "Count of errors by service"
    filter: 'severity>=ERROR'
    labelExtractors:
      service: 'EXTRACT(resource.labels.service_name)'
      error_type: 'EXTRACT(jsonPayload.error_type)'
    metricDescriptor:
      metricKind: COUNTER
      valueType: INT64

  - name: "security_events"
    description: "Security-related events"
    filter: |
      protoPayload.serviceName="iam.googleapis.com"
      AND (protoPayload.methodName:"SetIamPolicy"
      OR protoPayload.methodName:"CreateServiceAccount"
      OR protoPayload.methodName:"DeleteServiceAccount")
    metricDescriptor:
      metricKind: COUNTER
      valueType: INT64

  - name: "failed_authentication_attempts"
    description: "Failed authentication attempts"
    filter: 'protoPayload.authenticationInfo.principalEmail!="" AND severity="ERROR"'
    labelExtractors:
      user: 'EXTRACT(protoPayload.authenticationInfo.principalEmail)'
    metricDescriptor:
      metricKind: COUNTER
      valueType: INT64
```

### Application Logging Standards

#### Structured Logging Format
```json
{
  "timestamp": "2025-10-24T14:30:00.000Z",
  "severity": "INFO",
  "service": "walmart-inventory-service",
  "version": "1.2.3",
  "trace": "projects/wmt-retail/traces/4bf92f3577b34da6a3ce929d0e0e4736",
  "span": "span-id-12345",
  "message": "Processing inventory update",
  "context": {
    "userId": "user123",
    "storeId": "store456",
    "operation": "update_inventory",
    "items_processed": 150
  },
  "labels": {
    "environment": "production",
    "team": "inventory-team",
    "cost-center": "CC-RETAIL-001"
  }
}
```

#### Log Levels and Usage
- [ ] **CRITICAL**: System failures requiring immediate attention
- [ ] **ERROR**: Application errors that affect functionality
- [ ] **WARNING**: Potential issues or degraded performance
- [ ] **INFO**: Normal operations and business events
- [ ] **DEBUG**: Detailed troubleshooting information (dev/test only)

### Audit Logging Configuration

#### Enable Audit Logs
```yaml
# audit-config.yaml
auditConfigs:
  - service: allServices
    auditLogConfigs:
      - logType: ADMIN_READ
        exemptedMembers:
          - "serviceAccount:monitoring@wmt-project.iam.gserviceaccount.com"
      - logType: DATA_READ
        exemptedMembers:
          - "serviceAccount:app-service@wmt-project.iam.gserviceaccount.com"
      - logType: DATA_WRITE

  - service: storage.googleapis.com
    auditLogConfigs:
      - logType: DATA_READ
      - logType: DATA_WRITE

  - service: bigquery.googleapis.com
    auditLogConfigs:
      - logType: DATA_READ
      - logType: DATA_WRITE
```

## Performance Monitoring

### Application Performance Monitoring (APM)

#### Cloud Trace Configuration
```yaml
# trace-config.yaml
tracingConfig:
  samplingRate: 0.1  # Sample 10% of requests
  spanKinds:
    - SERVER
    - CLIENT
    - PRODUCER
    - CONSUMER
  attributeKeys:
    - user.id
    - store.id
    - transaction.id
```

#### Cloud Profiler Setup
```yaml
# profiler-config.yaml
profilerConfig:
  serviceNames:
    - "walmart-inventory-service"
    - "walmart-pricing-service"
    - "walmart-checkout-service"
  profileTypes:
    - CPU
    - HEAP
    - THREADS
  duration: "60s"
  interval: "60s"
```

### Service Level Objectives (SLOs)

#### SLO Configuration
```yaml
# slo-config.yaml
serviceLevelObjectives:
  - displayName: "API Availability SLO"
    serviceLevelIndicator:
      requestBased:
        distributionCut:
          range:
            min: 0
            max: 500  # 500ms threshold
    goal: 0.99  # 99% availability
    rollingPeriod: 2592000s  # 30 days

  - displayName: "Error Rate SLO"
    serviceLevelIndicator:
      requestBased:
        goodTotalRatio:
          goodServiceFilter: 'metric.type="loadbalancing.googleapis.com/https/request_count" AND metric.labels.response_code!~"5.*"'
          totalServiceFilter: 'metric.type="loadbalancing.googleapis.com/https/request_count"'
    goal: 0.995  # 99.5% success rate
    rollingPeriod: 2592000s

  - displayName: "Latency SLO"
    serviceLevelIndicator:
      requestBased:
        distributionCut:
          range:
            min: 0
            max: 2000  # 2 seconds
    goal: 0.95  # 95% of requests under 2s
    rollingPeriod: 86400s  # 1 day
```

## Uptime Monitoring

### External Monitoring Setup
```yaml
# uptime-checks.yaml
uptimeCheckConfigs:
  - displayName: "Walmart E-commerce Site"
    httpCheck:
      path: "/health"
      port: 443
      useSsl: true
      validateSsl: true
    monitoredResource:
      type: "uptime_url"
      labels:
        host: "walmart.com"
    checkIntervalSeconds: 60
    timeout: 10s
    selectedRegions:
      - "USA_IOWA"
      - "USA_OREGON"
      - "USA_VIRGINIA"

  - displayName: "Internal API Health Check"
    httpCheck:
      path: "/api/v1/health"
      port: 8080
      headers:
        Authorization: "Bearer ${SECRET_TOKEN}"
    monitoredResource:
      type: "gce_instance"
      labels:
        instance_id: "api-server-1"
    checkIntervalSeconds: 30
```

## Error Reporting

### Error Reporting Configuration
```yaml
# error-reporting.yaml
errorReportingConfig:
  reportErrors: true
  services:
    - "walmart-inventory-service"
    - "walmart-pricing-service"
    - "walmart-checkout-service"
  
  notificationChannels:
    - "projects/wmt-monitoring/notificationChannels/dev-team-slack"
    - "projects/wmt-monitoring/notificationChannels/oncall-email"
  
  errorFilters:
    - name: "Critical Errors Only"
      filter: 'severity="CRITICAL" OR message:"NullPointerException"'
    - name: "Production Errors"
      filter: 'serviceContext.service!="test-service"'
```

## Notification Channels

### Notification Configuration
```yaml
# notification-channels.yaml
notificationChannels:
  - type: "email"
    displayName: "Development Team Email"
    description: "Email notifications for development team"
    labels:
      email_address: "dev-team@walmart.com"
    enabled: true

  - type: "slack"
    displayName: "Operations Slack Channel"
    description: "Slack notifications for operations team"
    labels:
      channel_name: "#walmart-ops-alerts"
      webhook_url: "${SLACK_WEBHOOK_URL}"
    enabled: true

  - type: "sms"
    displayName: "On-Call SMS"
    description: "SMS notifications for critical alerts"
    labels:
      number: "+1-555-0123"
    enabled: true

  - type: "pagerduty"
    displayName: "PagerDuty Integration"
    description: "PagerDuty integration for critical incidents"
    labels:
      service_key: "${PAGERDUTY_SERVICE_KEY}"
    enabled: true
```

## Log Analysis and Querying

### BigQuery Log Analysis
```sql
-- Query to analyze error patterns
SELECT
  timestamp,
  severity,
  resource.labels.service_name as service,
  jsonPayload.error_type as error_type,
  COUNT(*) as error_count
FROM
  `wmt-security-logs.security_audit.cloudaudit_googleapis_com_*`
WHERE
  _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
  AND severity = 'ERROR'
GROUP BY
  timestamp, severity, service, error_type
ORDER BY
  error_count DESC
LIMIT 100;

-- Query to analyze security events
SELECT
  timestamp,
  protoPayload.authenticationInfo.principalEmail as user,
  protoPayload.methodName as method,
  protoPayload.resourceName as resource,
  COUNT(*) as event_count
FROM
  `wmt-security-logs.security_audit.cloudaudit_googleapis_com_*`
WHERE
  _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
  AND protoPayload.serviceName = 'iam.googleapis.com'
GROUP BY
  timestamp, user, method, resource
ORDER BY
  event_count DESC;
```

### Log Export for Long-term Storage
```yaml
# log-export-jobs.yaml
exportJobs:
  - name: "daily-audit-export"
    schedule: "0 2 * * *"  # Daily at 2 AM
    query: |
      SELECT *
      FROM `wmt-security-logs.security_audit.cloudaudit_googleapis_com_*`
      WHERE _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
    destination: "gs://wmt-audit-archive/year={year}/month={month}/day={day}/"
    format: "PARQUET"
    compression: "GZIP"

  - name: "weekly-performance-export"
    schedule: "0 3 * * 0"  # Weekly on Sunday at 3 AM
    query: |
      SELECT
        timestamp,
        resource.type,
        metric.type,
        metric.labels,
        points.value
      FROM `wmt-monitoring.metrics.monitoring_*`
      WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
    destination: "gs://wmt-performance-archive/"
```

## Monitoring Automation

### Automated Remediation
```yaml
# auto-remediation.yaml
cloudFunctions:
  - name: "auto-scale-function"
    trigger:
      eventTrigger:
        eventType: "google.monitoring.alertPolicy.conditionDisplayNameEventType"
        resource: "projects/wmt-project/alertPolicies/high-cpu-alert"
    sourceArchiveUrl: "gs://wmt-functions/auto-scale.zip"
    
  - name: "security-response-function"
    trigger:
      eventTrigger:
        eventType: "google.logging.logEntry"
        resource: "projects/wmt-project"
        filter: 'protoPayload.methodName:"SetIamPolicy" AND severity="WARNING"'
    sourceArchiveUrl: "gs://wmt-functions/security-response.zip"
```