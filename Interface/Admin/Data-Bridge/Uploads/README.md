# Data-Bridge Uploads

This folder stores uploaded data files and their version history.

## Structure

```
Uploads/
└── Projects/
    └── [organization-name]/
        ├── v1/
        │   ├── source-file.xlsx        # Original uploaded file
        │   ├── mapping-config.json     # Applied column mapping
        │   └── upload-log.json         # Upload metadata
        └── v2/
            └── ...                     # Updated versions
```

## Upload Process

1. User uploads file via Projects > Upload Projects interface
2. File is stored in versioned folder (v1, v2, etc.)
3. Column mapping is configured and saved
4. Upload log captures metadata (timestamp, user, record count)

## Version Management

- Each new upload creates a new version folder
- Previous versions are preserved for audit trail
- Mappings can be reused or updated between versions
