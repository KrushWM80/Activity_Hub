# Network Setup and Configuration Guide

## VPC Architecture Design

### Network Architecture Overview

#### Hub-and-Spoke Design
```yaml
# network-architecture.yaml
networkTopology:
  hubProject: "wmt-network-hub"
  spokeProjects:
    - "wmt-retail-prod"
    - "wmt-retail-staging"
    - "wmt-retail-dev"
    - "wmt-analytics-prod"
    - "wmt-analytics-dev"

  sharedVPCs:
    - name: "walmart-hub-vpc"
      project: "wmt-network-hub"
      region: "us-central1"
      subnets:
        - name: "shared-services-subnet"
          cidr: "10.0.0.0/24"
          purpose: "Shared services (DNS, monitoring, security)"
        - name: "management-subnet"
          cidr: "10.0.1.0/24"
          purpose: "Management and bastion hosts"
```

### VPC Network Configuration

#### Primary VPC Setup
```yaml
# vpc-config.yaml
vpcs:
  - name: "walmart-production-vpc"
    project: "wmt-retail-prod"
    autoCreateSubnetworks: false
    routingMode: "REGIONAL"
    
    subnets:
      - name: "web-tier-subnet"
        region: "us-central1"
        ipCidrRange: "10.1.0.0/24"
        privateIpGoogleAccess: true
        enableFlowLogs: true
        logConfig:
          aggregationInterval: "INTERVAL_5_SEC"
          flowSampling: 0.5
          metadata: "INCLUDE_ALL_METADATA"
          
      - name: "app-tier-subnet"
        region: "us-central1"
        ipCidrRange: "10.1.1.0/24"
        privateIpGoogleAccess: true
        enableFlowLogs: true
        
      - name: "data-tier-subnet"
        region: "us-central1"
        ipCidrRange: "10.1.2.0/24"
        privateIpGoogleAccess: true
        enableFlowLogs: true
        
      - name: "management-subnet"
        region: "us-central1"
        ipCidrRange: "10.1.10.0/24"
        privateIpGoogleAccess: true
        purpose: "Bastion hosts and management tools"

  - name: "walmart-staging-vpc"
    project: "wmt-retail-staging"
    autoCreateSubnetworks: false
    routingMode: "REGIONAL"
    
    subnets:
      - name: "staging-subnet"
        region: "us-central1"
        ipCidrRange: "10.2.0.0/24"
        privateIpGoogleAccess: true

  - name: "walmart-development-vpc"
    project: "wmt-retail-dev"
    autoCreateSubnetworks: false
    routingMode: "REGIONAL"
    
    subnets:
      - name: "dev-subnet"
        region: "us-central1"
        ipCidrRange: "10.3.0.0/24"
        privateIpGoogleAccess: true
```

#### Secondary IP Ranges (for GKE)
```yaml
# gke-secondary-ranges.yaml
secondaryRanges:
  - subnetName: "web-tier-subnet"
    secondaryRanges:
      - rangeName: "web-pods-range"
        ipCidrRange: "172.16.0.0/14"  # Pod IPs
      - rangeName: "web-services-range"
        ipCidrRange: "172.20.0.0/16"  # Service IPs
        
  - subnetName: "app-tier-subnet"
    secondaryRanges:
      - rangeName: "app-pods-range"
        ipCidrRange: "172.24.0.0/14"
      - rangeName: "app-services-range"
        ipCidrRange: "172.28.0.0/16"
```

## Firewall Rules and Security

### Network Security Rules

