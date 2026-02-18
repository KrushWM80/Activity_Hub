#!/usr/bin/env python3
"""
Compare OPS_SUP_MARKET_TEAM and OPS_SUP_REGION_TEAM members 
with tableau_home_office_all_type_a AD Group

This script determines if users from the OPS groups are also in the Tableau group.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

print("=" * 80)
print("OPS Groups vs Tableau Group Comparison")
print("=" * 80)
print()

# Define source files
ad_groups_file = "ad_groups_20251215_154559.csv"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Check if AD groups file exists
if not Path(ad_groups_file).exists():
    print(f"ERROR: {ad_groups_file} not found!")
    print("This file should contain OPS_SUP_MARKET_TEAM and OPS_SUP_REGION_TEAM data.")
    sys.exit(1)

# Load AD groups data
print(f"Loading AD groups data from {ad_groups_file}...")
ad_df = pd.read_csv(ad_groups_file)

# Extract OPS_SUP_MARKET_TEAM members
ops_market = ad_df[ad_df['group'] == 'OPS_SUP_MARKET_TEAM'].copy()
print(f"✓ Loaded OPS_SUP_MARKET_TEAM: {len(ops_market)} members")

# Extract OPS_SUP_REGION_TEAM members
ops_region = ad_df[ad_df['group'] == 'OPS_SUP_REGION_TEAM'].copy()
print(f"✓ Loaded OPS_SUP_REGION_TEAM: {len(ops_region)} members")

# Combine both OPS groups
ops_combined = pd.concat([ops_market, ops_region], ignore_index=True)
ops_combined_unique = ops_combined.drop_duplicates(subset=['email'])
print(f"✓ Combined OPS groups (unique): {len(ops_combined_unique)} members")
print()

# Look for Tableau group file
tableau_files = list(Path('.').glob('tableau_home_office_all_type_a*.csv'))

if not tableau_files:
    print("=" * 80)
    print("TABLEAU GROUP DATA NOT FOUND")
    print("=" * 80)
    print()
    print("Please run the PowerShell script to extract Tableau group members:")
    print("  .\\Extract-Tableau-Group.ps1")
    print()
    print("Then run this script again.")
    print()
    sys.exit(1)

# Use the most recent Tableau file
tableau_file = max(tableau_files, key=lambda p: p.stat().st_mtime)
print(f"Loading Tableau group data from {tableau_file}...")

try:
    tableau_df = pd.read_csv(tableau_file)
    print(f"✓ Loaded tableau_home_office_all_type_a: {len(tableau_df)} members")
    print()
except Exception as e:
    print(f"ERROR reading {tableau_file}: {e}")
    sys.exit(1)

# Normalize emails for comparison (lowercase)
ops_emails = set(ops_combined_unique['email'].str.lower().dropna())
tableau_emails = set(tableau_df['email'].str.lower().dropna())

# Find overlaps
ops_in_tableau = ops_emails & tableau_emails
ops_not_in_tableau = ops_emails - tableau_emails

print("=" * 80)
print("ANALYSIS RESULTS")
print("=" * 80)
print()
print(f"OPS Groups (Market + Region):      {len(ops_emails):>5} unique members")
print(f"Tableau Group:                     {len(tableau_emails):>5} unique members")
print()
print(f"OPS members ALSO in Tableau:       {len(ops_in_tableau):>5} members ({len(ops_in_tableau)/len(ops_emails)*100:.1f}%)")
print(f"OPS members NOT in Tableau:        {len(ops_not_in_tableau):>5} members ({len(ops_not_in_tableau)/len(ops_emails)*100:.1f}%)")
print()

# Create detailed reports
if len(ops_in_tableau) > 0:
    # Users in both OPS and Tableau
    ops_in_tableau_df = ops_combined_unique[
        ops_combined_unique['email'].str.lower().isin(ops_in_tableau)
    ].copy()
    ops_in_tableau_df['Status'] = 'In Both OPS and Tableau'
    
    output_file_both = f'OPS_in_Tableau_{timestamp}.csv'
    ops_in_tableau_df.to_csv(output_file_both, index=False)
    print(f"✅ OPS members also in Tableau: {output_file_both}")

if len(ops_not_in_tableau) > 0:
    # Users in OPS but NOT in Tableau
    ops_not_in_tableau_df = ops_combined_unique[
        ops_combined_unique['email'].str.lower().isin(ops_not_in_tableau)
    ].copy()
    ops_not_in_tableau_df['Status'] = 'In OPS but NOT in Tableau'
    
    output_file_not = f'OPS_NOT_in_Tableau_{timestamp}.csv'
    ops_not_in_tableau_df.to_csv(output_file_not, index=False)
    print(f"✅ OPS members NOT in Tableau: {output_file_not}")

print()

# Show detailed breakdown by group
print("=" * 80)
print("BREAKDOWN BY OPS GROUP")
print("=" * 80)
print()

# OPS_SUP_MARKET_TEAM analysis
market_emails = set(ops_market['email'].str.lower().dropna())
market_in_tableau = market_emails & tableau_emails
market_not_in_tableau = market_emails - tableau_emails

print(f"OPS_SUP_MARKET_TEAM:")
print(f"  Total:              {len(market_emails):>5} members")
print(f"  In Tableau:         {len(market_in_tableau):>5} members ({len(market_in_tableau)/len(market_emails)*100:.1f}%)")
print(f"  NOT in Tableau:     {len(market_not_in_tableau):>5} members ({len(market_not_in_tableau)/len(market_emails)*100:.1f}%)")
print()

# OPS_SUP_REGION_TEAM analysis
region_emails = set(ops_region['email'].str.lower().dropna())
region_in_tableau = region_emails & tableau_emails
region_not_in_tableau = region_emails - tableau_emails

print(f"OPS_SUP_REGION_TEAM:")
print(f"  Total:              {len(region_emails):>5} members")
print(f"  In Tableau:         {len(region_in_tableau):>5} members ({len(region_in_tableau)/len(region_emails)*100:.1f}%)")
print(f"  NOT in Tableau:     {len(region_not_in_tableau):>5} members ({len(region_not_in_tableau)/len(region_emails)*100:.1f}%)")
print()

# Sample output
if len(ops_in_tableau) > 0:
    print("=" * 80)
    print("SAMPLE: OPS MEMBERS IN TABLEAU (first 10)")
    print("=" * 80)
    sample_df = ops_in_tableau_df[['email', 'display_name', 'title', 'group']].head(10)
    print(sample_df.to_string(index=False))
    print()

if len(ops_not_in_tableau) > 0:
    print("=" * 80)
    print("SAMPLE: OPS MEMBERS NOT IN TABLEAU (first 10)")
    print("=" * 80)
    sample_df = ops_not_in_tableau_df[['email', 'display_name', 'title', 'group']].head(10)
    print(sample_df.to_string(index=False))
    print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
