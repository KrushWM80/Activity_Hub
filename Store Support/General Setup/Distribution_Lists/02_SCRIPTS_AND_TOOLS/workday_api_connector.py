#!/usr/bin/env python3
"""
Workday API Direct Feed Connector
Establishes direct connection to Workday REST API for real-time job data

Requirements:
- Workday RaaS (Report as a Service) or REST API access
- API credentials from Workday admin
- requests library: pip install requests
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import csv
from typing import Dict, List, Optional
from datetime import datetime
import os


class WorkdayAPIConnector:
    """
    Direct connection to Workday API for job data extraction
    """

    def __init__(self, config_file: str = "workday_config.json"):
        """
        Initialize connector with configuration
        
        Config file should contain:
        {
            "tenant": "walmart",
            "api_version": "v1",
            "username": "your_api_username",
            "password": "your_api_password",
            "base_url": "https://wd5-impl-services1.workday.com",
            "raas_report_url": "optional_custom_report_url"
        }
        """
        self.config = self._load_config(config_file)
        self.session = None
        self.connected = False
        
    def _load_config(self, config_file: str) -> Dict:
        """Load API configuration from file"""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"X Error loading config: {e}")
        
        # Return default/template config
        return {
            "tenant": "walmart",
            "api_version": "v1",
            "username": "",
            "password": "",
            "base_url": "https://wd5-impl-services1.workday.com",
            "raas_report_url": ""
        }
    
    def create_config_template(self, filename: str = "workday_config.json") -> bool:
        """Create a configuration template file"""
        template = {
            "tenant": "walmart",
            "api_version": "v1",
            "username": "YOUR_WORKDAY_API_USERNAME",
            "password": "YOUR_WORKDAY_API_PASSWORD",
            "base_url": "https://wd5-impl-services1.workday.com",
            "raas_report_url": "",
            "notes": {
                "tenant": "Your Workday tenant name (usually company name)",
                "username": "API integration username from Workday admin",
                "password": "API integration password",
                "base_url": "Your Workday instance URL",
                "raas_report_url": "Optional: Direct URL to custom RaaS report"
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2)
            print(f"+ Configuration template created: {filename}")
            print(f"  Edit this file with your Workday API credentials")
            return True
        except Exception as e:
            print(f"X Error creating config template: {e}")
            return False
    
    def connect(self) -> bool:
        """Establish connection to Workday API"""
        if not self.config.get('username') or not self.config.get('password'):
            print("X API credentials not configured")
            print("  Run: create_config_template() to create config file")
            return False
        
        try:
            self.session = requests.Session()
            self.session.auth = HTTPBasicAuth(
                self.config['username'],
                self.config['password']
            )
            
            # Test connection with a simple API call
            test_url = f"{self.config['base_url']}/ccx/service/{self.config['tenant']}/Human_Resources/{self.config['api_version']}"
            
            response = self.session.get(test_url, timeout=10)
            
            if response.status_code == 200:
                self.connected = True
                print("+ Connected to Workday API successfully")
                return True
            else:
                print(f"X Connection failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"X Error connecting to Workday: {e}")
            return False
    
    def fetch_jobs_via_raas(self, report_url: str = None) -> List[Dict]:
        """
        Fetch jobs using Workday RaaS (Report as a Service)
        This is the recommended method for bulk data extraction
        
        Args:
            report_url: Custom report URL (if not in config)
        
        Returns:
            List of job dictionaries
        """
        if not self.connected:
            print("X Not connected. Call connect() first")
            return []
        
        # Use provided URL or config URL
        url = report_url or self.config.get('raas_report_url')
        
        if not url:
            print("X RaaS report URL not configured")
            print("  Contact Workday admin to create a custom report")
            print("  Report should include: Job_Code, Job_ID, Job_Title")
            return []
        
        try:
            # RaaS reports typically support JSON or CSV output
            params = {'format': 'json'}
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"+ Fetched {len(data.get('Report_Entry', []))} jobs from RaaS")
                return data.get('Report_Entry', [])
            else:
                print(f"X RaaS fetch failed: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"X Error fetching from RaaS: {e}")
            return []
    
    def fetch_job_by_code(self, job_code: str) -> Optional[Dict]:
        """
        Fetch single job by job code using REST API
        
        Args:
            job_code: Walmart job code (e.g., '800469')
        
        Returns:
            Job data dictionary or None
        """
        if not self.connected:
            print("X Not connected. Call connect() first")
            return None
        
        try:
            # Workday REST API endpoint for jobs
            # Note: Exact endpoint may vary by Workday version
            url = f"{self.config['base_url']}/ccx/service/{self.config['tenant']}/Human_Resources/{self.config['api_version']}/Job_Profiles"
            
            params = {
                'Job_Code': job_code
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"X Job fetch failed for {job_code}: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"X Error fetching job {job_code}: {e}")
            return None
    
    def fetch_all_jobs(self, job_codes: List[str]) -> List[Dict]:
        """
        Fetch multiple jobs by job codes
        
        Args:
            job_codes: List of job codes to fetch
        
        Returns:
            List of job data dictionaries
        """
        jobs = []
        total = len(job_codes)
        
        print(f"Fetching {total} jobs from Workday...")
        
        for i, code in enumerate(job_codes, 1):
            if i % 10 == 0:
                print(f"  Progress: {i}/{total}")
            
            job = self.fetch_job_by_code(code)
            if job:
                jobs.append(job)
        
        print(f"+ Fetched {len(jobs)} of {total} jobs")
        return jobs
    
    def export_to_csv(self, jobs: List[Dict], output_file: str = "workday_jobs_api.csv") -> bool:
        """
        Export fetched jobs to CSV format compatible with merge script
        
        Args:
            jobs: List of job dictionaries from API
            output_file: Output CSV filename
        
        Returns:
            True if successful
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'job_code', 'job_number', 'job_description',
                    'job_family', 'job_level', 'grade'
                ])
                writer.writeheader()
                
                for job in jobs:
                    # Map Workday API fields to our schema
                    # Note: Field names may vary by Workday configuration
                    row = {
                        'job_code': job.get('Job_Code', ''),
                        'job_number': job.get('Job_ID', ''),
                        'job_description': job.get('Job_Profile_Name', ''),
                        'job_family': job.get('Job_Family', ''),
                        'job_level': job.get('Management_Level', ''),
                        'grade': job.get('Compensation_Grade', '')
                    }
                    writer.writerow(row)
            
            print(f"+ Exported {len(jobs)} jobs to {output_file}")
            return True
            
        except Exception as e:
            print(f"X Error exporting to CSV: {e}")
            return False
    
    def get_unique_job_codes_from_ad_csv(self, ad_csv_file: str) -> List[str]:
        """
        Extract unique job codes from your AD extraction CSV
        
        Args:
            ad_csv_file: Path to AD groups CSV file
        
        Returns:
            List of unique job codes
        """
        job_codes = set()
        
        try:
            with open(ad_csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    code = row.get('job_code', '').strip()
                    if code:
                        job_codes.add(code)
            
            codes_list = sorted(list(job_codes))
            print(f"+ Found {len(codes_list)} unique job codes in {ad_csv_file}")
            return codes_list
            
        except Exception as e:
            print(f"X Error reading AD CSV: {e}")
            return []


def main():
    """
    Main workflow for Workday API integration
    """
    print("\n" + "="*80)
    print("WORKDAY API DIRECT FEED CONNECTOR")
    print("="*80 + "\n")
    
    # Step 1: Initialize connector
    connector = WorkdayAPIConnector()
    
    # Step 2: Create config if needed
    if not connector.config.get('username'):
        print("Configuration not found. Creating template...")
        connector.create_config_template()
        print("\n" + "="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("1. Edit workday_config.json with your Workday API credentials")
        print("2. Contact your Workday admin if you need:")
        print("   - API integration username/password")
        print("   - RaaS report URL for Job Master data")
        print("3. Run this script again after configuration\n")
        return
    
    # Step 3: Connect to Workday
    print("Connecting to Workday API...")
    if not connector.connect():
        print("\nConnection failed. Check your credentials in workday_config.json")
        return
    
    # Step 4: Option A - Fetch via RaaS (recommended for bulk)
    print("\n--- Option A: Fetch via RaaS Report ---")
    if connector.config.get('raas_report_url'):
        jobs = connector.fetch_jobs_via_raas()
        if jobs:
            connector.export_to_csv(jobs, "workday_jobs.csv")
    else:
        print("RaaS URL not configured. Contact Workday admin to set up.")
    
    # Step 5: Option B - Fetch specific job codes from AD data
    print("\n--- Option B: Fetch Jobs for Specific Codes ---")
    ad_csv = "ad_groups_20251215_154559.csv"
    if os.path.exists(ad_csv):
        job_codes = connector.get_unique_job_codes_from_ad_csv(ad_csv)
        if job_codes:
            print(f"Fetching {len(job_codes)} jobs from Workday...")
            print("This may take a few minutes...\n")
            jobs = connector.fetch_all_jobs(job_codes)
            if jobs:
                connector.export_to_csv(jobs, "workday_jobs.csv")
                print("\n+ SUCCESS! workday_jobs.csv created")
                print("\nNext step: Run merge script:")
                print("python merge_workday_data.py --ad-csv ad_groups_20251215_154559.csv --workday-csv workday_jobs.csv --output final_users_with_jobs.csv")
    else:
        print(f"AD CSV file not found: {ad_csv}")
    
    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
