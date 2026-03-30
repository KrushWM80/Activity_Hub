#!/usr/bin/env python3
"""
Neural Voice to MP4 Synthesizer
Uses edge-tts (Microsoft Edge Neural TTS) for Jenny/Guy/Aria neural voices,
with SAPI5 fallback for David/Zira when offline.
Outputs MP4 via FFmpeg.
"""

import subprocess
import asyncio
import sys
import logging
import tempfile
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# edge-tts voice mapping
EDGE_VOICES = {
    "Jenny": "en-US-JennyNeural",
    "Guy": "en-US-GuyNeural",
    "Aria": "en-US-AriaNeural",
    "David": "en-US-AndrewNeural",  # No David neural; Andrew is closest male
    "Zira": "en-US-JennyNeural",    # No Zira neural; Jenny is default female
}

# SAPI5 fallback voices (offline, non-neural)
SAPI5_VOICES = {
    "David": "Microsoft David Desktop",
    "Zira": "Microsoft Zira Desktop",
}


class WindowsMediaSynthesizer:
    """Synthesizes speech using edge-tts neural voices with SAPI5 fallback"""
    
    def __init__(self):
        self.ffmpeg_path = Path("C:\\ffmpeg\\bin\\ffmpeg.exe")
        if not self.ffmpeg_path.exists():
            raise FileNotFoundError(f"FFmpeg not found at {self.ffmpeg_path}")
        logger.info("WindowsMediaSynthesizer initialized (edge-tts + SAPI5 fallback)")
    
    def synthesize_to_mp4(self, text: str, output_file: str, voice: str = "Jenny", pitch: float = 1.0, rate: float = 0.95) -> bool:
        """Synthesize text to MP4. Uses edge-tts neural voices, falls back to SAPI5 if offline."""
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Temp MP3 for edge-tts or WAV for SAPI5
        temp_audio = output_path.parent / f"temp_{output_path.stem}"
        
        try:
            logger.info(f"Synthesizing with voice: {voice}")
            logger.info(f"Text length: {len(text)} characters")
            
            # Try edge-tts (neural) first
            edge_voice = EDGE_VOICES.get(voice, "en-US-JennyNeural")
            temp_mp3 = temp_audio.with_suffix(".mp3")
            success = self._synthesize_with_edge_tts(text, str(temp_mp3), edge_voice, rate)
            
            if success and temp_mp3.exists() and temp_mp3.stat().st_size > 0:
                input_file = temp_mp3
                logger.info(f"Neural audio created: {temp_mp3.stat().st_size:,} bytes")
            else:
                # Fallback to SAPI5
                logger.warning(f"edge-tts failed, falling back to SAPI5 for {voice}")
                temp_wav = temp_audio.with_suffix(".wav")
                sapi_voice = SAPI5_VOICES.get(voice, "Microsoft David Desktop")
                success = self._synthesize_with_sapi5(text, str(temp_wav), sapi_voice, rate)
                if not success or not temp_wav.exists():
                    logger.error("Both edge-tts and SAPI5 synthesis failed")
                    return False
                input_file = temp_wav
                logger.info(f"SAPI5 audio created: {temp_wav.stat().st_size:,} bytes")
            
            # Step 1: Encode audio to temporary MP4
            logger.info("Encoding audio to MP4 with FFmpeg...")
            temp_mp4 = output_path.parent / f"temp_audio_{output_path.stem}.mp4"
            ffmpeg_cmd = [
                str(self.ffmpeg_path),
                "-i", str(input_file),
                "-c:a", "aac",
                "-b:a", "256k",
                "-y",
                str(temp_mp4)
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"FFmpeg audio encode failed: {result.stderr}")
                return False
            
            # Step 2: Mux with thumbnail for Vimeo/Stream embed
            thumbnail = output_path.parent / "merch_msg_thumbnail.jpeg"
            if thumbnail.exists():
                logger.info("Muxing with thumbnail for embeddable video...")
                mux_cmd = [
                    str(self.ffmpeg_path),
                    "-y",
                    "-loop", "1",
                    "-i", str(thumbnail),
                    "-i", str(temp_mp4),
                    "-c:v", "libx264",
                    "-tune", "stillimage",
                    "-preset", "medium",
                    "-r", "25",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-shortest",
                    str(output_path)
                ]
                mux_result = subprocess.run(mux_cmd, capture_output=True, text=True)
                temp_mp4.unlink(missing_ok=True)
                
                if mux_result.returncode != 0:
                    logger.error(f"FFmpeg mux failed: {mux_result.stderr}")
                    return False
                logger.info(f"Embeddable MP4 created with thumbnail")
            else:
                # No thumbnail — just rename temp to final
                logger.warning(f"Thumbnail not found at {thumbnail}, output is audio-only")
                temp_mp4.rename(output_path)
            
            logger.info(f"MP4 encoded: {output_path.stat().st_size:,} bytes")
            logger.info(f"Complete: {output_path.name}")
            return True
        
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return False
        
        finally:
            for ext in [".mp3", ".wav"]:
                f = temp_audio.with_suffix(ext)
                if f.exists():
                    f.unlink(missing_ok=True)
    
    def _synthesize_with_edge_tts(self, text: str, output_mp3: str, voice: str, rate: float) -> bool:
        """Synthesize using edge-tts (Microsoft Edge Neural TTS service)."""
        try:
            import edge_tts
        except ImportError:
            logger.warning("edge-tts not installed")
            return False
        
        rate_pct = int((rate - 1.0) * 100)
        rate_str = f"{rate_pct:+d}%" if rate_pct != 0 else "+0%"
        
        async def _do_synth():
            communicate = edge_tts.Communicate(text, voice, rate=rate_str)
            await communicate.save(output_mp3)
        
        try:
            asyncio.run(_do_synth())
            return True
        except Exception as e:
            logger.warning(f"edge-tts synthesis failed: {e}")
            return False
    
    def _synthesize_with_sapi5(self, text: str, output_wav: str, voice_name: str, rate: float) -> bool:
        """Fallback: synthesize using SAPI5 (System.Speech) — David/Zira only, non-neural."""
        escaped_text = text.replace("'", "''").replace('"', '""')
        sapi_rate = max(-10, min(10, int((rate - 1.0) * 10)))
        
        ps_script = f'''
[void][System.Reflection.Assembly]::LoadWithPartialName("System.Speech")
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile('{output_wav}')
try {{ $synth.SelectVoice("{voice_name}") }} catch {{ }}
$synth.Rate = {sapi_rate}
$synth.Speak("{escaped_text}")
$synth.Dispose()
Write-Host "OK"
'''
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True, text=True, timeout=120
            )
            return result.returncode == 0 and "OK" in result.stdout
        except Exception as e:
            logger.error(f"SAPI5 error: {e}")
            return False


    def synthesize_segments_to_mp4(self, segments, output_file: str, voice: str = "Jenny") -> dict:
        """Synthesize a list of Segment objects with per-segment prosody to MP4.
        
        Each segment has its own rate/pitch/volume for fine-grained prosody control.
        Silence segments are generated as empty audio gaps.
        All speech segments are synthesized in a single asyncio event loop for speed.
        Returns dict with success, duration_seconds, segment_count, errors.
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = Path(tempfile.mkdtemp(prefix="zorro_segments_"))
        
        result = {'success': False, 'duration_seconds': 0, 'segment_count': 0, 'errors': 0}
        
        try:
            import edge_tts
        except ImportError:
            logger.error("edge-tts not installed")
            return result
        
        try:
            edge_voice = EDGE_VOICES.get(voice, "en-US-JennyNeural")
            
            # Pre-generate all silence files (fast, no network)
            segment_files = {}  # index -> Path
            errors = 0
            for i, seg in enumerate(segments):
                if seg.silence_ms > 0:
                    silence_file = temp_dir / f"seg_{i:03d}_silence.mp3"
                    duration_s = seg.silence_ms / 1000.0
                    cmd = [
                        str(self.ffmpeg_path), "-f", "lavfi", "-i",
                        f"anullsrc=r=24000:cl=mono",
                        "-t", f"{duration_s:.3f}",
                        "-c:a", "libmp3lame", "-b:a", "48k",
                        "-y", str(silence_file)
                    ]
                    r = subprocess.run(cmd, capture_output=True, text=True)
                    if r.returncode == 0 and silence_file.exists():
                        segment_files[i] = silence_file
                    else:
                        errors += 1
            
            # Synthesize all speech segments in a single async event loop
            speech_indices = [(i, seg) for i, seg in enumerate(segments) if seg.text]
            logger.info(f"Synthesizing {len(speech_indices)} speech segments in single async batch...")
            
            async def _synth_all():
                nonlocal errors
                for i, seg in speech_indices:
                    speech_file = temp_dir / f"seg_{i:03d}_speech.mp3"
                    label = seg.label[:50] if seg.label else f"seg_{i}"
                    logger.info(f"  [{i+1:03d}/{len(segments):03d}] {label} (rate={seg.rate}, pitch={seg.pitch})")
                    try:
                        comm = edge_tts.Communicate(
                            seg.text, edge_voice,
                            rate=seg.rate, pitch=seg.pitch, volume=seg.volume
                        )
                        await comm.save(str(speech_file))
                        if speech_file.exists() and speech_file.stat().st_size > 0:
                            segment_files[i] = speech_file
                        else:
                            logger.warning(f"  Segment {i} empty output: {label}")
                            errors += 1
                    except Exception as e:
                        logger.warning(f"  Segment {i} failed ({e}), skipping: {label}")
                        errors += 1
            
            asyncio.run(_synth_all())
            
            if not segment_files:
                logger.error("No segments synthesized successfully")
                return result
            
            # Concatenate all segments in original order
            ordered_files = [segment_files[i] for i in sorted(segment_files.keys())]
            concat_file = temp_dir / "concat_list.txt"
            with open(concat_file, "w", encoding="utf-8") as f:
                for sf in ordered_files:
                    safe_path = str(sf).replace("\\", "/").replace("'", "'\\''")
                    f.write(f"file '{safe_path}'\n")
            
            # Step 1: Concat to temp MP4
            temp_mp4 = temp_dir / "concat_output.mp4"
            concat_cmd = [
                str(self.ffmpeg_path),
                "-f", "concat", "-safe", "0",
                "-i", str(concat_file),
                "-c:a", "aac", "-b:a", "256k",
                "-y", str(temp_mp4)
            ]
            r = subprocess.run(concat_cmd, capture_output=True, text=True)
            if r.returncode != 0:
                logger.error(f"FFmpeg concat error: {r.stderr[:500]}")
                return result
            
            # Step 2: Mux with thumbnail for embeddable video
            thumbnail = output_path.parent / "merch_msg_thumbnail.jpeg"
            if thumbnail.exists():
                logger.info("Muxing with thumbnail for embeddable video...")
                mux_cmd = [
                    str(self.ffmpeg_path),
                    "-y",
                    "-loop", "1",
                    "-i", str(thumbnail),
                    "-i", str(temp_mp4),
                    "-c:v", "libx264",
                    "-tune", "stillimage",
                    "-preset", "medium",
                    "-r", "25",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-shortest",
                    str(output_path)
                ]
                mux_result = subprocess.run(mux_cmd, capture_output=True, text=True)
                if mux_result.returncode != 0:
                    logger.error(f"FFmpeg mux failed: {mux_result.stderr[:500]}")
                    # Fall back to audio-only
                    shutil.copy2(temp_mp4, output_path)
            else:
                logger.warning(f"Thumbnail not found, output is audio-only")
                shutil.copy2(temp_mp4, output_path)
            
            # Get audio duration via ffprobe
            duration = 0
            try:
                probe_cmd = [
                    str(self.ffmpeg_path).replace("ffmpeg.exe", "ffprobe.exe"),
                    "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(output_path)
                ]
                pr = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
                if pr.returncode == 0:
                    duration = float(pr.stdout.strip())
            except Exception:
                pass
            
            result['success'] = output_path.exists() and output_path.stat().st_size > 0
            result['duration_seconds'] = duration
            result['segment_count'] = len(segment_files)
            result['errors'] = errors
            
            if result['success']:
                logger.info(f"Segment-based MP4: {output_path.stat().st_size:,} bytes, {duration:.1f}s")
            
            return result
        
        except Exception as e:
            logger.error(f"Segment synthesis error: {e}")
            return result
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _synthesize_segment_edge_tts(self, text: str, output_mp3: str,
                                      voice: str, rate: str = "+0%",
                                      pitch: str = "+0Hz",
                                      volume: str = "+0%") -> bool:
        """Synthesize a single segment with edge-tts using specific prosody settings."""
        try:
            import edge_tts
        except ImportError:
            return False
        
        async def _do_synth():
            comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
            await comm.save(output_mp3)
        
        try:
            asyncio.run(_do_synth())
            return True
        except Exception as e:
            logger.warning(f"edge-tts segment failed: {e}")
            return False


if __name__ == "__main__":
    synth = WindowsMediaSynthesizer()
    
    test_text = "Hello, this is Jenny from Walmart Activity Hub. This is a neural voice test."
    output = "test_jenny.mp4"
    
    success = synth.synthesize_to_mp4(test_text, output, voice="Jenny", rate=0.95)
    
    if success:
        print(f"Successfully created: {output}")
    else:
        print("Synthesis failed")
        sys.exit(1)
