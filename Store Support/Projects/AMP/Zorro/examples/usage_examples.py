"""Example usage of the video generation pipeline."""

from src.core.pipeline import VideoGenerationPipeline
from src.utils import setup_logging


def example_basic_generation():
    """Basic example: Generate a single video."""
    print("=" * 60)
    print("Example 1: Basic Video Generation")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = VideoGenerationPipeline()
    
    # Generate video
    result = pipeline.generate(
        message_content="Complete your annual safety training by Friday",
        message_category="training",
        message_priority="high"
    )
    
    print(f"✅ Generated: {result.path}")
    print(f"   Duration: {result.duration:.2f}s")
    print(f"   Captions: {result.accessibility.captions_path}")
    print()


def example_recognition_message():
    """Example: Recognition message with celebration style."""
    print("=" * 60)
    print("Example 2: Recognition Message")
    print("=" * 60)
    
    pipeline = VideoGenerationPipeline()
    
    result = pipeline.generate(
        message_content="Congratulations on achieving 100% customer satisfaction this quarter!",
        message_category="recognition",
        message_priority="high"
    )
    
    print(f"✅ Generated: {result.path}")
    print(f"   Style: {result.prompt_used}")
    print()


def example_batch_generation():
    """Example: Generate multiple videos in batch."""
    print("=" * 60)
    print("Example 3: Batch Generation")
    print("=" * 60)
    
    pipeline = VideoGenerationPipeline()
    
    messages = [
        {
            "message_content": "New inventory system training available",
            "message_category": "training",
            "message_priority": "medium"
        },
        {
            "message_content": "Great work on your customer service scores!",
            "message_category": "recognition",
            "message_priority": "high"
        },
        {
            "message_content": "Reminder: Complete your OBW assessment",
            "message_category": "reminder",
            "message_priority": "medium"
        }
    ]
    
    results = pipeline.generate_batch(messages)
    
    print(f"✅ Generated {len(results)} videos:")
    for i, video in enumerate(results, 1):
        print(f"   {i}. {video.path}")
    print()


def example_with_walmart_abbreviations():
    """Example: Message with Walmart abbreviations."""
    print("=" * 60)
    print("Example 4: Walmart Abbreviations")
    print("=" * 60)
    
    pipeline = VideoGenerationPipeline()
    
    result = pipeline.generate(
        message_content="Review CBL modules for GWP compliance and OBW standards",
        message_category="training",
        message_priority="high"
    )
    
    print(f"✅ Generated: {result.path}")
    print("   Message processor automatically expanded:")
    print("   - CBL → Computer Based Learning")
    print("   - GWP → Great Workplace")
    print("   - OBW → One Best Way")
    print()


def example_alert_message():
    """Example: Critical alert with urgent styling."""
    print("=" * 60)
    print("Example 5: Critical Alert")
    print("=" * 60)
    
    pipeline = VideoGenerationPipeline()
    
    result = pipeline.generate(
        message_content="Emergency evacuation drill scheduled for 2 PM today",
        message_category="alert",
        message_priority="critical"
    )
    
    print(f"✅ Generated: {result.path}")
    print(f"   Priority: Critical")
    print(f"   Enhanced with urgent visual style")
    print()


def example_custom_editing():
    """Example: Custom video editing options."""
    print("=" * 60)
    print("Example 6: Custom Video Editing")
    print("=" * 60)
    
    pipeline = VideoGenerationPipeline()
    
    result = pipeline.generate(
        message_content="Thank you for your dedication to customer service",
        message_category="recognition",
        message_priority="medium",
        apply_editing=True,
        add_fade=True,
        trim_duration=8.0
    )
    
    print(f"✅ Generated: {result.path}")
    print(f"   Applied fade transitions")
    print(f"   Trimmed to 8 seconds")
    print()


def example_accessibility_features():
    """Example: Accessibility features demonstration."""
    print("=" * 60)
    print("Example 7: Accessibility Features")
    print("=" * 60)
    
    pipeline = VideoGenerationPipeline()
    
    result = pipeline.generate(
        message_content="Join us for the team building event this Friday at 3 PM",
        message_category="announcement",
        message_priority="medium",
        add_accessibility=True
    )
    
    print(f"✅ Generated: {result.path}")
    print(f"\n📋 Accessibility Features:")
    print(f"   - WebVTT Captions: {result.accessibility.captions_path}")
    print(f"   - Audio Description: {result.accessibility.audio_description_path}")
    print(f"   - Transcript: {result.accessibility.transcript_path}")
    print(f"   - WCAG Level: {result.accessibility.wcag_level}")
    print(f"   - Screen Reader Compatible: {result.accessibility.screen_reader_compatible}")
    print()


def main():
    """Run all examples."""
    # Setup logging
    setup_logging(level="INFO")
    
    print("\n" + "=" * 60)
    print("Walmart Activity Message Video Generation - Examples")
    print("=" * 60)
    print()
    
    try:
        # Run examples
        example_basic_generation()
        example_recognition_message()
        example_with_walmart_abbreviations()
        example_alert_message()
        example_custom_editing()
        example_accessibility_features()
        example_batch_generation()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        raise


if __name__ == "__main__":
    main()
