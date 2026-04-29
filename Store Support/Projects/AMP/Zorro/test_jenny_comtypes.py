"""
Phase 1: Test Jenny Neural SAPI synthesis — three approaches.

Test A: Pure comtypes (SpVoice + SpFileStream)
Test B: Pure win32com (SpVoice + SpFileStream) — new, not yet tried
Test C: win32com Speak to default output (no file stream)
"""
import os
import tempfile

JENNY_TOKEN = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_enUS_JennyNeural'
SSFM_CREATE_FOR_WRITE = 3

def test_b_pure_win32com():
    """Test B: Pure win32com for both SpVoice AND SpFileStream."""
    print("\n=== Test B: Pure win32com (SpVoice + SpFileStream) ===\n")
    import win32com.client

    voice = win32com.client.Dispatch('SAPI.SpVoice')
    token = win32com.client.Dispatch('SAPI.SpObjectToken')
    token.SetId(JENNY_TOKEN, '', False)
    voice.Voice = token
    print(f"   Voice: {voice.Voice.GetAttribute('Name')}")

    wav_path = os.path.join(tempfile.gettempdir(), 'jenny_win32com_test.wav')
    stream = win32com.client.Dispatch('SAPI.SpFileStream')
    stream.Open(wav_path, SSFM_CREATE_FOR_WRITE, False)
    print(f"   Stream opened: {wav_path}")

    voice.AudioOutputStream = stream
    print("   AudioOutputStream set")

    text = "Hello from Jenny Neural, testing with pure win32com."
    print(f"   Speaking: '{text}'")
    voice.Speak(text, 0)
    print("   Speak completed")

    stream.Close()
    size = os.path.getsize(wav_path) if os.path.exists(wav_path) else 0
    print(f"   WAV size: {size:,} bytes")
    return size > 0

def test_c_speak_to_speakers():
    """Test C: win32com Speak to default audio output (speakers)."""
    print("\n=== Test C: win32com Speak to speakers (no file) ===\n")
    import win32com.client

    voice = win32com.client.Dispatch('SAPI.SpVoice')
    token = win32com.client.Dispatch('SAPI.SpObjectToken')
    token.SetId(JENNY_TOKEN, '', False)
    voice.Voice = token
    print(f"   Voice: {voice.Voice.GetAttribute('Name')}")

    text = "Hello Jenny."
    print(f"   Speaking to speakers: '{text}'")
    voice.Speak(text, 0)
    print("   Speak completed (check speakers for audio)")
    return True

if __name__ == '__main__':
    results = {}

    # Test B: Pure win32com
    try:
        results['B'] = test_b_pure_win32com()
    except Exception as e:
        results['B'] = False
        print(f"   FAIL: {type(e).__name__}: {e}")

    # Test C: Speak to speakers (only if B failed)
    if not results['B']:
        try:
            results['C'] = test_c_speak_to_speakers()
        except Exception as e:
            results['C'] = False
            print(f"   FAIL: {type(e).__name__}: {e}")

    print("\n=== SUMMARY ===")
    for test, ok in results.items():
        print(f"   Test {test}: {'PASS' if ok else 'FAIL'}")

    if any(results.values()):
        print("\n   -> At least one local approach works! Proceed to Phase 2A.")
    else:
        print("\n   -> All local approaches failed. Proceed to Phase 2B (Option B: socket pre-check + edge-tts).")
