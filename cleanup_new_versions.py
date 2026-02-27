"""Clean up old versions and keep only the latest full-content audio files."""

import os
from pathlib import Path
import shutil

AUDIO_DIR = Path("Store Support/Projects/AMP/Zorro/output/podcasts")

print("=" * 70)
print("CLEANUP - REMOVING OLD VERSIONS")
print("=" * 70)
print()

# Find all WAV files
all_files = list(AUDIO_DIR.glob("*.wav"))

print(f"Found {len(all_files)} audio files\n")

# Delete everything except the newest dated files
print("Removing old/incomplete versions...")

# Keep only files from 20260226 (today's full versions) with timestamps 075737 and 075739
keep_files = {
    "amp_podcast_91202b13_david_male_20260226_075737.wav",
    "amp_podcast_91202b13_zira_female_20260226_075739.wav",
}

deleted_count = 0
for file in all_files:
    if file.name not in keep_files:
        try:
            file.unlink()
            print(f"  ✓ Deleted: {file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ Failed to delete {file.name}: {e}")

print(f"\nDeleted {deleted_count} files")
print()

# Rename to final format
print("Renaming to final Zorro format...")

rename_map = {
    "amp_podcast_91202b13_david_male_20260226_075737.wav": "Your Week 4 Messages are Here - Audio - David.wav",
    "amp_podcast_91202b13_zira_female_20260226_075739.wav": "Your Week 4 Messages are Here - Audio - Zira.wav",
}

renamed_count = 0
for old_name, new_name in rename_map.items():
    old_path = AUDIO_DIR / old_name
    new_path = AUDIO_DIR / new_name
    
    if old_path.exists():
        try:
            old_path.rename(new_path)
            size_mb = round(new_path.stat().st_size / (1024 * 1024), 2)
            print(f"  ✓ {new_name} ({size_mb} MB)")
            renamed_count += 1
        except Exception as e:
            print(f"  ✗ Failed to rename {old_name}: {e}")

print(f"\nRenamed {renamed_count} files")
print()

# Show final result
print("=" * 70)
print("FINAL AUDIO FILES (COMPLETE MESSAGE CONTENT)")
print("=" * 70)
print()

final_files = sorted(AUDIO_DIR.glob("*.wav"))
for file in final_files:
    size_mb = round(file.stat().st_size / (1024 * 1024), 2)
    print(f"  ✓ {file.name}")
    print(f"    Size: {size_mb} MB (Full message body included)")
    print()

print("Ready for deployment in Zorro!")
