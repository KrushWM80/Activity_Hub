"""Prompt generation module using LLM to enhance messages for video generation."""

import time
from typing import Any, Optional

from ..models.message import ActivityMessage, MessageCategory, MessagePriority
from ..models.prompt import (
    PromptGenerationResult,
    PromptMood,
    PromptStyle,
    VideoPrompt,
)
from ..utils import (
    LoggerMixin,
    get_config,
    get_logger,
    log_execution_time,
)
from ..utils.exceptions import (
    LLMServiceError,
)


class PromptGenerator(LoggerMixin):
    """
    Generates enhanced video prompts from activity messages using LLM.
    
    This class:
    - Converts activity messages into cinematic video prompts
    - Uses LLM (OpenAI, Anthropic, etc.) for enhancement
    - Maps message attributes to video style/mood
    - Provides fallback prompts for LLM failures
    - Supports passthrough mode for internal API enhancement
    
    Attributes:
        llm_service: LLM service instance (OpenAI, Anthropic, etc.)
        config: Configuration object
        fallback_enabled: Whether to use fallback prompts
        passthrough_mode: Skip external LLM, let Media Studio enhance
    
    Example:
        >>> generator = PromptGenerator()
        >>> message = ActivityMessage(
        ...     id="msg_001",
        ...     content="Complete safety training by Friday",
        ...     category="training",
        ...     sender="Safety Team"
        ... )
        >>> result = generator.generate(message)
        >>> print(result.prompt.enhanced_prompt)
    """
    
    def __init__(
        self,
        llm_service: Optional[Any] = None,
        fallback_enabled: bool = True
    ):
        """
        Initialize prompt generator.
        
        Args:
            llm_service: LLM service instance (will auto-create if None)
            fallback_enabled: Use fallback prompts on LLM failure
        """
        self.config = get_config()
        self.fallback_enabled = fallback_enabled
        
        # Check for passthrough mode (skip external LLM, use Media Studio's AI)
        self.passthrough_mode = self.config.get("llm.passthrough_mode", False)
        
        if self.passthrough_mode:
            self.logger.info(
                "PASSTHROUGH MODE ENABLED: Skipping external LLM, using Media Studio's built-in AI enhancement"
            )
            self.llm_service = None
        else:
            # Initialize LLM service
            if llm_service is None:
                from ..services.llm_service import LLMService
                self.llm_service = LLMService()
            else:
                self.llm_service = llm_service
        
        self.logger.info(
            "prompt_generator_initialized",
            llm_provider=self.config.get("llm.provider"),
            passthrough_mode=self.passthrough_mode,
            fallback_enabled=fallback_enabled
        )
    
    @log_execution_time(get_logger("PromptGenerator"))
    def generate(
        self,
        message: ActivityMessage,
        sanitized_content: Optional[str] = None
    ) -> PromptGenerationResult:
        """
        Generate enhanced video prompt from activity message.
        
        Args:
            message: Activity message to convert
            sanitized_content: Pre-sanitized content (uses message.content if None)
        
        Returns:
            PromptGenerationResult: Generation result with prompt or error
            
        Example:
            >>> result = generator.generate(message)
            >>> if result.success:
            ...     print(result.prompt.enhanced_prompt)
        """
        start_time = time.time()
        content = sanitized_content or message.content
        
        # VERBOSE LOGGING: Track prompt through enhancement
        self.logger.info("=" * 60)
        self.logger.info(f"[PROMPT GEN] Starting prompt generation")
        self.logger.info(f"[PROMPT GEN] Original content: {content[:100]}...")
        self.logger.info(f"[PROMPT GEN] Category: {message.category}, Priority: {message.priority}")
        self.logger.info(f"[PROMPT GEN] Passthrough mode: {self.passthrough_mode}")
        self.logger.info("=" * 60)
        
        self.logger.info(
            "generating_prompt",
            message_id=message.id,
            category=message.category,
            priority=message.priority
        )
        
        try:
            # Determine style and mood from message attributes
            style = self._determine_style(message)
            mood = self._determine_mood(message)
            
            self.logger.info(f"[PROMPT GEN] Determined style: {style}, mood: {mood}")
            
            # PASSTHROUGH MODE: Use original content, let Media Studio's AI enhance
            if self.passthrough_mode:
                self.logger.info("[PROMPT GEN] ✓ PASSTHROUGH MODE - Using original prompt directly")
                self.logger.info("[PROMPT GEN] Media Studio's 'enhanced_prompt: true' will enhance it")
                enhanced_prompt = content  # Pass through unchanged
            else:
                # Generate enhanced prompt using LLM
                self.logger.info("[PROMPT GEN] Calling LLM for enhancement...")
                enhanced_prompt = self._generate_with_llm(
                    content=content,
                    category=message.category,
                    priority=message.priority,
                    style=style,
                    mood=mood
                )
            
            # VERBOSE LOGGING: Log the enhanced result
            self.logger.info(f"[PROMPT GEN] Enhanced prompt: {enhanced_prompt[:150]}...")
            
            # Detect if we're using fallback (only in non-passthrough mode)
            if not self.passthrough_mode and "professional" in enhanced_prompt.lower() and len(enhanced_prompt) < 200:
                self.logger.warning(
                    "[PROMPT GEN] ⚠ POSSIBLE FALLBACK TEMPLATE DETECTED! "
                    "LLM may not be working. Check OPENAI_API_KEY."
                )
            
            # Extract keywords
            keywords = self._extract_keywords(content)
            
            # Determine duration hint
            duration_hint = self._calculate_duration_hint(content, message.priority)
            
            # Create video prompt
            prompt = VideoPrompt(
                original_message=content,
                enhanced_prompt=enhanced_prompt,
                style=style,
                mood=mood,
                keywords=keywords,
                duration_hint=duration_hint,
                negative_prompt=self._generate_negative_prompt(message.category),
                metadata={
                    "message_id": message.id,
                    "sender": message.sender,
                    "target_audience": message.target_audience,
                }
            )
            
            generation_time = time.time() - start_time
            
            # Determine model used (passthrough or actual LLM)
            model_used = "passthrough_to_media_studio" if self.passthrough_mode else self.config.get("llm.model")
            
            self.logger.info(f"[PROMPT GEN] ✓ Prompt generated in {generation_time:.2f}s")
            self.logger.info(f"[PROMPT GEN] Model used: {model_used}")
            
            result = PromptGenerationResult(
                success=True,
                prompt=prompt,
                generation_time=generation_time,
                llm_model_used=model_used,
                token_count=len(enhanced_prompt.split())  # Approximation
            )
            
            self.logger.info(
                "prompt_generated",
                message_id=message.id,
                generation_time=f"{generation_time:.2f}s",
                prompt_length=len(enhanced_prompt)
            )
            
            return result
            
        except LLMServiceError as e:
            self.logger.error(
                "llm_service_failed",
                message_id=message.id,
                error=str(e)
            )
            
            if self.fallback_enabled:
                return self._generate_fallback(message, content, start_time)
            else:
                return PromptGenerationResult(
                    success=False,
                    error_message=f"LLM service failed: {str(e)}",
                    generation_time=time.time() - start_time
                )
        
        except Exception as e:
            self.logger.error(
                "prompt_generation_failed",
                message_id=message.id,
                error=str(e),
                exc_info=True
            )
            
            return PromptGenerationResult(
                success=False,
                error_message=str(e),
                generation_time=time.time() - start_time
            )
    
    def _generate_with_llm(
        self,
        content: str,
        category: MessageCategory,
        priority: MessagePriority,
        style: PromptStyle,
        mood: PromptMood
    ) -> str:
        """
        Generate enhanced prompt using LLM.
        
        Args:
            content: Message content
            category: Message category
            priority: Message priority
            style: Video style
            mood: Video mood
        
        Returns:
            str: Enhanced prompt
        """
        # Build prompt for LLM
        system_prompt = self.config.get(
            "llm.system_prompt",
            "You are an expert at creating video generation prompts."
        )
        
        user_prompt = f"""Convert this Walmart activity message into a detailed video generation prompt:

Message: {content}
Category: {category.value}
Priority: {priority.value}
Desired Style: {style.value}
Desired Mood: {mood.value}

Create a vivid, cinematic prompt that:
1. Describes the visual scene in detail (2-3 sentences)
2. Is appropriate for a professional workplace
3. Emphasizes the key message
4. Uses inclusive, accessible language
5. Maintains Walmart brand values

Respond with ONLY the enhanced prompt, no explanations."""
        
        # Call LLM service
        enhanced_prompt = self.llm_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=self.config.get("llm.max_tokens", 500),
            temperature=self.config.get("llm.temperature", 0.7)
        )
        
        return enhanced_prompt.strip()
    
    def _generate_fallback(
        self,
        message: ActivityMessage,
        content: str,
        start_time: float
    ) -> PromptGenerationResult:
        """
        Generate fallback prompt when LLM fails.
        
        Args:
            message: Original message
            content: Message content
            start_time: Generation start time
        
        Returns:
            PromptGenerationResult: Fallback result
        """
        # VERBOSE WARNING: This means LLM is not working!
        self.logger.warning("=" * 60)
        self.logger.warning("[FALLBACK] ⚠️ USING FALLBACK TEMPLATE - LLM NOT WORKING!")
        self.logger.warning("[FALLBACK] Your specific prompt will NOT be properly enhanced!")
        self.logger.warning("[FALLBACK] Video may not match your input!")
        self.logger.warning("[FALLBACK] Fix: Configure OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        self.logger.warning("=" * 60)
        
        self.logger.warning(
            "using_fallback_prompt",
            message_id=message.id
        )
        
        # Simple template-based fallback
        category_visuals = {
            MessageCategory.SAFETY: "a clean, well-lit Walmart store environment with safety equipment visible",
            MessageCategory.TRAINING: "a professional training area with associates learning on digital tablets",
            MessageCategory.ANNOUNCEMENT: "a modern Walmart store interior with clear signage",
            MessageCategory.REMINDER: "a friendly store associate checking a digital device",
            MessageCategory.CELEBRATION: "excited associates celebrating in a vibrant Walmart store",
            MessageCategory.POLICY: "a professional office setting with clear documentation",
            MessageCategory.OPERATIONAL: "an efficient Walmart store operation in progress",
        }
        
        visual = category_visuals.get(
            message.category,
            "a professional Walmart store environment"
        )
        
        enhanced_prompt = f"{visual}, {content.lower()}, professional lighting, corporate setting"
        
        self.logger.warning(f"[FALLBACK] Generated generic prompt: {enhanced_prompt[:100]}...")
        
        prompt = VideoPrompt(
            original_message=content,
            enhanced_prompt=enhanced_prompt,
            style=self._determine_style(message),
            mood=self._determine_mood(message),
            keywords=self._extract_keywords(content),
            duration_hint=self._calculate_duration_hint(content, message.priority),
            metadata={"fallback": True, "message_id": message.id}
        )
        
        return PromptGenerationResult(
            success=True,
            prompt=prompt,
            generation_time=time.time() - start_time,
            llm_model_used="fallback_template"
        )
    
    def _determine_style(self, message: ActivityMessage) -> PromptStyle:
        """Determine video style from message attributes."""
        style_map = {
            MessageCategory.SAFETY: PromptStyle.PROFESSIONAL,
            MessageCategory.TRAINING: PromptStyle.PROFESSIONAL,
            MessageCategory.ANNOUNCEMENT: PromptStyle.PROFESSIONAL,
            MessageCategory.REMINDER: PromptStyle.CASUAL,
            MessageCategory.CELEBRATION: PromptStyle.ENERGETIC,
            MessageCategory.POLICY: PromptStyle.PROFESSIONAL,
            MessageCategory.OPERATIONAL: PromptStyle.PROFESSIONAL,
        }
        return style_map.get(message.category, PromptStyle.PROFESSIONAL)
    
    def _determine_mood(self, message: ActivityMessage) -> PromptMood:
        """Determine video mood from message attributes."""
        # Priority-based mood
        if message.priority == MessagePriority.URGENT:
            return PromptMood.URGENT
        
        # Category-based mood
        mood_map = {
            MessageCategory.SAFETY: PromptMood.SERIOUS,
            MessageCategory.TRAINING: PromptMood.INFORMATIVE,
            MessageCategory.ANNOUNCEMENT: PromptMood.INFORMATIVE,
            MessageCategory.REMINDER: PromptMood.FRIENDLY,
            MessageCategory.CELEBRATION: PromptMood.CELEBRATORY,
            MessageCategory.POLICY: PromptMood.SERIOUS,
            MessageCategory.OPERATIONAL: PromptMood.INFORMATIVE,
        }
        return mood_map.get(message.category, PromptMood.INFORMATIVE)
    
    def _extract_keywords(self, content: str) -> list:
        """Extract key terms from content."""
        # Simple keyword extraction (can be enhanced with NLP)
        words = content.lower().split()
        
        # Common words to exclude
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'by', 'your', 'is', 'are'}
        
        keywords = [word.strip('.,!?') for word in words if word not in stop_words and len(word) > 3]
        
        # Return unique keywords, limit to top 5
        return list(dict.fromkeys(keywords))[:5]
    
    def _calculate_duration_hint(self, content: str, priority: MessagePriority) -> int:
        """Calculate suggested video duration."""
        # Base duration on content length
        word_count = len(content.split())
        
        if word_count < 10:
            base_duration = 5
        elif word_count < 20:
            base_duration = 8
        elif word_count < 30:
            base_duration = 10
        else:
            base_duration = 12
        
        # Adjust for priority
        if priority == MessagePriority.URGENT:
            base_duration = max(5, base_duration - 2)
        
        return min(base_duration, 15)  # Cap at 15 seconds
    
    def _generate_negative_prompt(self, category: MessageCategory) -> str:
        """Generate negative prompt (what to avoid).
        
        Note: Include office/corporate environment exclusions to prevent
        the model from bleeding in office backgrounds when retail scenes
        are requested.
        """
        # Base exclusions for quality + office environment bleeding
        base_negative = (
            "blurry, low quality, distorted, unprofessional, dark, messy, "
            "office cubicle, office desk, computer monitors, office workers, "
            "corporate office, office building interior, cubicle farm, "
            "office chairs, conference room, business suits"
        )
        
        category_negatives = {
            MessageCategory.SAFETY: f"{base_negative}, unsafe conditions, hazards, accidents",
            MessageCategory.TRAINING: f"{base_negative}, confusion, disorder, empty room",
            MessageCategory.CELEBRATION: f"{base_negative}, sad, boring, empty, lonely",
            MessageCategory.OPERATIONAL: f"{base_negative}, empty shelves, closed store",
            MessageCategory.ANNOUNCEMENT: f"{base_negative}, unclear signage, empty store",
        }
        
        return category_negatives.get(category, base_negative)
