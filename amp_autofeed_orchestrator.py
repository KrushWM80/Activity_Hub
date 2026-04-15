#!/usr/bin/env python3
"""
AMP AutoFeed Daily Validation Orchestrator
Main entry point that coordinates validation and reporting
Runs daily to compare QuickBase API and AMP AutoFeed emails
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Import our validation modules
from amp_autofeed_validation import AutoFeedValidator
from amp_autofeed_csv_reporter import CSVReportGenerator


class ValidationOrchestrator:
    """Orchestrates daily validation and reporting"""
    
    def __init__(self, log_dir: str = "amp_validation_logs"):
        self.log_dir = Path(log_dir)
        self.validator = AutoFeedValidator(log_dir=log_dir)
        self.config_file = self.log_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def run_daily_validation(self, send_email: bool = False, 
                             recipient: Optional[str] = None) -> Dict:
        """Run daily validation and optionally send report"""
        
        print("\n" + "="*70)
        print("AMP AutoFeed Daily Validation")
        print("="*70)
        print(f"Started: {datetime.now().isoformat()}")
        
        # Run validation
        result = self.validator.validate_daily()
        
        print(f"\nValidation Status: {result.get('status', 'UNKNOWN')}")
        
        if result.get('status') == 'PASS':
            print("✓ Data match verified")
        elif result.get('status') == 'FAIL':
            print("✗ Discrepancies detected:")
            for diff in result.get('comparison', {}).get('differences', []):
                print(f"   - {diff}")
        elif result.get('status') == 'ERROR':
            print(f"✗ Error: {result.get('error')}")
        
        # Send email report if configured
        if send_email and recipient:
            self._send_report(result, recipient)
        
        print("\n" + "="*70)
        return result
    
    def _send_report(self, result: Dict, recipient: str):
        """Send email report"""
        try:
            from amp_autofeed_email_reporter import ValidationReportEmail
            import os
            
            smtp_server = os.getenv("VALIDATION_SMTP_SERVER", "smtp.gmail.com")
            sender_email = os.getenv("VALIDATION_SENDER_EMAIL")
            sender_password = os.getenv("VALIDATION_SENDER_PASSWORD")
            
            if not sender_email or not sender_password:
                print("\n⚠ Email not configured. Skipping email report.")
                print("  Set environment variables to enable:")
                print("    - VALIDATION_SENDER_EMAIL")
                print("    - VALIDATION_SENDER_PASSWORD")
                return
            
            reporter = ValidationReportEmail(
                smtp_server=smtp_server,
                sender_email=sender_email,
                sender_password=sender_password,
                recipient_email=recipient
            )
            
            print(f"\nSending report to {recipient}...")
            if reporter.send_report(result):
                print("✓ Report email sent")
            else:
                print("✗ Failed to send report email")
        
        except ImportError:
            print("✗ Email reporter module not available")
        except Exception as e:
            print(f"✗ Error sending report: {e}")
    
    def run_historical_analysis(self, days: int = 365) -> Dict:
        """Run historical analysis and generate report"""
        
        print("\n" + "="*70)
        print("Historical Validation Analysis")
        print("="*70)
        
        report = self.validator.generate_historical_report(days=days)
        
        print(f"\nReport saved to: {self.log_dir}")
        print(f"  - JSON: historical_report.json")
        print(f"  - Text: historical_report.txt")
        
        return report
    
    def configure_email(self, smtp_server: str, sender_email: str):
        """Configure email settings"""
        self.config['email'] = {
            'smtp_server': smtp_server,
            'sender_email': sender_email,
        }
        # Also save the email address for Exchange/Outlook access
        self.config['email_address'] = sender_email
        self._save_config()
        print(f"✓ Email configuration saved: {sender_email}")
    
    def show_status(self):
        """Show current status and recent validations"""
        
        history_file = self.log_dir / "validation_history.json"
        if not history_file.exists():
            print("No validation history found")
            return
        
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        print("\n" + "="*70)
        print("Recent Validation History")
        print("="*70)
        
        sorted_dates = sorted(history.keys(), reverse=True)[:7]
        
        for date in sorted_dates:
            result = history[date]
            status = result.get('status', 'UNKNOWN')
            status_symbol = {
                'PASS': '✓',
                'FAIL': '✗',
                'ERROR': '⚠'
            }.get(status, '?')
            
            print(f"{status_symbol} {date}: {status}")
            if result.get('comparison', {}).get('differences'):
                for diff in result['comparison']['differences'][:2]:
                    print(f"    - {diff[:60]}...")
        
        print("\n" + "="*70)
    
    def generate_csv_reports(self, days: int = 90) -> Dict[str, Path]:
        """Generate CSV reports for comprehensive analysis"""
        
        print("\n" + "="*70)
        print("CSV Report Generation")
        print("="*70)
        
        generator = CSVReportGenerator(log_dir=str(self.log_dir))
        reports = generator.generate_all_reports(days=days)
        
        print("\nGenerated Reports:")
        for report_type, filepath in reports.items():
            print(f"  {report_type}: {filepath.name}")
        
        return reports


def main():
    parser = argparse.ArgumentParser(
        description="AMP AutoFeed Daily Validation Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run daily validation
  %(prog)s daily
  
  # Run daily validation and send email
  %(prog)s daily --send-email --recipient your.email@walmart.com
  
  # Generate historical report (last 90 days)
  %(prog)s historical --days 90
  
  # Show recent validation results
  %(prog)s status
  
  # Configure email settings
  %(prog)s configure-email --smtp smtp.gmail.com --email your@gmail.com
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Daily validation command
    daily_parser = subparsers.add_parser('daily', help='Run daily validation')
    daily_parser.add_argument('--send-email', action='store_true',
                             help='Send email report after validation')
    daily_parser.add_argument('--recipient', help='Email recipient address')
    daily_parser.add_argument('--log-dir', default='amp_validation_logs',
                             help='Log directory')
    
    # Historical analysis command
    hist_parser = subparsers.add_parser('historical', help='Generate historical report')
    hist_parser.add_argument('--days', type=int, default=365,
                            help='Days back to analyze (default: 365)')
    hist_parser.add_argument('--log-dir', default='amp_validation_logs',
                            help='Log directory')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show validation status')
    status_parser.add_argument('--log-dir', default='amp_validation_logs',
                              help='Log directory')
    
    # Configure email command
    config_parser = subparsers.add_parser('configure-email', help='Configure email settings')
    config_parser.add_argument('--smtp', required=True, help='SMTP server')
    config_parser.add_argument('--email', required=True, help='Sender email')
    config_parser.add_argument('--log-dir', default='amp_validation_logs',
                              help='Log directory')
    
    # CSV report command
    csv_parser = subparsers.add_parser('csv-report', help='Generate CSV reports')
    csv_parser.add_argument('--days', type=int, default=90,
                           help='Days back to analyze (default: 90)')
    csv_parser.add_argument('--log-dir', default='amp_validation_logs',
                           help='Log directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        orchestrator = ValidationOrchestrator(log_dir=args.log_dir if hasattr(args, 'log_dir') else 'amp_validation_logs')
        
        if args.command == 'daily':
            result = orchestrator.run_daily_validation(
                send_email=args.send_email,
                recipient=args.recipient
            )
            return 0 if result.get('status') == 'PASS' else 1
        
        elif args.command == 'historical':
            orchestrator.run_historical_analysis(days=args.days)
            return 0
        
        elif args.command == 'status':
            orchestrator.show_status()
            return 0
        
        elif args.command == 'configure-email':
            orchestrator.configure_email(args.smtp, args.email)
            return 0
        
        elif args.command == 'csv-report':
            orchestrator.generate_csv_reports(days=args.days)
            return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
