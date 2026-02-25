#!/usr/bin/env python3
"""
CORRECTED: Extract Week 7 (2/16-2/23/26) assessment completion data from BigQuery
Query correct table: athena-gateway-prod.store_refresh.store_refresh_data
"""

from google.cloud import bigquery
from datetime import datetime, timedelta
import json
import os

def extract_week7_correct():
    """Extract Week 7 metrics from CORRECT BigQuery source."""
    
    try:
        client = bigquery.Client(project='wmt-assetprotection-prod')
    except Exception as e:
        print(f"❌ BigQuery connection failed: {e}")
        return None
    
    # Week 7: Latest snapshot for 2/23/26 (end of week)
    week7_date = "2026-02-23"
    
    print(f"🔍 Extracting correct Week 7 data from BigQuery")
    print(f"   Target date: {week7_date}")
    
    # DIAGNOSTIC: First, list available tables and see what exists
    print("\n📋 Checking available datasets and tables...")
    datasets_query = "SELECT schema_name FROM `athena-gateway-prod`.INFORMATION_SCHEMA.SCHEMATA LIMIT 10"
    
    try:
        print("\n🔎 Available datasets:")
        results = list(client.query(datasets_query).result())
        for row in results:
            print(f"   - {row['schema_name']}")
    except Exception as e:
        print(f"   ⚠️  Could not list datasets: {e}")
    
    #  Try multiple query approaches
    queries = [
        # Approach 1: Direct table query with DATE filter
        {
            'name': 'Direct date filter',
            'sql': """
            SELECT
                completion_date,
                total_completed_items,
                total_possible_items,
                ROUND(total_completed_items / total_possible_items * 100, 1) as completion_pct
            FROM `athena-gateway-prod.store_refresh.store_refresh_data`
            WHERE DATE(completion_date) = @target_date
            LIMIT 1
            """,
            'params': [bigquery.ScalarQueryParameter("target_date", "DATE", week7_date)]
        },
        # Approach 2: Using snapshot_date field
        {
            'name': 'snapshot_date field',
            'sql': """
            SELECT
                snapshot_date,
                total_completed_items,
                total_possible_items,
                ROUND(total_completed_items / total_possible_items * 100, 1) as completion_pct
            FROM `athena-gateway-prod.store_refresh.store_refresh_data`
            WHERE DATE(snapshot_date) = @target_date
            LIMIT 1
            """,
            'params': [bigquery.ScalarQueryParameter("target_date", "DATE", week7_date)]
        },
        # Approach 3: Generic SELECT * to see schema
        {
            'name': 'Schema discovery (SELECT *)',
            'sql': """
            SELECT *
            FROM `athena-gateway-prod.store_refresh.store_refresh_data`
            LIMIT 1
            """,
            'params': []
        },
    ]
    
    for query_info in queries:
        print(f"\n📊 Trying: {query_info['name']}...")
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=query_info['params'])
            results = client.query(query_info['sql'], job_config=job_config).result()
            rows = list(results)
            
            if rows:
                print(f"✅ Success with '{query_info['name']}'")
                print(f"   Row data: {dict(rows[0])}")
                
                # If we got schema info, show field names
                if 'SELECT *' in query_info['sql']:
                    print(f"\n📋 Available fields in store_refresh_data:")
                    for field in rows[0].keys():
                        print(f"   - {field}")
                    return None  # Continue to next approach
                
                # Extract completion data if available
                row = rows[0]
                if 'total_completed_items' in row and row['total_completed_items'] is not None:
                    total_completed_items = int(row['total_completed_items'])
                    total_possible_items = int(row['total_possible_items']) if 'total_possible_items' in row else 1677600
                    completion_pct = float(row['completion_pct']) if 'completion_pct' in row else (total_completed_items / total_possible_items * 100)
                    
                    print(f"\n✅ WEEK 7 DATA EXTRACTED:")
                    print(f"   ✨ Total Completed Items: {total_completed_items:,}")
                    print(f"   Total Possible Items: {total_possible_items:,}")
                    print(f"   Completion %: {completion_pct:.1f}%")
                    
                    return {
                        'total_completed_items': total_completed_items,
                        'total_possible_items': total_possible_items,
                        'completion_pct': completion_pct
                    }
            else:
                print(f"⚠️  No results")
                
        except Exception as e:
            print(f"❌ Query failed: {type(e).__name__}: {str(e)[:100]}")
    
    return None


def extract_division_stats(start_date, end_date):
    """Extract division-level stats for Week 7."""
    try:
        client = bigquery.Client(project='wmt-assetprotection-prod')
    except:
        return None
    
    query = """
    SELECT
        division_id,
        division_name,
        SUM(store_count) as store_count,
        SUM(assigned_count) as assigned_count,
        SUM(completed_count) as completed_count,
        SUM(max_possible_count) as max_possible_count,
        ROUND(SUM(completed_count) / SUM(max_possible_count) * 100, 1) as completion_pct
    FROM `athena-gateway-prod.store_refresh.store_refresh_division_stats`
    WHERE DATE(snapshot_date) BETWEEN @start_date AND @end_date
    GROUP BY division_id, division_name
    ORDER BY division_id
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    
    try:
        results = client.query(query, job_config=job_config).result()
        divisions = []
        for row in results:
            divisions.append({
                'division_id': row['division_id'],
                'division_name': row['division_name'],
                'store_count': int(row['store_count']),
                'assigned_count': int(row['assigned_count']),
                'completed_count': int(row['completed_count']),
                'max_possible_count': int(row['max_possible_count']),
                'completion_pct': float(row['completion_pct'])
            })
        return divisions
    except:
        return None


if __name__ == "__main__":
    print("=" * 70)
    print("CORRECTED WEEK 7 DATA EXTRACTION")
    print("=" * 70)
    
    week7_data = extract_week7_correct()
    
    if week7_data:
        print("\n" + "=" * 70)
        print("RESULT: Use this totalCompletedItems value:")
        print(f">>> {week7_data['total_completed_items']:,}")
        print("=" * 70)
    else:
        print("\n❌ Failed to extract Week 7 data")
