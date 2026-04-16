#!/usr/bin/env python3
"""
Data Bridge Schema Verification Helper for Activity Hub Projects Sync
Queries both source (Intake Hub) and target (Activity Hub Projects) tables
to verify column alignment and identify mapping requirements.

Usage:
    python verify_schema_alignment.py
    
Output:
    - Console summary with mapping status
    - schema_verification_report.csv for Admin review
"""

from google.cloud import bigquery
from typing import Dict, List, Tuple
import csv
from datetime import datetime
import sys

# Configuration
SOURCE_PROJECT = "wmt-assetprotection-prod"
SOURCE_DATASET = "Store_Support_Dev"
SOURCE_TABLE = "IH_Intake_Data"

TARGET_PROJECT = "wmt-assetprotection-prod"
TARGET_DATASET = "Store_Support_Dev"
TARGET_TABLE = "AH_Projects"

# Required columns in target (AH_Projects) with their descriptions
REQUIRED_COLUMNS = {
    "impact_id": "Project identifier",
    "title": "Project name",
    "business_area": "HR / Store Ops / Supply Chain / Technology",
    "owner_name": "Project owner name",
    "owner_id": "Project owner ID",
    "health_status": "On Track / At Risk / Off Track",
    "project_status": "Active / Inactive",
    "latest_update": "Most recent project update text",
    "created_at": "Timestamp when created",
    "updated_at": "Timestamp when last modified",
    "current_wm_week_update": "Boolean: True if updated in current Walmart Week"
}

# Suggested mappings where column names differ between source and target
# These are common naming variations to check during mapping logic
SUGGESTED_MAPPINGS = {
    "impact_id": ["project_id", "intake_id", "projectid", "id"],
    "title": ["project_name", "project_title", "name", "projectname"],
    "business_area": ["department", "area", "business_unit", "businessarea", "dept"],
    "owner_name": ["owner", "project_owner", "owner_full_name", "ownername"],
    "owner_id": ["owner_emp_id", "employee_id", "owner_employee_id", "ownerid"],
    "health_status": ["status", "project_health", "health", "healthstatus"],
    "project_status": ["state", "project_state", "active_status", "projectstatus"],
    "latest_update": ["last_update", "update_text", "recent_update", "latestupdate"],
    "created_at": ["creation_date", "created_date", "date_created", "createdat"],
    "updated_at": ["modification_date", "modified_date", "date_updated", "last_modified", "updatedat"],
    "current_wm_week_update": ["is_current_week_update", "updated_this_week", "week_updated", "currentweekupdate"]
}


def get_table_schema(project: str, dataset: str, table: str) -> Dict[str, str]:
    """
    Query BigQuery to get table schema.
    Returns dict of {column_name: column_type}
    """
    try:
        client = bigquery.Client(project=project)
        table_id = f"{project}.{dataset}.{table}"
        
        table = client.get_table(table_id)
        schema = {field.name: field.field_type for field in table.schema}
        
        return schema
    except Exception as e:
        print(f"Error retrieving schema for {project}.{dataset}.{table}: {str(e)}", file=sys.stderr)
        raise


def find_potential_mapping(target_column: str, source_columns: List[str]) -> Tuple[str, float]:
    """
    Find potential mapping in source columns for a target column.
    Returns (source_column, confidence_score) where score is 0-1.
    
    Scoring logic:
    - 1.0: Exact case-insensitive match
    - 0.9: Matches suggested mapping configuration
    - 0.7: Partial keyword match (substring match)
    - 0.0: No match found
    """
    target_lower = target_column.lower()
    source_lower_map = {col.lower(): col for col in source_columns}
    
    # 1. Exact match (score: 1.0)
    if target_lower in source_lower_map:
        return (source_lower_map[target_lower], 1.0)
    
    # 2. Check suggested mappings (score: 0.9)
    if target_column in SUGGESTED_MAPPINGS:
        for suggested in SUGGESTED_MAPPINGS[target_column]:
            suggested_lower = suggested.lower()
            if suggested_lower in source_lower_map:
                return (source_lower_map[suggested_lower], 0.9)
    
    # 3. Partial match - check if keywords exist (score: 0.7)
    keywords = target_lower.replace("_", " ").split()
    best_match = None
    best_score = 0
    
    for source_col in source_columns:
        source_col_lower = source_col.lower()
        matches = sum(1 for keyword in keywords if keyword in source_col_lower)
        if matches > 0:
            score = 0.7 * (matches / len(keywords))
            if score > best_score:
                best_score = score
                best_match = source_col
    
    if best_match:
        return (best_match, best_score)
    
    return (None, 0.0)


