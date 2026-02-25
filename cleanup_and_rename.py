"""Clean up old audio files and rename to new format."""

import os
import shutil
from pathlib import Path

AUDIO_DIR = Path("Store Support/Projects/AMP/Zorro/output/podcasts")

print("=" * 70)
print("CLEANUP & REORGANIZATION")
print("=" * 70)
print()

# Files to keep (latest versions)
KEEP_FILES = {
    "amp_podcast_91202b13_david_male_20260225_165754.wav": "Your Week 4 Messages are Here - Audio - David.wav",
    "amp_podcast_91202b13_zira_female_20260225_165756.wav": "Your Week 4 Messages are Here - Audio - Zira.wav",
}

# Get all WAV files
all_files = sorted(AUDIO_DIR.glob("*.wav"))

print(f"Found {len(all_files)} audio files")
print()

# Delete old files
print("Removing old/test files...")
deleted_count = 0
for file in all_files:
    if file.name not in KEEP_FILES:
        try:
            file.unlink()
            print(f"  ✓ Deleted: {file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ Failed: {file.name} ({e})")

print(f"\nDeleted {deleted_count} files")
print()

# Rename kept files
print("Renaming to new format...")
renamed_count = 0
for old_name, new_name in KEEP_FILES.items():
    old_path = AUDIO_DIR / old_name
    new_path = AUDIO_DIR / new_name
    
    if old_path.exists():
        try:
            old_path.rename(new_path)
            size_mb = new_path.stat().st_size / 1024 / 1024
            print(f"  ✓ {new_name} ({size_mb:.2f} MB)")
            renamed_count += 1
        except Exception as e:
            print(f"  ✗ Failed: {old_name} → {new_name} ({e})")

print(f"\nRenamed {renamed_count} files")
print()

# List final files
print("=" * 70)
print("FINAL AUDIO FILES")
print("=" * 70)
print()

final_files = sorted(AUDIO_DIR.glob("*.wav"))
for file in final_files:
    size_mb = file.stat().st_size / 1024 / 1024
    print(f"  ✓ {file.name}")
    print(f"    Size: {size_mb:.2f} MB")
    print()

print(f"Total: {len(final_files)} audio files")
print()
print("Ready for deployment!")
