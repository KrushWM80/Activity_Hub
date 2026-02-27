"""
Video Trimming Component

Provides UI components for trimming video clips with start/end time selection.
Uses FFmpeg for fast, lossless trimming when possible.
Includes AI disclosure watermark support for legal compliance.
"""

import streamlit as st
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Optional, Tuple
from datetime import timedelta


# AI Disclosure watermark options
AI_WATERMARK_OPTIONS = {
    "none": "No watermark",
    "ai_generated": "AI Generated",
    "created_with_ai": "Created with AI",
    "ai_assisted": "AI-Assisted Content",
    "custom": "Custom text..."
}

AI_WATERMARK_POSITIONS = {
    "bottom_right": "Bottom Right",
    "bottom_left": "Bottom Left", 
    "top_right": "Top Right",
    "top_left": "Top Left"
}


def add_watermark_ffmpeg(
    input_path: str,
    output_path: str,
    text: str,
    position: str = "bottom_right",
    font_size: int = 18,
    opacity: float = 0.7
) -> bool:
    """
    Add AI disclosure watermark to video using FFmpeg.
    
    Args:
        input_path: Path to input video
        output_path: Path for output video
        text: Watermark text
        position: Position (bottom_right, bottom_left, top_right, top_left)
        font_size: Font size in pixels
        opacity: Opacity (0.0-1.0)
    
    Returns:
        bool: True if successful
    """
    position_map = {
        "bottom_right": "x=w-tw-10:y=h-th-10",
        "bottom_left": "x=10:y=h-th-10",
        "top_right": "x=w-tw-10:y=10",
        "top_left": "x=10:y=10"
    }
    
    pos = position_map.get(position, position_map["bottom_right"])
    alpha = min(1.0, max(0.1, opacity))
    
    # Escape special characters for FFmpeg
    escaped_text = text.replace("'", "\\'").replace(":", "\\:")
    
    filter_str = (
        f"drawtext=text='{escaped_text}':"
        f"{pos}:"
        f"fontsize={font_size}:"
        f"fontcolor=white@{alpha}:"
        f"box=1:"
        f"boxcolor=black@{alpha * 0.5}:"
        f"boxborderw=5"
    )
    
    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vf", filter_str,
            "-c:a", "copy",
            "-y",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.returncode == 0 and Path(output_path).exists()
    except Exception as e:
        st.error(f"Watermark error: {e}")
        return False


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS.mmm"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{int(td.microseconds/1000):03d}"


def parse_time(time_str: str) -> float:
    """Parse time string to seconds."""
    try:
        parts = time_str.split(":")
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)
        elif len(parts) == 2:
            m, s = parts
            return int(m) * 60 + float(s)
        else:
            return float(time_str)
    except:
        return 0.0


