#!/usr/bin/env python3
"""
Snapshot Comparison Module
Compares two snapshots and identifies changes in manager assignments.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ManagerChange:
    """Represents a detected manager change."""
    location_id: str
    location_name: str
    location_type: str
    role: str
    previous_manager: str
    new_manager: str
    previous_email: Optional[str] = None
    new_email: Optional[str] = None
    change_detected: str = None
    market: Optional[str] = None
    region: Optional[str] = None
    
    def __post_init__(self):
        if self.change_detected is None:
            self.change_detected = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"[CHANGE] {self.location_name} ({self.location_id})\n"
            f"  Role: {self.role}\n"
            f"  Previous: {self.previous_manager}\n"
            f"  New: {self.new_manager}\n"
            f"  Detected: {self.change_detected}"
        )


class SnapshotComparator:
    """Compare two snapshots and detect manager changes."""
    
    def __init__(self, previous_snapshot: Dict[str, Any], current_snapshot: Dict[str, Any]):
        self.previous = previous_snapshot
        self.current = current_snapshot
        self.changes: List[ManagerChange] = []
    
    def _create_manager_key(self, manager: Dict[str, Any]) -> str:
        """
        Create a unique key for a manager position.
        Format: location_id|role
        """
        location_id = manager.get('location_id', '')
        role = manager.get('role', '')
        return f"{location_id}|{role}"
    
    def compare(self) -> List[ManagerChange]:
        """
        Compare snapshots and identify changes.
        
        Returns:
            List of ManagerChange objects
        """
        # Build lookup dictionaries
        previous_managers = {
            self._create_manager_key(m): m
            for m in self.previous.get('managers', [])
        }
        
        current_managers = {
            self._create_manager_key(m): m
            for m in self.current.get('managers', [])
        }
        
        # Find changes
        for key, current_mgr in current_managers.items():
            previous_mgr = previous_managers.get(key)
            
            if previous_mgr is None:
                # New position (not previously tracked)
                print(f"[NEW] {key}: {current_mgr.get('manager_name')}")
                continue
            
            # Compare manager names
            prev_name = previous_mgr.get('manager_name', '').strip().lower()
            curr_name = current_mgr.get('manager_name', '').strip().lower()
            
            if prev_name != curr_name and curr_name:  # Ignore empty names
                change = ManagerChange(
                    location_id=current_mgr.get('location_id', ''),
                    location_name=current_mgr.get('location_name', ''),
                    location_type=current_mgr.get('location_type', 'Store'),
                    role=current_mgr.get('role', ''),
                    previous_manager=previous_mgr.get('manager_name', ''),
                    new_manager=current_mgr.get('manager_name', ''),
                    previous_email=previous_mgr.get('manager_email'),
                    new_email=current_mgr.get('manager_email'),
                    market=current_mgr.get('market'),
                    region=current_mgr.get('region')
                )
                self.changes.append(change)
        
        return self.changes
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive change report.
        
        Returns:
            Dictionary containing report data
        """
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "previous_snapshot_date": self.previous.get('date'),
            "current_snapshot_date": self.current.get('date'),
            "total_changes": len(self.changes),
            "changes_by_role": {},
            "changes": [change.to_dict() for change in self.changes]
        }
        
        # Group changes by role
        for change in self.changes:
            role = change.role
            if role not in report['changes_by_role']:
                report['changes_by_role'][role] = 0
            report['changes_by_role'][role] += 1
        
        return report
    
    def print_summary(self):
        """
        Print a human-readable summary of changes.
        """
        print("\n" + "="*60)
        print("MANAGER CHANGE DETECTION REPORT")
        print("="*60)
        print(f"Previous Snapshot: {self.previous.get('date')}")
        print(f"Current Snapshot: {self.current.get('date')}")
        print(f"Total Changes Detected: {len(self.changes)}")
        print("="*60)
        
        if not self.changes:
            print("\n[INFO] No manager changes detected.\n")
            return
        
        # Group by role
        changes_by_role = {}
        for change in self.changes:
            if change.role not in changes_by_role:
                changes_by_role[change.role] = []
            changes_by_role[change.role].append(change)
        
        # Print by role
        for role, role_changes in changes_by_role.items():
            print(f"\n[{role}] - {len(role_changes)} change(s)")
            print("-" * 60)
            for change in role_changes:
                print(f"  Location: {change.location_name} ({change.location_id})")
                print(f"  Previous: {change.previous_manager}")
                print(f"  New:      {change.new_manager}")
                if change.new_email:
                    print(f"  Email:    {change.new_email}")
                if change.market:
                    print(f"  Market:   {change.market}")
                print()
        
        print("="*60 + "\n")


def load_snapshot(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Load a snapshot from a JSON file.
    
    Args:
        filepath: Path to the JSON snapshot file
    
    Returns:
        Snapshot data as dictionary, or None if not found
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Snapshot not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {filepath}: {e}")
        return None


def save_report(report: Dict[str, Any], filepath: str):
    """
    Save change report to a JSON file.
    
    Args:
        report: Report dictionary
        filepath: Path to save the report
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] Change report: {filepath}")


if __name__ == "__main__":
    # Test the comparison logic
    print("Testing Snapshot Comparator...\n")
    
    # Create test snapshots
    yesterday = {
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "managers": [
            {
                "location_id": "05403",
                "location_name": "Store 05403",
                "location_type": "Store",
                "role": "Store Manager",
                "manager_name": "Jane Smith",
                "manager_email": "jane.smith@walmart.com",
                "market": "Market 123",
                "region": "Region 5"
            },
            {
                "location_id": "1234",
                "location_name": "DC 1234",
                "location_type": "DC",
                "role": "DC General Manager",
                "manager_name": "Bob Johnson",
                "manager_email": "bob.johnson@walmart.com"
            }
        ]
    }
    
    today = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "managers": [
            {
                "location_id": "05403",
                "location_name": "Store 05403",
                "location_type": "Store",
                "role": "Store Manager",
                "manager_name": "John Doe",  # CHANGED!
                "manager_email": "john.doe@walmart.com",
                "market": "Market 123",
                "region": "Region 5"
            },
            {
                "location_id": "1234",
                "location_name": "DC 1234",
                "location_type": "DC",
                "role": "DC General Manager",
                "manager_name": "Bob Johnson",  # No change
                "manager_email": "bob.johnson@walmart.com"
            }
        ]
    }
    
    # Compare
    comparator = SnapshotComparator(yesterday, today)
    changes = comparator.compare()
    
    # Print summary
    comparator.print_summary()
    
    # Generate report
    report = comparator.generate_report()
    print("Generated report:")
    print(json.dumps(report, indent=2))
