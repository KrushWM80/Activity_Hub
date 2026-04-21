"""Add worker data endpoint to main.py"""
import re
import os

backend_dir = os.path.join(os.path.dirname(__file__), "dashboard", "backend")
main_py = os.path.join(backend_dir, "main.py")

with open(main_py, 'r', encoding='utf-8') as f:
    content = f.read()

endpoint_code = '''

@app.get("/Worker_Names_Stores_Missing_JobCodes.json")
async def get_worker_data():
    """Serve worker data for employee tooltips"""
    import json as json_lib
    worker_data_dir = TEAMING_DIR
    json_file = os.path.join(worker_data_dir, "Worker_Names_Stores_Missing_JobCodes.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json_lib.load(f)
        except Exception as e:
            print(f"Error reading worker JSON: {e}")
    csv_file = os.path.join(worker_data_dir, "Worker_Names_Stores_Missing_JobCodes.csv")
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading worker CSV: {e}")
    return []
'''

# Only add if not already present
if '@app.get("/Worker_Names_Stores_Missing_JobCodes.json")' not in content:
    # Replace the if __name__ line with endpoint + if __name__ line
    content = re.sub(
        r'(if __name__ == "__main__":)',
        endpoint_code + r'\n\1',
        content
    )
    with open(main_py, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Endpoint added successfully to main.py")
else:
    print("✓ Endpoint already exists in main.py")