def get_video_duration(video_path: str) -> Optional[float]:
    """Get video duration using FFprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except Exception as e:
        st.warning(f"Could not determine video duration: {e}")
    return None


def trim_video(
    input_path: str,
    output_path: str,
    start_time: float,
    end_time: float,
    fast_seek: bool = True
) -> bool:
    """
    Trim video using FFmpeg.
    
    Args:
        input_path: Path to input video
        output_path: Path to output video
        start_time: Start time in seconds
        end_time: End time in seconds
        fast_seek: Use fast seek (less accurate but faster)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        duration = end_time - start_time
        
        if fast_seek:
            # Fast seek - seek before input (less accurate but faster)
            cmd = [
                "ffmpeg",
                "-ss", str(start_time),
                "-i", input_path,
                "-t", str(duration),
                "-c", "copy",  # Copy streams without re-encoding
                "-avoid_negative_ts", "make_zero",
                "-y",  # Overwrite output
                output_path
            ]
        else:
            # Accurate seek - decode from beginning (slower but accurate)
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-ss", str(start_time),
                "-t", str(duration),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-y",
                output_path
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and Path(output_path).exists():
            return True
        else:
            st.error(f"FFmpeg error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        st.error("FFmpeg not found. Please install FFmpeg to enable video trimming.")
        return False
    except Exception as e:
        st.error(f"Error trimming video: {e}")
        return False


def render_video_trimmer(
    video_path: str,
    video_id: str = "video",
    default_start: float = 0.0,
    default_end: Optional[float] = None
) -> Optional[Tuple[str, float, float]]:
    """
    Render video trimming UI component.
    
    Args:
        video_path: Path to the video file
        video_id: Unique identifier for this video (for session state keys)
        default_start: Default start time
        default_end: Default end time (None = video duration)
    
    Returns:
        Tuple of (trimmed_video_path, start_time, end_time) if trimmed, None otherwise
    """
    if not Path(video_path).exists():
        st.error(f"Video file not found: {video_path}")
        return None
    
    # Get video duration
    duration = get_video_duration(video_path)
    if duration is None:
        duration = 10.0  # Default fallback
        st.warning("Could not determine video duration. Using default of 10 seconds.")
    
    if default_end is None:
        default_end = duration
    
    st.markdown("### ✂️ Trim Video")
    st.write("Adjust the start and end times to trim your video.")
    
    # Video preview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with open(video_path, 'rb') as f:
            st.video(f.read())
    
    with col2:
        st.metric("Original Duration", f"{duration:.1f}s")
        st.caption(f"File: {Path(video_path).name}")
    
    st.markdown("---")
    
    # Trim controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        start_time = st.slider(
            "Start Time (seconds)",
            min_value=0.0,
            max_value=float(duration),
            value=float(default_start),
            step=0.1,
            key=f"trim_start_{video_id}"
        )
    
    with col2:
        end_time = st.slider(
            "End Time (seconds)",
            min_value=0.0,
            max_value=float(duration),
            value=float(min(default_end, duration)),
            step=0.1,
            key=f"trim_end_{video_id}"
        )
    
    with col3:
        trimmed_duration = max(0, end_time - start_time)
        st.metric("Trimmed Duration", f"{trimmed_duration:.1f}s")
        
        if trimmed_duration <= 0:
            st.error("Invalid trim range!")
        elif trimmed_duration < 1:
            st.warning("Very short clip!")
    
    # Visual timeline
    st.markdown("**Timeline:**")
    timeline_col1, timeline_col2, timeline_col3 = st.columns([
        max(0.01, start_time / duration),
        max(0.01, trimmed_duration / duration),
        max(0.01, (duration - end_time) / duration)
    ])
    
    with timeline_col1:
        if start_time > 0.1:
            st.markdown(f"<div style='background:#ccc;height:10px;border-radius:5px 0 0 5px;'></div>", unsafe_allow_html=True)
            st.caption("Cut")
    
    with timeline_col2:
        st.markdown(f"<div style='background:#0071CE;height:10px;'></div>", unsafe_allow_html=True)
        st.caption("Keep")
    
    with timeline_col3:
        if duration - end_time > 0.1:
            st.markdown(f"<div style='background:#ccc;height:10px;border-radius:0 5px 5px 0;'></div>", unsafe_allow_html=True)
            st.caption("Cut")
    
    st.markdown("---")
    
    # Trim options
    col1, col2 = st.columns(2)
    
    with col1:
        accurate_mode = st.checkbox(
            "Accurate mode (slower but precise)",
            value=False,
            help="Re-encodes video for frame-accurate trimming. Slower but more precise.",
            key=f"accurate_mode_{video_id}"
        )
    
    with col2:
        output_name = st.text_input(
            "Output filename",
            value=f"{Path(video_path).stem}_trimmed",
            key=f"output_name_{video_id}"
        )
    
    # AI Disclosure Watermark section (Legal Requirement)
    st.markdown("### 🏷️ AI Disclosure Watermark")
    st.caption("Legal requirement: AI-generated content must be clearly identified")
    
    watermark_col1, watermark_col2 = st.columns(2)
    
    with watermark_col1:
        watermark_option = st.selectbox(
            "Watermark Text",
            options=list(AI_WATERMARK_OPTIONS.keys()),
            format_func=lambda x: AI_WATERMARK_OPTIONS[x],
            index=1,  # Default to "AI Generated"
            key=f"watermark_option_{video_id}"
        )
        
        if watermark_option == "custom":
            custom_watermark = st.text_input(
                "Custom watermark text",
                value="AI Generated Content",
                max_chars=50,
                key=f"custom_watermark_{video_id}"
            )
    
    with watermark_col2:
        watermark_position = st.selectbox(
            "Position",
            options=list(AI_WATERMARK_POSITIONS.keys()),
            format_func=lambda x: AI_WATERMARK_POSITIONS[x],
            index=0,  # Default to bottom right
            key=f"watermark_position_{video_id}",
            disabled=(watermark_option == "none")
        )
    
    st.markdown("---")
    
    # Trim button
    if st.button("✂️ Trim & Export Video", type="primary", key=f"trim_button_{video_id}"):
        if trimmed_duration <= 0:
            st.error("Please select a valid trim range.")
            return None
        
        # Create output path
        output_dir = Path(video_path).parent
        output_path = output_dir / f"{output_name}.mp4"
        
        with st.spinner("Trimming video..."):
            success = trim_video(
                input_path=video_path,
                output_path=str(output_path),
                start_time=start_time,
                end_time=end_time,
                fast_seek=not accurate_mode
            )
        
        if success:
            final_video_path = output_path
            
            # Apply watermark if selected
            if watermark_option != "none":
                watermark_text = (
                    custom_watermark if watermark_option == "custom" 
                    else AI_WATERMARK_OPTIONS[watermark_option]
                )
                
                watermarked_path = output_dir / f"{output_name}_watermarked.mp4"
                
                with st.spinner("Adding AI disclosure watermark..."):
                    watermark_success = add_watermark_ffmpeg(
                        input_path=str(output_path),
                        output_path=str(watermarked_path),
                        text=watermark_text,
                        position=watermark_position
                    )
                
                if watermark_success:
                    final_video_path = watermarked_path
                    st.success(f"✅ Video trimmed and watermarked successfully!")
                else:
                    st.warning("⚠️ Could not add watermark, but trimming succeeded.")
            else:
                st.success(f"✅ Video trimmed successfully!")
                st.warning("⚠️ No AI disclosure watermark applied. Legal requires AI content identification.")
            
            st.session_state[f"trimmed_video_{video_id}"] = str(final_video_path)
            st.session_state[f"trim_start_{video_id}_result"] = start_time
            st.session_state[f"trim_end_{video_id}_result"] = end_time
            
            # Show trimmed video
            st.markdown("### 📹 Final Video")
            with open(final_video_path, 'rb') as f:
                st.video(f.read())
            
            # Download button
            with open(final_video_path, 'rb') as f:
                st.download_button(
                    "⬇️ Download Video",
                    f,
                    file_name=f"{output_name}.mp4",
                    mime="video/mp4",
                    key=f"download_trimmed_{video_id}"
                )
            
            return (str(final_video_path), start_time, end_time)
        else:
            st.error("Failed to trim video. Please check FFmpeg installation.")
            return None
    
    # Return existing trimmed video if available
    if f"trimmed_video_{video_id}" in st.session_state:
        return (
            st.session_state[f"trimmed_video_{video_id}"],
            st.session_state.get(f"trim_start_{video_id}_result", start_time),
            st.session_state.get(f"trim_end_{video_id}_result", end_time)
        )
    
    return None


def render_quick_trim_button(video_path: str, video_id: str = "video") -> Optional[str]:
    """
    Render a simple quick trim button that opens a modal-like interface.
    
    Args:
        video_path: Path to the video file
        video_id: Unique identifier for session state
    
    Returns:
        Path to trimmed video if available, None otherwise
    """
    with st.expander("✂️ Trim Video", expanded=False):
        result = render_video_trimmer(video_path, video_id)
        if result:
            return result[0]
    return None
