"""
AMP AutoFeed Validation System
Reads HTML files extracted by VB from QuickBase and AMP emails
Compares AutoFeed data and generates comparison reports
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib

# For HTML parsing
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    # Fallback to html.parser from standard library
    from html.parser import HTMLParser


class SimpleHTMLTableParser(HTMLParser):
    """Fallback HTML parser using standard library (when BeautifulSoup not available)"""
    
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = None
        self.current_cell = None
        self.in_table = False
        self.in_row = False
        self.in_cell = False
    
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ['td', 'th'] and self.in_row:
            self.in_cell = True
            self.current_cell = []
    
    def handle_endtag(self, tag):
        if tag == 'table' and self.in_table:
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = None
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row is not None:
                self.current_table.append(self.current_row)
            self.current_row = None
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            if self.current_cell is not None:
                cell_text = ''.join(self.current_cell).strip()
                self.current_row.append(cell_text)
            self.current_cell = None
    
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)


class EmailFetcher:
    """Fetch emails from HTML files extracted by VB"""
    
    def __init__(self, data_dir: str = "amp_autofeed_data"):
        """
        Initialize with path to folder containing HTML files
        
        Files expected:
        - quickbase_responses.html: From "Quick Base API Response Data" email
        - amp_autofeed.html: From "Auto Feed" email
        
        VB saves these daily at ~4:05 AM
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        print(f"✓ Data directory: {self.data_dir}")
    
    def get_email_by_subject(self, subject_pattern: str = "", days_back: int = 1, folder_name: str = None) -> List[Dict]:
        """Read HTML file and return as email-like dict"""
        emails = []
        
        # Map folder names to file names
        if folder_name == "Quick Base API Response Data":
            file_name = "quickbase_responses.html"
        elif folder_name == "Auto Feed":
            file_name = "amp_autofeed.html"
        else:
            print(f"Unknown folder: {folder_name}, expected 'Quick Base API Response Data' or 'Auto Feed'")
            return []
        
        file_path = self.data_dir / file_name
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"HTML file not found: {file_path}\n"
                f"VB should save email HTML bodies here daily at ~4:05 AM\n"
                f"Expected file: {file_name}"
            )
        
        # Read HTML file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            emails.append({
                'subject': f"Email from {folder_name}",
                'received': datetime.now(),
                'sender': "vb_extraction@internal",
                'body': html_content,
                'html_body': html_content,
            })
            print(f"✓ Loaded {file_name} ({len(html_content)} bytes)")
        except Exception as e:
            raise RuntimeError(f"Failed to read {file_path}: {e}")
        
        return emails


