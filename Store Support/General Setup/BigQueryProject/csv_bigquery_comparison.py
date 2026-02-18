#!/usr/bin/env python3
"""
AMP Data Comparison Tool
Compares the updated AMP_Data_Primary.CSV with our BigQuery integration output
to identify missing fields and logic from AMP Data.tflx
"""

import csv
import json
from collections import defaultdict, Counter
import os

def analyze_csv_structure():
    """Analyze the structure and content of AMP_Data_Primary.CSV"""
    
    print("=" * 100)
    print("AMP Data CSV Analysis - Comparing with BigQuery Integration")
    print("=" * 100)
    print()
    
    csv_file = 'AMP_Data_Primary.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        return None
    
    try:
        # Get file size
        file_size = os.path.getsize(csv_file) / (1024 * 1024)  # MB
        print(f"📁 File Size: {file_size:.2f} MB")
        
        # Read CSV structure and sample data
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            
            # Use csv.Sniffer to detect format
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            print(f"📋 Detected delimiter: '{delimiter}'")
            
            # Read header and sample rows
            reader = csv.reader(f, delimiter=delimiter)
            headers = next(reader)
            
            print(f"📊 Total Columns: {len(headers)}")
            print()
            
            # Analyze column structure
            print("Column Analysis:")
            print("-" * 80)
            
            # Read sample rows for data analysis
            sample_rows = []
            row_count = 0
            for i, row in enumerate(reader):
                if i < 10:  # Get first 10 rows for analysis
                    sample_rows.append(row)
                row_count = i + 1
                if i >= 1000:  # Stop after 1000 rows to avoid memory issues
                    break
            
            print(f"📈 Total Rows Analyzed: {min(row_count, 1000)} (sample)")
            print()
            
            # Display columns with sample data
            for i, header in enumerate(headers):
                sample_values = []
                for row in sample_rows:
                    if i < len(row) and row[i].strip():
                        sample_values.append(row[i].strip())
                
                unique_values = len(set(sample_values)) if sample_values else 0
                sample_display = ', '.join(sample_values[:3]) if sample_values else 'No data'
                
                print(f"{i+1:3d}. {header:30} | Unique: {unique_values:4d} | Sample: {sample_display}")
            
            return {
                'headers': headers,
                'sample_rows': sample_rows,
                'row_count': row_count,
                'file_size_mb': file_size
            }
    
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None

def load_our_bigquery_schema():
    """Load our generated BigQuery schema for comparison"""
    
    try:
        with open('tableau_schema_extracted.json', 'r') as f:
            tableau_schema = json.load(f)
        
        # Get our BigQuery mapping
        bigquery_mapping = tableau_schema.get('bigquery_mapping', {})
        
        # Flatten all our BigQuery fields
        our_fields = []
        for category, fields in bigquery_mapping.items():
            our_fields.extend(fields)
        
        return {
            'tableau_schema': tableau_schema,
            'our_bigquery_fields': our_fields,
            'field_count': len(our_fields)
        }
    
    except Exception as e:
        print(f"❌ Error loading BigQuery schema: {e}")
        return None

def compare_schemas(csv_analysis, bigquery_schema):
    """Compare CSV columns with our BigQuery schema"""
    
    if not csv_analysis or not bigquery_schema:
        return
    
    print("=" * 100)
    print("SCHEMA COMPARISON: CSV vs BigQuery Integration")
    print("=" * 100)
    print()
    
    csv_headers = csv_analysis['headers']
    our_fields = bigquery_schema['our_bigquery_fields']
    
    print(f"📊 CSV Columns: {len(csv_headers)}")
    print(f"📊 Our BigQuery Fields: {len(our_fields)}")
    print()
    
    # Convert to sets for comparison
    csv_set = set(h.strip().lower().replace(' ', '_').replace('-', '_') for h in csv_headers)
    our_set = set(f.lower().replace(' ', '_').replace('-', '_') for f in our_fields)
    
    # Find missing fields
    missing_in_our_schema = csv_set - our_set
    missing_in_csv = our_set - csv_set
    common_fields = csv_set & our_set
    
    print("🔍 Field Comparison Results:")
    print("-" * 80)
    print(f"✅ Fields in Both: {len(common_fields)}")
    print(f"❌ Missing from Our Schema: {len(missing_in_our_schema)}")
    print(f"⚠️  Missing from CSV: {len(missing_in_csv)}")
    print()
    
    if missing_in_our_schema:
        print("❌ CRITICAL: Fields in CSV but MISSING from our BigQuery schema:")
        print("-" * 80)
        # Map back to original CSV headers
        missing_original = []
        for csv_header in csv_headers:
            normalized = csv_header.strip().lower().replace(' ', '_').replace('-', '_')
            if normalized in missing_in_our_schema:
                missing_original.append(csv_header)
        
        for i, field in enumerate(missing_original, 1):
            print(f"{i:3d}. {field}")
        print()
    
    if missing_in_csv:
        print("⚠️  Fields in our BigQuery schema but NOT in CSV:")
        print("-" * 80)
        for i, field in enumerate(sorted(missing_in_csv), 1):
            print(f"{i:3d}. {field}")
        print()
    
    return {
        'csv_fields': csv_headers,
        'our_fields': our_fields,
        'missing_in_our_schema': missing_original if missing_in_our_schema else [],
        'missing_in_csv': list(missing_in_csv),
        'common_fields': list(common_fields)
    }

