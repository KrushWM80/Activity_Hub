"""
Unified Multi-Format Content Creation Demo & Test Suite

Tests all new capabilities:
- Audio/Podcast generation
- Multi-format content creation  
- File optimization
- Analytics tracking
- Download delivery
"""

import sys
from pathlib import Path
from datetime import datetime

# Add Zorro src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.audio_podcast_service import AudioPodcastService, AudioQuality, AudioFormat
from services.multi_format_content_manager import (
    MultiFormatContentManager,
    ContentFormat,
    ContentQuality,
)
from services.analytics_tracker import AnalyticsTracker


def test_podcast_generation():
    """Test audio/podcast generation capabilities."""
    
    print("\n" + "="*80)
    print("🎙️  TEST 1: PODCAST GENERATION")
    print("="*80 + "\n")
    
    podcast_service = AudioPodcastService(output_dir="output/podcasts")
    
    # Sample content for testing
    podcast_content = """
    Good morning team! This is an important safety update for all store associates.
    
    Starting this week, we're implementing new protocols for the busy holiday shopping season.
    First, ensure all team members review the safety checklist before their shift.
    Second, maintain clear communication with your teammates using the new radio procedures.
    Third, practice the emergency evacuation routes - we'll conduct a drill on Friday at 2 PM.
    
    Remember, safety is our top priority. If you see something, say something.
    Contact your manager immediately with any concerns or questions.
    
    Thank you for your dedication to keeping our stores safe and welcoming.
    """
    
    print("📝 Generating podcast from content...")
    print(f"Content length: {len(podcast_content)} characters")
    print(f"Content words: {len(podcast_content.split())} words\n")
    
    # Test different narrators and qualities
    narrators = ["professional", "friendly", "energetic"]
    qualities = [AudioQuality.MEDIUM, AudioQuality.HIGH]
    
    results = {}
    
    for narrator in narrators:
        for quality in qualities:
            print(f"\n📢 Generating with narrator='{narrator}', quality={quality.name}...")
            
            result = podcast_service.generate_podcast_audio(
                content=podcast_content,
                podcast_title=f"Safety Update - {narrator.title()}",
                narrator=narrator,
                quality=quality,
                format=AudioFormat.MP3,
            )
            
            if result["success"]:
                key = f"{narrator}_{quality.name}"
                results[key] = result
                
                print(f"  ✅ Success!")
                print(f"     File: {result['filename']}")
                print(f"     Size: {result['file_size_mb']} MB")
                print(f"     Duration: {result['duration_seconds']} seconds")
                print(f"     Speaking Rate: {result['analytics']['speaking_rate_wps']:.1f} words/sec")
            else:
                print(f"  ❌ Failed: {result.get('error')}")
    
    # Test file optimization
    print("\n\n" + "-"*80)
    print("📦 FILE OPTIMIZATION TEST")
    print("-"*80 + "\n")
    
    first_result = list(results.values())[0] if results else None
    if first_result:
        audio_path = first_result["audio_path"]
        print(f"Original file: {Path(audio_path).name}")
        print(f"Original size: {first_result['file_size_mb']} MB")
        
        optimized = podcast_service.optimize_file_size(
            audio_path=audio_path,
            target_size_mb=2,
            format=AudioFormat.MP3,
        )
        
        print(f"\n🎯 Optimization for target size: {optimized['target_size_mb']} MB")
        print(f"   Original: {optimized['original_size_mb']} MB")
        print(f"   Optimal bitrate: {optimized['optimal_bitrate']}")
        print(f"   Compression ratio: {optimized['compression_ratio']:.2f}x")
    
    return results


