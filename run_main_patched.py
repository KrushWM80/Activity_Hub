"""
Wrapper that patches main.py code before executing as main module.
Patches:
1. BigQuery Client to use credential default project
2. client.query() call to specify polaris-analytics-prod project
"""
import sys
import os

# Set up path
os.chdir(r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend')
sys.path.insert(0, os.getcwd())

# Read and patch main.py code
with open('main.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Apply patches
print("[PATCH] Applying BigQuery fixes...")

# Patch 1: Remove explicit project from Client initialization
code = code.replace(
    'client = bigquery.Client(project="polaris-analytics-prod")',
    'client = bigquery.Client()  # Use credential default project'
)

# Patch 2: Add project to query() call
code = code.replace(
    'results = client.query(query).result()',
    'results = client.query(query, project="polaris-analytics-prod").result()'
)

# Verify patches
if 'bigquery.Client()' in code and 'project="polaris-analytics-prod"' in code:
    print("[PATCH] All patches applied successfully")
    # Execute the patched code as if it were main.py
    exec(compile(code, 'main.py', 'exec'), {'__name__': '__main__'})
else:
    print("[PATCH] ERROR: Could not apply all patches")
    sys.exit(1)