#### Base Firewall Rules
```yaml
# firewall-rules.yaml
firewallRules:
  # Deny all ingress by default (implicit rule, documented here)
  - name: "default-deny-ingress"
    direction: "INGRESS"
    priority: 65534
    action: "DENY"
    sourceRanges: ["0.0.0.0/0"]
    
  # Allow health checks
  - name: "allow-health-checks"
    direction: "INGRESS"
    priority: 1000
    action: "ALLOW"
    sourceRanges:
      - "130.211.0.0/22"  # Google Cloud health check ranges
      - "35.191.0.0/16"
    allowed:
      - IPProtocol: "tcp"
        ports: ["80", "443", "8080", "8443"]
    targetTags: ["http-server", "https-server"]

  # Allow load balancer traffic
  - name: "allow-lb-traffic"
    direction: "INGRESS"
    priority: 1000
    action: "ALLOW"
    sourceRanges: ["10.1.0.0/24"]  # Web tier subnet
    allowed:
      - IPProtocol: "tcp"
        ports: ["80", "443"]
    targetTags: ["web-server"]

  # Allow internal communication
  - name: "allow-internal-communication"
    direction: "INGRESS"
    priority: 1000
    action: "ALLOW"
    sourceRanges:
      - "10.1.0.0/16"  # Production VPC
      - "10.0.0.0/16"  # Hub VPC
    allowed:
      - IPProtocol: "tcp"
        ports: ["22", "3389", "443", "8080"]
      - IPProtocol: "icmp"
    targetTags: ["internal-server"]

  # SSH access from bastion
  - name: "allow-ssh-from-bastion"
    direction: "INGRESS"
    priority: 1000
    action: "ALLOW"
    sourceTags: ["bastion-host"]
    allowed:
      - IPProtocol: "tcp"
        ports: ["22"]
    targetTags: ["ssh-access"]

  # Database access
  - name: "allow-database-access"
    direction: "INGRESS"
    priority: 1000
    action: "ALLOW"
    sourceRanges: ["10.1.1.0/24"]  # App tier subnet
    allowed:
      - IPProtocol: "tcp"
        ports: ["3306", "5432", "1521", "1433"]
    targetTags: ["database-server"]

  # Deny direct internet access to data tier
  - name: "deny-internet-to-data-tier"
    direction: "INGRESS"
    priority: 900
    action: "DENY"
    sourceRanges: ["0.0.0.0/0"]
    targetTags: ["data-tier"]
```

#### Application-Specific Rules
```yaml
# app-firewall-rules.yaml
applicationRules:
  - name: "walmart-web-app-rules"
    rules:
      - name: "allow-https-from-internet"
        direction: "INGRESS"
        priority: 1000
        action: "ALLOW"
        sourceRanges: ["0.0.0.0/0"]
        allowed:
          - IPProtocol: "tcp"
            ports: ["443"]
        targetTags: ["walmart-web-frontend"]

      - name: "allow-api-from-web"
        direction: "INGRESS"
        priority: 1000
        action: "ALLOW"
        sourceTags: ["walmart-web-frontend"]
        allowed:
          - IPProtocol: "tcp"
            ports: ["8080", "8443"]
        targetTags: ["walmart-api-backend"]

  - name: "walmart-microservices-rules"
    rules:
      - name: "allow-service-mesh-communication"
        direction: "INGRESS"
        priority: 1000
        action: "ALLOW"
        sourceRanges: ["172.16.0.0/12"]  # Pod CIDR range
        allowed:
          - IPProtocol: "tcp"
            ports: ["8080", "9090", "15000-15010"]  # App and Istio ports
        targetTags: ["service-mesh"]
```

### Network Tags and Labels

#### Tagging Strategy
```yaml
# network-tags.yaml
taggingStrategy:
  tierTags:
    - "web-tier"
    - "app-tier" 
    - "data-tier"
    - "management-tier"
    
  serviceTags:
    - "http-server"
    - "https-server"
    - "database-server"
    - "cache-server"
    - "message-queue"
    
  accessTags:
    - "ssh-access"
    - "rdp-access"
    - "bastion-host"
    - "internal-server"
    - "public-server"
    
  environmentTags:
    - "production"
    - "staging"
    - "development"
    - "testing"
    
  securityTags:
    - "pci-compliant"
    - "sox-compliant"
    - "high-security"
    - "standard-security"
```

## Load Balancing Configuration

### Global Load Balancer Setup

