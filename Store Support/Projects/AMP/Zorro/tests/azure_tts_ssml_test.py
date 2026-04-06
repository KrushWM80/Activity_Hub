"""
Azure Cognitive Services TTS — SSML Test
=========================================
STANDALONE TEST — Does NOT touch any production code or pipeline.

Purpose: Evaluate Azure Speech Service for full SSML prosody control with
         en-US-JennyNeural, comparing against edge-tts (plain text only).

Prerequisites:
  1. Azure Speech resource (free tier F0 gives 500K chars/month = ~41 hrs)
     Create at: https://portal.azure.com → Cognitive Services → Speech
  2. Set env vars BEFORE running:
       $env:AZURE_SPEECH_KEY = "your-key-here"
       $env:AZURE_SPEECH_REGION = "eastus"   # or your region
  3. `requests` package (already installed in venv)

Usage:
  python azure_tts_ssml_test.py              # Run all tests
  python azure_tts_ssml_test.py --test 1     # Run specific test only
  python azure_tts_ssml_test.py --list       # List available tests

Output:
  tests/azure_tts_output/  (isolated from production output/)
"""

import requests
import os
import sys
import time
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# ── Configuration ───────────────────────────────────────────────────────────

OUTPUT_DIR = Path(__file__).parent / "azure_tts_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Azure Speech API config
AZURE_KEY = os.environ.get("AZURE_SPEECH_KEY", "")
AZURE_REGION = os.environ.get("AZURE_SPEECH_REGION", "")
VOICE = "en-US-JennyNeural"

# Audio formats (Azure supports many — we test a few)
FORMATS = {
    "mp3_128k": "audio-16khz-128kbitrate-mono-mp3",
    "mp3_256k": "audio-48khz-192kbitrate-mono-mp3",  # highest mp3 quality
    "wav_16k":  "riff-16khz-16bit-mono-pcm",
    "wav_48k":  "riff-48khz-16bit-mono-pcm",         # highest wav quality
    "ogg":      "ogg-48khz-16bit-mono-opus",
}
DEFAULT_FORMAT = "mp3_256k"


# ── SSML Test Definitions ──────────────────────────────────────────────────

@dataclass
class SSMLTest:
    id: int
    name: str
    description: str
    ssml: str
    plain_text: str  # equivalent plain text for comparison


