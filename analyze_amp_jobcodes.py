import pandas as pd
import os
from datetime import datetime

def analyze_amp_jobcodes():
    """Analyze AMP job codes from existing CSV files"""
    
    try:
        print("=" * 120)
        print("AMP JOB CODE ANALYSIS - FROM EXISTING DATA")
        print("=" * 120)
        print(f"\nStarting analysis at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Paths to CSV files
        user_details_path = r"Store Support/Projects/JobCodes-teaming/Teaming/User_Details_JobCodes.csv"
        polaris_codes_path = r"Store Support/Projects/JobCodes-teaming/Teaming/polaris_job_codes.csv"

        # Job codes by AMP category
        team_lead_codes = [
            '1-600-7200', '1-600-7220', '1-610-7210', '1-615-7200', '1-615-7210',
            '1-620-7200', '1-625-7200', '1-630-7200', '1-635-7240', '1-640-7200',
            '1-640-7210', '1-990-7210', '1-695-7500', '59-65-2104', '6-10-101',
            '6-37-814', '71-76-121', '71-76-122', '71-76-123', '1-695-7530'
        ]
        hr_codes = ['1-910-7250']
        sm_codes = ['1-993-1001', '1-993-1071', '1-993-3001', '1-993-1026']
        coach_codes = [
            '71-76-622', '71-76-623', '1-993-1099', '1-993-1072', '1-993-1077',
            '1-993-1097', '1-993-1076', '1-993-1075', '1-993-1078', '1-993-1062',
            '1-993-1074', '1-993-1079', '1-996-758', '6-10-812', '6-10-811', '1-993-1085'
        ]

        all_codes = sorted(set(team_lead_codes + hr_codes + sm_codes + coach_codes))
        print(f"Total codes to analyze: {len(all_codes)}\n")

        # Load User Details CSV
        print("Loading User Details data...")
        try:
            df_user_details = pd.read_csv(user_details_path)
            print(f"✓ Loaded {len(df_user_details)} employee records\n")
            
            # Create paytype mapping from actual employees
            paytype_map = {}
            for code in all_codes:
                employees = df_user_details[df_user_details['job_code'] == code]
                if not employees.empty:
                    paytypes = set(employees['worker_payment_type'].unique())
                    if len(paytypes) == 1:
                        paytype_map[code] = list(paytypes)[0]
                    elif len(paytypes) > 1:
                        paytype_map[code] = 'BOTH'
                    else:
                        paytype_map[code] = 'UNKNOWN'
        except Exception as e:
            print(f"⚠ Could not load User Details: {e}\n")
            paytype_map = {}

        # Load Polaris Job Codes CSV
        print("Loading Polaris Job Codes reference...")
        try:
            df_polaris = pd.read_csv(polaris_codes_path)
            df_polaris.columns = df_polaris.columns.str.lower()
            job_title_map = dict(zip(df_polaris['job_code'], df_polaris['job_nm']))
            print(f"✓ Loaded {len(df_polaris)} job code references\n")
        except Exception as e:
            print(f"⚠ Could not load Polaris codes: {e}\n")
            job_title_map = {}

        # Build combined results
        print("=" * 120)
        print("ALL RESULTS")
        print("=" * 120 + "\n")
        
        results = []
        found_count = 0
        
        for code in all_codes:
            paytype = paytype_map.get(code, 'NOT FOUND')
            title = job_title_map.get(code, 'Unknown')
            
            if paytype != 'NOT FOUND':
                found_count += 1
            
            results.append({
                'Job Code': code,
                'Paytype': paytype,
                'Job Title': title
            })
            
            print(f"  {code:15} | {paytype:10} | {title}")

        print(f"\nTotal found: {found_count}/{len(all_codes)}")

        # Category Summary
        print("\n" + "=" * 120)
        print("SUMMARY BY CATEGORY")
        print("=" * 120)

        categories = {
            'TEAM LEAD': team_lead_codes,
            'HR PERSONNEL': hr_codes,
            'STORE MANAGER': sm_codes,
            'COACH': coach_codes
        }
        
        for cat_name, cat_codes in categories.items():
            found_cat = sum(1 for code in cat_codes if paytype_map.get(code) != 'NOT FOUND')
            print(f"\n{cat_name}: {found_cat}/{len(cat_codes)}")
            print("-" * 120)
            
            for code in sorted(cat_codes):
                paytype = paytype_map.get(code, 'NOT FOUND')
                title = job_title_map.get(code, 'Unknown')
                status = "✓" if paytype != 'NOT FOUND' else "✗"
                print(f"  {status} {code:15} | {paytype:10} | {title}")

        print("\n" + "=" * 120)
        print(f"ANALYSIS COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 120)
        
        # Export to CSV
        df_results = pd.DataFrame(results)
        output_file = "amp_jobcodes_analysis.csv"
        df_results.to_csv(output_file, index=False)
        print(f"\n✓ Results exported to: {output_file}")

    except Exception as e:
        print(f'\n❌ ERROR: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    analyze_amp_jobcodes()
