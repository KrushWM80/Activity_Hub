"""Main entry point for video generation."""

import argparse
import sys
from pathlib import Path

from .core.pipeline import VideoGenerationPipeline
from .utils import get_logger, setup_logging


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Generate accessible videos from Walmart activity messages"
    )
    
    parser.add_argument(
        "message",
        help="Activity message content"
    )
    
    parser.add_argument(
        "--category",
        choices=[
            "training", "recognition", "announcement",
            "alert", "reminder", "celebration", "general"
        ],
        default="general",
        help="Message category"
    )
    
    parser.add_argument(
        "--priority",
        choices=["low", "medium", "high", "critical"],
        default="medium",
        help="Message priority"
    )
    
    parser.add_argument(
        "--provider",
        choices=["modelscope", "stability", "runwayml"],
        default="modelscope",
        help="Video generation provider"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/videos"),
        help="Output directory for generated videos"
    )
    
    parser.add_argument(
        "--no-editing",
        action="store_true",
        help="Skip video post-processing"
    )
    
    parser.add_argument(
        "--no-accessibility",
        action="store_true",
        help="Skip accessibility enhancements"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to custom configuration file"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    logger = get_logger(__name__)
    
    logger.info(
        "zorro_started",
        message=args.message[:50],
        category=args.category,
        priority=args.priority
    )
    
    try:
        # Initialize pipeline
        pipeline = VideoGenerationPipeline()
        
        # Generate video
        result = pipeline.generate(
            message_content=args.message,
            message_category=args.category,
            message_priority=args.priority,
            apply_editing=not args.no_editing,
            add_accessibility=not args.no_accessibility
        )
        
        # Print results
        print("\n✅ Video generated successfully!")
        print(f"   Video ID: {result.id}")
        print(f"   Path: {result.path}")
        print(f"   Duration: {result.duration:.2f}s")
        print(f"   Model: {result.generation_params.get('model', 'unknown')}")
        
        if result.accessibility:
            print("\n📋 Accessibility:")
            print(f"   Captions: {'✓' if result.accessibility.has_captions else '✗'}")
            print(f"   Audio Description: {'✓' if result.accessibility.has_audio_description else '✗'}")
            print(f"   WCAG Level: {result.accessibility.wcag_level}")
            
            if result.accessibility.captions_path:
                print(f"   Captions File: {result.accessibility.captions_path}")
        
        return 0
    
    except Exception as e:
        logger.error("generation_failed", error=str(e))
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
