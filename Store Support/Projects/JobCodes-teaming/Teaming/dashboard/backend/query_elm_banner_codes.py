#!/usr/bin/env python3
"""
Query ELM (Enterprise Location Management) datasource for Banner Codes
Pulls complete banner code and description from Walmart stores and facilities

Data Source: wmt-loc-cat-prod.catalog_location_views.division_view
Updates: Banner codes for Aligned dashboard
Usage: python query_elm_banner_codes.py [--divisions 1 10] [--output json|csv]
"""

from google.cloud import bigquery
import json
import csv
from datetime import datetime
import os
import sys

class ELMBannerCodeFetcher:
    def __init__(self, project_id='wmt-assetprotection-prod'):
        """Initialize BigQuery client and parameters"""
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.banner_codes = {}
        
    def query_division(self, division_nbr):
        """
        Query division_view for specific division
        
        Args:
            division_nbr (int): Division number (1=WM US Stores, 10=H&W)
        
        Returns:
            list: List of dicts with banner_code, banner_desc, count
        """
        query = f"""
        SELECT DISTINCT
          banner_code,
          banner_desc,
          COUNT(*) as store_count
        FROM
          `wmt-loc-cat-prod.catalog_location_views.division_view`
        WHERE
          physical_country_code = 'US'
          AND base_division_desc = "WAL-MART STORES INC."
          AND division_nbr = {division_nbr}
          AND bu_status_desc NOT IN ('CLOSED', '')
          AND Date(new_bu_start_date) <= date_add(current_date(), INTERVAL 90 DAY)
          AND banner_code IS NOT NULL
          AND banner_code != ''
        GROUP BY banner_code, banner_desc
        ORDER BY banner_code
        """
        
        print(f"\n📊 Querying Division {division_nbr}...")
        print(f"Query (simplified):\n  FROM division_view")
        print(f"  WHERE division_nbr = {division_nbr}\n")
        
        try:
            job_config = bigquery.QueryJobConfig(
                maximum_bytes_billed=1000000000  # 1GB limit
            )
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result(timeout=60)
            
            banner_list = []
            for row in results:
                banner_code = row['banner_code'].strip() if row['banner_code'] else None
                banner_desc = row['banner_desc'].strip() if row['banner_desc'] else None
                
                if banner_code and banner_desc:
                    banner_list.append({
                        'banner_code': banner_code,
                        'banner_desc': banner_desc,
                        'store_count': row['store_count'],
                        'division': division_nbr
                    })
            
            print(f"✅ Found {len(banner_list)} banner codes for Division {division_nbr}\n")
            for banner in sorted(banner_list, key=lambda x: x['banner_code']):
                print(f"   {banner['banner_code']:4} - {banner['banner_desc']:45} ({banner['store_count']:5} stores)")
            
            return banner_list
            
        except Exception as e:
            print(f"❌ Error querying Division {division_nbr}: {str(e)}")
            return []
    
    def fetch_all_banner_codes(self, divisions=[1, 10]):
        """
        Fetch banner codes from specified divisions
        
        Args:
            divisions (list): Division numbers to query
        
        Returns:
            dict: Deduplicated banner codes by code
        """
        all_banners = {}
        
        for div in divisions:
            banners = self.query_division(div)
            for banner in banners:
                code = banner['banner_code']
                if code not in all_banners:
                    all_banners[code] = banner
                else:
                    # If exists, note it appeared in multiple divisions
                    if 'divisions' not in all_banners[code]:
                        all_banners[code]['divisions'] = [all_banners[code]['division']]
                    all_banners[code]['divisions'].append(div)
        
        self.banner_codes = all_banners
        return all_banners
    
    def get_dropdown_format(self):
        """
        Format banner codes for dropdown display
        Format: "{CODE} - {DESCRIPTION}"
        
        Returns:
            list: Formatted strings for dropdown
        """
        formatted = []
        for code, data in sorted(self.banner_codes.items()):
            formatted_str = f"{code} - {data['banner_desc']}"
            formatted.append(formatted_str)
        
        return formatted
    
    def export_json(self, filepath=None):
        """Export banner codes as JSON"""
        if filepath is None:
            filepath = f"banner_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output = {
            'generated_at': datetime.now().isoformat(),
            'total_unique_banners': len(self.banner_codes),
            'banners': sorted(self.banner_codes.values(), key=lambda x: x['banner_code']),
            'dropdown_options': self.get_dropdown_format()
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✅ Exported to JSON: {filepath}")
        return filepath
    
    def export_csv(self, filepath=None):
        """Export banner codes as CSV"""
        if filepath is None:
            filepath = f"banner_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['banner_code', 'banner_desc', 'store_count', 'division', 'dropdown_format'])
            writer.writeheader()
            
            for code, data in sorted(self.banner_codes.items()):
                writer.writerow({
                    'banner_code': data['banner_code'],
                    'banner_desc': data['banner_desc'],
                    'store_count': data['store_count'],
                    'division': data['division'],
                    'dropdown_format': f"{data['banner_code']} - {data['banner_desc']}"
                })
        
        print(f"\n✅ Exported to CSV: {filepath}")
        return filepath
    
    def export_js_constant(self, filepath=None):
        """Export as JavaScript constant for frontend"""
        if filepath is None:
            filepath = f"banner_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"
        
        dropdown_options = self.get_dropdown_format()
        
        js_content = f"""// Banner Codes - Generated {datetime.now().isoformat()}
// Source: ELM (wmt-loc-cat-prod.catalog_location_views.division_view)
// Divisions: 1 (WM US Stores), 10 (H&W)
// Total Unique Banners: {len(self.banner_codes)}

const BANNER_CODE_OPTIONS = {json.dumps(dropdown_options, indent=2)};

// For use in HTML dropdown
// Example: populateDropdown('banner-codes-dropdown', BANNER_CODE_OPTIONS);
"""
        
        with open(filepath, 'w') as f:
            f.write(js_content)
        
        print(f"\n✅ Exported to JavaScript: {filepath}")
        return filepath
    
    def print_summary(self):
        """Print summary of banner codes"""
        print("\n" + "="*80)
        print("BANNER CODE SUMMARY")
        print("="*80)
        print(f"Total Unique Banner Codes: {len(self.banner_codes)}\n")
        
        print("Dropdown Format (for Aligned Dashboard):")
        print("-" * 80)
        for option in self.get_dropdown_format():
            print(f"  • {option}")
        
        print("\n" + "="*80)

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Query ELM banner codes')
    parser.add_argument('--divisions', nargs='+', type=int, default=[1, 10], 
                       help='Division numbers to query (default: 1 10)')
    parser.add_argument('--output', choices=['json', 'csv', 'js', 'all'], default='all',
                       help='Output format (default: all)')
    parser.add_argument('--show', action='store_true', help='Print to console')
    
    args = parser.parse_args()
    
    print("="*80)
    print("ELM BANNER CODE FETCHER")
    print("="*80)
    print(f"Source: wmt-loc-cat-prod.catalog_location_views.division_view")
    print(f"Divisions: {args.divisions}")
    print("="*80)
    
    fetcher = ELMBannerCodeFetcher()
    fetcher.fetch_all_banner_codes(divisions=args.divisions)
    
    if args.show:
        fetcher.print_summary()
    
    # Export in requested formats
    export_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.output in ['json', 'all']:
        fetcher.export_json(os.path.join(export_dir, f"banner_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"))
    
    if args.output in ['csv', 'all']:
        fetcher.export_csv(os.path.join(export_dir, f"banner_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"))
    
    if args.output in ['js', 'all']:
        fetcher.export_js_constant(os.path.join(export_dir, f"banner_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"))
    
    print("\n✅ Banner code extraction complete!")

if __name__ == '__main__':
    main()
