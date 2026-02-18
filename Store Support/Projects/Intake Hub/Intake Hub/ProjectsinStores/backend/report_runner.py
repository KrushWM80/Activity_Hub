"""
Report Runner Script for Windows Task Scheduler
This script runs a specific report configuration and sends it via email
Can be called by Windows Task Scheduler with: python report_runner.py <config_id>
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from database import DatabaseService
from email_service_simple import SimpleEmailReportService


async def run_report(config_id: str):
    """Load and execute a report configuration"""
    
    # Load report configuration
    config_file = Path(__file__).parent / "report_configs" / f"{config_id}.json"
    
    if not config_file.exists():
        print(f"❌ Configuration file not found: {config_file}")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"📧 Running report: {config['report_name']}")
        print(f"   To: {config['primary_email']}")
        
        # Initialize services
        db_service = DatabaseService()
        email_service = SimpleEmailReportService(db_service)
        
        # Generate and send report
        result = await email_service.generate_and_send_report(config)
        
        if result['success']:
            print(f"✅ {result['message']}")
            
            # Update last_sent timestamp
            config['last_sent'] = result['timestamp']
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        else:
            print(f"❌ {result['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Error running report: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for Windows Task Scheduler"""
    
    if len(sys.argv) < 2:
        print("Usage: python report_runner.py <config_id>")
        sys.exit(1)
    
    config_id = sys.argv[1]
    
    print(f"{'='*60}")
    print(f"Intake Hub Report Runner")
    print(f"Config ID: {config_id}")
    print(f"{'='*60}")
    
    # Run the report
    success = asyncio.run(run_report(config_id))
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
