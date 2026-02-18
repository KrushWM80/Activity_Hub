#!/usr/bin/env python3
"""
Workday Job Code Lookup Module
Maps Walmart job codes to Workday job descriptions and job numbers

Usage Options:
1. Load from CSV file with mappings
2. Load from JSON file with mappings
3. Query Workday API directly (if credentials available)
"""

import csv
import json
from typing import Dict, Optional
from dataclasses import dataclass
import os


@dataclass
class WorkdayJob:
    """Represents a Workday job"""
    job_code: str
    job_number: str
    job_description: str
    job_family: str = ""
    job_level: str = ""
    grade: str = ""


class WorkdayJobLookup:
    """Lookup Workday job information by job code"""

    def __init__(self):
        self.jobs: Dict[str, WorkdayJob] = {}
        self.loaded = False
        self.source = None

    def load_from_csv(self, csv_file: str) -> bool:
        """
        Load job mappings from CSV file
        Expected columns: job_code, job_number, job_description, job_family, job_level, grade
        """
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    job_code = row.get('job_code', '').strip()
                    if job_code:
                        job = WorkdayJob(
                            job_code=job_code,
                            job_number=row.get('job_number', '').strip(),
                            job_description=row.get('job_description', '').strip(),
                            job_family=row.get('job_family', '').strip(),
                            job_level=row.get('job_level', '').strip(),
                            grade=row.get('grade', '').strip()
                        )
                        self.jobs[job_code] = job
            
            self.loaded = True
            self.source = f"CSV: {csv_file}"
            print(f"+ Loaded {len(self.jobs)} job codes from {csv_file}")
            return True
        except Exception as e:
            print(f"X Error loading CSV: {e}")
            return False

    def load_from_json(self, json_file: str) -> bool:
        """
        Load job mappings from JSON file
        Expected format:
        {
            "job_code": {
                "job_number": "...",
                "job_description": "...",
                "job_family": "...",
                "job_level": "...",
                "grade": "..."
            }
        }
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for job_code, info in data.items():
                job = WorkdayJob(
                    job_code=job_code,
                    job_number=info.get('job_number', ''),
                    job_description=info.get('job_description', ''),
                    job_family=info.get('job_family', ''),
                    job_level=info.get('job_level', ''),
                    grade=info.get('grade', '')
                )
                self.jobs[job_code] = job
            
            self.loaded = True
            self.source = f"JSON: {json_file}"
            print(f"+ Loaded {len(self.jobs)} job codes from {json_file}")
            return True
        except Exception as e:
            print(f"X Error loading JSON: {e}")
            return False

    def get_job(self, job_code: str) -> Optional[WorkdayJob]:
        """
        Get job details by job code
        """
        return self.jobs.get(job_code.strip())

    def lookup_job_description(self, job_code: str) -> str:
        """
        Get just the job description
        """
        job = self.get_job(job_code)
        return job.job_description if job else ""

    def lookup_job_number(self, job_code: str) -> str:
        """
        Get just the job number
        """
        job = self.get_job(job_code)
        return job.job_number if job else ""

    def get_stats(self) -> Dict:
        """
        Return statistics about loaded data
        """
        return {
            'total_jobs': len(self.jobs),
            'source': self.source,
            'loaded': self.loaded
        }

    def export_template(self, filename: str = 'workday_job_template.csv') -> bool:
        """
        Create a template CSV for manual entry or Workday export
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=['job_code', 'job_number', 'job_description', 'job_family', 'job_level', 'grade']
                )
                writer.writeheader()
                writer.writerow({
                    'job_code': '800469',
                    'job_number': 'EXAMPLE',
                    'job_description': 'Director, Market Health and Wellness',
                    'job_family': 'Management',
                    'job_level': 'Director',
                    'grade': 'GR40'
                })
            print(f"+ Template exported to {filename}")
            return True
        except Exception as e:
            print(f"X Error creating template: {e}")
            return False


class WorkdayAPILookup(WorkdayJobLookup):
    """
    Extended class for Workday API integration
    (Requires Workday API credentials and setup)
    """

    def __init__(self, api_url: str = None, api_key: str = None):
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to Workday API
        Note: Requires proper credentials and Workday setup
        """
        if not self.api_url or not self.api_key:
            print("X Workday API credentials not configured")
            print("  Set api_url and api_key to use API lookup")
            return False
        
        try:
            import requests
            # Example Workday API call (customize based on Workday instance)
            headers = {'Authorization': f'Bearer {self.api_key}'}
            # This is a placeholder - actual endpoint depends on Workday setup
            response = requests.get(
                f"{self.api_url}/api/v1/jobs",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.connected = True
                self.source = "Workday API"
                print("+ Connected to Workday API")
                return True
            else:
                print(f"X Workday API error: {response.status_code}")
                return False
        except ImportError:
            print("X requests library not installed")
            print("  Install with: pip install requests")
            return False
        except Exception as e:
            print(f"X Error connecting to Workday API: {e}")
            return False

    def lookup_from_api(self, job_code: str) -> Optional[WorkdayJob]:
        """
        Query Workday API for job details
        """
        if not self.connected:
            return None
        
        try:
            import requests
            headers = {'Authorization': f'Bearer {self.api_key}'}
            # Customize based on Workday API structure
            response = requests.get(
                f"{self.api_url}/api/v1/jobs/{job_code}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                job = WorkdayJob(
                    job_code=job_code,
                    job_number=data.get('id', ''),
                    job_description=data.get('name', ''),
                    job_family=data.get('family', ''),
                    job_level=data.get('level', '')
                )
                self.jobs[job_code] = job
                return job
            return None
        except Exception as e:
            print(f"X API lookup error for {job_code}: {e}")
            return None


def main():
    """
    Example usage
    """
    print("\n" + "="*80)
    print("Workday Job Code Lookup Module")
    print("="*80 + "\n")

    # Create lookup instance
    lookup = WorkdayJobLookup()

    # Option 1: Load from CSV (if you have one)
    csv_file = "workday_jobs.csv"
    if os.path.exists(csv_file):
        print(f"Loading from {csv_file}...")
        lookup.load_from_csv(csv_file)
    else:
        print(f"X {csv_file} not found")
        print("\nTo use this module:")
        print("1. Get Workday job code mapping from your HR team")
        print("2. Create CSV with columns: job_code, job_number, job_description")
        print("3. Load with: lookup.load_from_csv('your_file.csv')")

    # Option 2: Load from JSON
    json_file = "workday_jobs.json"
    if os.path.exists(json_file):
        print(f"Loading from {json_file}...")
        lookup.load_from_json(json_file)

    # Option 3: Create empty template
    print("\nCreating template for manual entry...")
    lookup.export_template()

    # Show what we have
    stats = lookup.get_stats()
    print(f"\nStatus: {stats['loaded']}")
    print(f"Source: {stats['source']}")
    print(f"Total Jobs Loaded: {stats['total_jobs']}")

    if stats['total_jobs'] > 0:
        # Example lookup
        test_code = list(lookup.jobs.keys())[0]
        job = lookup.get_job(test_code)
        print(f"\nExample: Job Code {test_code}")
        print(f"  Job Number: {job.job_number}")
        print(f"  Description: {job.job_description}")


if __name__ == "__main__":
    main()