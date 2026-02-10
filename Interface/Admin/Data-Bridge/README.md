# Data Bridge

Admin-configurable data schema and mapping management for Activity Hub.

## Purpose

The Data Bridge system enables:
- **Canonical Schemas**: Define the "source of truth" column definitions
- **Column Mapping**: Bridge external data sources to our standard schema
- **Upload Management**: Track uploaded data versions and configurations

## Structure

```
Admin/Data-Bridge/
├── README.md
├── Schemas/                    # Canonical column definitions
│   ├── projects-schema.json    # Projects data schema (35 fields)
│   └── _schema-template.json   # Template for new schemas
│
├── Mappings/                   # Source-to-schema mappings
│   └── Projects/
│       ├── intake-hub-mapping.json    # Intake Hub → Projects
│       └── _mapping-template.json     # Template for new mappings
│
└── Uploads/                    # Upload history & versions
    └── README.md
```

## Schemas

Schemas define the **canonical column structure** for each data type. They are the source of truth that all external data sources must align to.

### Projects Schema

| Category | Fields | Description |
|----------|--------|-------------|
| Identifiers | 3 | project_id, intake_card, title |
| Status | 4 | status, phase, health, project_source |
| Location | 11 | division, region, market, facility, city, state, etc. |
| Time | 6 | created_date, last_updated, wm_week, fiscal_year, etc. |
| Ownership | 3 | owner, director, sr_director |
| Categorization | 6 | project_type, initiative_type, business_type, etc. |
| Impact | 2 | associate_impact, customer_impact |
| Description | 2 | summary, overview |

**Required Fields**: project_id, title, status, project_source, created_date, last_updated

### Creating New Schemas

1. Copy `Schemas/_schema-template.json`
2. Rename to `[data-type]-schema.json`
3. Define columns organized by category
4. Include aliases for known alternate column names
5. Specify validation rules

## Mappings

Mappings define how columns from external data sources align to canonical schemas.

### Current Mappings

| Source | Target Schema | Status |
|--------|---------------|--------|
| Intake Hub (BigQuery) | projects-schema.json | Active |

### Creating New Mappings

1. Copy `Mappings/[DataType]/_mapping-template.json`
2. Rename to `[source-name]-mapping.json`
3. Map each source column to a target canonical column
4. Specify transformations where data formats differ
5. Document value mappings for enums
6. Set status to "active" when complete

## User Flow (Future)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Projects > Upload Projects                    │
├─────────────────────────────────────────────────────────────────┤
│  1. User uploads Excel/CSV file                                  │
│  2. System detects source columns                                │
│  3. User maps columns via wizard (or uses saved mapping)         │
│  4. System validates data against schema                         │
│  5. Data imported with transformation applied                    │
│  6. Upload versioned in Uploads/Projects/[org]/                  │
└─────────────────────────────────────────────────────────────────┘
```

## Related Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Transformation Code | Platform/Data-Bridge/ | Backend processing logic |
| Upload Interface | Interface/Projects/Upload Projects/ | User-facing upload UI |
| Admin Dashboard | Interface/Admin/admin-dashboard.html | Schema/mapping management UI |

## Changelog

| Date | Change |
|------|--------|
| 2026-02-10 | Initial creation with Projects schema and Intake Hub mapping |
