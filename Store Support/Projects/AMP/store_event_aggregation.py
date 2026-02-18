import pandas as pd

# Read the AMP primary data
df = pd.read_csv(r'c:\Users\krush\Documents\VSCode\AMP\AMP data\AMP_Data_Primary.csv')

# Filter for Week 2, FY 2026 to match current dashboard
df_week2 = df[(df['WM_YEAR_NBR'] == 2026) & (df['Week'] == 2)]

# Group by store and count distinct event_ids
store_event_counts = df_week2.groupby('store')['event_id'].nunique().reset_index()
store_event_counts.columns = ['store', 'event_count']

# Calculate high and low
store_high = store_event_counts['event_count'].max()
store_low = store_event_counts['event_count'].min()
store_avg = store_event_counts['event_count'].mean()

print(f"AMP Store-Level Event Distribution (WM Week 2, 2026)")
print(f"=" * 60)
print(f"Store High: {store_high} events")
print(f"Store Low: {store_low} events")
print(f"Store Avg: {store_avg:.2f} events")
print(f"\nTotal Unique Stores: {len(store_event_counts)}")
print(f"\nTop 10 Stores by Event Count:")
print(store_event_counts.nlargest(10, 'event_count').to_string(index=False))
print(f"\nBottom 10 Stores by Event Count:")
print(store_event_counts.nsmallest(10, 'event_count').to_string(index=False))

# Save as JSON for dashboard use
import json
output = {
    'store_high': int(store_high),
    'store_low': int(store_low),
    'store_avg': round(store_avg, 2),
    'total_stores': len(store_event_counts),
    'week': 2,
    'fy': 2026
}

with open(r'c:\Users\krush\Documents\VSCode\AMP\Store Updates Dashboard\store_metrics.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ Store metrics saved to store_metrics.json")
