#!/usr/bin/env python3
"""
Fetch data from BigQuery table: wmt-pricingops-analytics.Ad_Hoc_Copp_Tables.mixed_base
"""

from google.cloud import bigquery
import pandas as pd
import os
from pathlib import Path

def fetch_mixed_base_data(limit=None):
    """
    Fetch data from the mixed_base table.
    
    Args:
        limit: Maximum number of rows to fetch (None = all rows)
    
    Returns:
        DataFrame with the fetched data
    """
    try:
        # Initialize BigQuery client
        client = bigquery.Client()
        
        # Build query
        query = """
        SELECT *
        FROM `wmt-pricingops-analytics.Ad_Hoc_Copp_Tables.mixed_base`
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        print(f"Fetching data from BigQuery...")
        print(f"Query: {query.strip()}")
        print("-" * 80)
        
        # Execute query
        df = client.query(query).to_dataframe()
        
        print(f"✓ Successfully fetched {len(df)} rows")
        print(f"✓ Columns: {list(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        print(f"Make sure you have BigQuery credentials set up.")
        return None


def save_to_csv(df, filename="mixed_base_data.csv"):
    """Save DataFrame to CSV file"""
    if df is None:
        return False
    
    try:
        filepath = Path(__file__).parent / filename
        df.to_csv(filepath, index=False)
        print(f"✓ Data saved to: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error saving CSV: {e}")
        return False


def display_sample(df, rows=10):
    """Display sample of the data"""
    if df is None:
        return
    
    print(f"\n📊 Sample Data (first {min(rows, len(df))} rows):")
    print("-" * 80)
    print(df.head(rows).to_string())
    print("-" * 80)
    print(f"\nData Info:")
    print(f"  Total Rows: {len(df)}")
    print(f"  Total Columns: {len(df.columns)}")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
    print(f"  Memory Usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")


def main():
    """Main execution"""
    print("=" * 80)
    print("BigQuery Data Fetcher - Mixed Base Table")
    print("=" * 80)
    
    # Fetch data (limit to 1000 for testing, remove limit for all data)
    df = fetch_mixed_base_data(limit=None)
    
    if df is not None:
        # Display sample
        display_sample(df, rows=5)
        
        # Save to CSV
        save_to_csv(df)
        
        print("\n✓ Done! Your data is ready to use in the HTML viewer.")
        print(f"  Open: data-viewer.html")
    else:
        print("\n✗ Failed to fetch data. Check your BigQuery credentials.")


if __name__ == "__main__":
    main()
