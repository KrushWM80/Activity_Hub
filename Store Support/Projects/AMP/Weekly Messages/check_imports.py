#!/usr/bin/env python3
"""Quick syntax and import check."""
import sys
sys.path.insert(0, r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\AMP\Weekly Messages')

try:
    # Just import to check syntax
    import adobe_to_bigquery_loader
    print("✓ adobe_to_bigquery_loader imports successfully")
except SyntaxError as e:
    print(f"✗ Syntax error in adobe_to_bigquery_loader: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

try:
    import adobe_raw_data_loader
    print("✓ adobe_raw_data_loader imports successfully")
except SyntaxError as e:
    print(f"✗ Syntax error in adobe_raw_data_loader: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

print("\n✓ All modules imported successfully")
