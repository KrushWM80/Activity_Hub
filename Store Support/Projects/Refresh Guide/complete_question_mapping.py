#!/usr/bin/env python3
"""
Complete Question Organization by Format & Area
================================================

Load all 334 questions and organize them by:
- Format (SC, DIV1, NHM)
- Area (Backroom, Asset Protection, Fresh, etc.)

This matches the baseline_structure.json counts:
- SC: 328 questions across 8 areas
- DIV1: 327 questions across 8 areas
- NHM: 209 questions across 6 areas
- EXTRA: 6 questions not in baseline (Q_329-Q_334)

Uses:
1. all_questions_with_metadata.json - Full question descriptions
2. baseline_questions_mapping.json - Partial Q_ID → Area mapping (42 mapped)
3. Heuristic categorization for unmapped questions based on description keywords
"""

import json
from pathlib import Path
from collections import defaultdict

# Load data files
metadata_file = Path(__file__).parent / "all_questions_with_metadata.json"
mapping_file = Path(__file__).parent / "baseline_questions_mapping.json"

with open(metadata_file) as f:
    all_questions = {q['id']: q['description'] for q in json.load(f)}

with open(mapping_file) as f:
    mapping_data = json.load(f)
    mapped_questions = mapping_data.get('mapped', {})

print("=" * 100)
print("COMPLETE QUESTION MAPPING BY FORMAT & AREA")
print("=" * 100)
print()

# Area keywords for categorization - derived from mapped questions and description patterns
AREA_KEYWORDS = {
    'Backroom': [
        'bins', 'vizpick', 'backroom', 'baler', 'compactor', 'steel', 'location', 'FAST',
        'trailer', 'fixture', 'supply', 'huddle board', 'one touch', 'carousel', 'freight',
        'cooler', 'freezer', 'location labels', 'zone', 'organize', 'tote'
    ],
    'Asset Protection': [
        'cctv', 'security', 'fuel', 'panic', 'dex', 'camera', 'door chime', 'call box',
        'emergency', 'blue claims', 'dsl', 'product removal'
    ],
    'Fresh': [
        'produce', 'bakery', 'deli', 'meat', 'dairy', 'frozen', 'fruit', 'vegetable',
        'wet wall', 'case', 'cooler', 'mister', 'scale', 'donut', 'pizza', 'deli island',
        'protein divider', 'sanitization', 'FIFO'
    ],
    'Salesfloor': [
        'aisle', 'endcap', 'action alley', 'modular', 'feature', 'topstock', 'label',
        'signing', 'shelf', 'availability', 'pinpoint', 'vizpick', 'device', 'deep clean zone',
        'hunting', 'fishing', 'paint'
    ],
    'Fashion': [
        'fashion', 'fitting room', 'waco', 'rfid', 'rack', 'shoe', 'mirror', 'rolling rack',
        'bench', 'jewelry', 'department 23', 'department 24', 'department 25', 'department 26',
        'department 29', 'department 31', 'department 32', 'department 33', 'department 34'
    ],
    'Store Fulfillment': [
        'inhome', 'inHome', 'pick path', 'fulfillment', 'parking', 'dispensing', 'mfl',
        'vehicle', 'alcohol', 'tote consolidation', 'badging', 'safety vest', 'van loading',
        'pre-trip', 'equipment readiness', 'shift guide', 'uniform'
    ],
    'ACC': [
        'acc', 'tire', 'service', 'oil bay', 'torque', 'wheel weight', 'balancer', 'tire machine',
        'lube', 'filter', 'wiper', 'battery', 'tpms', 'service writer', 'lower bay', 'upper bay',
        'fender', 'bump cap', 'ppe', 'smoke area'
    ],
    'Front End': [
        'front end', 'register', 'self checkout', 'service desk', 'scale', 'cash office',
        'marketplace', 'kiosk', 'vending', 'lottery', 'propane', 'payment', 'returns',
        'vestibule', 'money center', 'services', 'permit', 'snap', 'wic', 'sensory-friendly',
        'tenant', 'lounge'
    ]
}

