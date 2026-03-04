"""
Map all 335 questions to Area/Topic and create baseline questions master file
"""
import json
import re
from collections import defaultdict

# Question mapping based on NOTES_ANALYSIS_REPORT.md data
# This includes all questions mentioned in the report with their Area/Topic
question_mapping = {
    # Asset Protection
    'Q_67': ('Asset Protection', 'CCTV System'),
    'Q_68': ('Asset Protection', 'Security - Fuel Station'),
    'Q_70': ('Asset Protection', 'Call Boxes'),
    'Q_75': ('Asset Protection', 'DSL Blue Tote'),
    
    # Backroom
    'Q_33': ('Backroom', 'California Baler Keys'),
    'Q_38': ('Backroom', 'FAST Unloader Equipment'),
    'Q_41': ('Backroom', 'Fixture Cage'),
    'Q_48': ('Backroom', 'Trailers'),
    
    # ACC (Auto Care Center) - Q_224 to Q_267
    'Q_224': ('ACC', 'Exterior Service Writer Station'),
    'Q_225': ('ACC', 'Exterior Signing'),
    'Q_226': ('ACC', 'Exterior Signing'),
    'Q_227': ('ACC', 'Service Area'),
    'Q_228': ('ACC', 'Tools Boards/Wheel Weight'),
    'Q_229': ('ACC', 'Tools Boards/Wheel Weight'),
    'Q_230': ('ACC', 'Tools Boards/Wheel Weight'),
    'Q_231': ('ACC', 'Tools Boards/Wheel Weight'),
    'Q_232': ('ACC', 'Tools Boards/Wheel Weight'),
    'Q_233': ('ACC', 'Service Area Equipment'),
    'Q_234': ('ACC', 'Service Area Equipment'),
    'Q_238': ('ACC', 'Service Area Equipment'),
    'Q_239': ('ACC', 'Lower Bay/Upper Bay'),
    'Q_242': ('ACC', 'Lower Bay/Upper Bay'),
    'Q_243': ('ACC', 'Lower Bay/Upper Bay'),
    'Q_246': ('ACC', 'Backroom'),
    'Q_254': ('ACC', 'Oil Bay/Filter Modular'),
    'Q_255': ('ACC', 'Oil Bay/Filter Modular'),
    
    # Store Fulfillment / InHome
    'Q_202': ('Store Fulfillment', 'InHome Equipment'),
    'Q_203': ('Store Fulfillment', 'Equipment Readiness'),
    'Q_220': ('Store Fulfillment', 'InHome Shift Guide'),
    'Q_221': ('Store Fulfillment', 'InHome Vehicle Guide'),
    'Q_222': ('Store Fulfillment', 'InHome Uniforms'),
    'Q_223': ('Store Fulfillment', 'InHome Pre-trip'),
    
    # Fresh
    'Q_93': ('Fresh', 'Meat'),
    'Q_100': ('Fresh', 'Bakery'),
    
    # Front End
    'Q_282': ('Front End', 'First Impressions'),
    'Q_307': ('Front End', 'Service Desk'),
    'Q_310': ('Front End', 'Marketplace Returns'),
    'Q_324': ('Front End', 'Automated Kiosks/Vending'),
    'Q_325': ('Front End', 'Automated Kiosks/Vending'),
    'Q_326': ('Front End', 'Automated Kiosks/Vending'),
    'Q_331': ('Front End', 'Tenant Services'),
    
    # Salesfloor
    'Q_148': ('Salesfloor', 'Modulars'),
    
    # Uncategorized - will need manual mapping or additional data
    # For now, create placeholder entries
}

# Load all 335 questions
with open('all_questions_2_23.json', 'r') as f:
    all_questions = json.load(f)

# Build full mapping
full_mapping = {}
unmapped = []

for q_data in all_questions:
    q_id = q_data['id']
    if q_id in question_mapping:
        area, topic = question_mapping[q_id]
        full_mapping[q_id] = (area, topic)
    else:
        unmapped.append(q_id)

print(f"Total questions: {len(all_questions)}")
print(f"Mapped questions: {len(full_mapping)}")
print(f"Unmapped questions: {len(unmapped)}")

if unmapped:
    print(f"\nUnmapped question IDs:")
    print(', '.join(unmapped[:50]))  # Show first 50
    if len(unmapped) > 50:
        print(f"... and {len(unmapped) - 50} more")

# Organize by Area/Topic
area_topic_questions = defaultdict(lambda: defaultdict(list))

for q_id, (area, topic) in full_mapping.items():
    area_topic_questions[area][topic].append(q_id)

# Sort everything
sorted_areas = sorted(area_topic_questions.keys())

# Create markdown file in user's format
markdown_content = """# Store Refresh Checklist - Baseline Questions Master List

**Generated:** March 3, 2026  
**Total Unique Questions (2/23/2026 Data):** {total_questions}  
**Mapped Questions:** {mapped_questions}  
**Unmapped Questions:** {unmapped_count}

---

## Baseline Questions by Area & Topic

""".format(
    total_questions=len(all_questions),
    mapped_questions=len(full_mapping),
    unmapped_count=len(unmapped)
)

for area in sorted_areas:
    markdown_content += f"\n### {area}\n\n"
    
    for topic in sorted(area_topic_questions[area].keys()):
        questions = sorted(area_topic_questions[area][topic], 
                          key=lambda x: int(x.split('_')[1]))
        markdown_content += f"**{topic}**\n"
        markdown_content += f"{', '.join(questions)}\n\n"

if unmapped:
    markdown_content += "\n---\n\n## Unmapped Questions (Need Area/Topic Assignment)\n\n"
    markdown_content += f"**Count:** {len(unmapped)}\n\n"
    
    # Group unmapped by ID range to identify patterns
    unmapped_sorted = sorted(unmapped, key=lambda x: int(x.split('_')[1]))
    markdown_content += ', '.join(unmapped_sorted) + "\n"

# Save markdown file
with open('BASELINE_QUESTIONS_MASTER.md', 'w') as f:
    f.write(markdown_content)

print("\n✓ Created BASELINE_QUESTIONS_MASTER.md")

# Also save JSON for programmatic use
mapping_json = {
    'total_questions': len(all_questions),
    'mapped': {q_id: {'area': area, 'topic': topic} for q_id, (area, topic) in full_mapping.items()},
    'unmapped': unmapped,
    'summary': {
        'total': len(all_questions),
        'mapped_count': len(full_mapping),
        'unmapped_count': len(unmapped)
    }
}

with open('baseline_questions_mapping.json', 'w') as f:
    json.dump(mapping_json, f, indent=2)

print("✓ Created baseline_questions_mapping.json")
print("\nFiles saved:")
print("  - BASELINE_QUESTIONS_MASTER.md")
print("  - baseline_questions_mapping.json")
