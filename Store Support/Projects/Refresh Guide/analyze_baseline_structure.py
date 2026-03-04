"""
Extract questions and organize them by Area/Topic structure
"""
import json
from collections import defaultdict

# Load all questions with descriptions
with open('all_questions_with_metadata.json', 'r') as f:
    questions = json.load(f)

# Define the baseline structure from embedded data
baseline_structure = {
    'SC': {
        'Backroom': 54,
        'Asset Protection': 19,
        'Fresh': 49,
        'Salesfloor': 27,
        'Fashion': 44,
        'Store Fulfillment': 24,
        'ACC': 55,
        'Front End': 56
    },
    'DIV1': {
        'Backroom': 54,
        'Asset Protection': 19,
        'Fresh': 49,
        'Salesfloor': 27,
        'Fashion': 44,
        'Store Fulfillment': 23,
        'ACC': 55,
        'Front End': 56
    },
    'NHM': {
        'Backroom': 51,
        'Asset Protection': 15,
        'Fresh': 47,
        'Salesfloor': 18,
        'Store Fulfillment': 24,
        'Front End': 54
    }
}

# Calculate totals
total_baseline_sc = sum(baseline_structure['SC'].values())
total_baseline_div1 = sum(baseline_structure['DIV1'].values())
total_baseline_nhm = sum(baseline_structure['NHM'].values())
total_baseline = total_baseline_sc + total_baseline_div1 + total_baseline_nhm

print("=" * 70)
print("BASELINE QUESTION STRUCTURE ANALYSIS")
print("=" * 70)
print(f"\nBaseline totals:")
print(f"  SC:    {total_baseline_sc} questions")
print(f"  DIV1:  {total_baseline_div1} questions")
print(f"  NHM:   {total_baseline_nhm} questions")
print(f"  TOTAL: {total_baseline} questions")

print(f"\nActual questions found on 2/23: {len(questions)}")
print(f"Difference: {len(questions) - total_baseline} extra questions")

print("\n" + "=" * 70)
print("BASELINE STRUCTURE BY FORMAT AND AREA")
print("=" * 70)

for fmt in ['SC', 'DIV1', 'NHM']:
    print(f"\n{fmt} Format:")
    total = 0
    for area in sorted(baseline_structure[fmt].keys()):
        count = baseline_structure[fmt][area]
        total += count
        print(f"  {area}: {count} questions")
    print(f"  TOTAL: {total}")

# Save structure for use in other scripts
with open('baseline_structure.json', 'w') as f:
    json.dump({
        'SC': baseline_structure['SC'],
        'DIV1': baseline_structure['DIV1'],
        'NHM': baseline_structure['NHM'],
        'summary': {
            'total_sc': total_baseline_sc,
            'total_div1': total_baseline_div1,
            'total_nhm': total_baseline_nhm,
            'total_baseline': total_baseline,
            'actual_questions_on_2_23': len(questions),
            'extra_questions': len(questions) - total_baseline
        }
    }, f, indent=2)

print(f"\n✓ Structure saved to baseline_structure.json")

print("\n" + "=" * 70)
print("ACTION NEEDED")
print("=" * 70)
print(f"\nWe have {len(questions)} total questions on 2/23")
print(f"Baseline expects {total_baseline} questions")
print(f"\n{len(questions) - total_baseline} questions are ABOVE baseline")
print("\nNext step: Categorize all 334 questions by Area and Topic")
print("based on their descriptions from BigQuery")