# Format baseline definition
BASELINE = {
    'SC': {
        'areas': ['Backroom', 'Asset Protection', 'Fresh', 'Salesfloor', 'Fashion', 'Store Fulfillment', 'ACC', 'Front End'],
        'counts': {
            'Backroom': 54, 'Asset Protection': 19, 'Fresh': 49, 'Salesfloor': 27,
            'Fashion': 44, 'Store Fulfillment': 24, 'ACC': 55, 'Front End': 56
        },
        'total': 328
    },
    'DIV1': {
        'areas': ['Backroom', 'Asset Protection', 'Fresh', 'Salesfloor', 'Fashion', 'Store Fulfillment', 'ACC', 'Front End'],
        'counts': {
            'Backroom': 54, 'Asset Protection': 19, 'Fresh': 49, 'Salesfloor': 27,
            'Fashion': 44, 'Store Fulfillment': 23, 'ACC': 55, 'Front End': 56
        },
        'total': 327
    },
    'NHM': {
        'areas': ['Backroom', 'Asset Protection', 'Fresh', 'Salesfloor', 'Store Fulfillment', 'Front End'],
        'counts': {
            'Backroom': 51, 'Asset Protection': 15, 'Fresh': 47, 'Salesfloor': 18,
            'Store Fulfillment': 24, 'Front End': 54
        },
        'total': 209
    }
}

# Function to heuristically categorize a question
def categorize_question(q_id, description, mapped_categories):
    """
    Determine which area(s) a question belongs to based on:
    1. Direct mapping from baseline_questions_mapping.json
    2. Keyword matching in description
    3. Return best match or 'Unknown'
    """
    
    # Check if already mapped
    if q_id in mapped_categories:
        return mapped_categories[q_id]['area']
    
    # Keyword matching
    description_lower = description.lower()
    
    # Score each area based on keyword matches
    area_scores = defaultdict(int)
    for area, keywords in AREA_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in description_lower:
                area_scores[area] += 1
    
    if area_scores:
        best_area = max(area_scores, key=area_scores.get)
        return best_area
    
    return 'Unknown'

# Categorize all questions
categorized = defaultdict(lambda: defaultdict(list))
extra_questions = []
unknown_questions = []

print("CATEGORIZING ALL 334 QUESTIONS...")
print()

for q_id in sorted(all_questions.keys(), key=lambda x: int(x.split('_')[1])):
    description = all_questions[q_id]
    area = categorize_question(q_id, description, mapped_questions)
    
    q_num = int(q_id.split('_')[1])
    
    # Check if extra (beyond baseline)
    is_extra = q_num > 328
    
    if area == 'Unknown':
        unknown_questions.append((q_id, description))
    elif is_extra:
        extra_questions.append((q_id, area, description))
    else:
        # Assign to appropriate format(s)
        if area in BASELINE['NHM']['counts']:
            categorized['NHM'][area].append(q_id)
        categorized['SC'][area].append(q_id)
        if area in BASELINE['DIV1']['counts']:
            categorized['DIV1'][area].append(q_id)

# Output organized by Format
output = []
output.append("=" * 100)
output.append("STORE REFRESH QUESTIONS - ORGANIZED BY FORMAT & AREA")
output.append("=" * 100)
output.append("")

# SC Format
output.append("FORMAT: SUPERCENTER (SC) - 328 BASELINE QUESTIONS")
output.append("-" * 100)
sc_total = 0
for area in BASELINE['SC']['areas']:
    baseline_count = BASELINE['SC']['counts'][area]
    actual_qs = categorized['SC'][area]
    actual_count = len(actual_qs)
    sc_total += actual_count
    
    output.append("")
    output.append(f"  AREA: {area} ({baseline_count} baseline questions)")
    output.append(f"  Current: {actual_count} questions assigned")
    if actual_count != baseline_count:
        output.append(f"  ⚠️  GAP: {baseline_count - actual_count} questions")
    output.append(f"  Questions: {', '.join(sorted(actual_qs, key=lambda x: int(x.split('_')[1])))}")
