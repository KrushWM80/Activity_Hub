"""SSL/TLS configuration management."""

import os
import warnings
from pathlib import Path
from typing import Union, Dict, Any

from ..utils import get_logger

logger = get_logger(__name__)


class SSLConfiguration:
    """
    Manage SSL/TLS settings per environment.
    
    Production: Requires valid CA certificate
    Staging: Recommended to use CA certificate
    Development: Can disable for internal network
    
    Example:
        >>> ssl = SSLConfiguration()
        >>> requests.get(url, **ssl.get_requests_kwargs())
    """
    
    def __init__(self):
        """Initialize SSL configuration."""
        self.environment = os.getenv("ZORRO_ENV", "development")
        self.ca_bundle = os.getenv("WALMART_CA_BUNDLE")
        self.ssl_verify = self._determine_ssl_verify()
        
        logger.info(
            "ssl_config_initialized",
            environment=self.environment,
            ssl_verify=str(self.ssl_verify),
            ca_bundle=self.ca_bundle or "None"
        )
    
    def _determine_ssl_verify(self) -> Union[bool, str]:
        """
        Determine SSL verification setting based on environment.
        
        Returns:
            Union[bool, str]: True, False, or path to CA bundle
            
        Raises:
            ValueError: If production requires CA bundle but not provided
        """
        # Check explicit SSL_VERIFY setting
        ssl_verify_env = os.getenv("WALMART_SSL_VERIFY", "").lower()
        
        if self.environment == "production":
            # Production MUST verify SSL
            if ssl_verify_env == "false":
                raise ValueError(
                    "SSL verification cannot be disabled in production. "
                    "Remove WALMART_SSL_VERIFY=false or change ZORRO_ENV."
                )
            
            # Require CA bundle in production
            if not self.ca_bundle:
                logger.warning(
                    "production_ssl_warning",
                    message="WALMART_CA_BUNDLE not set, using system certificates"
                )
                return True
            
            # Validate CA bundle exists
            ca_path = Path(self.ca_bundle)
            if not ca_path.exists():
                raise ValueError(
                    f"CA bundle not found: {self.ca_bundle}\n"
                    "Verify WALMART_CA_BUNDLE path is correct."
                )
            
            logger.info("ssl_ca_bundle_loaded", path=self.ca_bundle)
            return str(ca_path)
        
        elif self.environment == "staging":
            # Staging should verify but can be disabled
            if ssl_verify_env == "false":
                warnings.warn(
                    "SSL verification disabled in staging. "
                    "Enable for production readiness testing."
                )
                return False
            
            if self.ca_bundle and Path(self.ca_bundle).exists():
                return self.ca_bundle
            
            logger.warning(
                "staging_ssl_not_configured",
                message="Using default SSL verification"
            )
            return True
        
        else:  # development
            # Development can disable for internal Walmart network
            if ssl_verify_env == "false":
                logger.info(
                    "ssl_disabled_development",
                    message="Acceptable for internal network only"
                )
                return False
            
            # Use CA bundle if provided
            if self.ca_bundle and Path(self.ca_bundle).exists():
                return self.ca_bundle
            
            return True
    
    def get_requests_kwargs(self) -> Dict[str, Any]:
        """
        Get kwargs for requests.get/post/etc.
        
        Returns:
            Dict with 'verify' and 'timeout' keys
            
        Example:
            >>> kwargs = ssl_config.get_requests_kwargs()
            >>> response = requests.get(url, **kwargs)
        """
        return {
            "verify": self.ssl_verify,
            "timeout": int(os.getenv("REQUEST_TIMEOUT", "30"))
        }
    
    def validate_certificate(self, cert_path: str) -> bool:
        """
        Validate that a certificate can be loaded.
        
        Args:
            cert_path: Path to certificate file
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If certificate invalid
        """
        try:
            import ssl
            ssl.create_default_context(cafile=cert_path)
            logger.info("certificate_validated", path=cert_path)
            return True
        except Exception as e:
            raise ValueError(f"Invalid certificate: {str(e)}")
    
    @property
    def is_secure(self) -> bool:
        """Check if SSL verification is enabled."""
        return self.ssl_verify is not False


# Global SSL configuration instance
ssl_config = SSLConfiguration()
