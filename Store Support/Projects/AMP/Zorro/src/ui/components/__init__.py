"""UI components for Zorro Video Generator."""

from .design_selector import (
    render_design_selector,
    render_design_preview,
    create_design_preset,
)
from .video_trimmer import (
    render_video_trimmer,
    render_quick_trim_button,
    trim_video,
    get_video_duration,
)

__all__ = [
    "render_design_selector",
    "render_design_preview", 
    "create_design_preset",
    "render_video_trimmer",
    "render_quick_trim_button",
    "trim_video",
    "get_video_duration",
]
