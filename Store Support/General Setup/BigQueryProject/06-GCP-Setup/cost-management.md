# Cost Management and Budgeting Guide

## Budget Planning and Setup

### Project Budget Configuration

#### Budget Creation
```yaml
# budget-config.yaml
budgets:
  - displayName: "Production Environment Budget"
    budgetFilter:
      projects:
        - "projects/wmt-retail-prod"
      creditTypesTreatment: INCLUDE_ALL_CREDITS
      services:
        - "services/6F81-5844-456A"  # Compute Engine
        - "services/95FF-2EF5-5EA1"  # Cloud Storage
        - "services/24E6-581D-38E5"  # BigQuery
    amount:
      specifiedAmount:
        currencyCode: "USD"
        units: "5000"  # $5,000/month
    thresholdRules:
      - thresholdPercent: 0.5
        spendBasis: CURRENT_SPEND
      - thresholdPercent: 0.8
        spendBasis: CURRENT_SPEND
      - thresholdPercent: 1.0
        spendBasis: CURRENT_SPEND
        alertEmailRecipients:
          - "finance-team@walmart.com"
          - "cloud-ops@walmart.com"

  - displayName: "Development Environment Budget"
    budgetFilter:
      projects:
        - "projects/wmt-retail-dev"
        - "projects/wmt-retail-staging"
    amount:
      specifiedAmount:
        currencyCode: "USD"
        units: "1000"  # $1,000/month
    thresholdRules:
      - thresholdPercent: 0.8
        spendBasis: CURRENT_SPEND
      - thresholdPercent: 1.0
        spendBasis: CURRENT_SPEND
```

#### Cost Center Allocation
- [ ] **Tag Resources**: Apply cost center labels to all resources
- [ ] **Department Mapping**: Map projects to Walmart departments
- [ ] **Team Attribution**: Assign costs to specific development teams
- [ ] **Project Lifecycle**: Track costs across project phases

### Budget Alert Configuration

#### Alert Thresholds
```yaml
# budget-alerts.yaml
alertPolicies:
  - displayName: "Budget Alert - 50% Threshold"
    conditions:
      - displayName: "50% of budget consumed"
        conditionThreshold:
          filter: 'resource.type="billing_account"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 0.5
    notificationChannels:
      - "projects/wmt-billing/notificationChannels/team-leads"
    severity: WARNING

  - displayName: "Budget Alert - 80% Threshold"
    conditions:
      - displayName: "80% of budget consumed"
        conditionThreshold:
          filter: 'resource.type="billing_account"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 0.8
    notificationChannels:
      - "projects/wmt-billing/notificationChannels/finance-team"
    severity: HIGH

  - displayName: "Budget Alert - 100% Threshold"
    conditions:
      - displayName: "Budget exceeded"
        conditionThreshold:
          filter: 'resource.type="billing_account"'
          comparison: COMPARISON_GREATER_THAN
          thresholdValue: 1.0
    notificationChannels:
      - "projects/wmt-billing/notificationChannels/executives"
    severity: CRITICAL
```

## Cost Optimization Strategies

### Compute Cost Optimization

#### Right-sizing Recommendations
- [ ] **Machine Type Analysis**: Use rightsizing recommendations
- [ ] **Utilization Monitoring**: Track CPU, memory, and disk usage
- [ ] **Preemptible Instances**: Use for non-critical workloads (up to 80% savings)
- [ ] **Custom Machine Types**: Create optimized configurations

```yaml
# compute-optimization.yaml
computeOptimization:
  preemptibleInstances:
    workloadTypes:
      - "batch-processing"
      - "data-analysis"
      - "CI/CD-pipelines"
    excludeWorkloads:
      - "production-web-servers"
      - "database-servers"
      - "real-time-processing"

  autoScaling:
    minInstances: 2
    maxInstances: 10
    targetCpuUtilization: 0.6
    scaleInControlled:
      maxScaleInPercentage: 50
      timeWindowMinutes: 5

  scheduledScaling:
    - name: "business-hours-scaling"
      schedule: "0 8 * * 1-5"  # Scale up at 8 AM Mon-Fri
      targetSize: 5
    - name: "after-hours-scaling"
      schedule: "0 18 * * 1-5"  # Scale down at 6 PM Mon-Fri
      targetSize: 2
```

