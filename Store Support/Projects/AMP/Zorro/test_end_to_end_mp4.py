"""
End-to-End MP4 Generation Test
==============================
Tests complete workflow from activity message to MP4 file.

Date: March 10, 2026
Status: Full MP4 pipeline validation
"""

import sys
from pathlib import Path
import time

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "Audio"))

from generate_amp_podcast import AMPActivityPodcastGenerator, get_sample_amp_activity


def test_jenny_default_voice():
    """Test 1: Jenny voice (default primary voice)"""
    print("\n" + "="*80)
    print("TEST 1: Activity Hub Message -> MP4 (JENNY VOICE)")
    print("="*80 + "\n")
    
    generator = AMPActivityPodcastGenerator(voice="jenny")
    activity = get_sample_amp_activity()
    
    print(f"📝 Input Activity:")
    print(f"   Title: {activity['message_title']}")
    print(f"   Business Area: {activity['business_area']}")
    print(f"   Voice: JENNY (Primary Neural Voice)\n")
    
    start_time = time.time()
    
    result = generator.create_amp_podcast(
        event_id=activity['event_id'],
        message_title=activity['message_title'],
        message_description=activity['message_description'],
        business_area=activity['business_area'],
        activity_type=activity['activity_type'],
        store_array=activity['store_array'],
        priority_level=activity['priority_level'],
        voice="jenny",
    )
    
    elapsed = time.time() - start_time
    
    if result['success']:
        print("✅ TEST 1 PASSED\n")
        print("📊 Output Results:")
        print(f"   Podcast ID: {result['podcast_id']}")
        print(f"   File: {result['filename']}")
        print(f"   Location: {result['metadata']['file_path']}")
        print(f"   Format: {result['metadata']['format'].upper()}")
        print(f"   Size: {result['file_size_mb']:.2f} KB")
        print(f"   Duration: {result['duration_seconds']} seconds")
        print(f"   Voice: {result['voice']}")
        print(f"   Codec: {result['metadata'].get('codec', 'AAC')}")
        print(f"   Bitrate: {result['metadata']['bitrate']}")
        print(f"   Synthesis Time: {elapsed:.2f}s\n")
        return True
    else:
        print("[FAIL] TEST 1 FAILED\n")
        print(f"Error: {result.get('error', 'Unknown error')}\n")
        return False


def test_david_fallback_voice():
    """Test 2: David voice (fallback)"""
    print("="*80)
    print("TEST 2: Activity Hub Message -> MP4 (DAVID VOICE)")
    print("="*80 + "\n")
    
    generator = AMPActivityPodcastGenerator(voice="david")
    
    activity_data = {
        "event_id": "test-david-2026-001",
        "message_title": "Store Remodeling Project Update",
        "message_description": "Phase 2 of store remodeling begins next week. Temporary sections will be cordoned off. Ensure customer signage is prominently displayed.",
        "business_area": "Store Operations",
        "activity_type": "FYI",
        "store_array": "[1001, 1002, 1003]",
        "priority_level": 2,
    }
    
    print(f"📝 Input Activity:")
    print(f"   Title: {activity_data['message_title']}")
    print(f"   Business Area: {activity_data['business_area']}")
    print(f"   Voice: DAVID (Fallback Voice)\n")
    
    start_time = time.time()
    
    result = generator.create_amp_podcast(
        event_id=activity_data['event_id'],
        message_title=activity_data['message_title'],
        message_description=activity_data['message_description'],
        business_area=activity_data['business_area'],
        activity_type=activity_data['activity_type'],
        store_array=activity_data['store_array'],
        priority_level=activity_data['priority_level'],
        voice="david",
    )
    
    elapsed = time.time() - start_time
    
    if result['success']:
        print("[PASS] TEST 2 PASSED\n")
        print("📊 Output Results:")
        print(f"   Podcast ID: {result['podcast_id']}")
        print(f"   File: {result['filename']}")
        print(f"   Location: {result['metadata']['file_path']}")
        print(f"   Format: {result['metadata']['format'].upper()}")
        print(f"   Size: {result['file_size_mb']:.2f} KB")
        print(f"   Duration: {result['duration_seconds']} seconds")
        print(f"   Voice: {result['voice']}")
        print(f"   Codec: {result['metadata'].get('codec', 'AAC')}")
        print(f"   Bitrate: {result['metadata']['bitrate']}")
        print(f"   Synthesis Time: {elapsed:.2f}s\n")
        return True
    else:
        print("[FAIL] TEST 2 FAILED\n")
        print(f"Error: {result.get('error', 'Unknown error')}\n")
        return False


