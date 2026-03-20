"""Quick diagnostic: test plain text, then progressively add SSML features."""
import asyncio
import os
import edge_tts
import edge_tts.communicate as cm

original_mkssml = cm.mkssml

def passthrough_mkssml(tc, partial_text):
    s = partial_text.decode("utf-8") if isinstance(partial_text, (bytes, bytearray)) else str(partial_text)
    if s.strip().startswith("<speak"):
        return s
    return original_mkssml(tc, partial_text)


async def test(name, approach, text_or_ssml):
    fname = f"diag_{name}.mp3"
    try:
        if approach == "plain":
            c = edge_tts.Communicate(text_or_ssml, "en-US-JennyNeural")
            await c.save(fname)
        elif approach == "ssml_full":
            cm.mkssml = passthrough_mkssml
            c = edge_tts.Communicate("dummy", "en-US-JennyNeural")
            c.texts = (s.encode("utf-8") for s in [text_or_ssml])
            await c.save(fname)
            cm.mkssml = original_mkssml

        sz = os.path.getsize(fname)
        print(f"  {name}: OK ({sz:,} bytes)")
        os.remove(fname)
        return True
    except Exception as e:
        print(f"  {name}: FAILED - {e}")
        if os.path.exists(fname):
            os.remove(fname)
        return False


async def main():
    print("=== Connectivity check ===")
    await test("plain_text", "plain", "Hello world. This is a connectivity test.")

    print("\n=== SSML tests - full <speak> blocks ===")

    # Test 1: Minimal - just text, no special tags
    await test("ssml_plain_only", "ssml_full",
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        '<voice name="en-US-JennyNeural">'
        '<prosody pitch="+0Hz" rate="+0%" volume="+0%">'
        'Hello world. This is a test.'
        '</prosody>'
        '</voice>'
        '</speak>'
    )

    # Test 2: With break tag
    await test("ssml_break", "ssml_full",
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        '<voice name="en-US-JennyNeural">'
        '<prosody pitch="+0Hz" rate="+0%" volume="+0%">'
        'Hello. <break time="500ms"/> This is after a pause.'
        '</prosody>'
        '</voice>'
        '</speak>'
    )

    # Test 3: With emphasis
    await test("ssml_emphasis", "ssml_full",
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        '<voice name="en-US-JennyNeural">'
        '<prosody pitch="+0Hz" rate="+0%" volume="+0%">'
        'This is <emphasis level="moderate">very important</emphasis> news.'
        '</prosody>'
        '</voice>'
        '</speak>'
    )

    # Test 4: No prosody wrapper, just voice
    await test("ssml_no_prosody", "ssml_full",
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        '<voice name="en-US-JennyNeural">'
        'Hello. <break time="500ms"/> This is after a pause.'
        '</voice>'
        '</speak>'
    )

    # Test 5: With mstts namespace (Microsoft specific)
    await test("ssml_mstts", "ssml_full",
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">'
        '<voice name="en-US-JennyNeural">'
        'Hello. <break time="500ms"/> This is after a pause.'
        '</voice>'
        '</speak>'
    )

    # Test 6: Single quotes instead of double
    await test("ssml_single_quotes", "ssml_full",
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
        "<voice name='en-US-JennyNeural'>"
        "<prosody pitch='+0Hz' rate='+0%' volume='+0%'>"
        "Hello. This is plain inside single-quote SSML."
        "</prosody>"
        "</voice>"
        "</speak>"
    )

asyncio.run(main())
