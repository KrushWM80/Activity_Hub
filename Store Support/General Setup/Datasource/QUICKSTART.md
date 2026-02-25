# 🚀 Datasource Quick Start

## Start Here! 👋

Welcome to Activity Hub's Datasource Documentation. This guide helps you quickly find what you need.

---

## 📌 I Need Help With...

### "I want to understand what data sources Activity Hub uses"
**→ Start here**: [README.md](./README.md)

This gives you:
- Overview of all datasources
- Quick reference table
- Data flow diagrams
- Which folders use what

### "I need to query Polaris or other BigQuery data"
**→ Go to**: [BigQuery/README.md](./BigQuery/README.md)

This covers:
- Connection details for each BigQuery project
- SQL query examples
- Performance best practices
- Error troubleshooting

### "I'm integrating with an external API (Workday, Active Directory, etc)"
**→ Go to**: [APIs/README.md](./APIs/README.md)

This includes:
- Authentication setup
- API endpoints and examples
- Code samples (Python, JavaScript)
- Rate limiting and best practices

### "I need to import data from files (CSV, Excel, JSON)"
**→ Go to**: [File-Based/README.md](./File-Based/README.md)

This shows:
- File format requirements
- Validation rules
- Upload process
- Common errors

### "I'm setting up PostgreSQL or Redis caching"
**→ Go to**: [Databases/README.md](./Databases/README.md)

This provides:
- Connection strings
- Database schema
- Performance tuning
- Backup procedures

### "I want to see which folders use which data sources"
**→ Check**: [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md)

This shows:
- Complete usage matrix
- Data dependencies
- Update frequencies
- Critical dependencies

### "I need to understand data synchronization"
**→ Read**: [SYNC-GUIDE.md](./SYNC-GUIDE.md)

This documents:
- Sync schedule (when data updates)
- How syncs work
- Troubleshooting sync issues
- Monitoring data health

---

## 🗂️ Folder Structure

```
Datasource/
├── README.md                    ◄─ START: Overview guide
├── DATASOURCE-MATRIX.md         ◄─ Which folders use what?
├── SYNC-GUIDE.md                ◄─ Data updates & schedules
│
├── BigQuery/
│   ├── README.md                ◄─ All BigQuery sources
│   ├── Polaris.md               (Coming soon: Details)
│   ├── Asset-Protection.md      (Coming soon: Details)
│   ├── Store-Refresh.md         (Coming soon: Details)
│   ├── Pricing.md               (Coming soon: Details)
│   └── templates/
│       └── bigquery-query-template.sql
│
├── APIs/
│   ├── README.md                ◄─ All API sources
│   ├── Workday.md               (Coming soon: Details)
│   ├── Active-Directory.md      (Coming soon: Details)
│   ├── MS-Graph.md              (Coming soon: Details)
│   ├── Sparky-AI.md             (Coming soon: Details)
│   └── templates/
│       └── api-connection-template.md
│
├── File-Based/
│   ├── README.md                ◄─ File uploads guide
│   ├── CSV-Excel-Imports.md     (Coming soon: Details)
│   ├── JSON-Config.md           (Coming soon: Details)
│   └── templates/
│       └── file-import-template.md
│
├── Databases/
│   ├── README.md                ◄─ Database setup guide
│   ├── PostgreSQL.md            (Coming soon: Details)
│   └── templates/
│       └── db-connection-template.md
│
└── QUICKSTART.md                ◄─ This file!
```

---

## 🎯 Common Tasks

### Task 1: Find which folder uses a specific datasource

**Step 1**: Open [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md)
**Step 2**: Find the datasource name (e.g., "Polaris")
**Step 3**: Look at the "Used By" column

**Example**: 
```
Polaris (BigQuery)
├─ Projects/JobCodes-teaming/
├─ Projects/AMP/Store Updates Dashboard/
└─ Root scripts (test files)
```

---

### Task 2: Check if a data source is currently working

**Step 1**: Open [SYNC-GUIDE.md](./SYNC-GUIDE.md)
**Step 2**: Look for "Health Check Dashboard" section
**Step 3**: Run the monitoring command or check status page

**Quick Check**:
```bash
# Check BigQuery status
bq ls -d

# Check PostgreSQL connection
psql -h db.host -d activity_hub_prod -c "SELECT 1"

# Check Redis
redis-cli ping
```

---

### Task 3: Understand a data flow

**Example**: "How does Project data get from BigQuery to the Projects Dashboard?"

**Answer**: 
1. Data originates in Asset Protection system
2. ETL loads to `wmt-assetprotection-prod.Store_Support_Dev`
3. Backend API queries BigQuery
4. Data cached in Redis
5. Frontend fetches from cache → displays