def test_production_podcast():
    """Test 3: Full production podcast generation"""
    print("="*80)
    print("TEST 3: Production Podcast - Complete MP4 with Metadata")
    print("="*80 + "\n")
    
    generator = AMPActivityPodcastGenerator(voice="jenny")
    
    activity_data = {
        "event_id": "prod-001-2026-Q1",
        "message_title": "Q1 Sales Performance and Targets",
        "message_description": "Review Q1 sales performance against targets. Focus on high-performing product categories and areas for improvement. Regional managers should schedule team briefings this week.",
        "business_area": "Sales & Performance",
        "activity_type": "Action Required",
        "store_array": "[1001, 1002, 1003, 2045, 2046, 2047, 3100, 3101]",
        "priority_level": 1,
    }
    
    print(f"📝 Input Activity:")
    print(f"   Title: {activity_data['message_title']}")
    print(f"   Business Area: {activity_data['business_area']}")
    print(f"   Priority: HIGH")
    print(f"   Stores: {activity_data['store_array']}")
    print(f"   Voice: JENNY\n")
    
    start_time = time.time()
    
    result = generator.create_amp_podcast(
        event_id=activity_data['event_id'],
        message_title=activity_data['message_title'],
        message_description=activity_data['message_description'],
        business_area=activity_data['business_area'],
        activity_type=activity_data['activity_type'],
        store_array=activity_data['store_array'],
        priority_level=activity_data['priority_level'],
        voice="jenny",
    )
    
    elapsed = time.time() - start_time
    
    if result['success']:
        print("✅ TEST 3 PASSED\n")
        print("📊 Complete Podcast Metadata:")
        print(f"   Podcast ID: {result['podcast_id']}")
        print(f"   Event ID: {result['event_id']}")
        print(f"   Title: {result['title']}")
        print(f"   File: {result['filename']}")
        print(f"   Location: {result['metadata']['file_path']}")
        print(f"   Format: {result['metadata']['format'].upper()}")
        print(f"   Size: {result['file_size_mb']:.2f} KB")
        print(f"   Duration: {result['duration_seconds']} seconds")
        print(f"   Voice: {result['voice']}")
        print(f"   Codec: {result['metadata'].get('codec', 'AAC')}")
        print(f"   Bitrate: {result['metadata']['bitrate']}")
        print(f"   Sample Rate: {result['metadata']['sample_rate']} Hz")
        print(f"   Quality: {result['metadata']['quality'].upper()}")
        print(f"   Production Ready: {'✅ YES' if result['production_ready'] else '⚠️  NO'}")
        print(f"   Synthesis Time: {elapsed:.2f}s\n")
        
        print("🔗 Distribution Links:")
        print(f"   Live Link: {result['live_link']}")
        print(f"   Download: {result['download_url']}\n")
        
        return True
    else:
        print("❌ TEST 3 FAILED\n")
        print(f"Error: {result.get('error', 'Unknown error')}\n")
        return False


def main():
    """Run all end-to-end tests"""
    print("\n" + "="*80)
    print("END-TO-END MP4 GENERATION TEST SUITE")
    print("="*80)
    print("MP4-ONLY PIPELINE (No WAV Intermediates)")
    print("Testing Complete Workflow: Activity Message -> MP4 File")
    print("="*80)
    
    # Run tests
    test_results = []
    
    test_results.append(("Jenny Voice (Default)", test_jenny_default_voice()))
    test_results.append(("David Voice (Fallback)", test_david_fallback_voice()))
    test_results.append(("Production Podcast", test_production_podcast()))
    
    # Summary
    print("="*80)
    print("📋 TEST SUMMARY")
    print("="*80 + "\n")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        status_text = "PASS" if result else "FAIL"
        print(f"[{status_text}] {test_name}")
    
    print(f"\nTotal: {passed}/{total} PASSED")
    
    if passed == total:
        print("\nALL TESTS PASSED - MP4 PIPELINE FULLY OPERATIONAL")
        print("\nSystem Ready for:")
        print("   - Activity Hub message to MP4 conversion")
        print("   - Jenny neural voice as default")
        print("   - Direct MP4 output (no WAV files)")
        print("   - Production deployment")
        return 0
    else:
        print("\n[WARNING] SOME TESTS FAILED - Review output above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
