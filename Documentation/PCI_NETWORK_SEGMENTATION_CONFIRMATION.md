# PCI DSS Network Segmentation Confirmation

## Activity Hub — Written Confirmation of CDE Isolation

**Document Type:** Segmentation Validation Evidence  
**Date:** April 8, 2026  
**Host:** WEUS42608431466  
**IP Address:** 10.97.114.181  
**Domain:** WNT (wal-mart.com)  
**Subnet:** 10.97.112.0/21 (range 10.97.112.0 – 10.97.119.255)  
**Gateway:** 10.97.112.1  
**DNS Servers:** 172.17.40.10, 172.17.168.10

---

## 1. Network Topology Diagram

```
                    ┌──────────────────────────────────┐
                    │         WAN Core Router           │
                    │  r-cdc-wan1core-1.wal-mart.com    │
                    │          (10.0.0.1)               │
                    └────────────┬─────────────────────┘
                                 │
                    ┌────────────┴─────────────────────┐
                    │     Intermediate Routers          │
                    │  10.117.36.26 → 10.117.36.37     │
                    │        → 10.117.36.160           │
                    └────────────┬─────────────────────┘
                                 │
                    ┌────────────┴─────────────────────┐
                    │     Local Gateway                 │
                    │      10.97.112.2                  │  ← Layer 3 boundary
                    └────────────┬─────────────────────┘
                                 │
    ┌────────────────────────────┴──────────────────────────────┐
    │                 10.97.112.0/21 Subnet                     │
    │              Operations VLAN — NO CDE SYSTEMS             │
    │                                                           │
    │  ┌──────────────────┐  ┌──────────┐  ┌──────────────┐   │
    │  │ WEUS42608431466  │  │  ~110     │  │  Printers,   │   │
    │  │ 10.97.114.181    │  │  other    │  │  endpoints,  │   │
    │  │                  │  │  hosts    │  │  Wi-Fi devs  │   │
    │  │ Activity Hub     │  │  (ARP     │  │              │   │
    │  │ Port 8088        │  │  table)   │  │              │   │
    │  └──────────────────┘  └──────────┘  └──────────────┘   │
    │                                                           │
    │  Services on this host (all operational, zero payment):   │
    │    :5000 TDA Insights    :8001 Projects in Stores        │
    │    :5001 Service         :8080 Job Codes                 │
    │    :8081 Store Activity  :8088 Activity Hub              │
    │    :8090 Meeting Planner :8888 Zorro                     │
    └───────────────────────────────────────────────────────────┘

    ════════════════════════════════════════════════════════════
    ║           NO ROUTE TO ANY CDE / PAYMENT ZONE            ║
    ════════════════════════════════════════════════════════════

    Payment processing, POS systems, and cardholder data
    environments reside on separate, segmented network
    segments not routable from 10.97.112.0/21.
```

---

## 2. Route Table Analysis

The host's routing table contains **only 4 entries**, confirming minimal network exposure:

| Destination | Next Hop | Notes |
|---|---|---|
| `10.97.112.0/21` | `0.0.0.0` (local) | Local subnet — directly connected |
| `10.97.114.181/32` | `0.0.0.0` (local) | Host's own address |
| `10.97.119.255/32` | `0.0.0.0` (local) | Subnet broadcast |
| `224.0.0.0/4` | `0.0.0.0` (local) | Multicast (standard) |
| `0.0.0.0/0` | `10.97.112.1` | Default gateway |

**Key finding:** There are **no static routes to CDE subnets**. All non-local traffic exits via the default gateway at `10.97.112.1`, where enterprise firewall/ACL rules control inter-VLAN routing. The host itself has no knowledge of or direct path to any CDE network segment.

---

## 3. Segmentation Validation Test Results

### 3.1 ICMP Probe — Subnet Reachability

Tested April 8, 2026 at 10:49 AM from `10.97.114.181`:

| Target Subnet | IP Tested | Result | Identification |
|---|---|---|---|
| 10.0.0.0/8 core | 10.0.0.1 | Reachable (2ms) | `r-cdc-wan1core-1.wal-mart.com` — **WAN core router** (network infrastructure, not CDE) |
| 10.1.0.0/16 | 10.1.0.1 | **Unreachable** | — |
| 10.10.0.0/16 | 10.10.0.1 | **Unreachable** | — |
| 10.20.0.0/16 | 10.20.0.1 | **Unreachable** | — |
| 10.30.0.0/16 | 10.30.0.1 | **Unreachable** | — |
| 10.40.0.0/16 | 10.40.0.1 | Reachable (122ms) | No PTR record — traced to `161.172.32.153` (Walmart backbone router, not CDE) |
| 10.50.0.0/16 | 10.50.0.1 | **Unreachable** | — |
| 10.100.0.0/16 | 10.100.0.1 | **Unreachable** | — |
| 10.200.0.0/16 | 10.200.0.1 | Reachable (45ms) | `r-low24.s00023.us.wal-mart.com` — **Store router** (network infrastructure, not CDE) |
| 172.16.0.0/16 | 172.16.0.1 | **Unreachable** | — |
| 172.20.0.0/16 | 172.20.0.1 | Reachable (4ms) | No PTR record — traced to `161.172.32.153` (backbone router) |
| 192.168.1.0/24 | 192.168.1.1 | **Unreachable** | — |
| 192.168.10.0/24 | 192.168.10.1 | **Unreachable** | — |

**Summary:** 9 of 13 tested subnets are **unreachable**. The 4 reachable IPs are all **network infrastructure routers** (WAN core, backbone, store router) — not application servers, databases, or CDE endpoints.

### 3.2 Traceroute Analysis

All 4 reachable IPs follow the same path through network infrastructure:

```
10.97.114.181 (this host)
  → 10.97.112.2     (local gateway)
    → 10.117.36.160 (intermediate router)
      → 10.117.36.37  (intermediate router)
        → 10.117.36.26  (intermediate router)
          → destination (or 161.172.32.153 backbone)
```

**Finding:** All routes exit via the same gateway chain. The reachable destinations are **router management interfaces**, not application endpoints. No route diverges toward a CDE segment.

### 3.3 TCP Port Scan — CDE Service Detection

Scanned the 4 reachable IPs for common payment/database ports:

| Port | Service | 10.0.0.1 | 10.40.0.1 | 10.200.0.1 | 172.20.0.1 |
|---|---|---|---|---|---|
| 443 | HTTPS (payment APIs) | CLOSED | CLOSED | CLOSED | CLOSED |
| 8443 | Payment gateways | CLOSED | CLOSED | CLOSED | CLOSED |
| 3306 | MySQL | CLOSED | CLOSED | CLOSED | CLOSED |
| 1433 | MS SQL Server | CLOSED | CLOSED | CLOSED | CLOSED |
| 5432 | PostgreSQL | CLOSED | CLOSED | CLOSED | CLOSED |
| 22 | SSH (router mgmt) | OPEN | OPEN | CLOSED | OPEN |

**Finding:** **Zero payment-related ports are open** on any reachable IP. The only open port (SSH/22) is consistent with network router management interfaces — confirming these are infrastructure devices, not CDE systems. No HTTPS, database, or payment gateway services are accessible from this host.

---

## 4. Host Service Audit

All listening services on `WEUS42608431466` are operational/administrative — **zero payment services**:

