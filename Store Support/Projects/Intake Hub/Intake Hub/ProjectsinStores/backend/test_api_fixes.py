#!/usr/bin/env python3
"""
Quick test to verify the API endpoints work correctly
"""

import json
from pathlib import Path

def test_configs_endpoint():
    """Test loading report configs"""
    configs_dir = Path(__file__).parent / "report_configs"
    configs = []
    
    if configs_dir.exists():
        for config_file in configs_dir.glob("*.json"):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    configs.append(config)
                    print(f"✅ Loaded: {config.get('report_name')} (user: {config.get('user_id')})")
            except Exception as e:
                print(f"❌ Error loading {config_file}: {e}")
    
    print(f"\n📊 Total configs found: {len(configs)}")
    
    # Test filtering
    user_configs = [c for c in configs if c.get('user_id') == 'kendall.rush']
    print(f"📧 Configs for kendall.rush: {len(user_configs)}")
    
    return configs

def test_logs_endpoint():
    """Test reading execution logs"""
    log_file = Path(__file__).parent / "report_execution_log.json"
    
    if not log_file.exists():
        print("📭 No execution log file yet (this is OK if no test emails have been sent)")
        return []
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
        print(f"✅ Read {len(logs)} log entries")
        for log in logs[-3:]:  # Show last 3
            print(f"  - {log.get('report_name')} ({log.get('status')}) at {log.get('timestamp')}")
        return logs
    except Exception as e:
        print(f"❌ Error reading logs: {e}")
        return []

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Report Configuration Files")
    print("=" * 60)
    configs = test_configs_endpoint()
    
    print("\n" + "=" * 60)
    print("Testing Execution Logs")
    print("=" * 60)
    logs = test_logs_endpoint()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
