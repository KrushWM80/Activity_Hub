"""Add optimized worker data endpoint"""
import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '@app.get("/Worker_Names_Stores_Missing_JobCodes_Optimized.json")' not in content:
    endpoint_code = '''

@app.get("/Worker_Names_Stores_Missing_JobCodes_Optimized.json")
async def get_worker_data_optimized():
    """Serve optimized worker data (count + sample) for faster tooltip loading"""
    import json as json_lib
    worker_data_dir = TEAMING_DIR
    json_file = os.path.join(worker_data_dir, "Worker_Names_Stores_Missing_JobCodes_Optimized.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json_lib.load(f)
        except Exception as e:
            print(f"Error reading optimized worker JSON: {e}")
    return []
'''
    content = re.sub(
        r'(@app\.get\("/Worker_Names_Stores_Missing_JobCodes\.json"\))',
        endpoint_code + r'\n\1',
        content
    )
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓ Optimized endpoint added to main.py')
else:
    print('✓ Optimized endpoint already exists')