def generate_csv_report(source_schema: Dict[str, str], 
                       target_schema: Dict[str, str],
                       output_file: str = "schema_verification_report.csv") -> bool:
    """
    Generate CSV report for Admin Dashboard review.
    Includes mapping status and recommendations for each required column.
    """
    rows = []
    
    # CSV Header
    rows.append([
        "Target Column",
        "Status",
        "Target Type",
        "Source Column Match",
        "Source Type",
        "Match Confidence",
        "Column Description",
        "Admin Action Required"
    ])
    
    source_columns = list(source_schema.keys())
    
    for target_col in REQUIRED_COLUMNS.keys():
        target_type = target_schema.get(target_col, "MISSING")
        
        # Check if column exists in target
        if target_col in target_schema:
            status = "✓ Exists in Target"
        else:
            status = "⚠ Missing in Target"
        
        # Find best mapping from source
        source_match, confidence = find_potential_mapping(target_col, source_columns)
        
        if source_match:
            source_type = source_schema[source_match]
            confidence_pct = f"{confidence * 100:.0f}%"
            
            # Determine admin action
            if confidence == 1.0:
                action = "Ready for direct mapping"
            elif confidence == 0.9:
                action = "Verify mapping before sync - column name variation detected"
            else:
                action = "Manual review required - implement transformation logic or verify new column"
        else:
            source_match = "NOT FOUND"
            source_type = "N/A"
            confidence_pct = "0%"
            action = "Column missing from source - configure static value or custom logic"
        
        rows.append([
            target_col,
            status,
            target_type,
            source_match,
            source_type,
            confidence_pct,
            REQUIRED_COLUMNS[target_col],
            action
        ])
    
    # Write CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        
        print(f"✓ CSV Report saved: {output_file}")
        return True
    except Exception as e:
        print(f"Error writing CSV report: {str(e)}", file=sys.stderr)
        return False


def print_console_summary(source_schema: Dict[str, str], 
                         target_schema: Dict[str, str]):
    """
    Print human-readable summary to console for quick review.
    """
    print("\n" + "="*90)
    print("DATA BRIDGE SCHEMA VERIFICATION REPORT")
    print("="*90)
    print(f"\nSource:  {SOURCE_PROJECT}.{SOURCE_DATASET}.{SOURCE_TABLE}")
    print(f"Target:  {TARGET_PROJECT}.{TARGET_DATASET}.{TARGET_TABLE}")
    print(f"Report:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    print("\n" + "-"*90)
    print(f"{'Column':<25} {'Status':<10} {'Match':<30} {'Confidence':<12} {'Action':<15}")
    print("-"*90)
    
    source_columns = list(source_schema.keys())
    
    perfect_count = 0
    suggested_count = 0
    missing_count = 0
    not_in_target = 0
    
    for target_col in REQUIRED_COLUMNS.keys():
        # Check target
        if target_col not in target_schema:
            status = "MISSING"
            not_in_target += 1
            print(f"{target_col:<25} {status:<10} {'[NOT IN TARGET]':<30} {'':<12} {'Add column':<15}")
            continue
        
        # Find mapping
        source_match, confidence = find_potential_mapping(target_col, source_columns)
        
        if source_match:
            confidence_pct = f"{confidence * 100:.0f}%"
            
            if confidence == 1.0:
                status_sym = "✓"
                perfect_count += 1
                action = "Ready"
            elif confidence == 0.9:
                status_sym = "→"
                suggested_count += 1
                action = "Verify"
            else:
                status_sym = "~"
                suggested_count += 1
                action = "Review"
            
            print(f"{target_col:<25} {status_sym:<10} {source_match:<30} {confidence_pct:<12} {action:<15}")
        else:
            missing_count += 1
            print(f"{target_col:<25} {'✗':<10} {'[NO MAPPING]':<30} {'0%':<12} {'Create map':<15}")
    
    print("\n" + "-"*90)
    print("SUMMARY STATISTICS")
    print("-"*90)
    print(f"Required columns:        {len(REQUIRED_COLUMNS)}")
    print(f"  - Perfect mappings:    {perfect_count}  (exact match)")
    print(f"  - Suggested mappings:  {suggested_count}  (name variations)")
    print(f"  - Missing mappings:    {missing_count}  (no source column)")
    print(f"  - Not in target:       {not_in_target}  (column doesn't exist yet)")
    print(f"\nSource columns available: {len(source_schema)}")
    print(f"Target columns total:     {len(target_schema)}")
    print("\n" + "="*90 + "\n")


def main():
    """Main execution function."""
    print("\n[Data Bridge Schema Verification] Initializing...")
    
    try:
        # Retrieve schemas
        print(f"[1/3] Querying source schema...")
        source_schema = get_table_schema(SOURCE_PROJECT, SOURCE_DATASET, SOURCE_TABLE)
        print(f"      Found {len(source_schema)} columns in source table")
        
        print(f"[2/3] Querying target schema...")
        target_schema = get_table_schema(TARGET_PROJECT, TARGET_DATASET, TARGET_TABLE)
        print(f"      Found {len(target_schema)} columns in target table")
        
        # Generate reports
        print(f"[3/3] Generating verification reports...")
        print_console_summary(source_schema, target_schema)
        generate_csv_report(source_schema, target_schema)
        
        print("[✓] Schema verification complete - CSV report ready for Admin Dashboard review\n")
        return 0
    
    except Exception as e:
        print(f"\n[ERROR] Schema verification failed: {str(e)}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