class HTMLEmailParser:
    """Parse HTML email content"""
    
    # Target columns to extract and compare
    TARGET_COLUMNS = ['AutoFeed Id', 'Message Title', 'Stores', 'Anchor Walmart Week', 'Status']
    
    @staticmethod
    def extract_data_from_html(html_content: str, extract_columns: bool = True) -> Dict:
        """
        Extract structured data from HTML email.
        Looks for tables with target columns and extracts records.
        Uses BeautifulSoup if available, falls back to standard library parser.
        """
        data = {
            'tables': [],
            'text_blocks': [],
            'lists': [],
            'summary_stats': {},
            'records': [],  # Extracted records with target columns
        }
        
        if HAS_BS4:
            # Use BeautifulSoup (preferred)
            soup = BeautifulSoup(html_content, 'html.parser')
            
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
            
            text = soup.get_text()
        
        else:
            # Use fallback parser (standard library)
            parser = SimpleHTMLTableParser()
            try:
                parser.feed(html_content)
            except:
                pass  # Ignore parsing errors
            
            data['tables'] = parser.tables
            
            # Extract target columns from tables
            if extract_columns:
                for table in parser.tables:
                    if len(table) > 0:
                        headers = table[0]
                        rows = table[1:]
                        HTMLEmailParser._extract_target_columns(rows, headers, data)
            
            # Get text for metrics
            text = html_content
        
        # Try to extract key metrics
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
        Extract specific target columns from table rows.
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
    """Validate and compare AutoFeed records from two sources"""
    
    def __init__(self):
        self.quickbase_data = []
        self.amp_data = []
        self.comparison_results = []
        self.discrepancies = []
    
    def load_data(self, quickbase_html: str, amp_html: str):
        """Load and parse HTML data from both sources"""
        # Parse QuickBase data
        qb_parsed = HTMLEmailParser.extract_data_from_html(quickbase_html)
        self.quickbase_data = qb_parsed.get('records', [])
        print(f"✓ QuickBase: {len(self.quickbase_data)} records")
        
        # Parse AMP data
        amp_parsed = HTMLEmailParser.extract_data_from_html(amp_html)
        self.amp_data = amp_parsed.get('records', [])
        print(f"✓ AMP AutoFeed: {len(self.amp_data)} records")
    
    def validate(self) -> Dict:
        """
        Compare records from both sources.
        Key: AutoFeed Id (should be unique identifier)
        Returns: Validation summary with discrepancies
        """
        results = {
            'total_quickbase': len(self.quickbase_data),
            'total_amp': len(self.amp_data),
            'matched': 0,
            'qb_only': [],
            'amp_only': [],
            'field_mismatches': [],
        }
        
        # Create lookup dicts by AutoFeed Id
        qb_dict = {r.get('AutoFeed Id'): r for r in self.quickbase_data if r.get('AutoFeed Id')}
        amp_dict = {r.get('AutoFeed Id'): r for r in self.amp_data if r.get('AutoFeed Id')}
        
        # Find matches and mismatches
        for autofeed_id in set(list(qb_dict.keys()) + list(amp_dict.keys())):
            qb_record = qb_dict.get(autofeed_id)
            amp_record = amp_dict.get(autofeed_id)
            
            if qb_record and amp_record:
                results['matched'] += 1
                
                # Check field differences
                for field in HTMLEmailParser.TARGET_COLUMNS:
                    qb_val = qb_record.get(field, "").strip()
                    amp_val = amp_record.get(field, "").strip()
                    
                    if qb_val != amp_val:
                        results['field_mismatches'].append({
                            'autofeed_id': autofeed_id,
                            'field': field,
                            'quickbase': qb_val,
                            'amp': amp_val,
                        })
            
            elif qb_record and not amp_record:
                results['qb_only'].append(autofeed_id)
            
            elif amp_record and not qb_record:
                results['amp_only'].append(autofeed_id)
        
        return results


def validate_daily():
    """
    Main validation function - runs daily at 5:00 AM
    Reads HTML files saved by VB at ~4:05 AM
    """
    try:
        print("\n" + "="*60)
        print(f"AMP AutoFeed Daily Validation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Initialize fetcher to read HTML files
        fetcher = EmailFetcher("amp_autofeed_data")
        
        # Get emails from both sources
        qb_emails = fetcher.get_email_by_subject(folder_name="Quick Base API Response Data")
        amp_emails = fetcher.get_email_by_subject(folder_name="Auto Feed")
        
        if not qb_emails or not amp_emails:
            print("✗ Missing email data. Both files required:")
            print("  - amp_autofeed_data/quickbase_responses.html")
            print("  - amp_autofeed_data/amp_autofeed.html")
            return False
        
        # Extract HTML content
        qb_html = qb_emails[0]['html_body']
        amp_html = amp_emails[0]['html_body']
        
        # Validate
        validator = AutoFeedValidator()
        validator.load_data(qb_html, amp_html)
        results = validator.validate()
        
        # Print results
        print("\n" + "-"*60)
        print("VALIDATION RESULTS")
        print("-"*60)
        print(f"QuickBase records: {results['total_quickbase']}")
        print(f"AMP records: {results['total_amp']}")
        print(f"Matched: {results['matched']}")
        print(f"QuickBase only: {len(results['qb_only'])}")
        print(f"AMP only: {len(results['amp_only'])}")
        print(f"Field mismatches: {len(results['field_mismatches'])}")
        
        if results['field_mismatches']:
            print("\nField Mismatches (first 10):")
            for mismatch in results['field_mismatches'][:10]:
                print(f"  AutoFeed {mismatch['autofeed_id']}: {mismatch['field']}")
                print(f"    QB: {mismatch['quickbase']}")
                print(f"    AMP: {mismatch['amp']}")
        
        print("\nValidation Status: PASS" if len(results['field_mismatches']) == 0 else "Validation Status: FAIL")
        print("="*60 + "\n")
        
        return len(results['field_mismatches']) == 0
    
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    validate_daily()