TESTS = [
    # Test 1: Basic prosody — rate and pitch (matches current prod -5% rate)
    SSMLTest(
        id=1,
        name="basic_prosody",
        description="Basic rate/pitch control — warm greeting style (matches prod intro_outro tier)",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <prosody rate='-5%' pitch='+2Hz'>
      Hello! Your Week 10 Weekly Messages are Here!
    </prosody>
  </voice>
</speak>""",
        plain_text="Hello! Your Week 10 Weekly Messages are Here!",
    ),

    # Test 2: Break tags — pauses between segments
    SSMLTest(
        id=2,
        name="break_tags",
        description="SSML break tags for controlled pauses between items",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <prosody rate='-5%' pitch='+1Hz'>Food and Consumables</prosody>
    <break time='600ms'/>
    <prosody rate='+0%'>
      Dept. 13: Tide Evo is a category-defining innovation.
      <break time='200ms'/>
      Stores should set the Tide Evo endcap in the action alley by Friday.
    </prosody>
    <break time='400ms'/>
    <prosody rate='+0%'>
      Dept. 46: Stores should immediately move the Emerging Brands modular to the approved 4-foot gondola per the floor plan.
    </prosody>
  </voice>
</speak>""",
        plain_text=(
            "Food and Consumables. "
            "Dept. 13: Tide Evo is a category-defining innovation. "
            "Stores should set the Tide Evo endcap in the action alley by Friday. "
            "Dept. 46: Stores should immediately move the Emerging Brands modular to the approved 4-foot gondola per the floor plan."
        ),
    ),

    # Test 3: Emphasis — moderate/strong emphasis on key action words
    SSMLTest(
        id=3,
        name="emphasis",
        description="Emphasis tags on key action words and department names",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <prosody rate='+0%'>
      <emphasis level='moderate'>Dept. 13</emphasis>:
      <break time='200ms'/>
      <emphasis level='moderate'>Tide Evo</emphasis> is a category-defining innovation.
      Stores should <emphasis level='strong'>immediately</emphasis> set the endcap by Friday.
    </prosody>
  </voice>
</speak>""",
        plain_text="Dept. 13: Tide Evo is a category-defining innovation. Stores should immediately set the endcap by Friday.",
    ),

    # Test 4: say-as — date, number, and abbreviation handling
    SSMLTest(
        id=4,
        name="say_as",
        description="say-as for dates, numbers, and abbreviations",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <prosody rate='+0%'>
      This activity runs from <say-as interpret-as='date' format='md'>4/7</say-as>
      through <say-as interpret-as='date' format='md'>4/11</say-as>.
      Target is <say-as interpret-as='cardinal'>2500</say-as> stores.
      Category <say-as interpret-as='characters'>C111</say-as> modular update.
    </prosody>
  </voice>
</speak>""",
        plain_text="This activity runs from 4/7 through 4/11. Target is 2500 stores. Category C111 modular update.",
    ),

    # Test 5: Nested prosody — multi-tier like prod (group header → area → body)
    SSMLTest(
        id=5,
        name="multi_tier_prosody",
        description="Full multi-tier prosody matching prod 6-tier system (group→area→headline→body→outro)",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <!-- Greeting (intro_outro tier: -5%, +2Hz) -->
    <prosody rate='-5%' pitch='+2Hz'>
      Hello! Your Week 10 Weekly Messages are Here!
    </prosody>
    <break time='800ms'/>

    <!-- Group Header (group_header tier: -10%, +1Hz) -->
    <prosody rate='-10%' pitch='+1Hz'>
      Food and Consumables
    </prosody>
    <break time='600ms'/>

    <!-- Area Header (area_header tier: -5%, +1Hz) -->
    <prosody rate='-5%' pitch='+1Hz'>
      Salesfloor, Consumables
    </prosody>
    <break time='300ms'/>

    <!-- Body (body tier: +0%) -->
    <prosody rate='+0%'>
      Dept. 13: Tide Evo is a category-defining innovation. Stores should set the Tide Evo endcap in the action alley by Friday.
    </prosody>
    <break time='400ms'/>

    <prosody rate='+0%'>
      Dept. 46: Stores should immediately move the Emerging Brands modular to the approved 4-foot gondola per the floor plan.
    </prosody>
    <break time='800ms'/>

    <!-- Outro (intro_outro tier: -5%, +1Hz) -->
    <prosody rate='-5%' pitch='+1Hz'>
      That's your Week 10 Weekly Messages.
    </prosody>
    <break time='400ms'/>

    <!-- Sign-off (intro_outro tier: -8%, +2Hz) -->
    <prosody rate='-8%' pitch='+2Hz'>
      Have a Great Week!
    </prosody>
  </voice>
</speak>""",
        plain_text=(
            "Hello! Your Week 10 Weekly Messages are Here! "
            "Food and Consumables. "
            "Salesfloor, Consumables. "
            "Dept. 13: Tide Evo is a category-defining innovation. Stores should set the Tide Evo endcap in the action alley by Friday. "
            "Dept. 46: Stores should immediately move the Emerging Brands modular to the approved 4-foot gondola per the floor plan. "
            "That's your Week 10 Weekly Messages. "
            "Have a Great Week!"
        ),
    ),

    # Test 6: Phoneme — correct pronunciation of tricky terms
    SSMLTest(
        id=6,
        name="phoneme",
        description="Phoneme override for brand names and abbreviations",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <prosody rate='+0%'>
      <phoneme alphabet='ipa' ph='taɪd iːvoʊ'>Tide Evo</phoneme> is now available.
      Set the <phoneme alphabet='ipa' ph='ɛnd.kæp'>endcap</phoneme> in action alley.
    </prosody>
  </voice>
</speak>""",
        plain_text="Tide Evo is now available. Set the endcap in action alley.",
    ),

    # Test 7: Full realistic segment — actual summarized content example
    SSMLTest(
        id=7,
        name="realistic_segment",
        description="Full realistic summarized Weekly Message with all SSML features combined",
        ssml=f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    <prosody rate='-5%' pitch='+1Hz'>
      Salesfloor, Fresh
    </prosody>
    <break time='300ms'/>
    <prosody rate='+0%'>
      <emphasis level='moderate'>Dept. 80</emphasis>:
      <break time='150ms'/>
      Stores should ensure the seasonal berry display is built to the
      <emphasis level='moderate'>4-foot plan-o-gram</emphasis>
      and maintain cold chain compliance.
      <break time='200ms'/>
      Remove any expired pre-pack strawberries from the sales floor
      <emphasis level='strong'>immediately</emphasis> and process through claims.
    </prosody>
  </voice>
</speak>""",
        plain_text=(
            "Salesfloor, Fresh. "
            "Dept. 80: Stores should ensure the seasonal berry display is built to the 4-foot plan-o-gram "
            "and maintain cold chain compliance. Remove any expired pre-pack strawberries from the sales floor "
            "immediately and process through claims."
        ),
    ),
]


# ── Azure TTS REST API ─────────────────────────────────────────────────────

def get_token(key: str, region: str) -> Optional[str]:
    """Exchange API key for a short-lived bearer token (10 min TTL)."""
    url = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {"Ocp-Apim-Subscription-Key": key}
    r = requests.post(url, headers=headers, timeout=10)
    if r.status_code == 200:
        return r.text
    print(f"  [ERROR] Token exchange failed: {r.status_code} {r.text}")
    return None


def synthesize_ssml(ssml: str, output_path: Path, fmt: str = DEFAULT_FORMAT,
                    key: str = "", region: str = "") -> dict:
    """Send SSML to Azure TTS REST API, save audio, return metrics."""
    result = {"success": False, "bytes": 0, "elapsed_ms": 0, "format": fmt, "error": None}

    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": FORMATS[fmt],
        "User-Agent": "ZorroAudioHub-Test/1.0",
    }

    t0 = time.perf_counter()
    try:
        r = requests.post(url, headers=headers, data=ssml.encode("utf-8"), timeout=30)
        elapsed = (time.perf_counter() - t0) * 1000

        if r.status_code == 200:
            output_path.write_bytes(r.content)
            result["success"] = True
            result["bytes"] = len(r.content)
            result["elapsed_ms"] = round(elapsed, 1)
        else:
            result["error"] = f"HTTP {r.status_code}: {r.text[:200]}"
            result["elapsed_ms"] = round(elapsed, 1)
    except requests.RequestException as e:
        result["error"] = str(e)
        result["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 1)

    return result


# ── Main ────────────────────────────────────────────────────────────────────

def run_test(test: SSMLTest, key: str, region: str) -> dict:
    """Run a single SSML test and return results."""
    print(f"\n{'='*60}")
    print(f"  Test {test.id}: {test.name}")
    print(f"  {test.description}")
    print(f"{'='*60}")

    # Synthesize SSML version
    ssml_file = OUTPUT_DIR / f"test{test.id}_{test.name}_ssml.mp3"
    print(f"  Synthesizing SSML → {ssml_file.name} ...", end=" ", flush=True)
    ssml_result = synthesize_ssml(test.ssml, ssml_file, key=key, region=region)

    if ssml_result["success"]:
        print(f"OK  ({ssml_result['bytes']:,} bytes, {ssml_result['elapsed_ms']:.0f}ms)")
    else:
        print(f"FAILED  ({ssml_result['error']})")

    # Synthesize plain text version (wrapped in minimal SSML) for comparison
    plain_ssml = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='{VOICE}'>
    {test.plain_text}
  </voice>
</speak>"""
    plain_file = OUTPUT_DIR / f"test{test.id}_{test.name}_plain.mp3"
    print(f"  Synthesizing plain → {plain_file.name} ...", end=" ", flush=True)
    plain_result = synthesize_ssml(plain_ssml, plain_file, key=key, region=region)

    if plain_result["success"]:
        print(f"OK  ({plain_result['bytes']:,} bytes, {plain_result['elapsed_ms']:.0f}ms)")
    else:
        print(f"FAILED  ({plain_result['error']})")

    return {
        "test_id": test.id,
        "name": test.name,
        "ssml": ssml_result,
        "plain": plain_result,
    }


def print_summary(results: list):
    """Print a summary table of all test results."""
    print(f"\n{'='*70}")
    print("  AZURE TTS SSML TEST SUMMARY")
    print(f"{'='*70}")
    print(f"  {'#':<3} {'Test':<25} {'SSML':<12} {'Plain':<12} {'SSML Size':<12} {'Plain Size':<12}")
    print(f"  {'-'*3} {'-'*25} {'-'*12} {'-'*12} {'-'*12} {'-'*12}")

    total_ssml_chars = 0
    for r in results:
        status_ssml = "OK" if r["ssml"]["success"] else "FAIL"
        status_plain = "OK" if r["plain"]["success"] else "FAIL"
        sz_ssml = f"{r['ssml']['bytes']:,}B" if r["ssml"]["success"] else "-"
        sz_plain = f"{r['plain']['bytes']:,}B" if r["plain"]["success"] else "-"
        print(f"  {r['test_id']:<3} {r['name']:<25} {status_ssml:<12} {status_plain:<12} {sz_ssml:<12} {sz_plain:<12}")

    print(f"\n  Output directory: {OUTPUT_DIR}")
    print(f"  Compare SSML vs plain versions to hear the prosody difference.")
    print()

    # Cost estimate
    total_chars = sum(len(TESTS[i].ssml) + len(TESTS[i].plain_text) for i in range(len(results)))
    print(f"  Characters used in this test run: ~{total_chars:,}")
    print(f"  Azure F0 (free): 500K chars/month")
    print(f"  Azure S0 (paid): $16/1M chars → this run ≈ ${total_chars * 16 / 1_000_000:.4f}")
    print()


def main():
    # Parse args
    if "--list" in sys.argv:
        print("\nAvailable tests:")
        for t in TESTS:
            print(f"  {t.id}: {t.name} — {t.description}")
        return

    test_filter = None
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        if idx + 1 < len(sys.argv):
            test_filter = int(sys.argv[idx + 1])

    # Check credentials
    key = AZURE_KEY
    region = AZURE_REGION
    if not key or not region:
        print("\n" + "="*60)
        print("  AZURE SPEECH CREDENTIALS NOT SET")
        print("="*60)
        print()
        print("  Set these environment variables before running:")
        print()
        print('    $env:AZURE_SPEECH_KEY = "your-key-here"')
        print('    $env:AZURE_SPEECH_REGION = "eastus"')
        print()
        print("  To get a key:")
        print("    1. Go to https://portal.azure.com")
        print("    2. Create a 'Speech' resource (Free F0 tier = 500K chars/month)")
        print("    3. Copy Key 1 and Region from the resource's Keys & Endpoint page")
        print()
        print("  This test is STANDALONE and does NOT affect any production code.")
        print()

        # Still show what would be tested
        print("  Tests that would run:")
        for t in TESTS:
            print(f"    {t.id}: {t.name} — {t.description}")
        print()
        return

    # Run tests
    print(f"\n  Azure TTS SSML Test — Voice: {VOICE}")
    print(f"  Region: {region}")
    print(f"  Output: {OUTPUT_DIR}")

    tests_to_run = [t for t in TESTS if test_filter is None or t.id == test_filter]
    if not tests_to_run:
        print(f"  No test found with id={test_filter}")
        return

    results = []
    for test in tests_to_run:
        r = run_test(test, key, region)
        results.append(r)

    print_summary(results)

    # Save full results as JSON
    results_file = OUTPUT_DIR / "test_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Full results saved to: {results_file}")


if __name__ == "__main__":
    main()
