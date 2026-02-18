#!/usr/bin/env python3
"""
Live BigQuery Data Fetcher for AMP Dashboard
Connects to: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep
Exports data to JSON format for dashboard consumption
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

try:
    from google.cloud import bigquery
    from google.oauth2 import service_account
    BIGQUERY_AVAILABLE = True
except ImportError:
    print("⚠️  Google Cloud BigQuery library not installed")
    print("📦 Run: pip install google-cloud-bigquery")
    BIGQUERY_AVAILABLE = False

class LiveDataFetcher:
    def __init__(self):
        self.project_id = "wmt-assetprotection-prod"
        self.dataset_id = "Store_Support_Dev"
        self.table_id = "AMP_Data_Prep"
        self.client = None
        
    def setup_credentials(self, service_account_path: str = None):
        """Setup BigQuery client with authentication"""
        try:
            if service_account_path and os.path.exists(service_account_path):
                # Use service account JSON file
                credentials = service_account.Credentials.from_service_account_file(service_account_path)
                self.client = bigquery.Client(credentials=credentials, project=self.project_id)
                print(f"✅ Connected using service account: {service_account_path}")
            else:
                # Use default credentials (gcloud auth application-default login)
                self.client = bigquery.Client(project=self.project_id)
                print("✅ Connected using default application credentials")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def fetch_week39_data(self) -> List[Dict[str, Any]]:
        """Fetch all Week 39 published activities from BigQuery"""
        if not self.client:
            raise Exception("BigQuery client not initialized. Run setup_credentials() first.")
        
        # Query for Week 39 published activities with all required fields
        query = f"""
        SELECT 
            actv_title_home_ofc_nm as title,
            division,
            region,
            area,
            store_number,
            store_name,
            week_number as week,
            fiscal_year,
            published_date,
            preview_link,
            activity_type,
            status,
            created_by,
            last_modified
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE week_number = 39 
        AND status = 'Published'
        AND fiscal_year = 2026
        ORDER BY published_date DESC, division, region, area, store_number
        """
        
        print(f"🔍 Querying BigQuery table: {self.project_id}.{self.dataset_id}.{self.table_id}")
        print(f"📋 Query: {query}")
        
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            data = []
            for row in results:
                # Convert BigQuery row to dictionary
                item = {
                    'title': row.title or 'Untitled Activity',
                    'division': row.division or 'Unknown Division',
                    'region': row.region or 'Unknown Region', 
                    'area': row.area or 'Unknown Area',
                    'storeNumber': str(row.store_number) if row.store_number else 'N/A',
                    'storeName': row.store_name or 'Unknown Store',
                    'week': str(row.week) if row.week else '39',
                    'fiscalYear': str(row.fiscal_year) if row.fiscal_year else '2026',
                    'publishedDate': row.published_date.isoformat() if row.published_date else None,
                    'previewLink': row.preview_link or None,
                    'activityType': row.activity_type or 'Standard',
                    'status': row.status or 'Published',
                    'createdBy': row.created_by or 'System',
                    'lastModified': row.last_modified.isoformat() if row.last_modified else None,
                    'dataSource': 'BigQuery Live'
                }
                data.append(item)
            
            print(f"✅ Successfully fetched {len(data)} Week 39 published activities")
            return data
            
        except Exception as e:
            print(f"❌ Query failed: {e}")
            raise
    
    def export_to_json(self, data: List[Dict[str, Any]], filename: str = None) -> str:
        """Export data to JSON file for dashboard"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"live_amp_data_{timestamp}.json"
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        export_data = {
            'metadata': {
                'source': f"{self.project_id}.{self.dataset_id}.{self.table_id}",
                'exported_at': datetime.now().isoformat(),
                'total_records': len(data),
                'week_filter': '39',
                'fiscal_year': '2026',
                'status_filter': 'Published'
            },
            'data': data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Data exported to: {filepath}")
        return filepath

def main():
    """Main execution function"""
    print("🚀 AMP Dashboard Live Data Fetcher")
    print("=" * 50)
    
    if not BIGQUERY_AVAILABLE:
        print("\n❌ Cannot proceed without BigQuery library")
        print("📦 Install with: pip install google-cloud-bigquery")
        return False
    
    fetcher = LiveDataFetcher()
    
    # Try to setup credentials
    print("\n🔑 Setting up authentication...")
    
    # Check for service account file
    service_account_paths = [
        "service-account.json",
        "credentials.json",
        os.path.expanduser("~/Downloads/service-account.json")
    ]
    
    authenticated = False
    for path in service_account_paths:
        if os.path.exists(path):
            if fetcher.setup_credentials(path):
                authenticated = True
                break
    
    if not authenticated:
        # Try default credentials
        if fetcher.setup_credentials():
            authenticated = True
    
    if not authenticated:
        print("\n❌ Authentication failed!")
        print("\n📋 To authenticate, choose one option:")
        print("1. Place service account JSON file in current directory as 'service-account.json'")
        print("2. Run: gcloud auth application-default login")
        print("3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        return False
    
    # Fetch live data
    try:
        print(f"\n📊 Fetching Week 39 data from BigQuery...")
        data = fetcher.fetch_week39_data()
        
        if not data:
            print("⚠️  No data found for Week 39 FY2026 Published activities")
            return False
        
        # Export to JSON
        print(f"\n💾 Exporting {len(data)} records...")
        filepath = fetcher.export_to_json(data, "live_amp_data.json")
        
        # Summary
        print(f"\n📈 EXPORT SUMMARY:")
        print(f"   📁 File: {filepath}")
        print(f"   📊 Records: {len(data)}")
        
        preview_links = len([item for item in data if item.get('previewLink')])
        print(f"   🔗 Preview Links: {preview_links}")
        
        divisions = len(set(item.get('division', 'Unknown') for item in data))
        stores = len(set(item.get('storeNumber', 'N/A') for item in data))
        print(f"   🏪 Divisions: {divisions}, Stores: {stores}")
        
        print(f"\n✅ Live data ready! Load this file in your dashboard.")
        print(f"📂 File location: {os.path.abspath(filepath)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to fetch data: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)