#### Committed Use Discounts
```yaml
# committed-use.yaml
commitments:
  - region: "us-central1"
    resourceType: "compute"
    commitment:
      vcpu: 100
      memory: 400  # GB
    term: "12_MONTH"
    estimatedSavings: "25%"

  - region: "us-east1"
    resourceType: "memory"
    commitment:
      memory: 200  # GB
    term: "36_MONTH"
    estimatedSavings: "57%"
```

### Storage Cost Optimization

#### Storage Class Management
```yaml
# storage-lifecycle.yaml
lifecycleRules:
  - condition:
      age: 30
      matchesStorageClass: ["STANDARD"]
    action:
      type: "SetStorageClass"
      storageClass: "NEARLINE"
  
  - condition:
      age: 90
      matchesStorageClass: ["NEARLINE"]
    action:
      type: "SetStorageClass"
      storageClass: "COLDLINE"
  
  - condition:
      age: 365
      matchesStorageClass: ["COLDLINE"]
    action:
      type: "SetStorageClass"
      storageClass: "ARCHIVE"
  
  - condition:
      age: 2555  # 7 years
      matchesStorageClass: ["ARCHIVE"]
    action:
      type: "Delete"
```

#### Storage Usage Optimization
- [ ] **Data Compression**: Enable compression for stored data
- [ ] **Duplicate Detection**: Implement deduplication strategies
- [ ] **Archive Policies**: Move old data to cheaper storage classes
- [ ] **Regional Optimization**: Use regional storage for better performance and cost

### Network Cost Optimization

#### Network Traffic Analysis
```yaml
# network-optimization.yaml
networkOptimization:
  egressMonitoring:
    thresholds:
      warning: "1TB"
      critical: "5TB"
    regions:
      - "us-central1"
      - "us-east1"
    
  cdnConfiguration:
    enableCloudCDN: true
    cacheMode: "CACHE_ALL_STATIC"
    defaultTtl: 3600
    maxTtl: 86400
    
  loadBalancerOptimization:
    enableHttp2: true
    enableCompression: true
    connectionDraining: 300  # seconds
```

## Cost Tracking and Reporting

### Billing Export Configuration

#### BigQuery Export Setup
```sql
-- Create dataset for billing export
CREATE SCHEMA IF NOT EXISTS `wmt-billing.cost_analysis`
OPTIONS(
  description="Walmart cost analysis and reporting",
  location="US"
);

-- Create detailed billing table
CREATE TABLE IF NOT EXISTS `wmt-billing.cost_analysis.detailed_billing`
(
  billing_account_id STRING,
  service_id STRING,
  service_description STRING,
  sku_id STRING,
  sku_description STRING,
  project_id STRING,
  project_name STRING,
  location STRING,
  export_time TIMESTAMP,
  cost NUMERIC,
  currency STRING,
  currency_conversion_rate NUMERIC,
  usage_amount NUMERIC,
  usage_unit STRING,
  labels ARRAY<STRUCT<key STRING, value STRING>>,
  system_labels ARRAY<STRUCT<key STRING, value STRING>>,
  credits ARRAY<STRUCT<
    name STRING,
    amount NUMERIC,
    type STRING
  >>
)
PARTITION BY DATE(export_time)
CLUSTER BY project_id, service_id;
```

