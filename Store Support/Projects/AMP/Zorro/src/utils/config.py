"""Configuration management for Zorro video generation system."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .exceptions import ConfigurationError, InvalidConfigError, MissingConfigError

# Load environment variables
load_dotenv()


class VideoConfig(BaseModel):
    """Video generation configuration."""
    
    default_duration: int = Field(default=10, ge=1, le=60)
    default_fps: int = Field(default=24, ge=1, le=120)
    default_resolution: Dict[str, int] = Field(
        default={"width": 1920, "height": 1080}
    )
    generator: Dict[str, Any] = Field(default_factory=dict)
    output: Dict[str, Any] = Field(default_factory=dict)


class LLMConfig(BaseModel):
    """LLM service configuration."""
    
    provider: str = Field(default="openai")
    model: str = Field(default="gpt-4-turbo-preview")
    api_key_env: str = Field(default="OPENAI_API_KEY")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=500, ge=1)
    timeout: int = Field(default=30, ge=1)
    retry_attempts: int = Field(default=3, ge=0)


class AccessibilityConfig(BaseModel):
    """Accessibility features configuration."""
    
    captions: Dict[str, Any] = Field(default_factory=dict)
    audio_description: Dict[str, Any] = Field(default_factory=dict)
    visual: Dict[str, Any] = Field(default_factory=dict)


class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: str = Field(default="INFO")
    format: str = Field(default="json")
    output_dir: str = Field(default="logs")
    file_rotation: str = Field(default="1 day")


class Config(BaseModel):
    """
    Main configuration class for Zorro.
    
    This class manages all application configuration including video settings,
    LLM configuration, accessibility options, and more.
    
    Attributes:
        app: Application-level settings
        video: Video generation settings
        llm: LLM service configuration
        accessibility: Accessibility features
        logging: Logging configuration
        environment: Current environment (dev, prod, etc.)
    """
    
    app: Dict[str, Any] = Field(default_factory=dict)
    video: VideoConfig = Field(default_factory=VideoConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    accessibility: AccessibilityConfig = Field(
        default_factory=AccessibilityConfig
    )
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    message: Dict[str, Any] = Field(default_factory=dict)
    editing: Dict[str, Any] = Field(default_factory=dict)
    performance: Dict[str, Any] = Field(default_factory=dict)
    security: Dict[str, Any] = Field(default_factory=dict)
    monitoring: Dict[str, Any] = Field(default_factory=dict)
    features: Dict[str, Any] = Field(default_factory=dict)
    
    _environment: Optional[str] = None
    
    @classmethod
    def load(cls, config_path: Optional[str] = None, environment: Optional[str] = None) -> "Config":
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to configuration file. If None, uses default.
            environment: Environment name (dev, prod, etc.). If None, uses default.
        
        Returns:
            Config: Loaded configuration object
            
        Raises:
            MissingConfigError: If config file not found
            InvalidConfigError: If config file is invalid
        """
        # Determine config file path
        if config_path is None:
            base_dir = Path(__file__).parent.parent.parent
            config_dir = base_dir / "config"
            
            # Determine environment
            environment = environment or os.getenv("ZORRO_ENV", "development")
            
            # Load base config
            base_config_path = config_dir / "config.yaml"
            if not base_config_path.exists():
                raise MissingConfigError(
                    f"Base configuration file not found: {base_config_path}"
                )
            
            # Load environment-specific config
            env_config_path = config_dir / f"config.{environment}.yaml"
            
            try:
                with open(base_config_path, "r") as f:
                    config_data = yaml.safe_load(f) or {}
                
                # Merge environment-specific config if exists
                if env_config_path.exists():
                    with open(env_config_path, "r") as f:
                        env_data = yaml.safe_load(f) or {}
                    config_data = cls._merge_configs(config_data, env_data)
                
            except yaml.YAMLError as e:
                raise InvalidConfigError(f"Failed to parse config file: {e}")
            except Exception as e:
                raise ConfigurationError(f"Error loading config: {e}")
        else:
            # Load from specified path
            try:
                with open(config_path, "r") as f:
                    config_data = yaml.safe_load(f) or {}
            except FileNotFoundError:
                raise MissingConfigError(f"Config file not found: {config_path}")
            except yaml.YAMLError as e:
                raise InvalidConfigError(f"Failed to parse config file: {e}")
        
        # Create config instance
        config = cls(**config_data)
        config._environment = environment or "development"
        
        return config
    
    @staticmethod
    def _merge_configs(base: Dict, override: Dict) -> Dict:
        """
        Recursively merge override config into base config.
        
        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
        
        Returns:
            Dict: Merged configuration
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., "video.default_fps")
            default: Default value if key not found
        
        Returns:
            Any: Configuration value
            
        Example:
            >>> config.get("video.default_fps")
            24
            >>> config.get("video.generator.provider")
            "modelscope"
        """
        keys = key.split(".")
        value = self.model_dump()
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_api_key(self, service: str) -> str:
        """
        Get API key for a service from environment variables.
        
        Args:
            service: Service name (e.g., "openai", "anthropic")
        
        Returns:
            str: API key
            
        Raises:
            MissingConfigError: If API key not found
        """
        env_var_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "stability": "STABILITY_API_KEY",
            "runwayml": "RUNWAYML_API_KEY",
        }
        
        env_var = env_var_map.get(service.lower())
        if not env_var:
            raise InvalidConfigError(f"Unknown service: {service}")
        
        api_key = os.getenv(env_var)
        if not api_key:
            raise MissingConfigError(
                f"API key not found for {service}. "
                f"Please set {env_var} environment variable."
            )
        
        return api_key
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self._environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self._environment == "production"
    
    @property
    def debug_enabled(self) -> bool:
        """Check if debug mode is enabled."""
        return self.app.get("debug", False)


# Global configuration instance
_config: Optional[Config] = None


def get_config(reload: bool = False) -> Config:
    """
    Get global configuration instance (singleton pattern).
    
    Args:
        reload: Force reload configuration from file
    
    Returns:
        Config: Configuration instance
    """
    global _config
    
    if _config is None or reload:
        _config = Config.load()
    
    return _config


def set_config(config: Config) -> None:
    """
    Set global configuration instance.
    
    Args:
        config: Configuration instance to set
    """
    global _config
    _config = config
