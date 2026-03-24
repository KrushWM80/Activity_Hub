"""
Sample data: 49 Dallas POC projects for V.E.T. Dashboard
Includes 5 At Risk projects + 44 On Track projects
"""

import json

SAMPLE_DATA_49_PROJECTS = [
    # At Risk Projects (5)
    {'Initiative - Project Title': 'POS Modernization Phase 2', 'Health Status': 'At Risk', 'Phase': 'Roll/Deploy', '# of Stores': 85, 'Executive Notes': 'Jane Doe - Delays', 'TDA Ownership': 'Dallas POC', 'WM Week': 'WK10', 'Intake & Testing': 'Complete', 'Deployment': 'Behind'},
    {'Initiative - Project Title': 'Mobile App Stability', 'Health Status': 'At Risk', 'Phase': 'Test', '# of Stores': 120, 'Executive Notes': 'Robert - Bottleneck', 'TDA Ownership': 'Dallas POC', 'WM Week': 'WK12', 'Intake & Testing': 'Remediation', 'Deployment': 'Blocked'},
    {'Initiative - Project Title': 'Backend API Migration', 'Health Status': 'At Risk', 'Phase': 'Test', '# of Stores': 45, 'Executive Notes': 'Sarah Chen - Errors', 'TDA Ownership': 'Dallas POC', 'WM Week': 'WK11', 'Intake & Testing': 'Delayed', 'Deployment': 'Pending'},
    {'Initiative - Project Title': 'Store Network Upgrade', 'Health Status': 'At Risk', 'Phase': 'Roll/Deploy', '# of Stores': 200, 'Executive Notes': 'Mike - Hardware issue', 'TDA Ownership': 'Dallas POC', 'WM Week': 'WK09', 'Intake & Testing': 'Complete', 'Deployment': 'Shortage'},
    {'Initiative - Project Title': 'Authentication System', 'Health Status': 'At Risk', 'Phase': 'POC/POT', '# of Stores': 60, 'Executive Notes': 'Lisa - Compliance', 'TDA Ownership': 'Dallas POC', 'WM Week': 'WK13', 'Intake & Testing': 'Approval', 'Deployment': 'Hold'},
    # On Track - Project groups by phase (44 total)
]

# Generate 44 On Track projects
for i in range(44):
    phase_list = ['Pending', 'POC/POT', 'Test', 'Mkt Scale', 'Roll/Deploy']
    phase = phase_list[i % len(phase_list)]
    week = f'WK{15 + (i % 8)}'
    stores = 100 + (i * 3)
    poc = f'POC {chr(65 + (i % 26))}'
    
    project = {
        'Initiative - Project Title': f'E-Commerce Platform {i+1}',
        'Health Status': 'On Track',
        'Phase': phase,
        '# of Stores': stores,
        'Executive Notes': f'{poc} - On track',
        'TDA Ownership': 'Dallas POC',
        'WM Week': week,
        'Intake & Testing': 'Active',
        'Deployment': 'On schedule'
    }
    SAMPLE_DATA_49_PROJECTS.append(project)

# Verify count
assert len(SAMPLE_DATA_49_PROJECTS) == 49, f'Expected 49 projects, got {len(SAMPLE_DATA_49_PROJECTS)}'