#### Cost Analysis Queries
```sql
-- Monthly cost breakdown by project
SELECT
  project_name,
  service_description,
  DATE_TRUNC(DATE(export_time), MONTH) as month,
  SUM(cost) as total_cost,
  ARRAY_AGG(DISTINCT location IGNORE NULLS) as locations
FROM `wmt-billing.cost_analysis.detailed_billing`
WHERE DATE(export_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY project_name, service_description, month
ORDER BY month DESC, total_cost DESC;

-- Cost by team/department
SELECT
  EXTRACT(key FROM label WHERE key = 'team') as team,
  EXTRACT(key FROM label WHERE key = 'cost-center') as cost_center,
  DATE_TRUNC(DATE(export_time), WEEK) as week,
  SUM(cost) as weekly_cost,
  COUNT(DISTINCT project_id) as project_count
FROM `wmt-billing.cost_analysis.detailed_billing`,
  UNNEST(labels) as label
WHERE DATE(export_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 8 WEEK)
  AND label.key IN ('team', 'cost-center')
GROUP BY team, cost_center, week
ORDER BY week DESC, weekly_cost DESC;

-- Identify cost anomalies
WITH daily_costs as (
  SELECT
    project_id,
    service_description,
    DATE(export_time) as date,
    SUM(cost) as daily_cost
  FROM `wmt-billing.cost_analysis.detailed_billing`
  WHERE DATE(export_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY project_id, service_description, date
),
cost_stats as (
  SELECT
    project_id,
    service_description,
    AVG(daily_cost) as avg_cost,
    STDDEV(daily_cost) as stddev_cost
  FROM daily_costs
  GROUP BY project_id, service_description
)
SELECT
  dc.project_id,
  dc.service_description,
  dc.date,
  dc.daily_cost,
  cs.avg_cost,
  (dc.daily_cost - cs.avg_cost) / cs.stddev_cost as z_score
FROM daily_costs dc
JOIN cost_stats cs USING (project_id, service_description)
WHERE ABS((dc.daily_cost - cs.avg_cost) / cs.stddev_cost) > 2
ORDER BY ABS(z_score) DESC;
```

### Cost Reporting Dashboards

#### Executive Summary Dashboard
```yaml
# executive-dashboard.yaml
dashboard:
  displayName: "Walmart GCP Cost Executive Summary"
  mosaicLayout:
    tiles:
      - width: 6
        height: 4
        widget:
          title: "Monthly Spend Trend"
          xyChart:
            dataSets:
              - timeSeriesQuery:
                  filter: 'resource.type="billing_account"'
                plotType: LINE
            yAxis:
              label: "Cost (USD)"

      - width: 6
        height: 4
        widget:
          title: "Budget Utilization"
          scorecard:
            timeSeriesQuery:
              filter: 'metric.type="billing.googleapis.com/billing/percent_budget_used"'
            gaugeView:
              lowerBound: 0
              upperBound: 100

      - width: 6
        height: 4
        widget:
          title: "Cost by Service"
          pieChart:
            dataSets:
              - timeSeriesQuery:
                  filter: 'resource.type="billing_account"'
            chartType: DONUT

      - width: 6
        height: 4
        widget:
          title: "Cost by Project"
          table:
            dataSets:
              - timeSeriesQuery:
                  filter: 'resource.type="billing_account"'
            metricVisualization: BAR
```

### Automated Cost Alerts

#### Cost Anomaly Detection
```yaml
# cost-anomaly-detection.yaml
cloudFunctions:
  - name: "cost-anomaly-detector"
    runtime: "python39"
    trigger:
      eventTrigger:
        eventType: "google.pubsub.topic.publish"
        resource: "projects/wmt-billing/topics/billing-export"
    environmentVariables:
      ANOMALY_THRESHOLD: "2.0"  # Z-score threshold
      NOTIFICATION_TOPIC: "projects/wmt-billing/topics/cost-alerts"
    
    code: |
      import base64
      import json
      from google.cloud import bigquery
      from google.cloud import pubsub_v1

      def detect_anomalies(event, context):
          # Query for cost anomalies
          client = bigquery.Client()
          query = """
          WITH daily_costs AS (
              SELECT
                  project_id,
                  service_description,
                  DATE(export_time) as date,
                  SUM(cost) as daily_cost
              FROM `wmt-billing.cost_analysis.detailed_billing`
              WHERE DATE(export_time) = CURRENT_DATE()
              GROUP BY project_id, service_description, date
          ),
          historical_avg AS (
              SELECT
                  project_id,
                  service_description,
                  AVG(cost) as avg_cost,
                  STDDEV(cost) as stddev_cost
              FROM `wmt-billing.cost_analysis.detailed_billing`
              WHERE DATE(export_time) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
                    AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
              GROUP BY project_id, service_description
          )
          SELECT
              dc.project_id,
              dc.service_description,
              dc.daily_cost,
              ha.avg_cost,
              (dc.daily_cost - ha.avg_cost) / ha.stddev_cost as z_score
          FROM daily_costs dc
          JOIN historical_avg ha USING (project_id, service_description)
          WHERE ABS((dc.daily_cost - ha.avg_cost) / ha.stddev_cost) > 2
          """
          
          results = client.query(query).to_dataframe()
          
          if not results.empty:
              # Send alert
              publisher = pubsub_v1.PublisherClient()
              topic_path = publisher.topic_path('wmt-billing', 'cost-alerts')
              
              for _, row in results.iterrows():
                  alert_data = {
                      'project_id': row['project_id'],
                      'service': row['service_description'],
                      'current_cost': float(row['daily_cost']),
                      'average_cost': float(row['avg_cost']),
                      'anomaly_score': float(row['z_score'])
                  }
                  
                  publisher.publish(topic_path, json.dumps(alert_data).encode('utf-8'))
```

