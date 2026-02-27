"""
Basic usage example for Zorro video generation system.

This example demonstrates:
- Basic message processing
- Prompt generation
- Simple video generation workflow
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.message import ActivityMessage, MessageCategory, MessagePriority
from src.core.message_processor import MessageProcessor
from src.core.prompt_generator import PromptGenerator
from src.utils import setup_logging, get_logger, get_config


def main():
    """Run basic video generation example."""
    
    # Setup logging
    setup_logging(level="INFO", log_format="text")
    logger = get_logger(__name__)
    
    logger.info("Starting Zorro basic example")
    
    # Create a sample activity message
    message = ActivityMessage(
        id="example_001",
        content="Reminder: Complete your safety training CBL by Friday. "
                "This is important for maintaining our GWP standards.",
        category=MessageCategory.TRAINING,
        priority=MessagePriority.HIGH,
        sender="Safety Team",
        target_audience="all_associates"
    )
    
    logger.info(f"Created message: {message.id}")
    print(f"\nOriginal Message:\n{message.content}\n")
    
    # Step 1: Process and validate the message
    logger.info("Processing message...")
    processor = MessageProcessor()
    validation_result = processor.process(message)
    
    if not validation_result.is_valid:
        logger.error("Message validation failed")
        for error in validation_result.errors:
            print(f"Error: {error}")
        return
    
    print(f"Sanitized Message:\n{validation_result.sanitized_content}\n")
    
    if validation_result.warnings:
        print("Warnings:")
        for warning in validation_result.warnings:
            print(f"  - {warning}")
        print()
    
    # Step 2: Generate enhanced video prompt
    logger.info("Generating video prompt...")
    prompt_generator = PromptGenerator(fallback_enabled=True)
    
    prompt_result = prompt_generator.generate(
        message,
        sanitized_content=validation_result.sanitized_content
    )
    
    if not prompt_result.success:
        logger.error(f"Prompt generation failed: {prompt_result.error_message}")
        return
    
    prompt = prompt_result.prompt
    
    print(f"Enhanced Video Prompt:\n{prompt.enhanced_prompt}\n")
    print(f"Style: {prompt.style.value}")
    print(f"Mood: {prompt.mood.value}")
    print(f"Duration Hint: {prompt.duration_hint} seconds")
    print(f"Keywords: {', '.join(prompt.keywords)}")
    print(f"Negative Prompt: {prompt.negative_prompt}\n")
    
    print(f"Prompt Generation Time: {prompt_result.generation_time:.2f}s")
    print(f"LLM Model Used: {prompt_result.llm_model_used}")
    
    logger.info("Example completed successfully")
    
    # Note: Actual video generation would happen here
    # For this basic example, we stop at prompt generation
    print("\n" + "="*60)
    print("Basic example completed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Configure your LLM API key (OPENAI_API_KEY environment variable)")
    print("2. Install video generation dependencies")
    print("3. See advanced_usage.py for complete pipeline example")


if __name__ == "__main__":
    main()
