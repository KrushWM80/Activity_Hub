#!/usr/bin/env python3
"""
AMP AutoFeed Validation - CSV Report Generator
Creates comprehensive CSV reports for longer-term analysis and sharing
"""

import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class CSVReportGenerator:
    """Generate CSV reports from validation history"""
    
    def __init__(self, log_dir: str = "amp_validation_logs"):
        self.log_dir = Path(log_dir)
        self.history_file = self.log_dir / "validation_history.json"
        self.csv_report_dir = self.log_dir / "csv_reports"
        self.csv_report_dir.mkdir(exist_ok=True)
        
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Load validation history from file"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}
    
    def generate_daily_summary_csv(self) -> Path:
        """
        Generate CSV with daily validation summary
        Columns: Date, Status, QB Record Count, AMP Record Count, Differences, Missing Records, Extra Records
        """
        csv_file = self.csv_report_dir / f"daily_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        rows = []
        for date in sorted(self.history.keys(), reverse=True):
            result = self.history[date]
            
            if result.get('status') == 'ERROR':
                rows.append({
                    'Date': date,
                    'Status': 'ERROR',
                    'QB_Records': 'N/A',
                    'AMP_Records': 'N/A',
                    'Match': 'No',
                    'Differences': result.get('error', 'Unknown error'),
                    'Missing_in_AMP': 'N/A',
                    'Extra_in_AMP': 'N/A',
                })
            else:
                comparison = result.get('comparison', {})
                differences = comparison.get('differences', [])
                missing = comparison.get('missing_in_amp', [])
                extra = comparison.get('extra_in_amp', [])
                
                rows.append({
                    'Date': date,
                    'Status': result.get('status', 'UNKNOWN'),
                    'QB_Records': comparison.get('qb_record_count', 'N/A'),
                    'AMP_Records': comparison.get('amp_record_count', 'N/A'),
                    'Match': 'Yes' if comparison.get('match') else 'No',
                    'Differences': '; '.join(differences) if differences else 'None',
                    'Missing_in_AMP': len(missing),
                    'Extra_in_AMP': len(extra),
                })
        
        # Write CSV
        if rows:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'Date', 'Status', 'QB_Records', 'AMP_Records', 'Match',
                    'Differences', 'Missing_in_AMP', 'Extra_in_AMP'
                ])
                writer.writeheader()
                writer.writerows(rows)
        
        print(f"✓ Daily summary CSV: {csv_file}")
        return csv_file
    
    def generate_discrepancies_csv(self) -> Path:
        """
        Generate CSV with all discrepancies found
        Columns: Date, Type (Missing/Extra/FieldDiff), AutoFeed_Id, Field, QB_Value, AMP_Value
        """
        csv_file = self.csv_report_dir / f"discrepancies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        rows = []
        
        for date in sorted(self.history.keys()):
            result = self.history[date]
            
            if result.get('status') != 'FAIL':
                continue
            
            comparison = result.get('comparison', {})
            
            # Missing records
            for rec_id in comparison.get('missing_in_amp', []):
                rows.append({
                    'Date': date,
                    'Type': 'Missing in AMP',
                    'AutoFeed_Id': rec_id,
                    'Field': 'N/A',
                    'QB_Value': 'Present',
                    'AMP_Value': 'Missing',
                })
            
            # Extra records
            for rec_id in comparison.get('extra_in_amp', []):
                rows.append({
                    'Date': date,
                    'Type': 'Extra in AMP',
                    'AutoFeed_Id': rec_id,
                    'Field': 'N/A',
                    'QB_Value': 'Missing',
                    'AMP_Value': 'Present',
                })
            
            # Field differences
            field_diffs = comparison.get('field_differences', {})
            for field, diffs in field_diffs.items():
                for diff in diffs:
                    rows.append({
                        'Date': date,
                        'Type': 'Field Difference',
                        'AutoFeed_Id': diff.get('id', 'N/A'),
                        'Field': field,
                        'QB_Value': diff.get('qb_value', ''),
                        'AMP_Value': diff.get('amp_value', ''),
                    })
        
        # Write CSV
        if rows:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'Date', 'Type', 'AutoFeed_Id', 'Field', 'QB_Value', 'AMP_Value'
                ])
                writer.writeheader()
                writer.writerows(rows)
        
        print(f"✓ Discrepancies CSV: {csv_file}")
        return csv_file
    
    def generate_records_comparison_csv(self, days: int = 7) -> Path:
        """
        Generate CSV comparing actual records from recent validations
        Shows all records with their values from QB and AMP
        """
        csv_file = self.csv_report_dir / f"records_comparison_last{days}d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        # Collect all unique AutoFeed Ids
        all_records_by_id = defaultdict(lambda: {
            'dates': [],
            'qb_values': {},
            'amp_values': {},
            'latest_qb': {},
            'latest_amp': {},
        })
        
        for date in sorted(self.history.keys()):
            if date < cutoff_str:
                continue
            
            result = self.history[date]
            
            if result.get('status') == 'ERROR':
                continue
            
            comparison = result.get('comparison', {})
            qb_records = comparison.get('qb_records', [])
            amp_records = comparison.get('amp_records', [])
            
            # Index by AutoFeed Id
            for rec in qb_records:
                rec_id = rec.get('AutoFeed Id', 'Unknown')
                all_records_by_id[rec_id]['dates'].append(date)
                all_records_by_id[rec_id]['latest_qb'] = rec
            
            for rec in amp_records:
                rec_id = rec.get('AutoFeed Id', 'Unknown')
                if rec_id not in all_records_by_id:
                    all_records_by_id[rec_id]['dates'].append(date)
                all_records_by_id[rec_id]['latest_amp'] = rec
        
        # Generate rows
        rows = []
        from amp_autofeed_validation import HTMLEmailParser
        
        for rec_id in sorted(all_records_by_id.keys()):
            rec_data = all_records_by_id[rec_id]
            latest_qb = rec_data['latest_qb']
            latest_amp = rec_data['latest_amp']
            
            for col in HTMLEmailParser.TARGET_COLUMNS:
                rows.append({
                    'AutoFeed_Id': rec_id,
                    'Column': col,
                    'QB_Value': latest_qb.get(col, ''),
                    'AMP_Value': latest_amp.get(col, ''),
                    'Match': 'Yes' if latest_qb.get(col) == latest_amp.get(col) else 'No',
                    'Last_Seen': max(rec_data['dates']) if rec_data['dates'] else 'Unknown',
                })
        
        # Write CSV
        if rows:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'AutoFeed_Id', 'Column', 'QB_Value', 'AMP_Value', 'Match', 'Last_Seen'
                ])
                writer.writeheader()
                writer.writerows(rows)
        
        print(f"✓ Records comparison CSV: {csv_file}")
        return csv_file
    
    def generate_trend_statistics_csv(self, days: int = 90) -> Path:
        """
        Generate CSV with trend statistics
        Columns: Metric, Value, Percentage
        """
        csv_file = self.csv_report_dir / f"trend_statistics_{days}d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        total = 0
        passed = 0
        failed = 0
        errored = 0
        total_discrepancies = 0
        
        for date in self.history.keys():
            if date < cutoff_str:
                continue
            
            result = self.history[date]
            total += 1
            
            if result.get('status') == 'PASS':
                passed += 1
            elif result.get('status') == 'FAIL':
                failed += 1
                comparison = result.get('comparison', {})
                total_discrepancies += len(comparison.get('differences', []))
            elif result.get('status') == 'ERROR':
                errored += 1
        
        rows = [
            {
                'Metric': 'Total Validations',
                'Value': total,
                'Percentage': '100%',
            },
            {
                'Metric': 'Passed',
                'Value': passed,
                'Percentage': f"{(passed/total*100):.1f}%" if total > 0 else "N/A",
            },
            {
                'Metric': 'Failed',
                'Value': failed,
                'Percentage': f"{(failed/total*100):.1f}%" if total > 0 else "N/A",
            },
            {
                'Metric': 'Errors',
                'Value': errored,
                'Percentage': f"{(errored/total*100):.1f}%" if total > 0 else "N/A",
            },
            {
                'Metric': 'Total Discrepancies Found',
                'Value': total_discrepancies,
                'Percentage': 'N/A',
            },
        ]
        
        # Write CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Metric', 'Value', 'Percentage'])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Trend statistics CSV: {csv_file}")
        return csv_file
    
    def generate_all_reports(self, days: int = 90) -> Dict[str, Path]:
        """Generate all CSV reports"""
        print("\nGenerating comprehensive CSV reports...")
        print("="*70)
        
        reports = {
            'daily_summary': self.generate_daily_summary_csv(),
            'discrepancies': self.generate_discrepancies_csv(),
            'records_comparison': self.generate_records_comparison_csv(days=days),
            'trend_statistics': self.generate_trend_statistics_csv(days=days),
        }
        
        print("="*70)
        print(f"\n✓ All reports generated to: {self.csv_report_dir}")
        
        return reports


def main():
    """Generate CSV reports"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate CSV reports from validation history")
    parser.add_argument('--log-dir', default='amp_validation_logs', help='Log directory')
    parser.add_argument('--days', type=int, default=90, help='Days to include in analysis')
    
    args = parser.parse_args()
    
    generator = CSVReportGenerator(log_dir=args.log_dir)
    generator.generate_all_reports(days=args.days)


if __name__ == "__main__":
    main()
