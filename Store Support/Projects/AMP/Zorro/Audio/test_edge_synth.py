import asyncio
import edge_tts
from pathlib import Path

async def main():
    voice = "en-US-JennyNeural"
    text = "Hello, this is Jenny from the Walmart Activity Hub. Testing neural voice synthesis."
    output = "test_edge_jenny.mp3"
    
    print(f"Synthesizing with {voice}...")
    communicate = edge_tts.Communicate(text, voice, rate="-5%")
    await communicate.save(output)
    
    size = Path(output).stat().st_size
    print(f"Success! File: {output} ({size:,} bytes)")

asyncio.run(main())