output.append("")
output.append(f"SC TOTAL: {sc_total} questions (Baseline: {BASELINE['SC']['total']})")
output.append("")

# DIV1 Format
output.append("=" * 100)
output.append("FORMAT: DIVISION 1 (DIV1) - 327 BASELINE QUESTIONS")
output.append("-" * 100)
div1_total = 0
for area in BASELINE['DIV1']['areas']:
    baseline_count = BASELINE['DIV1']['counts'][area]
    actual_qs = categorized['DIV1'][area]
    actual_count = len(actual_qs)
    div1_total += actual_count
    
    output.append("")
    output.append(f"  AREA: {area} ({baseline_count} baseline questions)")
    output.append(f"  Current: {actual_count} questions assigned")
    if actual_count != baseline_count:
        output.append(f"  ⚠️  GAP: {baseline_count - actual_count} questions")
    output.append(f"  Questions: {', '.join(sorted(actual_qs, key=lambda x: int(x.split('_')[1])))}")
output.append("")
output.append(f"DIV1 TOTAL: {div1_total} questions (Baseline: {BASELINE['DIV1']['total']})")
output.append("")

# NHM Format
output.append("=" * 100)
output.append("FORMAT: NEIGHBORHOOD MARKET (NHM) - 209 BASELINE QUESTIONS")
output.append("-" * 100)
nhm_total = 0
for area in BASELINE['NHM']['areas']:
    baseline_count = BASELINE['NHM']['counts'][area]
    actual_qs = categorized['NHM'][area]
    actual_count = len(actual_qs)
    nhm_total += actual_count
    
    output.append("")
    output.append(f"  AREA: {area} ({baseline_count} baseline questions)")
    output.append(f"  Current: {actual_count} questions assigned")
    if actual_count != baseline_count:
        output.append(f"  ⚠️  GAP: {baseline_count - actual_count} questions")
    output.append(f"  Questions: {', '.join(sorted(actual_qs, key=lambda x: int(x.split('_')[1])))}")
output.append("")
output.append(f"NHM TOTAL: {nhm_total} questions (Baseline: {BASELINE['NHM']['total']})")
output.append("")

# Extra Questions
output.append("=" * 100)
output.append("EXTRA QUESTIONS (NOT IN BASELINE - MARKED WITH *)")
output.append("-" * 100)
output.append("")
for q_id, area, description in extra_questions:
    output.append(f"  {q_id} * ({area})")
    output.append(f"    → {description[:80]}...")
output.append("")
output.append(f"EXTRA TOTAL: {len(extra_questions)} questions")
output.append("")

# Summary
output.append("=" * 100)
output.append("SUMMARY")
output.append("=" * 100)
output.append(f"SC Questions:          {sc_total:3d} / {BASELINE['SC']['total']} baseline")
output.append(f"DIV1 Questions:        {div1_total:3d} / {BASELINE['DIV1']['total']} baseline")
output.append(f"NHM Questions:         {nhm_total:3d} / {BASELINE['NHM']['total']} baseline")
output.append(f"Extra Questions:       {len(extra_questions):3d} (Q_329-Q_334)")
output.append(f"Unknown Questions:     {len(unknown_questions):3d}")
output.append(f"TOTAL QUESTIONS:       {sc_total + div1_total + nhm_total + len(extra_questions) + len(unknown_questions)} on 2/23/26")
output.append("")
output.append(f"Maximum Possible Items (Correct Baseline):")
output.append(f"  SC:   3,555 stores × 328 questions =   1,166,040 items")
output.append(f"  DIV1:   366 stores × 327 questions =     119,682 items")
output.append(f"  NHM:    674 stores × 209 questions =     140,866 items")
output.append(f"  TOTAL:                                 1,426,588 items")
output.append("")

# Print output
report = "\n".join(output)
print(report)

# Save to file
output_file = Path(__file__).parent / "COMPLETE_QUESTION_STRUCTURE.txt"
with open(output_file, 'w') as f:
    f.write(report)

print()
print(f"✅ Report saved to: {output_file}")