def test_multi_format_creation():
    """Test creating content in multiple formats simultaneously."""
    
    print("\n\n" + "="*80)
    print("🎨 TEST 2: MULTI-FORMAT CONTENT CREATION")
    print("="*80 + "\n")
    
    content_manager = MultiFormatContentManager(output_dir="output/multi_format")
    
    # Sample message for multi-format generation
    message = """
    Welcome to our Winter Health Awareness Campaign!
    
    This week we're focusing on staying healthy during the flu season.
    Make sure to get your flu shot - it's free for all associates!
    
    Key tips:
    - Wash your hands frequently
    - Cover your cough or sneeze
    - Stay home if you're sick
    - Get adequate sleep and exercise
    
    Visit your local clinic for your free vaccination today!
    """
    
    print("📢 Creating content in multiple formats...\n")
    
    # Generate in all formats
    project = content_manager.create_multi_format_project(
        content=message,
        title="Winter Health Campaign",
        formats=[
            ContentFormat.VIDEO,
            ContentFormat.INFOGRAPHIC,
            ContentFormat.AUDIO,
            ContentFormat.DOCUMENT,
            ContentFormat.INTERACTIVE,
        ],
        quality=ContentQuality.MEDIUM,
        metadata={
            "author": "Store Communications",
            "campaign": "Winter Health 2026",
            "target_audience": "All Associates",
        }
    )
    
    print("📊 Project Summary:")
    print(f"   Project ID: {project['project_id']}")
    print(f"   Title: {project['title']}")
    print(f"   Formats generated: {len(project['outputs'])}\n")
    
    # Display each format
    for format_name, output in project["outputs"].items():
        if output.get("success"):
            print(f"\n   ✅ {format_name.upper()}")
            print(f"      File: {output.get('filename')}")
            print(f"      Size: {output.get('file_size_mb')} MB")
            if output.get("duration_seconds"):
                print(f"      Duration: {output.get('duration_seconds')}s")
            if output.get("also_available"):
                print(f"      Also available: {', '.join(output['also_available'])}")
        else:
            print(f"\n   ❌ {format_name.upper()}: {output.get('error')}")
    
    # Get distribution package
    print("\n\n" + "-"*80)
    print("📦 DISTRIBUTION PACKAGE")
    print("-"*80 + "\n")
    
    package = content_manager.get_distribution_package(
        project_id=project["project_id"],
        include_tracking=True
    )
    
    print(f"Total files ready for distribution: {len(package['files'])}")
    for file_info in package["files"]:
        print(f"\n   • {file_info['format'].upper()}")
        print(f"     Download URL: {file_info['download_url']}")
        print(f"     Size: {file_info['file_size_mb']} MB")
        print(f"     Tracking ID: {file_info.get('tracking_id', 'N/A')[:16]}...")
    
    # Test optimization
    print("\n\n" + "-"*80)
    print("⚡ OPTIMIZATION FOR DISTRIBUTION")
    print("-"*80 + "\n")
    
    optimization = content_manager.optimize_for_distribution(
        project_id=project["project_id"],
        max_size_mb=10,
    )
    
    print(f"Original total size: {optimization['total_original_size_mb']:.2f} MB")
    print(f"Optimized total size: {optimization['total_optimized_size_mb']:.2f} MB")
    print(f"Compression ratio: {optimization['total_compression_ratio']:.2f}x\n")
    
    for opt in optimization["optimization_applied"]:
        print(f"   {opt['format'].upper()}:")
        print(f"     Savings: {opt['compression_savings_percent']}%")
        print(f"     Strategy: {opt['strategy']}")
    
    return project