#### HTTPS Load Balancer
```yaml
# load-balancer-config.yaml
loadBalancers:
  - name: "walmart-global-https-lb"
    type: "GLOBAL_EXTERNAL_HTTP_HTTPS"
    protocol: "HTTPS"
    
    sslCertificates:
      - name: "walmart-ssl-cert"
        type: "GOOGLE_MANAGED"
        domains:
          - "walmart.com"
          - "www.walmart.com"
          - "api.walmart.com"
    
    backendServices:
      - name: "walmart-web-backend"
        protocol: "HTTP"
        port: 80
        healthCheck: "walmart-web-health-check"
        backends:
          - group: "projects/wmt-retail-prod/zones/us-central1-a/instanceGroups/web-servers-ig"
            balancingMode: "UTILIZATION"
            maxUtilization: 0.8
          - group: "projects/wmt-retail-prod/zones/us-central1-b/instanceGroups/web-servers-ig"
            balancingMode: "UTILIZATION"
            maxUtilization: 0.8
        
        connectionDraining:
          drainingTimeoutSec: 300
        
        circuitBreakers:
          maxRequestsPerConnection: 10
          maxConnections: 1000
          maxPendingRequests: 100
          maxRetries: 3

      - name: "walmart-api-backend"
        protocol: "HTTP"
        port: 8080
        healthCheck: "walmart-api-health-check"
        backends:
          - group: "projects/wmt-retail-prod/zones/us-central1-a/instanceGroups/api-servers-ig"

    urlMap:
      defaultService: "walmart-web-backend"
      pathMatchers:
        - name: "api-matcher"
          defaultService: "walmart-api-backend"
          pathRules:
            - paths: ["/api/*", "/v1/*", "/v2/*"]
              service: "walmart-api-backend"
```

#### Internal Load Balancer
```yaml
# internal-load-balancer.yaml
internalLoadBalancers:
  - name: "walmart-internal-api-lb"
    type: "REGIONAL_INTERNAL"
    region: "us-central1"
    subnet: "app-tier-subnet"
    
    backendService:
      name: "internal-api-backend"
      protocol: "TCP"
      port: 8080
      healthCheck: "internal-api-health-check"
      backends:
        - group: "projects/wmt-retail-prod/zones/us-central1-a/instanceGroups/internal-api-ig"
      sessionAffinity: "CLIENT_IP"
      
    ipAddress: "10.1.1.100"  # Static internal IP
```

### Health Checks

#### Health Check Configuration
```yaml
# health-checks.yaml
healthChecks:
  - name: "walmart-web-health-check"
    type: "HTTP"
    checkIntervalSec: 10
    timeoutSec: 5
    healthyThreshold: 2
    unhealthyThreshold: 3
    httpHealthCheck:
      port: 80
      requestPath: "/health"
      proxyHeader: "NONE"

  - name: "walmart-api-health-check"
    type: "HTTP"
    checkIntervalSec: 10
    timeoutSec: 5
    healthyThreshold: 2
    unhealthyThreshold: 3
    httpHealthCheck:
      port: 8080
      requestPath: "/api/health"
      proxyHeader: "NONE"

  - name: "walmart-database-health-check"
    type: "TCP"
    checkIntervalSec: 30
    timeoutSec: 10
    healthyThreshold: 2
    unhealthyThreshold: 3
    tcpHealthCheck:
      port: 3306
      proxyHeader: "NONE"
```

## VPN and Hybrid Connectivity

### Site-to-Site VPN Setup

#### VPN Gateway Configuration
```yaml
# vpn-config.yaml
vpnGateways:
  - name: "walmart-datacenter-vpn"
    region: "us-central1"
    network: "walmart-production-vpc"
    
    tunnels:
      - name: "tunnel-to-datacenter-primary"
        peerIp: "203.0.113.1"  # Walmart datacenter public IP
        sharedSecret: "${SECRET_SHARED_KEY}"
        targetVpnGateway: "walmart-datacenter-vpn"
        ikeVersion: 2
        
        localTrafficSelector:
          - "10.1.0.0/16"  # GCP VPC CIDR
        remoteTrafficSelector:
          - "192.168.0.0/16"  # Datacenter CIDR
          
      - name: "tunnel-to-datacenter-backup"
        peerIp: "203.0.113.2"  # Backup datacenter IP
        sharedSecret: "${SECRET_SHARED_KEY_BACKUP}"
        targetVpnGateway: "walmart-datacenter-vpn"
        ikeVersion: 2

    routes:
      - name: "route-to-datacenter"
        destRange: "192.168.0.0/16"
        nextHopVpnTunnel: "tunnel-to-datacenter-primary"
        priority: 1000
        
      - name: "route-to-datacenter-backup"
        destRange: "192.168.0.0/16"
        nextHopVpnTunnel: "tunnel-to-datacenter-backup"
        priority: 2000
```

