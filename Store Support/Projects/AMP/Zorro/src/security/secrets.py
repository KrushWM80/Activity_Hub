"""Secret management using Azure Key Vault."""

import os
from typing import Optional, Dict
from functools import lru_cache

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from ..utils import get_logger

logger = get_logger(__name__)


class SecretManager:
    """
    Manage secrets with Azure Key Vault fallback to environment variables.
    
    Production: Uses Azure Key Vault
    Development: Falls back to .env file
    
    Example:
        >>> secrets = SecretManager()
        >>> api_key = secrets.get_secret("openai-api-key")
    """
    
    def __init__(self, vault_url: Optional[str] = None):
        """
        Initialize secret manager.
        
        Args:
            vault_url: Azure Key Vault URL (uses AZURE_VAULT_URL env if None)
        """
        self.environment = os.getenv("ZORRO_ENV", "development")
        self.vault_url = vault_url or os.getenv("AZURE_VAULT_URL")
        self.client: Optional[SecretClient] = None
        
        if self.environment == "production" and not self.vault_url:
            logger.error(
                "azure_vault_required",
                message="AZURE_VAULT_URL required in production"
            )
            raise ValueError(
                "AZURE_VAULT_URL environment variable required in production. "
                "Set to your Azure Key Vault URL."
            )
        
        if self.vault_url and AZURE_AVAILABLE:
            try:
                credential = DefaultAzureCredential()
                self.client = SecretClient(
                    vault_url=self.vault_url,
                    credential=credential
                )
                logger.info("azure_vault_initialized", vault_url=self.vault_url)
            except Exception as e:
                logger.warning(
                    "azure_vault_init_failed",
                    error=str(e),
                    fallback="environment_variables"
                )
                self.client = None
        else:
            if self.environment == "production":
                raise ValueError(
                    "azure-identity and azure-keyvault-secrets packages required. "
                    "Install with: pip install azure-identity azure-keyvault-secrets"
                )
            logger.info(
                "secret_manager_fallback",
                mode="environment_variables",
                environment=self.environment
            )
    
    def get_secret(self, secret_name: str, default: Optional[str] = None) -> str:
        """
        Fetch secret from Key Vault or environment.
        
        Args:
            secret_name: Secret name (use hyphens, e.g., "openai-api-key")
            default: Default value if not found
            
        Returns:
            str: Secret value
            
        Raises:
            ValueError: If secret not found and no default provided
        """
        # Try Azure Key Vault first
        if self.client:
            try:
                secret = self.client.get_secret(secret_name)
                logger.debug("secret_retrieved_from_vault", secret_name=secret_name)
                return secret.value
            except Exception as e:
                logger.warning(
                    "vault_secret_not_found",
                    secret_name=secret_name,
                    error=str(e)
                )
        
        # Fallback to environment variable
        env_name = secret_name.upper().replace("-", "_")
        value = os.getenv(env_name, default)
        
        if value is None:
            raise ValueError(
                f"Secret '{secret_name}' not found in Key Vault or environment. "
                f"Set {env_name} environment variable or add to Key Vault."
            )
        
        logger.debug("secret_retrieved_from_env", secret_name=secret_name)
        return value
    
    def get_all_secrets(self, prefix: str = "") -> Dict[str, str]:
        """
        Fetch all secrets matching prefix.
        
        Args:
            prefix: Secret name prefix filter
            
        Returns:
            Dict[str, str]: Secret name to value mapping
        """
        secrets = {}
        
        if self.client:
            try:
                for secret_property in self.client.list_properties_of_secrets():
                    if prefix and not secret_property.name.startswith(prefix):
                        continue
                    try:
                        secret = self.client.get_secret(secret_property.name)
                        secrets[secret_property.name] = secret.value
                    except Exception:
                        pass
            except Exception as e:
                logger.error("failed_to_list_secrets", error=str(e))
        
        return secrets


# Global instance
_secret_manager: Optional[SecretManager] = None


@lru_cache(maxsize=None)
def get_secret(secret_name: str, default: Optional[str] = None) -> str:
    """
    Global function to get secrets (cached).
    
    Args:
        secret_name: Secret name
        default: Default value
        
    Returns:
        str: Secret value
        
    Example:
        >>> from src.security import get_secret
        >>> api_key = get_secret("openai-api-key")
    """
    global _secret_manager
    
    if _secret_manager is None:
        _secret_manager = SecretManager()
    
    return _secret_manager.get_secret(secret_name, default)
