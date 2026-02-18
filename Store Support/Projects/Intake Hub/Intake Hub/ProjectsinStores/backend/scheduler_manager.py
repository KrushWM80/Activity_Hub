"""
Windows Task Scheduler Manager
Creates, updates, and deletes scheduled tasks for email reports
Uses native Windows Task Scheduler instead of APScheduler
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime, time


class WindowsSchedulerManager:
    """Manages Windows Task Scheduler tasks for email reports"""
    
    def __init__(self):
        self.python_exe = r"C:\Users\krush\.code-puppy-venv\Scripts\python.exe"
        self.runner_script = Path(__file__).parent / "report_runner.py"
        self.task_prefix = "IntakeHub_Report_"
    
    def create_scheduled_task(self, config: Dict) -> bool:
        """Create a Windows scheduled task for a report"""
        
        config_id = config['config_id']
        task_name = f"{self.task_prefix}{config_id}"
        
        # Build schedule parameters
        schedule_params = self._build_schedule_params(config)
        
        # Build task command
        task_command = f'"{self.python_exe}" "{self.runner_script}" {config_id}'
        
        # Create the task using schtasks command
        cmd = [
            'schtasks', '/Create',
            '/TN', task_name,
            '/TR', task_command,
            '/SC', schedule_params['schedule_type'],
        ]
        
        # Add day of week for weekly tasks
        if schedule_params.get('day'):
            cmd.extend(['/D', schedule_params['day']])
        
        # Add start time
        cmd.extend(['/ST', schedule_params['start_time']])
        
        # Run as current user
        cmd.extend(['/RU', 'SYSTEM'])
        
        # Force create (overwrite if exists)
        cmd.append('/F')
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Created scheduled task: {task_name}")
                return True
            else:
                print(f"❌ Error creating task: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Exception creating task: {str(e)}")
            return False
    
    def _build_schedule_params(self, config: Dict) -> Dict:
        """Build schedule parameters from config"""
        
        frequency = config['frequency']
        delivery_time = config['delivery_time']  # Format: "HH:MM"
        
        params = {
            'start_time': delivery_time
        }
        
        if frequency == 'Daily':
            params['schedule_type'] = 'DAILY'
        
        elif frequency == 'Weekly':
            params['schedule_type'] = 'WEEKLY'
            params['day'] = config.get('delivery_day', 'MON')[:3].upper()
        
        elif frequency.startswith('Every '):
            # Extract day (e.g., "Every Monday" -> "MON")
            day = frequency.replace('Every ', '').upper()
            params['schedule_type'] = 'WEEKLY'
            params['day'] = self._get_day_abbreviation(day)
        
        elif frequency == 'Bi-Weekly':
            params['schedule_type'] = 'WEEKLY'
            params['day'] = config.get('delivery_day', 'MON')[:3].upper()
            # Note: Bi-weekly requires custom scheduling in Task Scheduler
        
        elif frequency == 'Monthly':
            params['schedule_type'] = 'MONTHLY'
        
        else:
            params['schedule_type'] = 'DAILY'
        
        return params
    
    def _get_day_abbreviation(self, day: str) -> str:
        """Convert day name to 3-letter abbreviation"""
        day_map = {
            'MONDAY': 'MON',
            'TUESDAY': 'TUE',
            'WEDNESDAY': 'WED',
            'THURSDAY': 'THU',
            'FRIDAY': 'FRI',
            'SATURDAY': 'SAT',
            'SUNDAY': 'SUN'
        }
        return day_map.get(day.upper(), 'MON')
    
    def delete_scheduled_task(self, config_id: str) -> bool:
        """Delete a Windows scheduled task"""
        
        task_name = f"{self.task_prefix}{config_id}"
        
        cmd = ['schtasks', '/Delete', '/TN', task_name, '/F']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Deleted scheduled task: {task_name}")
                return True
            else:
                print(f"⚠️  Task may not exist: {task_name}")
                return True  # Not an error if task doesn't exist
                
        except Exception as e:
            print(f"❌ Exception deleting task: {str(e)}")
            return False
    
    def update_scheduled_task(self, config: Dict) -> bool:
        """Update a Windows scheduled task (delete and recreate)"""
        
        config_id = config['config_id']
        
        # Delete existing task
        self.delete_scheduled_task(config_id)
        
        # Create new task
        return self.create_scheduled_task(config)
    
    def list_report_tasks(self) -> List[str]:
        """List all IntakeHub report tasks"""
        
        cmd = ['schtasks', '/Query', '/FO', 'LIST', '/V']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Filter for IntakeHub tasks
            tasks = []
            for line in result.stdout.split('\n'):
                if self.task_prefix in line:
                    # Extract task name
                    if 'TaskName:' in line:
                        task_name = line.split('TaskName:')[1].strip()
                        tasks.append(task_name)
            
            return tasks
            
        except Exception as e:
            print(f"❌ Exception listing tasks: {str(e)}")
            return []
    
    def enable_task(self, config_id: str) -> bool:
        """Enable a scheduled task"""
        
        task_name = f"{self.task_prefix}{config_id}"
        cmd = ['schtasks', '/Change', '/TN', task_name, '/ENABLE']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def disable_task(self, config_id: str) -> bool:
        """Disable a scheduled task"""
        
        task_name = f"{self.task_prefix}{config_id}"
        cmd = ['schtasks', '/Change', '/TN', task_name, '/DISABLE']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
