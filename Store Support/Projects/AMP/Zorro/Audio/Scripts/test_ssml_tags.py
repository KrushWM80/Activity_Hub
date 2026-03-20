#!/usr/bin/env python3
"""Quick test: which SSML tags does edge-tts actually support?"""
import asyncio
import os
import edge_tts
import edge_tts.communicate as cm

original_mkssml = cm.mkssml

def patched_mkssml(tc, text):
    """Pass text through without escaping."""
    return (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
        f"<voice name='{tc.voice}'>"
        f"<prosody pitch='{tc.pitch}' rate='{tc.rate}' volume='{tc.volume}'>"
        f"{text}"
        "</prosody>"
        "</voice>"
        "</speak>"
    )


async def test_tag(name, ssml_text):
    cm.mkssml = patched_mkssml
    c = edge_tts.Communicate("dummy", "en-US-JennyNeural")
    c.texts = [ssml_text]
    fname = f"test_{name}.mp3"
    try:
        await c.save(fname)
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
    print("Testing SSML tag support in edge-tts (Jenny Neural):")
    print()
    
    # Test 1: break
    await test_tag("break", 'Hello. <break time="500ms"/> This is after a pause.')
    
    # Test 2: emphasis
    await test_tag("emphasis", 'This is <emphasis level="moderate">important</emphasis> news.')
    
    # Test 3: prosody nested
    await test_tag("prosody_nested", 'Normal. <prosody rate="slow">This is slower.</prosody> Back to normal.')
    
    # Test 4: just break with longer text
    await test_tag("multi_break", 
        'Hello everyone. <break time="300ms"/> '
        'Welcome to the weekly update. <break time="500ms"/> '
        'Here are the key items. <break time="300ms"/> '
        'Department 13 has a new product launch.'
    )
    
    # Test 5: emphasis strong
    await test_tag("emphasis_strong", 'This is <emphasis level="strong">critical</emphasis> information.')
    
    # Test 6: break + emphasis combined
    await test_tag("break_emphasis", 
        'Hello. <break time="400ms"/> '
        '<emphasis level="moderate">Food and Consumables.</emphasis> '
        '<break time="300ms"/> '
        'Department 13 has updates.'
    )
    
    # Test 7: say-as (numbers)
    await test_tag("say_as", 'The price is <say-as interpret-as="currency">$6.98</say-as>.')
    
    # Test 8: sub (substitution)
    await test_tag("sub", 'Check the <sub alias="out of stock">OOS</sub> report.')


asyncio.run(main())
