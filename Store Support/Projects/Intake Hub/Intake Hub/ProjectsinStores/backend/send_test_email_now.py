#!/usr/bin/env python3
"""
Send a test email report
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

async def send_test_email():
    """Send a test email"""
    
    from database import DatabaseService
    from email_service_simple import SimpleEmailReportService
    
    # Initialize database
    db_service = DatabaseService()
    
    # Load the first test report config
    configs_dir = Path(__file__).parent / "report_configs"
    config_file = configs_dir / "4b80e040-b338-4489-b8ff-6b3f8f5ee4be.json"
    
    if not config_file.exists():
        print("❌ Config file not found")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print(f"📧 Sending test email for: {config.get('report_name')}")
    print(f"📨 To: kendall.rush@walmart.com")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # Initialize email service
    email_service = SimpleEmailReportService(db_service)
    
    # Send test email
    result = await email_service.generate_and_send_report(
        config,
        override_email="kendall.rush@walmart.com"
    )
    
    print(f"\n✅ Result: {result}")
    
    if result['success']:
        print(f"✅ Email sent successfully!")
        print(f"📧 Sent to: {', '.join(result.get('sent_to', []))}")
        
        # Log the execution
        log_file = Path(__file__).parent / "report_execution_log.json"
        log_entry = {
            "config_id": config.get('config_id'),
            "report_name": config.get('report_name'),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success",
            "recipients": ', '.join(result.get('sent_to', [])),
            "error_message": None
        }
        
        try:
            logs = []
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            logs.append(log_entry)
            logs = logs[-1000:]  # Keep last 1000
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            print("✅ Logged to execution log")
        except Exception as e:
            print(f"⚠️ Error logging: {e}")
    else:
        print(f"❌ Error: {result.get('message')}")

if __name__ == "__main__":
    asyncio.run(send_test_email())
