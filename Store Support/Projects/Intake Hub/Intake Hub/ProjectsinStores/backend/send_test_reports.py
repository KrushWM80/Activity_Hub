import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from email_service_simple import SimpleEmailReportService
from database import DatabaseService

# Load environment variables from .env
load_dotenv()

async def send_test_reports():
    """Send test emails for both active reports"""
    
    # Initialize services
    db_service = DatabaseService()
    email_service = SimpleEmailReportService(db_service)
    
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"From Email: {email_service.from_email}")
    print()
    
    # Load report configs
    configs_dir = Path(__file__).parent / "report_configs"
    
    reports = [
        {
            "name": "Kendall's Daily",
            "file": "4b80e040-b338-4489-b8ff-6b3f8f5ee4be.json"
        },
        {
            "name": "New Projects & Daily Recap", 
            "file": "6058279f-4f63-411d-adce-3c826b95687e.json"
        }
    ]
    
    for report in reports:
        config_file = configs_dir / report["file"]
        
        if not config_file.exists():
            print(f"❌ {report['name']}: Config file not found")
            continue
            
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print(f"\n📧 Sending: {report['name']}")
            print(f"   To: {config['primary_email']}")
            print(f"   Filters: {config.get('filters', {})}")
            
            # Send the report
            result = await email_service.generate_and_send_report(config)
            
            if result['success']:
                print(f"   ✅ {result['message']}")
                # Update last_sent
                config['last_sent'] = result['timestamp']
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)
            else:
                print(f"   ❌ {result['message']}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("="*60)
    print("TESTING EMAIL REPORTS")
    print("="*60)
    asyncio.run(send_test_reports())
    print("\n" + "="*60)
    print("Test complete. Check your email inbox.")
    print("="*60)
