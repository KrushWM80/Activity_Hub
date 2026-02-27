"""
Centralized Application Settings using Pydantic Settings.

This module provides type-safe, environment-aware configuration management.
All settings can be overridden via environment variables.

Usage:
    from src.utils.settings import settings
    
    # Access settings
    api_url = settings.walmart_media_studio_api
    debug = settings.debug
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration (for future PostgreSQL migration)."""
    
    url: str = Field(
        default="sqlite:///./data/zorro.db",
        description="Database connection URL"
    )
    pool_size: int = Field(default=5, ge=1, le=20)
    max_overflow: int = Field(default=10, ge=0, le=50)
    echo: bool = Field(default=False, description="Log SQL queries")
    
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        extra="ignore"
    )


class RedisSettings(BaseSettings):
    """Redis configuration for caching and job queue."""
    
    url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    max_connections: int = Field(default=10, ge=1)
    socket_timeout: int = Field(default=5, ge=1)
    
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        extra="ignore"
    )


class WalmartMediaStudioSettings(BaseSettings):
    """Walmart Media Studio API configuration."""
    
    api_url: str = Field(
        default="https://retina-ds-genai-backend.prod.k8s.walmart.net",
        description="Media Studio API endpoint"
    )
    timeout: int = Field(default=300, ge=30, le=600)
    max_retries: int = Field(default=3, ge=0, le=10)
    ssl_verify: bool = Field(default=False, description="Enable SSL verification")
    ca_bundle: Optional[str] = Field(default=None, description="Path to CA bundle")
    
    # Circuit breaker settings
    circuit_failure_threshold: int = Field(default=5, ge=1)
    circuit_recovery_timeout: int = Field(default=60, ge=10)
    
    model_config = SettingsConfigDict(
        env_prefix="WALMART_",
        extra="ignore"
    )


class LLMSettings(BaseSettings):
    """LLM service configuration."""
    
    provider: str = Field(default="openai")
    model: str = Field(default="gpt-4-turbo-preview")
    api_key: Optional[str] = Field(default=None, description="LLM API key")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=500, ge=1)
    timeout: int = Field(default=30, ge=1)
    
    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        extra="ignore"
    )
    
    @field_validator("api_key", mode="before")
    @classmethod
    def get_api_key(cls, v):
        """Get API key from environment if not set."""
        if v:
            return v
        return os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")


class LoggingSettings(BaseSettings):
    """Logging configuration."""
    
    level: str = Field(default="INFO")
    format: str = Field(default="json", description="json or text")
    output_dir: str = Field(default="logs")
    
    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        extra="ignore"
    )


class SecuritySettings(BaseSettings):
    """Security configuration."""
    
    sso_token: Optional[str] = Field(default=None, description="Walmart SSO token")
    secret_key: str = Field(
        default="development-secret-key-change-in-production",
        description="Application secret key"
    )
    allowed_hosts: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        description="Allowed hostnames"
    )
    cors_origins: List[str] = Field(
        default=["http://localhost:8501"],
        description="CORS allowed origins"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="SECURITY_",
        extra="ignore"
    )
    
    @field_validator("sso_token", mode="before")
    @classmethod
    def get_sso_token(cls, v):
        """Get SSO token from environment if not set."""
        if v:
            return v
        return os.getenv("WALMART_SSO_TOKEN")


class Settings(BaseSettings):
    """
    Main application settings.
    
    All settings can be overridden via environment variables.
    Nested settings use their own prefixes (e.g., DATABASE_URL, REDIS_URL).
    """
    
    # Application
    app_name: str = Field(default="Zorro Video Generator")
    version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    # Base path
    base_path: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent
    )
    
    # Data directories
    data_dir: Path = Field(default=Path("data"))
    output_dir: Path = Field(default=Path("output/videos"))
    
    # Feature flags
    enable_accessibility: bool = Field(default=True)
    enable_video_editing: bool = Field(default=True)
    enable_design_studio: bool = Field(default=True)
    
    # Nested settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    walmart: WalmartMediaStudioSettings = Field(default_factory=WalmartMediaStudioSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="ZORRO_",
        extra="ignore",
        case_sensitive=False
    )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() in ("production", "prod")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment.lower() in ("development", "dev")


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are only loaded once.
    """
    return Settings()


# Global settings instance
settings = get_settings()


# Export commonly used settings for convenience
def get_database_url() -> str:
    """Get database URL."""
    return settings.database.url


def get_redis_url() -> str:
    """Get Redis URL."""
    return settings.redis.url


def is_debug() -> bool:
    """Check if debug mode is enabled."""
    return settings.debug