**Reference**: [DATASOURCE-MATRIX.md - Data Flow Diagrams](./DATASOURCE-MATRIX.md#-data-flow-diagrams)

---

### Task 4: Set up a new data connection

**Step 1**: Determine datasource type:
- BigQuery? → [BigQuery/README.md](./BigQuery/README.md)
- REST API? → [APIs/README.md](./APIs/README.md)
- File upload? → [File-Based/README.md](./File-Based/README.md)
- Database? → [Databases/README.md](./Databases/README.md)

**Step 2**: Follow the Authentication section in relevant README

**Step 3**: Use code examples/templates provided

**Step 4**: Test connection using provided test scripts

---

## 🤔 FAQ

### Q: Where does Activity Hub get its data?
**A**: From 5 main sources:
1. **BigQuery** (cloud data warehouse) - 60% of data
2. **APIs** (Workday, Active Directory, MS Graph) - 25% of data
3. **File uploads** (CSV, Excel) - 10% of data
4. **PostgreSQL** (internal database) - 4% of data
5. **Redis** (cache layer) - 1% of data

See [README.md](./README.md#quick-reference-datasources-at-a-glance) for details.

---

### Q: How often is data updated?
**A**: Depends on the source:
- **Scheduled syncs**: Nightly 1:00-3:30 AM CT (Polaris, HR, Projects)
- **Real-time**: Active Directory, MS Graph, Sparky AI (instant)
- **On-demand**: File uploads, Custom APIs (when triggered)

See [SYNC-GUIDE.md](./SYNC-GUIDE.md#-synchronization-schedule) for full schedule.

---

### Q: What if a data source is down?
**A**: Activity Hub uses fallback logic:
1. Try primary source (BigQuery, API, etc.)
2. Fall back to **cached data** if available
3. Fall back to **last known snapshot** if cache expired
4. Show **offline mode** to user with message

See [SYNC-GUIDE.md - Error Handling](./SYNC-GUIDE.md#-error-handling--recovery) for details.

---

### Q: How do I troubleshoot slow queries?
**A**: 
1. Check [BigQuery best practices](./BigQuery/README.md#-query-best-practices)
2. Add time filters to reduce data scan
3. Use existing views instead of raw tables
4. Check query EXPLAIN plan
5. Contact database team if p95 > 500ms

---

### Q: Can I export Activity Hub data?
**A**: Yes! Multiple options:
- **CSV export**: From Projects interface
- **SQL queries**: Direct BigQuery access (read-only)
- **API**: Custom REST API downloads
- **Reports**: Built-in reporting module

See [File-Based/README.md](./File-Based/README.md) for export formats.

---

## 📊 Data Sizes

| Datasource | Size | Record Count | Growth/Month |
|---|---|---|---|
| Polaris Schedules | 450 MB | 2.5M | +5% |
| Projects | 5 MB | 196 | +2% |
| Distribution Lists | 25 MB | 450 | +1% |
| Store Data | 150 MB | 4,200+ | Stable |
| Pricing | 100 MB | 50K+ | +3% |

---

## ⚡ Performance Expectations

| Operation | P50 | P95 | P99 |
|---|---|---|---|
| BigQuery query | 100ms | 500ms | 2s |
| PostgreSQL query | 10ms | 50ms | 100ms |
| Redis access | 1ms | 5ms | 10ms |
| API call | 50ms | 200ms | 500ms |
| Page load | 1s | 3s | 5s |

---

## 🔒 Security Notes

### Data Classification
- **Public**: Store names, locations, general schedule info
- **Internal Use**: Project details, budget, employee assignments
- **Confidential**: HR data, salary info, distribution lists

### Access Control
- **Polaris**: Department managers and above
- **Asset Protection**: Project teams and admins
- **HR/Workday**: HR staff and admins only
- **Admin functions**: System admins only

See [DATA-CLASSIFICATION-ASSESSMENT.md](../../DATA-CLASSIFICATION-ASSESSMENT.md) in project root.

---

## 📞 Getting Help

| Question | Contact | Response Time |
|---|---|---|
| BigQuery issues | cloud-support@walmart.com | 1 hour |
| Database issues | dba-team@walmart.com | 30 min |
| API integration | integration-team@walmart.com | 2 hours |
| System down | activity-hub-oncall@walmart.com | 15 min |

---

## 🎓 Learning Resources

### For Developers
- [BigQuery Documentation](./BigQuery/README.md) - SQL queries
- [API Integration Guide](./APIs/README.md) - OAuth, REST
- [Python Examples](./APIs/README.md#python-example) - Code samples

### For Data Analysts
- [DATASOURCE-MATRIX.md](./DATASOURCE-MATRIX.md) - Data dependencies
- [Query Templates](./BigQuery/README.md#templates--examples) - Pre-built queries
- [Performance Tuning](./BigQuery/README.md#-query-best-practices) - Optimization tips

### For DevOps/SRE
- [SYNC-GUIDE.md](./SYNC-GUIDE.md) - Monitoring and health checks
- [Databases/README.md](./Databases/README.md) - DB administration
- [Error Handling](./SYNC-GUIDE.md#-error-handling--recovery) - Troubleshooting

---

## 📝 Version & Updates

| Date | Version | Changes |
|---|---|---|
| Feb 25, 2026 | 1.0 | Initial documentation |

**Last Updated**: February 25, 2026
**Next Review**: March 25, 2026

---

## ✅ Next Steps

1. **Bookmark this page** for quick reference
2. **Read the main README.md** for overview
3. **Check DATASOURCE-MATRIX.md** to understand data flows
4. **Explore specific folders** based on your needs
5. **Use templates** for new integrations

---

Need more help? Check the relevant section above or contact the support team!

