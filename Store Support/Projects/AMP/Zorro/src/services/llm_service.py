"""LLM service for prompt generation using OpenAI, Anthropic, or other providers."""

import time
from typing import Any, Dict, Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ..utils import LoggerMixin, get_config
from ..utils.exceptions import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMServiceError,
    LLMTimeoutError,
)


class LLMService(LoggerMixin):
    """
    Service for interacting with Large Language Models.
    
    Supports:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Azure OpenAI
    - Automatic retries with exponential backoff
    - Rate limiting
    - Error handling
    
    Example:
        >>> service = LLMService()
        >>> response = service.generate(
        ...     system_prompt="You are helpful",
        ...     user_prompt="Write a video prompt"
        ... )
    """
    
    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize LLM service.
        
        Args:
            provider: LLM provider ("openai", "anthropic", "azure")
            api_key: API key (uses environment variable if None)
        """
        self.config = get_config()
        self.provider = provider or self.config.get("llm.provider", "openai")
        self.model = self.config.get("llm.model", "gpt-4-turbo-preview")
        
        # Get API key
        if api_key:
            self.api_key = api_key
        else:
            try:
                self.api_key = self.config.get_api_key(self.provider)
            except Exception as e:
                self.logger.warning(
                    "api_key_not_configured",
                    provider=self.provider,
                    error=str(e)
                )
                self.api_key = None
        
        # Initialize client based on provider
        self.client = self._initialize_client()
        
        self.logger.info(
            "llm_service_initialized",
            provider=self.provider,
            model=self.model,
            api_key_configured=self.api_key is not None
        )
    
    def _initialize_client(self) -> Any:
        """Initialize the appropriate LLM client."""
        if self.provider == "openai":
            try:
                import openai
                if self.api_key:
                    return openai.OpenAI(api_key=self.api_key)
                else:
                    self.logger.warning("openai_client_not_initialized_no_api_key")
                    return None
            except ImportError:
                self.logger.error("openai_package_not_installed")
                return None
        
        elif self.provider == "anthropic":
            try:
                import anthropic
                if self.api_key:
                    return anthropic.Anthropic(api_key=self.api_key)
                else:
                    self.logger.warning("anthropic_client_not_initialized_no_api_key")
                    return None
            except ImportError:
                self.logger.error("anthropic_package_not_installed")
                return None
        
        else:
            self.logger.warning("unsupported_provider", provider=self.provider)
            return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(LLMRateLimitError),
        reraise=True
    )
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            system_prompt: System/context prompt
            user_prompt: User query/request
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-2)
            **kwargs: Additional provider-specific parameters
        
        Returns:
            str: Generated text
            
        Raises:
            LLMServiceError: On generation failure
            LLMTimeoutError: On timeout
            LLMRateLimitError: On rate limit
            
        Example:
            >>> response = service.generate(
            ...     system_prompt="You are an expert",
            ...     user_prompt="Create a video prompt"
            ... )
        """
        if not self.client:
            raise LLMServiceError(
                "LLM client not initialized. Check API key configuration."
            )
        
        max_tokens = max_tokens or self.config.get("llm.max_tokens", 500)
        temperature = temperature if temperature is not None else self.config.get("llm.temperature", 0.7)
        timeout = self.config.get("llm.timeout", 30)
        
        self.logger.debug(
            "generating_text",
            provider=self.provider,
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        start_time = time.time()
        
        try:
            if self.provider == "openai":
                response = self._generate_openai(
                    system_prompt,
                    user_prompt,
                    max_tokens,
                    temperature,
                    timeout
                )
            elif self.provider == "anthropic":
                response = self._generate_anthropic(
                    system_prompt,
                    user_prompt,
                    max_tokens,
                    temperature,
                    timeout
                )
            else:
                raise LLMServiceError(f"Unsupported provider: {self.provider}")
            
            generation_time = time.time() - start_time
            
            self.logger.info(
                "text_generated",
                provider=self.provider,
                generation_time=f"{generation_time:.2f}s",
                response_length=len(response)
            )
            
            return response
            
        except Exception as e:
            generation_time = time.time() - start_time
            self.logger.error(
                "generation_failed",
                provider=self.provider,
                error=str(e),
                generation_time=f"{generation_time:.2f}s",
                exc_info=True
            )
            raise
    
    def _generate_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
        timeout: int
    ) -> str:
        """Generate using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_str = str(e).lower()
            
            if "rate" in error_str or "429" in error_str:
                raise LLMRateLimitError(f"OpenAI rate limit exceeded: {e}")
            elif "timeout" in error_str:
                raise LLMTimeoutError(f"OpenAI request timed out: {e}")
            elif "auth" in error_str or "401" in error_str:
                raise LLMAuthenticationError(f"OpenAI authentication failed: {e}")
            else:
                raise LLMServiceError(f"OpenAI request failed: {e}")
    
    def _generate_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
        timeout: int
    ) -> str:
        """Generate using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
            
            return response.content[0].text
            
        except Exception as e:
            error_str = str(e).lower()
            
            if "rate" in error_str or "429" in error_str:
                raise LLMRateLimitError(f"Anthropic rate limit exceeded: {e}")
            elif "timeout" in error_str:
                raise LLMTimeoutError(f"Anthropic request timed out: {e}")
            elif "auth" in error_str or "401" in error_str:
                raise LLMAuthenticationError(f"Anthropic authentication failed: {e}")
            else:
                raise LLMServiceError(f"Anthropic request failed: {e}")
    
    def is_available(self) -> bool:
        """
        Check if LLM service is available.
        
        Returns:
            bool: True if service is configured and ready
        """
        return self.client is not None and self.api_key is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.
        
        Returns:
            dict: Model configuration info
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "available": self.is_available(),
            "max_tokens": self.config.get("llm.max_tokens"),
            "temperature": self.config.get("llm.temperature"),
        }
