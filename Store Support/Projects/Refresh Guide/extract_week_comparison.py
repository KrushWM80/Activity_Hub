from google.cloud import bigquery

client = bigquery.Client(project="athena-gateway-prod")

# Get Week 6 and Week 7 cumulative data separately
queries = {
    "Week 6 (through 2026-02-14)": "WHERE exportDate <= '2026-02-14'",
    "Week 7 (through 2026-02-21)": "WHERE exportDate <= '2026-02-21'"
}

print("=" * 80)
print("CUMULATIVE ENGAGEMENT METRICS BY WEEK")
print("=" * 80)
print()

for week_label, where_clause in queries.items():
    query = f"""
    SELECT 
        COUNT(DISTINCT assignedTo) as workers,
        COUNT(DISTINCT assignedBy) as managers,
        COUNT(*) as total_actions
    FROM `athena-gateway-prod.store_refresh.store_refresh_data`
    {where_clause}
    """
    
    try:
        results = client.query(query).result()
        for row in results:
            total_users = row.workers + row.managers
            actions_per_user = row.total_actions / total_users if total_users > 0 else 0
            
            print(f"{week_label}:")
            print(f"  Workers:           {row.workers:,}")
            print(f"  Managers:          {row.managers:,}")
            print(f"  Total Users:       {total_users:,}")
            print(f"  Total Actions:     {row.total_actions:,}")
            print(f"  Actions per User:  {actions_per_user:.1f}")
            print()
            
    except Exception as e:
        print(f"Error for {week_label}: {e}")
        print()

print("=" * 80)
