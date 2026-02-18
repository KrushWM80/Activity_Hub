import sqlite3
conn = sqlite3.connect('projects_cache.db')
cursor = conn.cursor()

print("Checking data in 7 missing columns:")
cols = ['owner', 'store_area', 'business_area', 'health', 'business_type', 'associate_impact', 'customer_impact']
for col in cols:
    cursor.execute(f'SELECT COUNT(DISTINCT {col}) FROM projects WHERE {col} IS NOT NULL AND {col} != ""')
    count = cursor.fetchone()[0]
    print(f"  {col}: {count} distinct values")

conn.close()
