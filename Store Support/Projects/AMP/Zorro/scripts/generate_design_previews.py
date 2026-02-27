"""Generate preview images for existing design elements."""

import sys
from pathlib import Path
import subprocess

# Add parent to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.services.design_studio_service import DesignStudioService
from src.core.pipeline import VideoGenerationPipeline
from src.models.design_element import DesignElementType


def extract_thumbnail(video_path: str, output_path: str) -> bool:
    """Extract first frame from video as thumbnail."""
    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", "00:00:00.000",
            "-vframes", "1",
            "-vf", "scale=400:300",
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Could not extract thumbnail: {e}")
        return False


def generate_preview_for_element(service, element, pipeline):
    """Generate preview image for a design element."""
    
    # Skip if already has visual reference
    if element.visual_reference_path and Path(element.visual_reference_path).exists():
        print(f"⏭️  Skipping {element.name} (already has preview)")
        return
    
    print(f"\n🎬 Generating preview for: {element.name}")
    
    try:
        # Generate test video using the element's prompt
        test_message = f"Test video for {element.name}"
        
        result = pipeline.generate(
            message_content=test_message,
            message_category="training",
            message_priority="medium",
            apply_editing=True,
            add_accessibility=False,
            trim_duration=5
        )
        
        if result and result.path and Path(result.path).exists():
            # Create assets directory
            assets_dir = Path("design_assets")
            assets_dir.mkdir(exist_ok=True)
            
            # Generate thumbnail path
            thumbnail_path = assets_dir / f"{element.type.value}_{element.name.lower().replace(' ', '_')}_thumb.png"
            
            # Extract thumbnail
            if extract_thumbnail(result.path, str(thumbnail_path)):
                # Update element with visual reference
                service.update_element(
                    element.id,
                    visual_reference_path=str(thumbnail_path)
                )
                print(f"✅ Preview saved: {thumbnail_path}")
                return True
            else:
                print(f"⚠️  Failed to extract thumbnail")
                return False
        else:
            print(f"⚠️  Video generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error generating preview: {e}")
        return False


def generate_all_previews():
    """Generate previews for all elements without them."""
    
    print("🎨 Design Element Preview Generator")
    print("=" * 60)
    
    service = DesignStudioService()
    pipeline = VideoGenerationPipeline()
    
    # Get all elements
    all_elements = service.list_elements()
    
    if not all_elements:
        print("No design elements found")
        return
    
    # Separate characters (focus on these)
    characters = [e for e in all_elements if e.type == DesignElementType.CHARACTER]
    other_elements = [e for e in all_elements if e.type != DesignElementType.CHARACTER]
    
    print(f"\n📊 Found {len(all_elements)} total elements:")
    print(f"   - {len(characters)} Characters")
    print(f"   - {len(other_elements)} Other elements")
    
    # Generate previews for characters first
    print("\n" + "=" * 60)
    print("🎬 Generating previews for CHARACTERS:")
    print("=" * 60)
    
    char_count = 0
    for element in characters:
        if generate_preview_for_element(service, element, pipeline):
            char_count += 1
    
    print(f"\n✅ Generated {char_count} character previews")
    
    # Optionally generate for other elements
    print("\n" + "=" * 60)
    print("🎬 Generating previews for OTHER ELEMENTS:")
    print("=" * 60)
    
    other_count = 0
    for element in other_elements:
        if generate_preview_for_element(service, element, pipeline):
            other_count += 1
    
    print(f"\n✅ Generated {other_count} other element previews")
    
    # Final statistics
    print("\n" + "=" * 60)
    print("📊 FINAL STATISTICS:")
    print("=" * 60)
    
    stats = service.get_statistics()
    elements_with_preview = sum(
        1 for e in all_elements 
        if e.visual_reference_path and Path(e.visual_reference_path).exists()
    )
    
    print(f"Total elements: {stats['total_elements']}")
    print(f"Elements with preview: {elements_with_preview}")
    print(f"Characters with preview: {len([e for e in characters if e.visual_reference_path and Path(e.visual_reference_path).exists()])}")
    
    print("\n✅ Preview generation complete!")


if __name__ == "__main__":
    generate_all_previews()
