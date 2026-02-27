"""
Advanced usage example for Zorro video generation system.

This example demonstrates:
- Complete end-to-end pipeline
- Custom configuration
- Batch processing
- Error handling
- Accessibility features
"""

import sys
from pathlib import Path
from typing import List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.message import ActivityMessage, MessageCategory, MessagePriority
from src.utils import setup_logging, get_logger


def create_sample_messages() -> List[ActivityMessage]:
    """Create a batch of sample messages for processing."""
    return [
        ActivityMessage(
            id="batch_001",
            content="URGENT: Store closing early today at 6 PM due to weather conditions",
            category=MessageCategory.ANNOUNCEMENT,
            priority=MessagePriority.URGENT,
            sender="Operations",
            target_audience="all_associates"
        ),
        ActivityMessage(
            id="batch_002",
            content="Congratulations to our team for achieving 100% customer satisfaction this week!",
            category=MessageCategory.CELEBRATION,
            priority=MessagePriority.MEDIUM,
            sender="Store Manager",
            target_audience="all_associates"
        ),
        ActivityMessage(
            id="batch_003",
            content="New AP procedures effective Monday. Please review the updated OBW guidelines.",
            category=MessageCategory.POLICY,
            priority=MessagePriority.HIGH,
            sender="Asset Protection",
            target_audience="all_associates"
        ),
        ActivityMessage(
            id="batch_004",
            content="Don't forget to schedule your PTO for the holidays. Talk to your SM or ASM.",
            category=MessageCategory.REMINDER,
            priority=MessagePriority.LOW,
            sender="HR Team",
            target_audience="all_associates"
        ),
    ]


def process_single_message(message: ActivityMessage, output_dir: Path):
    """
    Process a single message through the complete pipeline.
    
    Args:
        message: Activity message to process
        output_dir: Directory for outputs
    """
    logger = get_logger(__name__)
    
    logger.info(f"Processing message: {message.id}")
    print(f"\n{'='*60}")
    print(f"Message ID: {message.id}")
    print(f"Category: {message.category.value}")
    print(f"Priority: {message.priority.value}")
    print(f"Content: {message.content}")
    print(f"{'='*60}\n")
    
    try:
        # Step 1: Message Processing
        from src.core.message_processor import MessageProcessor
        
        processor = MessageProcessor()
        validation_result = processor.process(message)
        
        if not validation_result.is_valid:
            logger.error(f"Validation failed for {message.id}")
            for error in validation_result.errors:
                print(f"  ❌ Error: {error}")
            return None
        
        print(f"✓ Message validated and sanitized")
        if validation_result.warnings:
            for warning in validation_result.warnings:
                print(f"  ⚠️  {warning}")
        
        # Step 2: Prompt Generation
        from src.core.prompt_generator import PromptGenerator
        
        prompt_generator = PromptGenerator(fallback_enabled=True)
        prompt_result = prompt_generator.generate(
            message,
            sanitized_content=validation_result.sanitized_content
        )
        
        if not prompt_result.success:
            logger.error(f"Prompt generation failed: {prompt_result.error_message}")
            return None
        
        prompt = prompt_result.prompt
        print(f"✓ Prompt generated ({prompt_result.generation_time:.2f}s)")
        print(f"  Style: {prompt.style.value}")
        print(f"  Mood: {prompt.mood.value}")
        print(f"  Duration: {prompt.duration_hint}s")
        print(f"\n  Enhanced Prompt:\n  {prompt.enhanced_prompt}\n")
        
        # Step 3: Video Generation (simulated in this example)
        print(f"✓ Video generation would happen here")
        print(f"  Output: {output_dir / f'{message.id}.mp4'}")
        
        # Step 4: Accessibility Enhancement (simulated)
        print(f"✓ Accessibility features would be added:")
        print(f"  - Captions (WebVTT)")
        print(f"  - Audio description")
        print(f"  - High contrast overlays")
        
        logger.info(f"Successfully processed {message.id}")
        return prompt
        
    except Exception as e:
        logger.error(f"Failed to process {message.id}: {str(e)}", exc_info=True)
        print(f"  ❌ Processing failed: {str(e)}")
        return None


def main():
    """Run advanced example with batch processing."""
    
    # Setup logging
    setup_logging(level="INFO", log_format="text", output_dir="logs")
    logger = get_logger(__name__)
    
    logger.info("Starting Zorro advanced example")
    
    print("\n" + "="*60)
    print("Zorro Video Generation System - Advanced Example")
    print("="*60)
    
    # Create output directory
    output_dir = Path("output/examples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample messages
    messages = create_sample_messages()
    
    print(f"\nProcessing {len(messages)} messages...\n")
    
    # Process each message
    results = []
    successful = 0
    failed = 0
    
    for message in messages:
        result = process_single_message(message, output_dir)
        results.append(result)
        
        if result:
            successful += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("Processing Summary")
    print("="*60)
    print(f"Total messages: {len(messages)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/len(messages)*100):.1f}%")
    
    # Display all generated prompts
    print("\n" + "="*60)
    print("Generated Prompts")
    print("="*60)
    
    for i, (message, result) in enumerate(zip(messages, results), 1):
        if result:
            print(f"\n{i}. {message.id} ({message.category.value}):")
            print(f"   {result.enhanced_prompt[:100]}...")
    
    print("\n" + "="*60)
    print("Advanced example completed!")
    print("="*60)
    
    logger.info("Advanced example completed")


if __name__ == "__main__":
    main()
