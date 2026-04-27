from google.cloud import bigquery

client = bigquery.Client(project='wmt-assetprotection-prod')

# Get detailed column information for Cal_Dim_Data
query = """
SELECT 
    column_name,
    data_type,
    is_nullable,
    ordinal_position
FROM `wmt-assetprotection-prod.Store_Support_Dev.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'Cal_Dim_Data'
ORDER BY ordinal_position
"""

results = list(client.query(query).result())

print("=" * 80)
print("Cal_Dim_Data Table Schema")
print("=" * 80)
print(f"{'Column Name':<30} {'Data Type':<15} {'Nullable':<10} {'Position':<10}")
print("-" * 80)

for row in results:
    nullable = "YES" if row.is_nullable == "YES" else "NO"
    print(f"{row.column_name:<30} {row.data_type:<15} {nullable:<10} {row.ordinal_position:<10}")

print("\n" + "=" * 80)
print("Sample Data from Cal_Dim_Data (current date)")
print("=" * 80)

sample_query = """
SELECT *
FROM `wmt-assetprotection-prod.Store_Support_Dev.Cal_Dim_Data`
WHERE CALENDAR_DATE = CURRENT_DATE()
LIMIT 1
"""

sample_results = list(client.query(sample_query).result())

if sample_results:
    row = sample_results[0]
    print(f"\nDate: {row.CALENDAR_DATE}")
    print(f"WM Week: {row.WM_WEEK_NBR}")
    print(f"Fiscal Year: {row.FISCAL_YEAR_NBR}")
    print(f"Calendar Year: {row.CAL_YEAR_NBR}")
    print(f"WM Quarter: {row.WM_QTR_NAME}")
    print(f"Day of Week: {row.Week_Day}")
else:
    print("No data for current date")
