#!/usr/bin/env python3
"""
OneDrive Helper Module
Handles all OneDrive operations via Microsoft Graph msgraph agent.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import config


class OneDriveHelper:
    """
    Helper class to interact with OneDrive via the msgraph Code Puppy agent.
    """
    
    def __init__(self, folder_name: str = config.ONEDRIVE_FOLDER):
        self.folder_name = folder_name
        self.folder_path = None
    
    def _invoke_msgraph(self, prompt: str) -> str:
        """
        Invoke the msgraph agent via Code Puppy.
        For now, this is a placeholder - in production we'll use the actual agent.
        """
        # This will be replaced with actual msgraph agent invocation
        # For now, return a mock response
        print(f"[ONEDRIVE] Would invoke msgraph: {prompt}")
        return "Success"
    
    def ensure_folder_exists(self) -> bool:
        """
        Ensure the ManagerSnapshots folder exists in OneDrive.
        Returns True if folder exists or was created.
        """
        prompt = f"""
        Check if a folder named '{self.folder_name}' exists in my OneDrive root directory.
        If it doesn't exist, create it.
        Return the folder ID or path.
        """
        
        try:
            result = self._invoke_msgraph(prompt)
            print(f"[ONEDRIVE] Folder '{self.folder_name}' is ready")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to ensure folder exists: {e}")
            return False
    
    def upload_snapshot(self, snapshot_data: Dict[str, Any], date: str = None) -> bool:
        """
        Upload a snapshot to OneDrive.
        
        Args:
            snapshot_data: Dictionary containing the snapshot data
            date: Date string (YYYY-MM-DD), defaults to today
        
        Returns:
            True if upload successful
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        filename = config.SNAPSHOT_FILENAME_PATTERN.format(date=date)
        filepath = f"{self.folder_name}/{filename}"
        
        # Convert snapshot to JSON string
        json_content = json.dumps(snapshot_data, indent=2, ensure_ascii=False)
        
        prompt = f"""
        Upload a file to my OneDrive at path '{filepath}'.
        The content is a JSON file with the following data:
        {json_content}
        
        If a file with this name already exists, overwrite it.
        """
        
        try:
            result = self._invoke_msgraph(prompt)
            print(f"[ONEDRIVE] Uploaded snapshot: {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to upload snapshot: {e}")
            return False
    
    def download_snapshot(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Download a snapshot from OneDrive.
        
        Args:
            date: Date string (YYYY-MM-DD)
        
        Returns:
            Snapshot data as dictionary, or None if not found
        """
        filename = config.SNAPSHOT_FILENAME_PATTERN.format(date=date)
        filepath = f"{self.folder_name}/{filename}"
        
        prompt = f"""
        Download the file at path '{filepath}' from my OneDrive.
        Return the full content of the file.
        """
        
        try:
            result = self._invoke_msgraph(prompt)
            # Parse JSON content from result
            # For now, return None (will implement parsing later)
            print(f"[ONEDRIVE] Downloaded snapshot: {filepath}")
            return None
        except Exception as e:
            print(f"[ERROR] Failed to download snapshot: {e}")
            return None
    
    def list_snapshots(self) -> list:
        """
        List all snapshot files in OneDrive folder.
        
        Returns:
            List of snapshot filenames
        """
        prompt = f"""
        List all files in the '{self.folder_name}' folder in my OneDrive.
        Filter for JSON files only.
        Return the list of filenames with their modification dates.
        """
        
        try:
            result = self._invoke_msgraph(prompt)
            print(f"[ONEDRIVE] Listed snapshots in {self.folder_name}")
            return []
        except Exception as e:
            print(f"[ERROR] Failed to list snapshots: {e}")
            return []
    
    def save_locally(self, snapshot_data: Dict[str, Any], date: str = None) -> Path:
        """
        Save snapshot locally as fallback.
        
        Args:
            snapshot_data: Dictionary containing the snapshot data
            date: Date string (YYYY-MM-DD), defaults to today
        
        Returns:
            Path to saved file
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Create local snapshots directory
        local_dir = Path("snapshots_local")
        local_dir.mkdir(exist_ok=True)
        
        filename = config.SNAPSHOT_FILENAME_PATTERN.format(date=date)
        filepath = local_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(snapshot_data, f, indent=2, ensure_ascii=False)
        
        print(f"[LOCAL] Saved snapshot: {filepath}")
        return filepath
    
    def load_local(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Load snapshot from local storage.
        
        Args:
            date: Date string (YYYY-MM-DD)
        
        Returns:
            Snapshot data as dictionary, or None if not found
        """
        local_dir = Path("snapshots_local")
        filename = config.SNAPSHOT_FILENAME_PATTERN.format(date=date)
        filepath = local_dir / filename
        
        if not filepath.exists():
            print(f"[LOCAL] Snapshot not found: {filepath}")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"[LOCAL] Loaded snapshot: {filepath}")
        return data


if __name__ == "__main__":
    # Test OneDrive helper
    print("Testing OneDrive Helper...\n")
    
    helper = OneDriveHelper()
    
    # Test data
    test_snapshot = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "managers": [
            {
                "location": "Store 1234",
                "role": "Store Manager",
                "name": "John Doe",
                "email": "john.doe@walmart.com"
            }
        ]
    }
    
    # Test local save/load
    print("Testing local save/load...")
    saved_path = helper.save_locally(test_snapshot)
    loaded_data = helper.load_local(datetime.now().strftime("%Y-%m-%d"))
    print(f"Loaded data: {loaded_data}\n")
    
    print("OneDrive Helper test complete!")
