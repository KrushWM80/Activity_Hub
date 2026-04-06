"""
Service Registration Helper for Activity Hub Logic Rules Engine

This module provides utilities for the Scheduler Service to register itself
with Activity Hub and discover other services.
"""

import logging
import requests
import json
from datetime import datetime
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class ServiceRegistry:
    """Manages service registration and discovery"""
    
    def __init__(self, service_name: str, service_port: int, service_type: str = "logic-scheduler"):
        """
        Initialize service registry
        
        Args:
            service_name: Display name (e.g., "Logic Rules Engine - Scheduler")
            service_port: Port service runs on (e.g., 5011)
            service_type: Service category (e.g., "logic-scheduler", "logic-notification", "logic-task")
        """
        self.service_name = service_name
        self.service_port = service_port
        self.service_type = service_type
        self.service_url = f"http://localhost:{service_port}"
        self.api_base = f"{self.service_url}/api/v1"
        
        # Where to register (will try multiple endpoints)
        self.activity_hub_urls = [
            "http://localhost:8001",  # Projects in Stores
            "http://localhost:8002",  # Projects Data-Bridge
            "http://localhost:5001",  # V.E.T. Dashboard
        ]
    
    def register_with_hub(self) -> bool:
        """
        Register this service with Activity Hub registry
        
        Returns:
            True if registered successfully, False otherwise
        """
        registration_data = {
            "service_name": self.service_name,
            "service_type": self.service_type,
            "port": self.service_port,
            "url": self.service_url,
            "api_base": self.api_base,
            "health_endpoint": f"{self.service_url}/health",
            "registered_at": datetime.utcnow().isoformat(),
            "capabilities": self._get_capabilities()
        }
        
        # Try registering at Activity Hub
        for hub_url in self.activity_hub_urls:
            try:
                response = requests.post(
                    f"{hub_url}/api/admin/services/register",
                    json=registration_data,
                    timeout=5
                )
                if response.status_code in [200, 201]:
                    logger.info(f"✓ Registered with Activity Hub at {hub_url}")
                    return True
            except Exception as e:
                logger.debug(f"Could not register with {hub_url}: {e}")
                continue
        
        # If no Activity Hub responds, save to local registry file
        logger.warning("Could not register with Activity Hub, saving to local registry")
        self._save_local_registry(registration_data)
        return True  # Count as success (can operate standalone)
    
    def _get_capabilities(self) -> List[str]:
        """Get list of service capabilities"""
        return [
            "trigger-detection",
            "rule-evaluation",
            "notification-delivery",
            "execution-logging",
            "audit-trail"
        ]
    
    def _save_local_registry(self, registration_data: Dict) -> None:
        """Save registration to local file as fallback"""
        try:
            registry_file = f"Interface/Admin/Logic/Config/service_registry.json"
            registry = {}
            
            # Read existing registry if present
            try:
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
            except FileNotFoundError:
                pass
            
            # Add this service
            registry[self.service_type] = registration_data
            
            # Write back
            with open(registry_file, 'w') as f:
                json.dump(registry, f, indent=2)
            
            logger.info(f"✓ Saved to local registry: {registry_file}")
        except Exception as e:
            logger.error(f"Could not save local registry: {e}")
    
    def discover_services(self) -> Dict[str, Dict]:
        """
        Discover other Activity Hub services
        
        Returns:
            Dict mapping service types to service info
        """
        services = {}
        
        # Check Activity Hub endpoints
        for hub_url in self.activity_hub_urls:
            try:
                response = requests.get(
                    f"{hub_url}/api/admin/services/list",
                    timeout=5
                )
                if response.status_code == 200:
                    hub_services = response.json()
                    services.update(hub_services)
                    logger.info(f"✓ Discovered {len(hub_services)} services from {hub_url}")
                    return services
            except Exception as e:
                logger.debug(f"Could not discover from {hub_url}: {e}")
        
        # Fallback to local registry
        return self._load_local_registry()
    
    def _load_local_registry(self) -> Dict[str, Dict]:
        """Load services from local registry file"""
        try:
            registry_file = f"Interface/Admin/Logic/Config/service_registry.json"
            with open(registry_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Local registry file not found")
            return {}
    
    def healthcheck(self) -> bool:
        """Check if this service is responding"""
        try:
            response = requests.get(f"{self.service_url}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False


class ServiceDiscovery:
    """Discovers and caches Activity Hub services"""
    
    def __init__(self):
        self.services = {}
        self.last_refresh = None
    
    def get_service_url(self, service_type: str) -> Optional[str]:
        """
        Get URL for a service by type
        
        Args:
            service_type: e.g., "projects-in-stores", "vet-dashboard", "job-codes"
        
        Returns:
            Service URL or None if not found
        """
        if not self.services:
            self.refresh()
        
        service = self.services.get(service_type, {})
        return service.get('url')
    
    def refresh(self) -> None:
        """Refresh service list from Activity Hub"""
        registry = ServiceRegistry("temp", 0)
        self.services = registry.discover_services()
        self.last_refresh = datetime.utcnow()
    
    def list_services(self) -> List[str]:
        """Get list of available service types"""
        if not self.services:
            self.refresh()
        return list(self.services.keys())


# Global instance for easy access
_discovery = ServiceDiscovery()

def get_service_url(service_type: str) -> Optional[str]:
    """Get service URL by type"""
    return _discovery.get_service_url(service_type)

def list_services() -> List[str]:
    """List all available services"""
    return _discovery.list_services()

def register_scheduler_service(scheduler_instance_id: str) -> bool:
    """Convenience function to register Scheduler Service"""
    registry = ServiceRegistry(
        service_name="Activity Hub Logic Rules Engine - Scheduler",
        service_port=5011,
        service_type="logic-scheduler"
    )
    success = registry.register_with_hub()
    if success:
        logger.info(f"Scheduler Service {scheduler_instance_id} registered")
    return success
