"""
Report Scheduler Service for Intake Hub
Handles scheduled execution of email reports using APScheduler
"""

import os
import json
import asyncio
from datetime import datetime, time
from typing import Dict, List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from email_report_models import (
    EmailReportConfig, ReportFrequency, ReportExecutionLog
)
from email_service import EmailReportService
from database import DatabaseService


class ReportScheduler:
    """Manages scheduling and execution of email reports"""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.email_service = EmailReportService(db_service)
        self.scheduler = AsyncIOScheduler()
        self.configs: Dict[str, EmailReportConfig] = {}
        self.config_file = os.path.join(
            os.path.dirname(__file__), 
            "report_configs.json"
        )
        self._load_configs()
    
    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        self._schedule_all_reports()
        print("✅ Report scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("🛑 Report scheduler stopped")
    
    def _load_configs(self):
        """Load report configurations from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    for config_data in data:
                        config = EmailReportConfig(**config_data)
                        self.configs[config.config_id] = config
                print(f"📁 Loaded {len(self.configs)} report configurations")
            except Exception as e:
                print(f"⚠️ Error loading report configs: {e}")
                self.configs = {}
        else:
            self.configs = {}
            print("📁 No existing report configurations found")
    
    def _save_configs(self):
        """Save report configurations to file"""
        try:
            data = [config.model_dump(mode='json') for config in self.configs.values()]
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"💾 Saved {len(self.configs)} report configurations")
        except Exception as e:
            print(f"⚠️ Error saving report configs: {e}")
    
    def add_report_config(self, config: EmailReportConfig) -> str:
        """Add a new report configuration and schedule it"""
        if not config.config_id:
            import uuid
            config.config_id = str(uuid.uuid4())
        
        self.configs[config.config_id] = config
        self._save_configs()
        
        if config.is_active:
            self._schedule_report(config)
        
        print(f"➕ Added report config: {config.report_name} (ID: {config.config_id})")
        return config.config_id
    
    def update_report_config(self, config_id: str, config: EmailReportConfig) -> bool:
        """Update an existing report configuration"""
        if config_id not in self.configs:
            return False
        
        # Remove old schedule
        self._unschedule_report(config_id)
        
        # Update config
        config.config_id = config_id
        config.updated_at = datetime.utcnow()
        self.configs[config_id] = config
        self._save_configs()
        
        # Reschedule if active
        if config.is_active:
            self._schedule_report(config)
        
        print(f"✏️ Updated report config: {config.report_name} (ID: {config_id})")
        return True
    
    def delete_report_config(self, config_id: str) -> bool:
        """Delete a report configuration"""
        if config_id not in self.configs:
            return False
        
        config = self.configs[config_id]
        self._unschedule_report(config_id)
        del self.configs[config_id]
        self._save_configs()
        
        print(f"🗑️ Deleted report config: {config.report_name} (ID: {config_id})")
        return True
    
    def get_report_config(self, config_id: str) -> EmailReportConfig:
        """Get a report configuration by ID"""
        return self.configs.get(config_id)
    
    def get_all_report_configs(self, user_id: str = None) -> List[EmailReportConfig]:
        """Get all report configurations, optionally filtered by user"""
        if user_id:
            return [c for c in self.configs.values() if c.user_id == user_id]
        return list(self.configs.values())
    
    def toggle_report_config(self, config_id: str, is_active: bool) -> bool:
        """Enable or disable a report configuration"""
        if config_id not in self.configs:
            return False
        
        config = self.configs[config_id]
        config.is_active = is_active
        config.updated_at = datetime.utcnow()
        self._save_configs()
        
        if is_active:
            self._schedule_report(config)
        else:
            self._unschedule_report(config_id)
        
        status = "enabled" if is_active else "disabled"
        print(f"🔄 Report config {status}: {config.report_name}")
        return True
    
    def _schedule_all_reports(self):
        """Schedule all active report configurations"""
        for config in self.configs.values():
            if config.is_active:
                self._schedule_report(config)
    
    def _schedule_report(self, config: EmailReportConfig):
        """Schedule a single report configuration"""
        job_id = f"report_{config.config_id}"
        
        # Remove existing job if present
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
        
        # Parse delivery time
        try:
            hour, minute = map(int, config.delivery_time.split(':'))
        except:
            hour, minute = 8, 0  # Default to 8:00 AM
        
        # Create trigger based on frequency
        if config.frequency == ReportFrequency.DAILY:
            trigger = CronTrigger(hour=hour, minute=minute)
        
        elif config.frequency == ReportFrequency.WEEKLY:
            # Map day name to cron day_of_week (0=Monday, 6=Sunday)
            day_map = {
                'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                'Friday': 4, 'Saturday': 5, 'Sunday': 6
            }
            day_of_week = day_map.get(config.delivery_day, 4)  # Default to Friday
            trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute)
        
        elif config.frequency == ReportFrequency.BIWEEKLY:
            # Run every 2 weeks on the specified day
            day_map = {
                'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                'Friday': 4, 'Saturday': 5, 'Sunday': 6
            }
            day_of_week = day_map.get(config.delivery_day, 4)
            trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute, week='*/2')
        
        elif config.frequency == ReportFrequency.MONTHLY:
            # Run on 1st of each month
            trigger = CronTrigger(day=1, hour=hour, minute=minute)
        
        else:
            print(f"⚠️ Unsupported frequency: {config.frequency}")
            return
        
        # Add job to scheduler
        self.scheduler.add_job(
            self._execute_report,
            trigger=trigger,
            args=[config.config_id],
            id=job_id,
            name=f"Email Report: {config.report_name}",
            replace_existing=True
        )
        
        print(f"📅 Scheduled report: {config.report_name} ({config.frequency.value})")
    
    def _unschedule_report(self, config_id: str):
        """Unschedule a report configuration"""
        job_id = f"report_{config_id}"
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
            print(f"📅 Unscheduled report: {config_id}")
    
    async def _execute_report(self, config_id: str):
        """Execute a scheduled report"""
        config = self.configs.get(config_id)
        if not config or not config.is_active:
            print(f"⚠️ Report config {config_id} not found or inactive")
            return
        
        print(f"🔄 Executing scheduled report: {config.report_name}")
        
        try:
            # Generate and send report
            result = await self.email_service.generate_and_send_report(config)
            
            # Update last sent timestamp
            config.last_sent = datetime.utcnow()
            self._save_configs()
            
            # Log execution
            self._log_execution(config_id, result.success, result.sent_to, 
                              error=None if result.success else result.message,
                              report_name=config.report_name)
            
            if result.success:
                print(f"✅ Report sent successfully: {config.report_name}")
            else:
                print(f"❌ Report failed: {config.report_name} - {result.message}")

        
        except Exception as e:
            print(f"❌ Error executing report {config.report_name}: {str(e)}")
            self._log_execution(config_id, False, [], error=str(e), report_name=config.report_name)
    
    async def execute_report_now(self, config_id: str, override_email: str = None):
        """Execute a report immediately (for testing or manual trigger)"""
        config = self.configs.get(config_id)
        if not config:
            raise ValueError(f"Report config {config_id} not found")
        
        print(f"🔄 Manually executing report: {config.report_name}")
        
        result = await self.email_service.generate_and_send_report(
            config, 
            override_email=override_email
        )
        
        if not override_email:
            # Only update last_sent if not a test
            config.last_sent = datetime.utcnow()
            self._save_configs()
        
        self._log_execution(
            config_id, 
            result.success, 
            result.sent_to,
            error=None if result.success else result.message,
            report_name=config.report_name
        )
        
        return result
    
    def _log_execution(
        self, 
        config_id: str, 
        success: bool, 
        recipients: List[str],
        error: str = None,
        report_name: str = None
    ):
        """Log report execution (simple file-based logging)"""
        log_file = os.path.join(os.path.dirname(__file__), "report_execution_log.json")
        
        log_entry = {
            "config_id": config_id,
            "report_name": report_name or config_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success" if success else "failed",
            "recipients": ', '.join(recipients) if recipients else "",
            "error_message": error
        }
        
        # Append to log file
        try:
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            # Keep only last 1000 entries
            logs = logs[-1000:]
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        
        except Exception as e:
            print(f"⚠️ Error logging execution: {e}")
    
    def get_execution_logs(
        self, 
        config_id: str = None, 
        limit: int = 50
    ) -> List[Dict]:
        """Get execution logs, optionally filtered by config_id"""
        log_file = os.path.join(os.path.dirname(__file__), "report_execution_log.json")
        
        if not os.path.exists(log_file):
            return []
        
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            if config_id:
                logs = [log for log in logs if log.get("config_id") == config_id]
            
            # Return most recent logs
            return sorted(logs, key=lambda x: x["timestamp"], reverse=True)[:limit]
        
        except Exception as e:
            print(f"⚠️ Error reading execution logs: {e}")
            return []


# Global scheduler instance
_scheduler_instance = None

def get_scheduler(db_service: DatabaseService = None) -> ReportScheduler:
    """Get or create the global scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None and db_service:
        _scheduler_instance = ReportScheduler(db_service)
    return _scheduler_instance
