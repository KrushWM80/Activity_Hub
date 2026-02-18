"""
Simplified BigQuery Direct Connection
Uses Google Cloud CLI authentication (gcloud auth)
"""

import subprocess
import json
import sys
import os
from datetime import datetime

def check_gcloud_auth():
    """Check if user is authenticated with gcloud"""
    try:
        result = subprocess.run(['gcloud', 'auth', 'list'], 
                              capture_output=True, text=True, check=True)
        
        if 'ACTIVE' in result.stdout:
            print("✅ Google Cloud authentication found")
            return True
        else:
            print("❌ No active Google Cloud authentication")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ gcloud CLI not found or not authenticated")
        return False
    except FileNotFoundError:
        print("❌ Google Cloud CLI not installed")
        return False

def authenticate_gcloud():
    """Authenticate with Google Cloud"""
    print("🔐 Starting Google Cloud authentication...")
    
    try:
        # Run gcloud auth login
        subprocess.run(['gcloud', 'auth', 'login'], check=True)
        
        # Set the project
        subprocess.run(['gcloud', 'config', 'set', 'project', 'wmt-assetprotection-prod'], check=True)
        
        print("✅ Authentication successful!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Authentication failed: {e}")
        return False

def fetch_bigquery_data():
    """Fetch data directly from BigQuery using bq command"""
    
    query = """
    SELECT 
        actv_title_home_ofc_nm as title,
        division,
        region,
        market,
        store_nbr,
        store_name,
        week,
        created_date,
        preview_link,
        status,
        verification_status
    FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
    WHERE week = 39 
      AND status = 'Published'
      AND preview_link IS NOT NULL
      AND preview_link != ''
    ORDER BY created_date DESC
    LIMIT 1000
    """
    
    print("📊 Fetching data from BigQuery...")
    print("🎯 Table: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep")
    
    try:
        # Use bq query command to fetch data
        result = subprocess.run([
            'bq', 'query',
            '--use_legacy_sql=false',
            '--format=json',
            '--max_rows=1000',
            query
        ], capture_output=True, text=True, check=True)
        
        # Parse the JSON output
        data = json.loads(result.stdout)
        
        print(f"✅ Successfully fetched {len(data)} records")
        
        # Save to file for dashboard
        output_file = 'real_bigquery_data.json'
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved to: {output_file}")
        
        # Show preview of data
        if data:
            print("\n📋 Data Preview:")
            print(f"   First title: {data[0].get('title', 'N/A')}")
            print(f"   Preview link: {data[0].get('preview_link', 'N/A')[:80]}...")
            print(f"   Division: {data[0].get('division', 'N/A')}")
        
        return data
        
    except subprocess.CalledProcessError as e:
        print(f"❌ BigQuery query failed: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON output: {e}")
        return None

def main():
    """Main function to connect to BigQuery"""
    
    print("🔗 BigQuery Direct Connection")
    print("=" * 40)
    
    # Check if already authenticated
    if not check_gcloud_auth():
        print("\n🔐 Authentication required...")
        
        choice = input("Do you want to authenticate now? (y/n): ").lower().strip()
        if choice != 'y':
            print("❌ Authentication required to continue")
            return
        
        if not authenticate_gcloud():
            print("❌ Failed to authenticate")
            return
    
    # Fetch the data
    data = fetch_bigquery_data()
    
    if data:
        print("\n🎉 SUCCESS! BigQuery data is ready!")
        print("\n📋 Next steps:")
        print("1. Refresh your dashboard (F5)")
        print("2. Look for 'REAL BigQuery Data Connected!' status")
        print("3. Test the preview links - they should all work!")
        
        # Optional: Start the dashboard server
        start_server = input("\nStart dashboard server now? (y/n): ").lower().strip()
        if start_server == 'y':
            print("🚀 Starting dashboard server...")
            os.system('python -m http.server 8080')
    else:
        print("\n❌ Failed to fetch BigQuery data")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure you have access to wmt-assetprotection-prod project")
        print("2. Verify BigQuery API is enabled")
        print("3. Check your permissions for Store_Support_Dev.AMP_Data_Prep")

if __name__ == '__main__':
    main()