#### Cloud Interconnect (for high-bandwidth requirements)
```yaml
# cloud-interconnect.yaml
interconnect:
  - name: "walmart-dedicated-interconnect"
    type: "DEDICATED"
    linkType: "LINK_TYPE_ETHERNET_10G_LR"
    location: "den-zone1-1"  # Denver colocation facility
    
    attachments:
      - name: "walmart-prod-attachment"
        router: "walmart-cloud-router"
        region: "us-central1"
        vlan: 100
        
        bgp:
          asn: 65001  # Walmart ASN
          peerAsn: 16550  # Google ASN
          advertisedRoutePriority: 100
          
        ipAddresses:
          customerAddress: "169.254.1.1/30"
          googleAddress: "169.254.1.2/30"
```

### Cloud Router Configuration

#### BGP Router Setup
```yaml
# cloud-router.yaml
cloudRouters:
  - name: "walmart-cloud-router"
    region: "us-central1"
    network: "walmart-production-vpc"
    asn: 65001  # Walmart private ASN
    
    bgpPeers:
      - name: "datacenter-bgp-peer"
        interface: "vpn-interface-1"
        peerIpAddress: "169.254.1.1"
        peerAsn: 65002
        advertisedRoutePriority: 100
        
        advertisedGroups:
          - "ALL_SUBNETS"
        
        customAdvertisedRoutes:
          - range: "10.1.0.0/16"
            priority: 100
```

## DNS Configuration

### Cloud DNS Setup

#### Private DNS Zones
```yaml
# dns-config.yaml
dnsZones:
  - name: "walmart-internal-zone"
    dnsName: "internal.walmart.com."
    visibility: "private"
    networks:
      - "projects/wmt-retail-prod/global/networks/walmart-production-vpc"
      - "projects/wmt-retail-staging/global/networks/walmart-staging-vpc"
    
    recordSets:
      - name: "db-primary.internal.walmart.com."
        type: "A"
        ttl: 300
        rrdatas: ["10.1.2.10"]
        
      - name: "db-replica.internal.walmart.com."
        type: "A"
        ttl: 300
        rrdatas: ["10.1.2.11"]
        
      - name: "cache.internal.walmart.com."
        type: "A"
        ttl: 300
        rrdatas: ["10.1.2.20"]

  - name: "walmart-public-zone"
    dnsName: "walmart.com."
    visibility: "public"
    
    recordSets:
      - name: "walmart.com."
        type: "A"
        ttl: 300
        rrdatas: ["34.102.136.180"]  # Load balancer IP
        
      - name: "www.walmart.com."
        type: "CNAME"
        ttl: 300
        rrdatas: ["walmart.com."]
        
      - name: "api.walmart.com."
        type: "A"
        ttl: 300
        rrdatas: ["34.102.136.181"]
```

#### DNS Forwarding
```yaml
# dns-forwarding.yaml
forwardingRules:
  - name: "forward-to-datacenter-dns"
    dnsName: "corp.walmart.com."
    targetNameServers:
      - ipv4Address: "192.168.10.10"
        forwardingPath: "private"
      - ipv4Address: "192.168.10.11"
        forwardingPath: "private"
    networks:
      - "projects/wmt-retail-prod/global/networks/walmart-production-vpc"
```

## Network Security and Monitoring

### VPC Flow Logs Analysis

#### Flow Log Configuration
```yaml
# flow-logs-config.yaml
flowLogsConfig:
  subnets:
    - name: "web-tier-subnet"
      enable: true
      aggregationInterval: "INTERVAL_5_SEC"
      flowSampling: 1.0  # 100% sampling for security analysis
      metadata: "INCLUDE_ALL_METADATA"
      filterExpr: "true"  # Log all traffic
      
    - name: "data-tier-subnet"
      enable: true
      aggregationInterval: "INTERVAL_10_SEC"
      flowSampling: 0.5  # 50% sampling
      metadata: "INCLUDE_ALL_METADATA"
      filterExpr: 'inIpv4 != "10.1.0.0/16"'  # Log external traffic only

  exportDestination:
    bigqueryDataset: "wmt-security.network_logs"
    pubsubTopic: "projects/wmt-security/topics/flow-logs"
```

