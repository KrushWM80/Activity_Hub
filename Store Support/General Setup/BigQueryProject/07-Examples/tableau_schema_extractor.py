#!/usr/bin/env python3
"""
Tableau Schema Extractor for AMP Data Integration
Extracts field definitions, data sources, and relationships from Tableau flow files
"""

import json
import re
from collections import defaultdict

def extract_tableau_schema():
    """Extract schema information from Tableau flow and display settings"""
    
    print("=" * 80)
    print("AMP Data - Tableau Schema Extraction")
    print("=" * 80)
    print()
    
    # Read flow file
    try:
        with open('AMP_Data_contents/flow', 'r', encoding='utf-8') as f:
            flow_data = json.load(f)
        print("✓ Flow file loaded successfully")
    except Exception as e:
        print(f"✗ Error loading flow file: {e}")
        return
    
    # Read display settings
    try:
        with open('AMP_Data_contents/displaySettings', 'r', encoding='utf-8') as f:
            display_data = json.load(f)
        print("✓ Display settings loaded successfully")
    except Exception as e:
        print(f"✗ Error loading display settings: {e}")
        return
    
    print()
    
    # Extract field information from display settings
    field_ordinals = display_data.get('fieldOrder', {}).get('fieldOrdinals', {})
    
    print("Field Definitions Extracted from Tableau:")
    print("-" * 80)
    
    # Parse field names and clean them
    field_mapping = {}
    business_fields = []
    
    for field_id, ordinal in field_ordinals.items():
        # Extract meaningful field names
        field_parts = field_id.split('-')
        if len(field_parts) > 1:
            field_name = field_parts[-1]
            # Clean up field names
            field_name = field_name.replace(' ', '_').replace('(', '').replace(')', '')
            if field_name and not field_name.startswith('58d06522') and not field_name.startswith('285df139'):
                if field_name not in ['Default', 'Split', '1', '2', '3']:
                    business_fields.append(field_name)
                    field_mapping[field_id] = field_name
    
    # Remove duplicates and sort
    unique_fields = sorted(list(set(business_fields)))
    
    print(f"Total unique business fields identified: {len(unique_fields)}")
    print()
    
    # Categorize fields
    amp_event_fields = []
    calendar_fields = []
    store_fields = []
    system_fields = []
    
    for field in unique_fields:
        field_lower = field.lower()
        if any(keyword in field_lower for keyword in ['event', 'message', 'amp', 'title', 'status', 'priority', 'urgent', 'legal', 'hidden']):
            amp_event_fields.append(field)
        elif any(keyword in field_lower for keyword in ['wm', 'week', 'year', 'day', 'created', 'ts']):
            calendar_fields.append(field)
        elif any(keyword in field_lower for keyword in ['store', 'cnt', 'area', 'target', 'audience']):
            store_fields.append(field)
        else:
            system_fields.append(field)
    
    # Display categorized fields
    print("AMP Event Fields:")
    for i, field in enumerate(amp_event_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    print("Calendar/Time Fields:")
    for i, field in enumerate(calendar_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    print("Store/Business Fields:")
    for i, field in enumerate(store_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    print("System/Other Fields:")
    for i, field in enumerate(system_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    # Extract data source information from flow
    print("Data Source Analysis:")
    print("-" * 80)
    
    # Look for data connections in flow
    nodes = flow_data.get('nodes', {})
    data_sources = []
    
    for node_id, node_data in nodes.items():
        node_type = node_data.get('nodeType', '')
        if 'Input' in node_type or 'Load' in node_type:
            name = node_data.get('name', 'Unknown')
            data_sources.append(name)
    
    if data_sources:
        print("Identified Data Sources:")
        for i, source in enumerate(data_sources, 1):
            print(f"  {i}. {source}")
    else:
        print("No explicit data sources found in flow - likely using embedded data")
    
    print()
    
    # Generate BigQuery field mapping
    print("Suggested BigQuery Field Mapping:")
    print("-" * 80)
    
    bigquery_mapping = {
        'AMP_Event_Fields': [
            'event_id',
            'message_id', 
            'message_title',
            'message_description',
            'message_start_date',
            'message_end_date',
            'message_date',
            'business_area',
            'activity_type',
            'message_type',
            'message_status',
            'priority_level',
            'store_number',
            'created_by',
            'created_date',
            'modified_by',
            'modified_date',
            'published_date',
            'expiration_date',
            'approval_status',
            'workflow_stage'
        ],
        'Calendar_Fields': [
            'FISCAL_YEAR_NBR',
            'WM_WEEK_NBR',
            'WM_QTR_NAME',
            'WM_YEAR_NBR',
            'CAL_YEAR_NBR',
            'Date_Day_Number',
            'THE_DAY',
            'Today',
            'Week_Day'
        ],
        'Store_Fields': [
            'STORE_NBR',
            'CITY_NAME',
            'POSTAL_CODE',
            'REGION_NBR',
            'MARKET_AREA_NBR',
            'format_code',
            'SUBDIV_NAME',
            'BANNER_CODE',
            'BANNER_DESC',
            'STORE_TYPE_CODE',
            'STORE_TYPE_DESC',
            'OPEN_STATUS_CODE',
            'OPEN_STATUS_DESC',
            'COUNTY_NAME',
            'COUNTRY_CODE',
            'STATE_PROV_CODE',
            'LATITUDE_DGR',
            'LONGITUDE_DGR'
        ]
    }
    
    for category, fields in bigquery_mapping.items():
        print(f"{category}:")
        for field in fields:
            print(f"  - {field}")
        print()
    
    # Generate integration recommendations
    print("Integration Recommendations:")
    print("-" * 80)
    
    print("1. Primary BigQuery Table Mapping:")
    print("   wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT")
    print("   Maps to: AMP Event Fields from Tableau schema")
    print()
    
    print("2. Calendar Dimension Integration:")
    print("   wmt-edw-prod.US_CORE_DIM_VM.CALENDAR_DIM")
    print("   Maps to: Calendar/Time Fields with Walmart-specific calculations")
    print()
    
    print("3. Store Business Unit Integration:")
    print("   wmt-loc-cat-prod.catalog_location_views.businessunit_view")
    print("   Maps to: Store/Business Fields with subdivision mapping")
    print()
    
    print("4. Key Join Strategy:")
    print("   - AMP Events ↔ Calendar: DATE(message_start_date) = CALENDAR_DATE")
    print("   - AMP Events ↔ Stores: store_number = CAST(business_unit_nbr AS NUMERIC)")
    print()
    
    # Save extracted schema
    schema_output = {
        'extraction_summary': {
            'total_fields': len(unique_fields),
            'amp_fields': len(amp_event_fields),
            'calendar_fields': len(calendar_fields),
            'store_fields': len(store_fields),
            'system_fields': len(system_fields)
        },
        'tableau_fields': {
            'amp_event_fields': amp_event_fields,
            'calendar_fields': calendar_fields,
            'store_fields': store_fields,
            'system_fields': system_fields
        },
        'bigquery_mapping': bigquery_mapping,
        'data_sources': data_sources
    }
    
    with open('tableau_schema_extracted.json', 'w') as f:
        json.dump(schema_output, f, indent=2)
    
    print(f"5. Schema Details Saved:")
    print("   tableau_schema_extracted.json - Complete field mapping and analysis")
    print()
    
    print("=" * 80)
    print("Schema extraction complete!")
    print("Use this mapping to align Tableau fields with BigQuery table structure.")
    print("=" * 80)

if __name__ == "__main__":
    extract_tableau_schema()