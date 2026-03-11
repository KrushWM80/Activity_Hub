import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    jenny = [v for v in voices if 'Jenny' in v['ShortName']]
    for v in jenny:
        print(f"{v['ShortName']} | {v['Gender']} | {v['Locale']}")

asyncio.run(main())