## Resource Quota Management

### Quota Configuration
```yaml
# quota-management.yaml
quotas:
  compute:
    instances: 50
    cpus: 500
    disks: 100
    diskSizeGb: 10240  # 10TB total
    staticIps: 10
    
  storage:
    buckets: 20
    totalSizeGb: 51200  # 50TB total
    
  networking:
    networks: 5
    firewallRules: 100
    loadBalancers: 10
    
  bigquery:
    slotsPerProject: 2000
    storageGb: 102400  # 100TB
    
  monitoring:
    alertPolicies: 50
    uptimeChecks: 25
    customMetrics: 500
```

### Resource Usage Monitoring
```yaml
# quota-monitoring.yaml
quotaAlerts:
  - name: "High CPU Quota Usage"
    quotaMetric: "compute.googleapis.com/cpus"
    threshold: 0.8  # 80% of quota
    regions: ["us-central1", "us-east1"]
    
  - name: "Storage Quota Warning"
    quotaMetric: "storage.googleapis.com/quota/total_bytes"
    threshold: 0.9  # 90% of quota
    
  - name: "Network Quota Alert"
    quotaMetric: "compute.googleapis.com/networks"
    threshold: 0.8
```

## Cost Governance Policies

### Spending Controls
```yaml
# spending-controls.yaml
policies:
  - name: "Require Cost Center Tag"
    constraint: "constraints/gcp.resourceLabels"
    rules:
      - condition: "true"
        requireLabels: ["cost-center", "team", "environment"]
        
  - name: "Restrict Expensive Machine Types"
    constraint: "constraints/compute.vmExternalIpAccess"
    rules:
      - condition: "resource.machineType.startsWith('n1-highmem-') || resource.machineType.startsWith('n1-highcpu-')"
        enforce: false
        
  - name: "Limit Regional Deployments"
    constraint: "constraints/gcp.resourceLocations"
    rules:
      - condition: "true"
        allowedValues:
          - "us-central1"
          - "us-east1"
          - "us-west1"
```

### Cost Review Process
- [ ] **Weekly Reviews**: Team leads review weekly spending reports
- [ ] **Monthly Analysis**: Finance team analyzes monthly costs and trends
- [ ] **Quarterly Planning**: Adjust budgets based on actual usage patterns
- [ ] **Annual Budgeting**: Plan budgets for the following fiscal year

### Cost Optimization Recommendations
```yaml
# optimization-recommendations.yaml
recommendations:
  - category: "Compute"
    actions:
      - "Implement auto-scaling for variable workloads"
      - "Use preemptible instances for batch processing"
      - "Right-size instances based on actual usage"
      - "Consider committed use discounts for stable workloads"
      
  - category: "Storage"
    actions:
      - "Implement lifecycle policies for data archival"
      - "Use appropriate storage classes for data access patterns"
      - "Enable compression for large datasets"
      - "Regular cleanup of unused snapshots and images"
      
  - category: "Networking"
    actions:
      - "Optimize egress traffic through CDN usage"
      - "Use regional load balancers when possible"
      - "Implement traffic compression"
      - "Monitor and optimize data transfer costs"
```