#### Flow Log Analysis Queries
```sql
-- Top traffic flows by volume
SELECT
  src_ip,
  dest_ip,
  src_port,
  dest_port,
  protocol,
  SUM(bytes) as total_bytes,
  COUNT(*) as flow_count
FROM `wmt-security.network_logs.compute_vpc_flows_*`
WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
GROUP BY src_ip, dest_ip, src_port, dest_port, protocol
ORDER BY total_bytes DESC
LIMIT 100;

-- Suspicious traffic patterns
SELECT
  src_ip,
  dest_ip,
  dest_port,
  COUNT(DISTINCT dest_port) as unique_ports,
  SUM(bytes) as total_bytes
FROM `wmt-security.network_logs.compute_vpc_flows_*`
WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 HOUR))
  AND src_ip NOT LIKE '10.%'  -- External traffic
GROUP BY src_ip, dest_ip
HAVING unique_ports > 10  -- Port scanning indicator
ORDER BY unique_ports DESC;
```

### Network Monitoring and Alerting

#### Network Performance Monitoring
```yaml
# network-monitoring.yaml
networkMonitoring:
  uptimeChecks:
    - displayName: "Walmart Website Uptime"
      httpCheck:
        path: "/"
        port: 443
        useSsl: true
        validateSsl: true
      monitoredResource:
        type: "uptime_url"
        labels:
          host: "walmart.com"
      checkIntervalSeconds: 60
      selectedRegions: ["usa", "europe", "asia_pacific"]

    - displayName: "Internal API Connectivity"
      tcpCheck:
        port: 8080
      monitoredResource:
        type: "gce_instance"
        labels:
          instance_id: "internal-api-server"
      checkIntervalSeconds: 30

  alertPolicies:
    - displayName: "High Network Latency"
      conditions:
        - displayName: "Latency above 100ms"
          conditionThreshold:
            filter: 'metric.type="networking.googleapis.com/vm_flow/rtt"'
            comparison: COMPARISON_GREATER_THAN
            thresholdValue: 100  # milliseconds
            duration: 300s

    - displayName: "Unusual Traffic Volume"
      conditions:
        - displayName: "Traffic spike detection"
          conditionThreshold:
            filter: 'metric.type="compute.googleapis.com/instance/network/received_bytes_count"'
            comparison: COMPARISON_GREATER_THAN
            thresholdValue: 1000000000  # 1GB
            duration: 60s
```

## Network Disaster Recovery

### Multi-Region Setup

#### Disaster Recovery Network
```yaml
# dr-network.yaml
disasterRecovery:
  primaryRegion: "us-central1"
  secondaryRegion: "us-east1"
  
  networks:
    - name: "walmart-dr-vpc"
      region: "us-east1"
      subnets:
        - name: "dr-web-subnet"
          ipCidrRange: "10.10.0.0/24"
        - name: "dr-app-subnet"
          ipCidrRange: "10.10.1.0/24"
        - name: "dr-data-subnet"
          ipCidrRange: "10.10.2.0/24"

  vpcPeering:
    - name: "prod-to-dr-peering"
      network1: "projects/wmt-retail-prod/global/networks/walmart-production-vpc"
      network2: "projects/wmt-retail-dr/global/networks/walmart-dr-vpc"
      autoCreateRoutes: true
      
  failoverProcedures:
    - step: "Update DNS records to point to DR region"
    - step: "Start DR instances and services"
    - step: "Verify application functionality"
    - step: "Monitor performance and adjust capacity"
```

### Network Backup and Recovery
```yaml
# network-backup.yaml
backupProcedures:
  configurations:
    - name: "Daily VPC Configuration Backup"
      schedule: "0 2 * * *"  # Daily at 2 AM
      resources:
        - "VPC networks"
        - "Subnets"
        - "Firewall rules"
        - "Routes"
        - "VPN gateways and tunnels"
      destination: "gs://wmt-network-backups/"
      
  recovery:
    rto: "4 hours"  # Recovery Time Objective
    rpo: "1 hour"   # Recovery Point Objective
    procedures:
      - "Restore VPC configuration from backup"
      - "Re-establish VPN connections"
      - "Verify DNS resolution"
      - "Test application connectivity"
      - "Update monitoring and alerting"
```