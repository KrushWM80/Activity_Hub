#!/usr/bin/env python3
"""
Test script to verify execution logging for email reports
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

async def test_email_logging():
    """Test email sending and logging"""
    
    # Import dependencies
    from database import DatabaseService
    from email_service_simple import SimpleEmailReportService
    from report_scheduler import get_scheduler
    
    # Initialize database
    db_service = DatabaseService()
    
    # Load a test report config
    configs_dir = Path(__file__).parent / "report_configs"
    config_files = list(configs_dir.glob("*.json"))
    
    if not config_files:
        print("❌ No report configs found")
        return
    
    config_file = config_files[0]
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print(f"📧 Testing email send for: {config.get('report_name')}")
    
    # Initialize email service
    email_service = SimpleEmailReportService(db_service)
    
    # Send test email
    test_recipient = "kendall.rush@walmart.com"
    print(f"Sending test email to: {test_recipient}")
    
    result = await email_service.generate_and_send_report(
        config,
        override_email=test_recipient
    )
    
    print(f"✅ Send result: {result}")
    
    # Log the execution
    scheduler = get_scheduler(db_service)
    scheduler._log_execution(
        config_file.stem,
        result['success'],
        result.get('sent_to', []),
        error=None if result['success'] else result.get('message'),
        report_name=config.get('report_name', 'Test Report')
    )
    
    print("✅ Logged execution")
    
    # Read back the logs to verify
    logs = scheduler.get_execution_logs(limit=5)
    print(f"\n📝 Recent logs ({len(logs)} found):")
    for log in logs[-3:]:  # Show last 3
        print(f"  - {log['report_name']} ({log['status']}) at {log['timestamp']}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_email_logging())