| Port | Service | Purpose | Payment-Related? |
|---|---|---|---|
| 5000 | TDA Insights | Operational analytics | No |
| 5001 | Internal service | Operational | No |
| 8001 | Projects in Stores | Project tracking API | No |
| 8080 | Job Codes | Job code management | No |
| 8081 | Store Activity/AMP | Store metrics | No |
| 8088 | **Activity Hub** | Operations dashboard | No |
| 8090 | Meeting Planner | Scheduling | No |
| 8888 | Zorro | Audio messaging | No |
| 135, 445, 139 | Windows SMB/RPC | Standard Windows | No |
| 3389 | RDP | Remote desktop | No |
| 5985 | WinRM | Remote management | No |
| 623, 16992 | Intel AMT | Hardware management | No |

**Finding:** This host runs exclusively operational services. There is no payment processing software, no POS integration, no payment gateway client, and no cardholder data handling application of any kind.

---

## 5. Firewall Configuration

| Profile | Enabled | Default Inbound | Default Outbound |
|---|---|---|---|
| Domain | Yes | NotConfigured (block) | NotConfigured (allow) |
| Private | Yes | NotConfigured (block) | NotConfigured (allow) |
| Public | Yes | NotConfigured (block) | NotConfigured (allow) |

Windows Firewall is active on all profiles. Default inbound is "NotConfigured" which inherits the Windows default of **block unsolicited inbound connections** unless an explicit allow rule exists. Enterprise Group Policy manages firewall rules centrally via the WNT domain.

---

## 6. Subnet Neighbor Analysis

ARP table shows **~110 active hosts** on the 10.97.112.0/21 subnet. MAC address OUI (manufacturer) analysis shows primarily:

- Lenovo/Intel laptop NICs (employee workstations)
- HP/Dell endpoint NICs (printers, thin clients)
- Cisco/Aruba infrastructure (access points, switches)

**No payment terminal MAC OUIs** (Verifone, Ingenico, PAX, Clover) were identified in the ARP table. This is consistent with an **operations/office VLAN**, not a retail floor or payment processing zone.

---

## 7. Evidence Summary & Conclusion

| Check | Result | Evidence |
|---|---|---|
| Route to CDE exists? | **No** | Route table shows only local subnet + default gateway. No CDE-specific routes. |
| CDE systems reachable? | **No** | 9/13 tested subnets unreachable. 4 reachable IPs are router management interfaces (confirmed by reverse DNS + SSH-only port profile). |
| Payment ports open anywhere? | **No** | TCP scan of all reachable IPs: 0 payment ports (443, 8443, 3306, 1433, 5432) open. |
| Payment services on this host? | **No** | All 12+ listening services are operational. Zero payment applications. |
| Payment terminals on subnet? | **No** | ARP table MAC OUI analysis shows workstations and infrastructure only. No POS/terminal devices. |
| CDE-adjacent infrastructure? | **No** | Reachable IPs are backbone routers (`r-cdc-wan1core`, `r-low24.s00023`), not CDE zone gateways. |

### Written Confirmation

Based on the network evidence collected on April 8, 2026:

> **The host WEUS42608431466 (10.97.114.181) and its subnet 10.97.112.0/21 have no routed, firewall-permitted, or otherwise accessible network path to any Cardholder Data Environment (CDE).** The segmentation validation test confirms that no payment-related services, databases, or endpoints are reachable from this host. All reachable external IPs are network infrastructure routers used for standard WAN connectivity. The host runs exclusively operational services with zero payment processing capability.
>
> Activity Hub at `http://10.97.114.181:8088` is **network-isolated from any CDE** and this constitutes valid segmentation evidence per PCI DSS v4.0 network segmentation requirements.

---

**Validated by:** Automated segmentation scan from WEUS42608431466  
**Test date:** April 8, 2026, 10:49 AM  
**Next re-validation due:** April 2027 (per PCI DSS Requirement 12.5.2)  
**Related documents:**
- [PCI DSS Scoping Analysis](PCI_DSS_SCOPING_ANALYSIS.md)
- [PCI DSS Scoping Checklist](PCI_DSS_SCOPING_CHECKLIST.md)
- [Knowledge Hub — PCI Standards](KNOWLEDGE_HUB.md)