def analyze_csv_data_patterns(csv_analysis):
    """Analyze data patterns in the CSV to understand Tableau logic"""
    
    if not csv_analysis:
        return
    
    print("=" * 100)
    print("CSV DATA PATTERN ANALYSIS")
    print("=" * 100)
    print()
    
    headers = csv_analysis['headers']
    sample_rows = csv_analysis['sample_rows']
    
    # Look for key patterns that might indicate missing logic
    calculated_fields = []
    date_fields = []
    status_fields = []
    numeric_fields = []
    
    for i, header in enumerate(headers):
        header_lower = header.lower()
        
        # Check for calculated/derived fields
        if any(keyword in header_lower for keyword in ['calculation', 'calc', 'derived', 'computed']):
            calculated_fields.append(header)
        
        # Check for date fields
        if any(keyword in header_lower for keyword in ['date', 'time', 'ts', 'day', 'week', 'month', 'year']):
            date_fields.append(header)
        
        # Check for status fields  
        if any(keyword in header_lower for keyword in ['status', 'state', 'flag', 'ind', 'type']):
            status_fields.append(header)
        
        # Analyze sample data for this column
        sample_values = []
        for row in sample_rows:
            if i < len(row) and row[i].strip():
                sample_values.append(row[i].strip())
        
        # Check if numeric
        numeric_count = 0
        for val in sample_values:
            try:
                float(val)
                numeric_count += 1
            except:
                pass
        
        if numeric_count > len(sample_values) * 0.8 and sample_values:  # 80% numeric
            numeric_fields.append(header)
    
    print("🔢 Calculated/Derived Fields Found:")
    for i, field in enumerate(calculated_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    print("📅 Date/Time Fields Found:")
    for i, field in enumerate(date_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    print("📊 Status/Flag Fields Found:")
    for i, field in enumerate(status_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    print("🔢 Numeric Fields Found:")
    for i, field in enumerate(numeric_fields, 1):
        print(f"  {i:2d}. {field}")
    print()
    
    return {
        'calculated_fields': calculated_fields,
        'date_fields': date_fields,
        'status_fields': status_fields,
        'numeric_fields': numeric_fields
    }

def generate_missing_field_analysis(comparison_result):
    """Generate detailed analysis of missing fields and required updates"""
    
    if not comparison_result or not comparison_result['missing_in_our_schema']:
        print("✅ No missing fields detected - our schema appears complete!")
        return
    
    print("=" * 100)
    print("REQUIRED BIGQUERY SCHEMA UPDATES")
    print("=" * 100)
    print()
    
    missing_fields = comparison_result['missing_in_our_schema']
    
    print(f"🚨 CRITICAL: {len(missing_fields)} fields found in CSV that are MISSING from our BigQuery integration!")
    print()
    
    # Categorize missing fields
    amp_event_missing = []
    calendar_missing = []
    store_missing = []
    calculated_missing = []
    other_missing = []
    
    for field in missing_fields:
        field_lower = field.lower()
        
        if any(keyword in field_lower for keyword in ['event', 'message', 'amp', 'activity', 'title', 'priority', 'status']):
            amp_event_missing.append(field)
        elif any(keyword in field_lower for keyword in ['date', 'time', 'week', 'year', 'day', 'calendar', 'fiscal']):
            calendar_missing.append(field)
        elif any(keyword in field_lower for keyword in ['store', 'location', 'city', 'state', 'region', 'banner']):
            store_missing.append(field)
        elif any(keyword in field_lower for keyword in ['calculation', 'calc', 'computed', 'derived', 'rank', 'count']):
            calculated_missing.append(field)
        else:
            other_missing.append(field)
    
    print("📋 Missing Fields by Category:")
    print("-" * 80)
    
    if amp_event_missing:
        print(f"🎯 AMP Event Fields Missing ({len(amp_event_missing)}):")
        for field in amp_event_missing:
            print(f"   - {field}")
        print()
    
    if calendar_missing:
        print(f"📅 Calendar/Date Fields Missing ({len(calendar_missing)}):")
        for field in calendar_missing:
            print(f"   - {field}")
        print()
    
    if store_missing:
        print(f"🏪 Store/Location Fields Missing ({len(store_missing)}):")
        for field in store_missing:
            print(f"   - {field}")
        print()
    
    if calculated_missing:
        print(f"🔢 Calculated Fields Missing ({len(calculated_missing)}):")
        for field in calculated_missing:
            print(f"   - {field}")
        print()
    
    if other_missing:
        print(f"❓ Other Fields Missing ({len(other_missing)}):")
        for field in other_missing:
            print(f"   - {field}")
        print()
    
    # Generate update recommendations
    print("=" * 100)
    print("BIGQUERY INTEGRATION UPDATE RECOMMENDATIONS")
    print("=" * 100)
    print()
    
    print("🔧 Required Updates to BigQuery Schema:")
    print("-" * 80)
    
    print("1. Add missing AMP event fields to the primary query")
    print("2. Implement missing calculated fields from Tableau logic")
    print("3. Add missing calendar dimension calculations")
    print("4. Include missing store dimension fields")
    print("5. Re-examine AMP Data.tflx for complex calculated fields")
    print()
    
    print("📝 Next Steps:")
    print("-" * 80)
    print("1. Analyze each missing field in the original AMP Data.tflx")
    print("2. Identify calculated field formulas and business logic")
    print("3. Update BigQuery SQL to include missing fields")
    print("4. Validate updated schema against CSV output")
    print("5. Re-generate production integration query")
    print()
    
    return {
        'amp_event_missing': amp_event_missing,
        'calendar_missing': calendar_missing,
        'store_missing': store_missing,
        'calculated_missing': calculated_missing,  
        'other_missing': other_missing,
        'total_missing': len(missing_fields)
    }

def main():
    """Main analysis function"""
    
    print("🔍 Starting AMP Data CSV vs BigQuery Integration Comparison...")
    print()
    
    # Step 1: Analyze CSV structure
    csv_analysis = analyze_csv_structure()
    
    if not csv_analysis:
        print("❌ Failed to analyze CSV file. Exiting.")
        return
    
    # Step 2: Load our BigQuery schema
    bigquery_schema = load_our_bigquery_schema()
    
    if not bigquery_schema:
        print("❌ Failed to load BigQuery schema. Exiting.")
        return
    
    # Step 3: Compare schemas
    comparison_result = compare_schemas(csv_analysis, bigquery_schema)
    
    # Step 4: Analyze CSV data patterns
    data_patterns = analyze_csv_data_patterns(csv_analysis)
    
    # Step 5: Generate missing field analysis
    missing_analysis = generate_missing_field_analysis(comparison_result)
    
    # Save analysis results
    analysis_results = {
        'csv_analysis': {
            'total_columns': len(csv_analysis['headers']),
            'total_rows': csv_analysis['row_count'],
            'file_size_mb': csv_analysis['file_size_mb'],
            'headers': csv_analysis['headers']
        },
        'bigquery_schema': {
            'total_fields': bigquery_schema['field_count'],
            'our_fields': bigquery_schema['our_bigquery_fields']
        },
        'comparison': comparison_result,
        'data_patterns': data_patterns,
        'missing_analysis': missing_analysis
    }
    
    # Save results to file
    output_file = f"amp_csv_bigquery_comparison_{os.path.splitext(os.path.basename(__file__))[0]}.json"
    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    print("=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    print(f"📁 Results saved to: {output_file}")
    print()
    
    if missing_analysis and missing_analysis['total_missing'] > 0:
        print("🚨 ACTION REQUIRED: Missing fields detected!")
        print(f"   {missing_analysis['total_missing']} fields need to be added to BigQuery integration")
        print("   Review the missing field analysis above and update the integration SQL")
    else:
        print("✅ Schema appears complete - no missing fields detected!")
    
    print("=" * 100)

if __name__ == "__main__":
    main()