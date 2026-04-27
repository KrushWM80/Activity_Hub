"""
AMP AutoFeeds Missing Daily - Counts by Dimensions and Status

Queries BigQuery table: wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily
Returns: Count of Stores grouped by Series Title, Auto Feed ID, WM WK, Published Date, and Status
"""

from google.cloud import bigquery
import pandas as pd
from datetime import datetime

def query_amp_autofeeds_counts():
    """Query AMP AutoFeeds table for store counts by dimensions and status."""
    
    client = bigquery.Client()
    
    # Query with PIVOT to show Status breakdown
    query = """
    SELECT 
      Series_Title,
      Auto_Feed_ID,
      WM_WEEK_NBR,
      Published_Date,
      Status,
      COUNT(DISTINCT Store) as Store_Count
    FROM 
      `wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily`
    GROUP BY 
      Series_Title,
      Auto_Feed_ID,
      WM_WEEK_NBR,
      Published_Date,
      Status
    ORDER BY 
      Published_Date DESC,
      Series_Title,
      Auto_Feed_ID,
      WM_WEEK_NBR,
      Status
    """
    
    print("=" * 100)
    print("AMP AutoFeeds Missing Daily - Store Counts by Dimensions and Status")
    print("=" * 100)
    print(f"\nQuery execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Execute query
        query_job = client.query(query)
        results = query_job.to_dataframe()
        
        print(f"Query completed. Total rows returned: {len(results)}")
        print()
        
        if len(results) == 0:
            print("No data found in the table.")
            return
        
        # Display full results
        print("FULL RESULTS:")
        print("-" * 100)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(results.to_string())
        print()
        
        # Summary statistics
        print("\nSUMMARY STATISTICS:")
        print("-" * 100)
        print(f"Total unique Series Titles: {results['Series Title'].nunique()}")
        print(f"Total unique Auto Feed IDs: {results['Auto feed id'].nunique()}")
        print(f"Total unique WM WK numbers: {results['WM WK number'].nunique()}")
        print(f"Total unique Published Dates: {results['Published Date'].nunique()}")
        print(f"Total unique Statuses: {results['Status'].nunique()}")
        print(f"  Statuses: {', '.join(results['Status'].unique())}")
        print(f"Total stores across all dimensions: {results['Store_Count'].sum()}")
        print()
        
        # Status breakdown
        print("STORE COUNT BY STATUS:")
        print("-" * 100)
        status_summary = results.groupby('Status')['Store_Count'].sum().sort_values(ascending=False)
        for status, count in status_summary.items():
            print(f"  {status}: {count:,} stores")
        print()
        
        # Top publishers
        print("TOP 10 - Most Recent Auto Feeds (by Published Date):")
        print("-" * 100)
        recent = results.nlargest(10, 'Published Date')[['Published Date', 'Series Title', 'Auto feed id', 'WM WK number', 'Status', 'Store_Count']]
        for idx, row in recent.iterrows():
            print(f"  {row['Published Date']} | {row['Series Title'][:30]:30} | Feed: {row['Auto feed id']} | WK: {row['WM WK number']} | {row['Status']:15} | Stores: {row['Store_Count']}")
        print()
        
        # Save to CSV for further analysis
        csv_filename = f"amp_autofeeds_counts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(csv_filename, index=False)
        print(f"Results saved to: {csv_filename}")
        print()
        
        return results
        
    except Exception as e:
        print(f"ERROR executing query: {str(e)}")
        print("Please ensure:")
        print("  1. You are authenticated to Google Cloud (gcloud auth application-default login)")
        print("  2. You have permission to access: wmt-assetprotection-prod.Store_Support_Dev")
        print("  3. The table 'AMP AutoFeeds Missing Daily' exists")
        return None

def query_amp_autofeeds_pivot():
    """Alternative query with Status as columns (PIVOT)."""
    
    client = bigquery.Client()
    
    # Query with PIVOT for Status comparison
    query = """
    SELECT 
      Series_Title,
      Auto_Feed_ID,
      WM_WEEK_NBR,
      Published_Date,
      IFNULL(CAST(COUNTIF(Status = 'Active') AS STRING), '0') as Active_Count,
      IFNULL(CAST(COUNTIF(Status = 'Inactive') AS STRING), '0') as Inactive_Count,
      IFNULL(CAST(COUNTIF(Status = 'Pending') AS STRING), '0') as Pending_Count,
      COUNTIF(Status NOT IN ('Active', 'Inactive', 'Pending')) as Other_Status_Count,
      COUNT(DISTINCT Store) as Total_Store_Count
    FROM 
      `wmt-assetprotection-prod.Store_Support_Dev.AMP AutoFeeds Missing Daily`
    GROUP BY 
      Series_Title,
      Auto_Feed_ID,
      WM_WEEK_NBR,
      Published_Date
    ORDER BY 
      Published_Date DESC,
      Series_Title,
      Auto_Feed_ID,
      WM_WEEK_NBR
    """
    
    print("=" * 100)
    print("AMP AutoFeeds Missing Daily - PIVOT VIEW (Status as Columns)")
    print("=" * 100)
    print()
    
    try:
        query_job = client.query(query)
        results = query_job.to_dataframe()
        
        print(f"Query completed. Total dimension combinations: {len(results)}")
        print()
        
        if len(results) == 0:
            print("No data found in the table.")
            return
        
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(results.to_string())
        print()
        
        # Save pivot view
        csv_filename = f"amp_autofeeds_pivot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(csv_filename, index=False)
        print(f"Pivot results saved to: {csv_filename}")
        print()
        
        return results
        
    except Exception as e:
        print(f"ERROR executing pivot query: {str(e)}")
        return None

if __name__ == "__main__":
    # Run standard query
    results = query_amp_autofeeds_counts()
    
    print("\n" + "=" * 100)
    print("Running PIVOT view for easier status comparison...")
    print("=" * 100 + "\n")
    
    # Run pivot query
    pivot_results = query_amp_autofeeds_pivot()
