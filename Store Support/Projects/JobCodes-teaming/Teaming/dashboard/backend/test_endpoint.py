#!/usr/bin/env python3
"""Test the load_job_code_data function"""
import sys
sys.path.insert(0, '.')

try:
    print("=" * 60)
    print("Testing load_job_code_data() function")
    print("=" * 60)
    
    from main import load_job_code_data
    
    merged_df, teaming_df = load_job_code_data()
    print(f"\n✓ SUCCESS: Data loaded")
    print(f"  Merged DataFrame shape: {merged_df.shape}")
    print(f"  Merged columns: {list(merged_df.columns)}")
    print(f"  Teaming columns: {list(teaming_df.columns)}")
    
    # Check first row
    if len(merged_df) > 0:
        first_row = merged_df.iloc[0]
        print(f"\n✓ First row:")
        print(f"  job_code: {first_row.get('job_code')}")
        print(f"  job_nm: {first_row.get('job_nm')}")
        print(f"  job_title: {first_row.get('job_title')}")
        print(f"  teamName type: {type(first_row.get('teamName'))}")
        print(f"  teamName value: {first_row.get('teamName')}")
    
    print("\n✓ All tests passed!")
    
except Exception as e:
    import traceback
    print(f"\n✗ ERROR: {e}")
    print("\nTraceback:")
    traceback.print_exc()
    sys.exit(1)
