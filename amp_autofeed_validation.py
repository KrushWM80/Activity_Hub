"""
AMP AutoFeed Validation System
Compares QuickBase API response data with AMP processed AutoFeed details
Identifies discrepancies and generates reports for historical analysis
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib

# For Outlook integration
try:
    from win32com.client import GetObject
    import win32com.client
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("WARNING: win32com not available. Install via: pip install pywin32")

# For HTML parsing
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("WARNING: BeautifulSoup4 not available. Install via: pip install beautifulsoup4")


class EmailFetcher:
    """Fetch emails from Outlook"""
    
    def __init__(self):
        if not HAS_WIN32:
            raise RuntimeError("win32com required for Outlook access")
        self.outlook = win32com.client.GetActiveObject("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")
    
    def get_email_by_subject(self, subject_pattern: str, days_back: int = 1, folder_name: str = None) -> List[Dict]:
        """Get emails matching subject pattern from last N days"""
        emails = []
        inbox = self.namespace.Folders.Item(1).Folders.Item("ATC")
        
        if not inbox:
            raise ValueError("Folder 'ATC' not found in Outlook")
        
        # Navigate to Reports > AMP > specific folder
        # Two separate folders:
        # - "Quick Base API Response Data" (source data from QuickBase)
        # - "Auto Feed" (AMP processed data)
        try:
            if folder_name is None:
                # Determine folder based on subject pattern
                if "Quick Base" in subject_pattern or "QuickBase" in subject_pattern:
                    folder_name = "Quick Base API Response Data"
                else:
                    folder_name = "Auto Feed"
            
            folder = inbox.Folders.Item("Reports").Folders.Item("AMP").Folders.Item(folder_name)
        except:
            print(f"Could not navigate to folder, listing available folders:")
            try:
                for f in inbox.Folders:
                    print(f"  - {f.Name}")
                    if f.Name == "Reports":
                        for f2 in f.Folders:
                            print(f"    - {f2.Name}")
                            if f2.Name == "AMP":
                                for f3 in f2.Folders:
                                    print(f"      - {f3.Name}")
            except:
                pass
            raise
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for item in folder.Items:
            if hasattr(item, 'Subject') and subject_pattern.lower() in item.Subject.lower():
                if item.ReceivedTime >= cutoff_date.timestamp():
                    emails.append({
                        'subject': item.Subject,
                        'received': item.ReceivedTime,
                        'sender': item.SenderEmailAddress,
                        'body': item.Body,
                        'html_body': item.HTMLBody if hasattr(item, 'HTMLBody') else None,
                    })
        
        return sorted(emails, key=lambda x: x['received'], reverse=True)


class HTMLEmailParser:
    """Parse HTML email content"""
    
    # Target columns to extract and compare
    TARGET_COLUMNS = ['AutoFeed Id', 'Message Title', 'Stores', 'Anchor Walmart Week', 'Status']
    
    @staticmethod
    def extract_data_from_html(html_content: str, extract_columns: bool = True) -> Dict:
        """
        Extract structured data from HTML email.
        Look for tables, lists, or data blocks
        If extract_columns=True, specifically extract target columns from tables
        """
        if not HAS_BS4:
            raise RuntimeError("BeautifulSoup4 required for HTML parsing")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        data = {
            'tables': [],
            'text_blocks': [],
            'lists': [],
            'summary_stats': {},
            'records': [],  # Extracted records with target columns
        }
        
        # Extract tables
        for table in soup.find_all('table'):
            rows = []
            headers = []
            for i, tr in enumerate(table.find_all('tr')):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
                    # First row is likely headers
                    if i == 0:
                        headers = cells
            
            if rows:
                data['tables'].append(rows)
                
                # Extract specific columns if this looks like data
                if extract_columns and headers:
                    HTMLEmailParser._extract_target_columns(rows, headers, data)
        
        
        # Extract text blocks (paragraphs with data)
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 10:
                data['text_blocks'].append(text)
        
        # Extract lists
        for ul in soup.find_all(['ul', 'ol']):
            items = [li.get_text(strip=True) for li in ul.find_all('li')]
            if items:
                data['lists'].append(items)
        
        # Try to extract key metrics
        text = soup.get_text()
        
        # Look for patterns like "Total: 123" or "Count: 456"
        patterns = [
            r'Total\s*:?\s*(\d+)',
            r'Count\s*:?\s*(\d+)',
            r'Records?\s*:?\s*(\d+)',
            r'Items?\s*:?\s*(\d+)',
            r'(\d+)\s*record',
            r'(\d+)\s*items?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                key = pattern.split('|')[0].strip(r'\s*:?')
                data['summary_stats'][key] = [int(m) for m in matches]
        
        return data
    
    @staticmethod
    def _extract_target_columns(rows: List[List[str]], headers: List[str], data: Dict):
        """
        Extract specific target columns from table rows
        Target columns: AutoFeed Id, Message Title, Stores, Anchor Walmart Week, Status
        """
        # Find indices of target columns
        col_indices = {}
        for col in HTMLEmailParser.TARGET_COLUMNS:
            for i, header in enumerate(headers):
                if col.lower() in header.lower() or header.lower() in col.lower():
                    col_indices[col] = i
                    break
        
        # Extract records with only target columns
        for row in rows[1:]:  # Skip header row
            if not row or not any(row):
                continue
            
            record = {}
            for col, idx in col_indices.items():
                if idx < len(row):
                    record[col] = row[idx]
            
            if record:  # Only add if we found at least one target column
                data['records'].append(record)
        


class AutoFeedValidator:
    """Main validation logic"""
    
    def __init__(self, log_dir: str = "amp_validation_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.history_file = self.log_dir / "validation_history.json"
        self.discrepancies_file = self.log_dir / "discrepancies_report.json"
        self.daily_report_dir = self.log_dir / "daily_reports"
        self.daily_report_dir.mkdir(exist_ok=True)
        
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load validation history from file"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_history(self):
        """Save validation history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)
    
    def validate_daily(self) -> Dict:
        """
        Perform daily validation:
        1. Get today's QuickBase API Response email from "Quick Base API Response Data" folder
        2. Get today's AMP AutoFeed email from "Auto Feed" folder
        3. Compare content
        4. Log results
        """
        print("\n=== AMP AutoFeed Daily Validation ===")
        print(f"Timestamp: {datetime.now()}")
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            fetcher = EmailFetcher()
            
            # Get today's emails (within last 24 hours) from separate folders
            print("\nFetching QuickBase API Response email...")
            qb_emails = fetcher.get_email_by_subject("", days_back=1, folder_name="Quick Base API Response Data")
            
            print("Fetching AMP AutoFeed Details email...")
            amp_emails = fetcher.get_email_by_subject("", days_back=1, folder_name="Auto Feed")
            
            if not qb_emails:
                print("ERROR: No QuickBase email found for today")
                qb_data = None
            else:
                print(f"Found QuickBase email: {qb_emails[0]['received']}")
                parser = HTMLEmailParser()
                qb_data = parser.extract_data_from_html(qb_emails[0]['html_body'] or qb_emails[0]['body'])
            
            if not amp_emails:
                print("ERROR: No AMP email found for today")
                amp_data = None
            else:
                print(f"Found AMP email: {amp_emails[0]['received']}")
                parser = HTMLEmailParser()
                amp_data = parser.extract_data_from_html(amp_emails[0]['html_body'] or amp_emails[0]['body'])
            
            # Compare
            result = {
                'date': today,
                'timestamp': datetime.now().isoformat(),
                'qb_email_found': qb_emails is not None and len(qb_emails) > 0,
                'amp_email_found': amp_emails is not None and len(amp_emails) > 0,
                'qb_data': qb_data,
                'amp_data': amp_data,
                'comparison': self._compare_data(qb_data, amp_data),
                'status': 'PASS' if self._compare_data(qb_data, amp_data).get('match') else 'FAIL',
            }
            
            # Store in history
            self.history[today] = result
            self._save_history()
            
            # Save daily report
            daily_report = self.daily_report_dir / f"validation_{today}.json"
            with open(daily_report, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            
            return result
            
        except Exception as e:
            error_result = {
                'date': today,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'ERROR',
            }
            self.history[today] = error_result
            self._save_history()
            print(f"ERROR: {e}")
            return error_result
    
    def _compare_data(self, qb_data: Optional[Dict], amp_data: Optional[Dict]) -> Dict:
        """Compare QuickBase and AMP data"""
        comparison = {
            'match': True,
            'differences': [],
            'qb_record_count': 0,
            'amp_record_count': 0,
            'qb_records': [],
            'amp_records': [],
            'missing_in_amp': [],
            'extra_in_amp': [],
        }
        
        if qb_data is None or amp_data is None:
            comparison['match'] = False
            if qb_data is None:
                comparison['differences'].append("QuickBase data missing")
            if amp_data is None:
                comparison['differences'].append("AMP data missing")
            return comparison
        
        # Extract records from both emails
        qb_records = qb_data.get('records', [])
        amp_records = amp_data.get('records', [])
        
        comparison['qb_record_count'] = len(qb_records)
        comparison['amp_record_count'] = len(amp_records)
        comparison['qb_records'] = qb_records
        comparison['amp_records'] = amp_records
        
        # Compare record counts
        if len(qb_records) != len(amp_records):
            comparison['match'] = False
            comparison['differences'].append(
                f"Record count mismatch: QB={len(qb_records)}, AMP={len(amp_records)}"
            )
        
        # Create sets of records for comparison (using AutoFeed Id as key)
        qb_by_id = {str(r.get('AutoFeed Id', '')).strip(): r for r in qb_records}
        amp_by_id = {str(r.get('AutoFeed Id', '')).strip(): r for r in amp_records}
        
        # Find missing and extra records
        missing_ids = set(qb_by_id.keys()) - set(amp_by_id.keys())
        extra_ids = set(amp_by_id.keys()) - set(qb_by_id.keys())
        
        if missing_ids:
            comparison['match'] = False
            comparison['missing_in_amp'] = list(missing_ids)
            comparison['differences'].append(f"Missing in AMP: {len(missing_ids)} records")
        
        if extra_ids:
            comparison['match'] = False
            comparison['extra_in_amp'] = list(extra_ids)
            comparison['differences'].append(f"Extra in AMP: {len(extra_ids)} records")
        
        # Compare matching records field by field
        common_ids = set(qb_by_id.keys()) & set(amp_by_id.keys())
        field_differences = {}
        
        for rec_id in common_ids:
            qb_rec = qb_by_id[rec_id]
            amp_rec = amp_by_id[rec_id]
            
            for field in HTMLEmailParser.TARGET_COLUMNS:
                qb_val = str(qb_rec.get(field, '')).strip() if field in qb_rec else ''
                amp_val = str(amp_rec.get(field, '')).strip() if field in amp_rec else ''
                
                if qb_val != amp_val:
                    comparison['match'] = False
                    if field not in field_differences:
                        field_differences[field] = []
                    field_differences[field].append({
                        'id': rec_id,
                        'qb_value': qb_val,
                        'amp_value': amp_val,
                    })
        
        if field_differences:
            for field, diffs in field_differences.items():
                comparison['differences'].append(
                    f"Field '{field}' differs in {len(diffs)} records"
                )
            comparison['field_differences'] = field_differences
        
        # Compare data hashes for quick change detection
        qb_hash = hashlib.md5(json.dumps(qb_records, sort_keys=True, default=str).encode()).hexdigest()
        amp_hash = hashlib.md5(json.dumps(amp_records, sort_keys=True, default=str).encode()).hexdigest()
        
        comparison['qb_hash'] = qb_hash
        comparison['amp_hash'] = amp_hash
        
        return comparison
    
    def generate_historical_report(self, days: int = 365) -> Dict:
        """Generate report of historical discrepancies"""
        print(f"\n=== Historical Validation Report (last {days} days) ===")
        
        report = {
            'generated': datetime.now().isoformat(),
            'period_days': days,
            'total_validations': len(self.history),
            'passed': 0,
            'failed': 0,
            'errored': 0,
            'missing_days': [],
            'discrepancies': [],
            'discrepancy_timeline': {},
        }
        
        # Analyze history
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for date_str, result in sorted(self.history.items()):
            if result.get('status') == 'PASS':
                report['passed'] += 1
            elif result.get('status') == 'FAIL':
                report['failed'] += 1
                report['discrepancies'].append({
                    'date': date_str,
                    'differences': result.get('comparison', {}).get('differences', []),
                })
                report['discrepancy_timeline'][date_str] = result.get('comparison', {}).get('differences', [])
            elif result.get('status') == 'ERROR':
                report['errored'] += 1
        
        # Identify missing days (dates with no validation)
        validated_dates = set(self.history.keys())
        current = datetime.now()
        for i in range(days):
            check_date = (current - timedelta(days=i)).strftime("%Y-%m-%d")
            if check_date not in validated_dates:
                report['missing_days'].append(check_date)
        
        # Save report
        report_file = self.log_dir / "historical_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Also save as readable text
        report_text_file = self.log_dir / "historical_report.txt"
        with open(report_text_file, 'w') as f:
            f.write(f"AMP AutoFeed Validation - Historical Report\n")
            f.write(f"Generated: {report['generated']}\n")
            f.write(f"Period: Last {days} days\n")
            f.write(f"\n=== Summary ===\n")
            f.write(f"Total Validations: {report['total_validations']}\n")
            f.write(f"Passed: {report['passed']}\n")
            f.write(f"Failed: {report['failed']}\n")
            f.write(f"Errors: {report['errored']}\n")
            f.write(f"\n=== Discrepancies Found ===\n")
            
            if report['discrepancies']:
                for disc in report['discrepancies']:
                    f.write(f"\nDate: {disc['date']}\n")
                    for diff in disc['differences']:
                        f.write(f"  - {diff}\n")
            else:
                f.write("No discrepancies found!\n")
            
            if report['missing_days']:
                f.write(f"\n=== Unvalidated Days ===\n")
                f.write(f"Total gaps: {len(report['missing_days'])}\n")
                if len(report['missing_days']) <= 10:
                    for day in report['missing_days']:
                        f.write(f"  - {day}\n")
                else:
                    f.write(f"  (Too many to list, see JSON report)\n")
        
        print(f"\nReports saved to: {self.log_dir}")
        print(f"\nSummary:")
        print(f"  Passed: {report['passed']}")
        print(f"  Failed: {report['failed']}")
        print(f"  Errors: {report['errored']}")
        
        return report


def main():
    """Run validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AMP AutoFeed Validation System")
    parser.add_argument('--action', choices=['daily', 'historical', 'both'], 
                       default='daily', help='Action to perform')
    parser.add_argument('--days', type=int, default=365, help='Days back for historical analysis')
    parser.add_argument('--log-dir', default='amp_validation_logs', help='Log directory')
    
    args = parser.parse_args()
    
    validator = AutoFeedValidator(log_dir=args.log_dir)
    
    if args.action in ['daily', 'both']:
        result = validator.validate_daily()
        print(f"\nDaily Validation Result: {result['status']}")
        if result.get('comparison', {}).get('differences'):
            print("Differences found:")
            for diff in result['comparison']['differences']:
                print(f"  - {diff}")
    
    if args.action in ['historical', 'both']:
        report = validator.generate_historical_report(days=args.days)


if __name__ == "__main__":
    main()
