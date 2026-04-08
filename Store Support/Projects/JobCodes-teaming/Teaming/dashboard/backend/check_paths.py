import os
main_py_path = r"c:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\Projects\JobCodes-teaming\Teaming\dashboard\backend\main.py"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(main_py_path)))
json_path = os.path.join(base_dir, 'job_codes_master.json')
print(f"main.py path: {main_py_path}")
print(f"BASE_DIR: {base_dir}")
print(f"JSON path: {json_path}")
print(f"JSON exists: {os.path.exists(json_path)}")

# Also check backend folder
backend_dir = os.path.dirname(os.path.abspath(main_py_path))
json_in_backend = os.path.join(backend_dir, 'job_codes_master.json')
print(f"\nAlternative in backend: {json_in_backend}")
print(f"Exists in backend: {os.path.exists(json_in_backend)}")
