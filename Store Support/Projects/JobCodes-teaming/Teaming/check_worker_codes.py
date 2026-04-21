import pandas as pd
worker = pd.read_csv('Worker_Names_Stores_JobCodes.csv')
print('Checking for missing job codes in worker data:')
test_codes = ['1-0-40407', '1-0-40413', '1-0-40404', '1-0-40405']
for code in test_codes:
    matching = worker[worker['job_code'] == code]
    print(f'{code}: {len(matching)} records')
    if len(matching) > 0:
        print(f'  Sample: {matching.iloc[0]["job_nm"]}')

# Also check what job codes exist
print('\nAll unique job codes in worker data:')
print(worker['job_code'].unique()[:20])
