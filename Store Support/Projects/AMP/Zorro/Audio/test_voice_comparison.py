#!/usr/bin/env python3
"""Quick test to verify Jenny vs David voice output"""
import sys
sys.path.insert(0, '.')
from windows_media_synthesizer import WindowsMediaSynthesizer

synth = WindowsMediaSynthesizer()

test_text = "Hello, this is a voice test from Walmart Activity Hub. This sentence tests the voice quality and identity."

# Generate with Jenny (neural)
print("\n=== Generating with JENNY (neural) ===")
synth.synthesize_to_mp4(test_text, "test_verify_jenny.mp4", voice="Jenny")

# Generate with David (neural Andrew)
print("\n=== Generating with DAVID (neural Andrew) ===")
synth.synthesize_to_mp4(test_text, "test_verify_david.mp4", voice="David")

# Compare file sizes and hashes
from pathlib import Path
import hashlib
print("\n=== File Comparison ===")
for name in ["test_verify_jenny.mp4", "test_verify_david.mp4"]:
    p = Path(name)
    if p.exists():
        h = hashlib.md5(p.read_bytes()).hexdigest()[:12]
        print(f"  {name}: {p.stat().st_size:,} bytes | md5={h}")
    else:
        print(f"  {name}: MISSING")
