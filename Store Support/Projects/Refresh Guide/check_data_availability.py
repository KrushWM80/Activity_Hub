from google.cloud import bigquery

client = bigquery.Client(project="athena-gateway-prod")

# Check what date range exists in the data
query = """
SELECT 
    MIN(exportDate) as earliest_date,
    MAX(exportDate) as latest_date,
    COUNT(DISTINCT exportDate) as unique_dates,
    COUNT(*) as total_records
FROM `athena-gateway-prod.store_refresh.store_refresh_data`
"""

print("=" * 70)
print("BIGQUERY DATA AVAILABILITY CHECK")
print("=" * 70)
print()

try:
    results = client.query(query).result()
    for row in results:
        print(f"Earliest Date:     {row.earliest_date}")
        print(f"Latest Date:       {row.latest_date}")
        print(f"Unique Dates:      {row.unique_dates}")
        print(f"Total Records:     {row.total_records:,}")
        print()
        
except Exception as e:
    print(f"Error: {e}")

print("=" * 70)
print()
print("Now checking engagement for EACH week with data...")
print()

# Check each week individually
weeks = {
    "Week 2 (2026-01-10 to 2026-01-17)": ("2026-01-10", "2026-01-17"),
    "Week 3 (2026-01-18 to 2026-01-24)": ("2026-01-18", "2026-01-24"),
    "Week 4 (2026-01-25 to 2026-01-31)": ("2026-01-25", "2026-01-31"),
    "Week 5 (2026-02-01 to 2026-02-07)": ("2026-02-01", "2026-02-07"),
    "Week 6 (2026-02-08 to 2026-02-14)": ("2026-02-08", "2026-02-14"),
    "Week 7 (2026-02-15 to 2026-02-21)": ("2026-02-15", "2026-02-21"),
}

for week_label, (start_date, end_date) in weeks.items():
    query = f"""
    SELECT 
        COUNT(DISTINCT assignedTo) as workers,
        COUNT(DISTINCT assignedBy) as managers,
        COUNT(*) as total_actions,
        COUNT(DISTINCT exportDate) as days_with_data
    FROM `athena-gateway-prod.store_refresh.store_refresh_data`
    WHERE exportDate BETWEEN '{start_date}' AND '{end_date}'
    """
    
    try:
        results = client.query(query).result()
        for row in results:
            print(f"{week_label}")
            print(f"  Days with data:    {row.days_with_data}")
            print(f"  Workers:           {row.workers:,}") 
            print(f"  Managers:          {row.managers:,}")
            print(f"  Total Actions:     {row.total_actions:,}")
            print()
            
    except Exception as e:
        print(f"Error for {week_label}: {e}")
        print()