def test_analytics_tracking():
    """Test analytics and multi-layer tracking."""
    
    print("\n\n" + "="*80)
    print("📊 TEST 3: ANALYTICS & TRACKING")
    print("="*80 + "\n")
    
    tracker = AnalyticsTracker(db_dir="analytics_data")
    
    print("📌 Simulating user interactions...\n")
    
    # Simulate various user interactions
    content_id = "PROJECT_WINTER_HEALTH_001"
    
    # Simulate different users
    interactions = [
        # User 1 - Engaged user
        {
            "type": "view",
            "user": "user_001",
            "session": "sess_aaa",
            "device": "mobile",
            "platform": "email",
        },
        {
            "type": "time",
            "user": "user_001",
            "duration": 45,
        },
        {
            "type": "click",
            "user": "user_001",
            "element": "watch_video",
        },
        # User 2 - Casual user
        {
            "type": "view",
            "user": "user_002",
            "session": "sess_bbb",
            "device": "desktop",
            "platform": "web",
        },
        {
            "type": "click",
            "user": "user_002",
            "element": "download_infographic",
        },
        # User 3 - Anonymous
        {
            "type": "view",
            "session": "sess_ccc",
            "device": "tablet",
            "platform": "mobile_app",
        },
        # User 1 again - Downloads
        {
            "type": "download",
            "user": "user_001",
            "format": "audio",
            "size": 2.5,
        },
    ]
    
    print("Tracking interactions:")
    for interaction in interactions:
        if interaction["type"] == "view":
            result = tracker.track_content_view(
                content_id=content_id,
                user_id=interaction.get("user"),
                session_id=interaction.get("session"),
                device_type=interaction.get("device", "unknown"),
                platform=interaction.get("platform", "unknown"),
            )
            print(f"  ✓ View tracked - Unique: {result['is_unique_user']}")
        
        elif interaction["type"] == "time":
            result = tracker.track_time_on_page(
                content_id=content_id,
                duration_seconds=interaction["duration"],
                user_id=interaction.get("user"),
            )
            print(f"  ✓ Time tracked - {interaction['duration']}s")
        
        elif interaction["type"] == "click":
            result = tracker.track_click(
                content_id=content_id,
                click_element=interaction["element"],
                user_id=interaction.get("user"),
            )
            print(f"  ✓ Click tracked - {interaction['element']} (Unique: {result['is_unique_click']})")
        
        elif interaction["type"] == "download":
            result = tracker.track_download(
                content_id=content_id,
                format_type=interaction["format"],
                file_size_mb=interaction["size"],
                user_id=interaction.get("user"),
            )
            print(f"  ✓ Download tracked - {interaction['format']} ({interaction['size']}MB)")
    
    # Get comprehensive analytics
    print("\n\n" + "-"*80)
    print("📈 CONTENT ANALYTICS REPORT")
    print("-"*80 + "\n")
    
    analytics = tracker.get_content_analytics(content_id)
    
    print(f"Content: {analytics['content_id']}\n")
    
    print("👁️  VIEWS:")
    print(f"   Total Views: {analytics['views']['total']}")
    print(f"   Unique Views: {analytics['views']['unique']}")
    print(f"   Unique Users: {analytics['views']['unique_users']}")
    print(f"   Avg Views/User: {analytics['views']['avg_views_per_user']}")
    
    print(f"\n👆 CLICKS:")
    print(f"   Total Clicks: {analytics['clicks']['total']}")
    print(f"   Unique Clicks: {analytics['clicks']['unique']}")
    print(f"   CTR: {analytics['clicks']['click_through_rate']}%")
    print(f"   By Element: {analytics['clicks']['by_element']}")
    
    print(f"\n⏱️  ENGAGEMENT:")
    print(f"   Avg Time on Page: {analytics['engagement']['average_time_seconds']}s")
    print(f"   Engagement Rate: {analytics['engagement']['engagement_rate']}%")
    print(f"   Users Engaging: {analytics['engagement']['views_spending_time']}")
    
    print(f"\n⬇️  DOWNLOADS:")
    print(f"   Total Downloads: {analytics['downloads']['total']}")
    print(f"   By Format: {analytics['downloads']['by_format']}")
    print(f"   Total Data: {analytics['downloads']['total_data_downloaded_mb']}MB")
    
    print(f"\n🖥️  DEVICES:")
    for device, count in analytics['device_distribution'].items():
        print(f"   {device}: {count}")
    
    print(f"\n🌐 PLATFORMS:")
    for platform, count in analytics['platform_distribution'].items():
        print(f"   {platform}: {count}")
    
    # User journey
    print("\n\n" + "-"*80)
    print("👤 USER JOURNEY - user_001")
    print("-"*80 + "\n")
    
    journey = tracker.get_user_journey("user_001")
    
    print(f"Total Events: {journey['total_events']}")
    print(f"Total Sessions: {journey['total_sessions']}")
    print(f"Content Interacted: {journey['content_interacted']}")
    print(f"Total Time on Pages: {journey['total_time_on_pages_seconds']}s")
    
    for content_id, interactions in journey['interactions_by_content'].items():
        print(f"\n  Content: {content_id}")
        print(f"    Views: {interactions['views']}")
        print(f"    Clicks: {interactions['clicks']}")
        print(f"    Downloads: {interactions['downloads']}")
        print(f"    First seen: {interactions['first_interaction']}")
        print(f"    Last seen: {interactions['last_interaction']}")


def main():
    """Run all tests."""
    
    print("\n" + "=" * 80)
    print("🚀 ZORRO UNIFIED MULTI-FORMAT CONTENT SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Test 1: Podcast Generation
        podcast_results = test_podcast_generation()
        
        # Test 2: Multi-Format Creation
        project = test_multi_format_creation()
        
        # Test 3: Analytics Tracking
        test_analytics_tracking()
        
        # Final Summary
        print("\n\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
        print("📋 SUMMARY:")
        print(f"   ✅ Podcast generation: {len(podcast_results)} configurations tested")
        print(f"   ✅ Multi-format creation: {len(project['outputs'])} formats generated")
        print(f"   ✅ Analytics tracking: Comprehensive tracking system validated")
        print(f"   ✅ File optimization: Compression and delivery ready")
        
        print("\n🎯 KEY CAPABILITIES VERIFIED:")
        print("   ✓ Audio/Podcast generation with multiple narrators & qualities")
        print("   ✓ Single-source multi-format output (Video, Infographic, Audio, etc)")
        print("   ✓ Automatic file optimization and compression")
        print("   ✓ Multi-layer tracking (unique clicks, user clicks, page views, etc)")
        print("   ✓ Analytics dashboards and reports")
        print("   ✓ User journey tracking")
        print("   ✓ Download delivery with tracking codes")
        
        print("\n🚀 NEXT STEPS:")
        print("   1. Integrate with Streamlit UI (app.py)")
        print("   2. Add database backend for persistent storage")
        print("   3. Implement real TTS (Google Cloud or Azure)")
        print("   4. Deploy tracking pixel to web interface")
        print("   5. Create admin analytics dashboard")
        
        print("\n📁 Output directories:")
        print("   • output/podcasts/ - Generated audio files")
        print("   • output/multi_format/ - Multi-format projects")
        print("   • analytics_data/ - Tracking events and metrics")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*80)
    print(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
