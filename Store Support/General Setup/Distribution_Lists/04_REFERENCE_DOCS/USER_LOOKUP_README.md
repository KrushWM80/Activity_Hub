# User ID Lookup Tool

A command-line tool for looking up User IDs (GUID format) for Walmart associates by their email addresses.

## Features

- ✅ Search single or multiple associates at once
- ✅ Works with both `@walmart.com` and `@wal-mart.com` email domains
- ✅ Automatically handles email format variations
- ✅ Export results to CSV
- ✅ Interactive and command-line modes

## Data Source

Currently uses: `exportGroupMembers_2025-12-23.csv` (256 members)
- Source: tableau_home_office_all_type_a group export
- Contains: Display names, emails, and User IDs (GUIDs)

## Quick Start

### Command Line (Fastest)

```bash
# Single email
python quick_lookup.py nathan.schmidt0@wal-mart.com

# Multiple emails
python quick_lookup.py email1@walmart.com email2@wal-mart.com email3@walmart.com
```

### Interactive Mode

```bash
python user_id_lookup.py
```

Then follow the menu prompts to search by:
1. Name
2. Email
3. Multiple (comma-separated)

## Example Output

```
====================================================================================================
USER ID LOOKUP
====================================================================================================
✓ Loaded 256 records from exportGroupMembers_2025-12-23.csv
  Email column: mail
  ID column: id

✓ Found 1 result(s):

====================================================================================================

📋 Nathan Schmidt
   User ID: 06f9cdae-7392-4978-a5f5-7a218d6aa8c8
   Email: Nathan.Schmidt0@walmart.com

====================================================================================================

Searched for 1 email(s), found 1 match(es)
```

## Usage Examples

### Command Line

```bash
# Test with sample emails
python quick_lookup.py crystal.mcdonagh@wal-mart.com scott.lukomske@wal-mart.com yasmin.tooley@wal-mart.com nicolas.cordero@wal-mart.com nathan.schmidt0@wal-mart.com

# Use in scripts
python quick_lookup.py john.doe@walmart.com > results.txt
```

### Programmatic Use (In Python Scripts)

```python
from user_id_lookup import UserIDLookup, quick_lookup

# Quick single lookup
results = quick_lookup("nathan.schmidt0@wal-mart.com")
# Returns: [("Nathan Schmidt", "06f9cdae-7392-4978-a5f5-7a218d6aa8c8", "Nathan.Schmidt0@walmart.com")]

# Advanced usage
lookup = UserIDLookup()
results = lookup.search_by_email("schmidt")
lookup.display_results(results, show_all_fields=True)

# Export to CSV
lookup.export_results(results, "my_results.csv")
```

## Files

- `user_id_lookup.py` - Main lookup class with all functionality
- `quick_lookup.py` - Simple command-line wrapper for quick searches
- `test_lookup.py` - Test script for debugging

## Future Enhancements

To expand the tool to search more associates:
1. Extract additional AD groups
2. Merge multiple group exports
3. Connect to BigQuery for live data
4. Add Microsoft Graph API integration

## Notes

- Email search is case-insensitive
- Automatically handles @walmart.com vs @wal-mart.com
- User IDs are in GUID format (e.g., `06f9cdae-7392-4978-a5f5-7a218d6aa8c8`)
- Currently searches 256 members from the tableau_home_office_all_type_a group
