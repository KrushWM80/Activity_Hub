# Data Bridge - Platform Backend

Backend transformation and validation logic for the Activity Hub Data Bridge system.

## Purpose

This module provides the code-level processing for data ingestion:

- **Transformations**: Convert source data to canonical format
- **Validators**: Ensure data meets schema requirements
- **Data Processing**: Handle batch imports and API integrations

## Structure

```
Platform/Data-Bridge/
├── README.md              
└── Transformations/
    ├── transformations.js   # Data transformation functions
    └── validators.js        # Data validation functions
```

## Relationship to Admin/Data-Bridge

| Component | Location | Purpose |
|-----------|----------|---------|
| Schemas | Admin/Data-Bridge/Schemas/ | Column definitions (admin-configurable) |
| Mappings | Admin/Data-Bridge/Mappings/ | Source-to-schema alignments (admin-configurable) |
| Uploads | Admin/Data-Bridge/Uploads/ | Upload history (admin-viewable) |
| Code Logic | Platform/Data-Bridge/ | Processing code (developer-maintained) |

## Usage

### Transformations

```javascript
const Transformations = require('./Transformations/transformations');

// Apply a single transformation
const marketCode = Transformations.normalize_market_3digit(8);  // "008"

// Apply named transformation from mapping
const value = Transformations.apply('normalize_status', 'ACTIVE');  // "Active"
```

### Validators

```javascript
const Validators = require('./Transformations/validators');
const schema = require('../Admin/Data-Bridge/Schemas/projects-schema.json');

// Validate a single record
const result = Validators.validateRecord(record, schema);
if (!result.valid) {
    console.log(result.errors);
}

// Validate a batch
const batchResult = Validators.validateBatch(records, schema);
console.log(`Valid: ${batchResult.valid}, Invalid: ${batchResult.invalid}`);
```

## Available Transformations

| Function | Description |
|----------|-------------|
| `to_integer` | Convert to integer |
| `to_float` | Convert to float |
| `to_string` | Convert to string |
| `to_date` | Convert to YYYY-MM-DD |
| `to_iso8601` | Convert to ISO8601 datetime |
| `uppercase` | Convert to uppercase |
| `lowercase` | Convert to lowercase |
| `normalize_market_3digit` | Pad market to 3 digits |
| `normalize_division` | Standardize division names |
| `normalize_status` | Standardize status values |
| `normalize_phase` | Standardize phase values |
| `resolve_project_id` | Multi-source project ID resolution |
| `resolve_title` | Multi-source title resolution |

## Future Enhancements

- [ ] Excel file parser integration
- [ ] CSV parser integration  
- [ ] API connector framework
- [ ] Real-time validation feedback
- [ ] Column auto-detection from aliases
