"""
DC to Store Manager Configuration
Manages the mapping of Distribution Centers to Store Managers and their contact info
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

class DCStoreManagerConfig:
    """Manages DC and Store Manager data"""
    
    def __init__(self, config_path=None):
        """Initialize with config file"""
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "dc_store_managers.json"
        
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(exist_ok=True)
        
        # Load existing config or create default
        self.data = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Create default structure
            return {
                "distribution_centers": {},
                "last_updated": None
            }
    
    def _save_config(self):
        """Save configuration to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_dc(self, dc_number: str, dc_name: str = None):
        """Add a new distribution center"""
        if dc_number not in self.data["distribution_centers"]:
            self.data["distribution_centers"][dc_number] = {
                "name": dc_name or f"Distribution Center {dc_number}",
                "managers": [],
                "gms": [],
                "agms": [],
                "region": None,
                "contact_info": {}
            }
            self._save_config()
    
    def add_manager(self, dc_number: str, manager_info: dict):
        """
        Add a store manager to a DC
        
        manager_info should contain:
        {
            "name": "John Smith",
            "title": "General Manager",
            "store_number": "1234",
            "store_name": "Store 1234",
            "email": "john.smith@walmart.com",
            "phone": "555-0123",
            "market": "Dallas/Fort Worth"
        }
        """
        if dc_number not in self.data["distribution_centers"]:
            self.add_dc(dc_number)
        
        self.data["distribution_centers"][dc_number]["managers"].append(manager_info)
        
        # Also categorize by title
        title = manager_info.get('title', '').lower()
        if 'general manager' in title:
            self.data["distribution_centers"][dc_number]["gms"].append(manager_info)
        elif 'assistant' in title and 'manager' in title:
            self.data["distribution_centers"][dc_number]["agms"].append(manager_info)
        
        self._save_config()
    
    def get_managers_for_dc(self, dc_number: str) -> List[Dict]:
        """Get all managers for a specific DC"""
        if dc_number in self.data["distribution_centers"]:
            managers = self.data["distribution_centers"][dc_number].get("managers", [])
            # Sort by title and name
            return sorted(managers, key=lambda x: (x.get('title', ''), x.get('name', '')))
        return []
    
    def get_dc_info(self, dc_number: str) -> Optional[Dict]:
        """Get detailed DC information"""
        return self.data["distribution_centers"].get(dc_number)
    
    def get_all_dcs(self) -> List[str]:
        """Get list of all DC numbers"""
        return sorted(list(self.data["distribution_centers"].keys()))
    
    def update_from_snapshot(self, snapshot_data: dict):
        """
        Update store managers from a manager snapshot
        
        snapshot_data format:
        {
            "stores": [
                {
                    "store_number": "1234",
                    "store_name": "Store Name",
                    "manager_name": "John Smith",
                    "manager_email": "john.smith@walmart.com",
                    "manager_title": "Store Manager",
                    "dc": "6020",
                    "market": "Dallas"
                },
                ...
            ]
        }
        """
        if "stores" not in snapshot_data:
            return {"status": "error", "message": "Invalid snapshot format"}
        
        updated_count = 0
        
        for store in snapshot_data["stores"]:
            dc_number = store.get("dc")
            if not dc_number:
                continue
            
            # Ensure DC exists
            if dc_number not in self.data["distribution_centers"]:
                self.add_dc(dc_number)
            
            manager_info = {
                "name": store.get("manager_name"),
                "title": store.get("manager_title", "Store Manager"),
                "store_number": store.get("store_number"),
                "store_name": store.get("store_name"),
                "email": store.get("manager_email"),
                "phone": store.get("manager_phone"),
                "market": store.get("market")
            }
            
            # Check if manager already exists and update
            dc_managers = self.data["distribution_centers"][dc_number]["managers"]
            existing = [m for m in dc_managers if m.get("store_number") == store.get("store_number")]
            
            if existing:
                # Update existing
                existing[0].update(manager_info)
            else:
                # Add new
                self.add_manager(dc_number, manager_info)
                updated_count += 1
        
        from datetime import datetime
        self.data["last_updated"] = datetime.now().isoformat()
        self._save_config()
        
        return {
            "status": "success",
            "message": f"Updated {updated_count} store managers"
        }
    
    def export_json(self, output_path=None):
        """Export configuration to JSON file"""
        if output_path is None:
            output_path = Path(__file__).parent / "reports" / "dc_store_managers_export.json"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        return str(output_path)
    
    def search_managers(self, search_term: str) -> List[Dict]:
        """Search for managers by name, email, or store"""
        results = []
        search_term = search_term.lower()
        
        for dc_number, dc_info in self.data["distribution_centers"].items():
            for manager in dc_info.get("managers", []):
                if (search_term in manager.get("name", "").lower() or
                    search_term in manager.get("email", "").lower() or
                    search_term in manager.get("store_number", "").lower() or
                    search_term in manager.get("store_name", "").lower()):
                    results.append({
                        "dc": dc_number,
                        **manager
                    })
        
        return results


# Example usage
if __name__ == "__main__":
    config = DCStoreManagerConfig()
    
    # Example: Add managers
    config.add_dc("6020", "Distribution Center 6020")
    
    config.add_manager("6020", {
        "name": "Sarah Johnson",
        "title": "Store Manager",
        "store_number": "1234",
        "store_name": "Plano, TX #1234",
        "email": "sarah.johnson@walmart.com",
        "phone": "555-0100",
        "market": "Dallas/Fort Worth"
    })
    
    # Get managers
    managers = config.get_managers_for_dc("6020")
    print(f"Managers for DC 6020: {len(managers)}")
    for m in managers:
        print(f"  - {m['name']} ({m['title']}) - Store {m['store_number']}")
