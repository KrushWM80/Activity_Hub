"""
Multi-Format Content Manager

Orchestrates generation of content in multiple formats: Video, Infographic, Audio/Podcast
Handles format selection, file optimization, and unified delivery.
"""

import json
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ContentFormat(Enum):
    """Supported content output formats."""
    VIDEO = "video"  # MP4, WebM
    INFOGRAPHIC = "infographic"  # HTML, PNG
    AUDIO = "audio"  # MP3, WAV, M4A (podcasts)
    DOCUMENT = "document"  # PDF, DOCX
    INTERACTIVE = "interactive"  # Interactive HTML


class ContentQuality(Enum):
    """Quality presets for all formats."""
    LOW = "low"  # Highly compressed, fast loading
    MEDIUM = "medium"  # Balanced quality/size
    HIGH = "high"  # Higher quality, larger files
    LOSSLESS = "lossless"  # Maximum quality


class MultiFormatContentManager:
    """
    Unified manager for generating content in multiple formats from single source.
    
    Capabilities:
    - Single input → Multiple format outputs
    - Automatic optimization for each format
    - Cross-format consistency
    - Unified file delivery
    - Format-specific metadata
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_cache = {}
        
    def create_multi_format_project(
        self,
        content: str,
        title: str,
        formats: List[ContentFormat],
        quality: ContentQuality = ContentQuality.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate content in multiple formats from a single source.
        
        Args:
            content: Source content/message
            title: Content title
            formats: List of output formats to generate
            quality: Quality level for all formats
            metadata: Additional metadata (author, tags, description, etc.)
            
        Returns:
            Dict with all generated files and metadata
        """
        
        project_id = self._generate_project_id(title)
        start_time = datetime.now()
        
        results = {
            "project_id": project_id,
            "title": title,
            "created": start_time.isoformat(),
            "formats_requested": [f.value for f in formats],
            "quality": quality.value,
            "outputs": {},
            "metadata": metadata or {},
            "assets": {"downloads": [], "previews": []},
        }
        
        # Generate each format
        for format_type in formats:
            logger.info(f"Generating {format_type.value} format...")
            
            try:
                if format_type == ContentFormat.VIDEO:
                    output = self._generate_video(content, title, quality)
                elif format_type == ContentFormat.INFOGRAPHIC:
                    output = self._generate_infographic(content, title, quality)
                elif format_type == ContentFormat.AUDIO:
                    output = self._generate_audio(content, title, quality)
                elif format_type == ContentFormat.DOCUMENT:
                    output = self._generate_document(content, title, quality)
                elif format_type == ContentFormat.INTERACTIVE:
                    output = self._generate_interactive(content, title, quality)
                else:
                    continue
                
                if output["success"]:
                    results["outputs"][format_type.value] = output
                    results["assets"]["downloads"].append({
                        "format": format_type.value,
                        "file": output.get("filename"),
                        "url": output.get("download_url"),
                        "size_mb": output.get("file_size_mb"),
                    })
                    
            except Exception as e:
                logger.error(f"Failed to generate {format_type.value}: {str(e)}")
                results["outputs"][format_type.value] = {"success": False, "error": str(e)}
        
        # Store project cache
        self.project_cache[project_id] = results
        
        return results
    
    def get_distribution_package(
        self,
        project_id: str,
        include_tracking: bool = True,
    ) -> Dict[str, Any]:
        """
        Get all files ready for distribution with tracking capabilities.
        """
        project = self.project_cache.get(project_id)
        
        if not project:
            return {"error": "Project not found"}
        
        package = {
            "project_id": project_id,
            "title": project["title"],
            "created": project["created"],
            "files": [],
            "metadata": project.get("metadata", {}),
        }
        
        # Build list of downloadable files
        for format_type, output in project["outputs"].items():
            if output.get("success"):
                file_info = {
                    "format": format_type,
                    "filename": output.get("filename"),
                    "download_url": output.get("download_url"),
                    "file_size_mb": output.get("file_size_mb"),
                    "mime_type": self._get_mime_type(format_type),
                }
                
                # Add tracking pixel/code if requested
                if include_tracking:
                    file_info["tracking_id"] = self._generate_tracking_id(project_id, format_type)
                    file_info["tracking_code"] = self._generate_tracking_code(file_info["tracking_id"])
                
                package["files"].append(file_info)
        
        return package
    
    def optimize_for_distribution(
        self,
        project_id: str,
        max_size_mb: int = 10,
    ) -> Dict[str, Any]:
        """
        Optimize all files in project to fit within size constraints.
        """
        project = self.project_cache.get(project_id)
        
        if not project:
            return {"error": "Project not found"}
        
        optimization_results = {
            "project_id": project_id,
            "optimization_applied": [],
            "total_original_size_mb": 0,
            "total_optimized_size_mb": 0,
        }
        
        for format_type, output in project["outputs"].items():
            if output.get("success"):
                original_size = output.get("file_size_mb", 0)
                optimization_results["total_original_size_mb"] += original_size
                
                # Apply format-specific optimization
                optimized = self._optimize_format(format_type, original_size, max_size_mb)
                optimization_results["optimization_applied"].append(optimized)
                optimization_results["total_optimized_size_mb"] += optimized["optimized_size_mb"]
        
        compression_ratio = (
            optimization_results["total_original_size_mb"] /
            optimization_results["total_optimized_size_mb"]
            if optimization_results["total_optimized_size_mb"] > 0
            else 0
        )
        
        optimization_results["total_compression_ratio"] = round(compression_ratio, 2)
        
        return optimization_results
    
    def _generate_video(self, content: str, title: str, quality: ContentQuality) -> Dict[str, Any]:
        """Generate video format."""
        # Would integrate with Zorro's VideoGenerationPipeline
        return {
            "success": True,
            "filename": f"{title}_video.mp4",
            "download_url": f"/files/{title}_video.mp4",
            "file_size_mb": self._calculate_video_size(quality),
            "duration_seconds": 30,
            "format": "mp4",
            "codec": "h264",
        }
    
    def _generate_infographic(self, content: str, title: str, quality: ContentQuality) -> Dict[str, Any]:
        """Generate infographic format."""
        # Would integrate with AMP Infographic system
        return {
            "success": True,
            "filename": f"{title}_infographic.html",
            "download_url": f"/files/{title}_infographic.html",
            "file_size_mb": self._calculate_infographic_size(quality),
            "format": "html",
            "mobile_optimized": True,
            "also_available": ["png", "pdf"],
        }
    
    def _generate_audio(self, content: str, title: str, quality: ContentQuality) -> Dict[str, Any]:
        """Generate audio/podcast format."""
        # Would integrate with AudioPodcastService
        duration = int(len(content.split()) / 140 * 60)  # Estimate duration
        return {
            "success": True,
            "filename": f"{title}_podcast.mp3",
            "download_url": f"/files/{title}_podcast.mp3",
            "file_size_mb": self._calculate_audio_size(quality),
            "duration_seconds": duration,
            "format": "mp3",
            "also_available": ["wav", "m4a", "aac"],
        }
    
    def _generate_document(self, content: str, title: str, quality: ContentQuality) -> Dict[str, Any]:
        """Generate document format."""
        return {
            "success": True,
            "filename": f"{title}_document.pdf",
            "download_url": f"/files/{title}_document.pdf",
            "file_size_mb": self._calculate_document_size(quality),
            "format": "pdf",
            "also_available": ["docx", "txt"],
        }
    
    def _generate_interactive(self, content: str, title: str, quality: ContentQuality) -> Dict[str, Any]:
        """Generate interactive HTML format."""
        return {
            "success": True,
            "filename": f"{title}_interactive.html",
            "download_url": f"/files/{title}_interactive.html",
            "file_size_mb": self._calculate_interactive_size(quality),
            "format": "html",
            "interactive_elements": True,
        }
    
    def _optimize_format(self, format_type: str, original_size_mb: float, max_size_mb: int) -> Dict[str, Any]:
        """Apply optimization to a specific format."""
        optimization_strategies = {
            "video": {"compression": "h265", "resolution": "720p"},
            "infographic": {"minify": True, "image_compression": "webp"},
            "audio": {"bitrate_reduction": "128k"},
            "document": {"no_optimization": True},
            "interactive": {"minify_js": True, "compress_images": True},
        }
        
        strategy = optimization_strategies.get(format_type, {})
        
        # Calculate new size (simplified)
        if format_type == "video":
            optimized_size = original_size_mb * 0.6  # 40% reduction
        elif format_type == "audio":
            optimized_size = original_size_mb * 0.75  # 25% reduction
        elif format_type == "infographic":
            optimized_size = original_size_mb * 0.4  # 60% reduction
        else:
            optimized_size = original_size_mb
        
        return {
            "format": format_type,
            "strategy": strategy,
            "original_size_mb": original_size_mb,
            "optimized_size_mb": round(optimized_size, 2),
            "compression_savings_percent": round((1 - optimized_size / original_size_mb) * 100, 1),
        }
    
    def _calculate_video_size(self, quality: ContentQuality) -> float:
        """Estimate video file size based on quality."""
        sizes = {
            ContentQuality.LOW: 15,
            ContentQuality.MEDIUM: 35,
            ContentQuality.HIGH: 75,
            ContentQuality.LOSSLESS: 150,
        }
        return sizes.get(quality, 35)
    
    def _calculate_infographic_size(self, quality: ContentQuality) -> float:
        """Estimate infographic file size."""
        sizes = {
            ContentQuality.LOW: 0.5,
            ContentQuality.MEDIUM: 1.5,
            ContentQuality.HIGH: 3.0,
            ContentQuality.LOSSLESS: 5.0,
        }
        return sizes.get(quality, 1.5)
    
    def _calculate_audio_size(self, quality: ContentQuality) -> float:
        """Estimate audio file size for 30-second podcast."""
        sizes = {
            ContentQuality.LOW: 0.25,  # 64k bitrate
            ContentQuality.MEDIUM: 0.5,  # 128k bitrate
            ContentQuality.HIGH: 0.75,  # 192k bitrate
            ContentQuality.LOSSLESS: 1.25,  # 320k bitrate
        }
        return sizes.get(quality, 0.5)
    
    def _calculate_document_size(self, quality: ContentQuality) -> float:
        """Estimate document file size."""
        return 0.3  # Relatively small regardless of quality
    
    def _calculate_interactive_size(self, quality: ContentQuality) -> float:
        """Estimate interactive HTML file size."""
        sizes = {
            ContentQuality.LOW: 0.8,
            ContentQuality.MEDIUM: 2.0,
            ContentQuality.HIGH: 4.0,
            ContentQuality.LOSSLESS: 8.0,
        }
        return sizes.get(quality, 2.0)
    
    def _generate_project_id(self, title: str) -> str:
        """Generate unique project ID."""
        import hashlib
        timestamp = datetime.now().isoformat()
        combined = f"{title}_{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]
    
    def _generate_tracking_id(self, project_id: str, format_type: str) -> str:
        """Generate unique tracking ID for file."""
        import hashlib
        combined = f"{project_id}_{format_type}_{datetime.now().isoformat()}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _generate_tracking_code(self, tracking_id: str) -> str:
        """Generate JavaScript tracking code snippet."""
        return f"""
        <script>
          (function() {{
            const trackingId = '{tracking_id}';
            // Tracking code would be injected here
            window.contentTracking = window.contentTracking || {{}};
            window.contentTracking.id = trackingId;
          }})();
        </script>
        """
    
    def _get_mime_type(self, format_type: str) -> str:
        """Get MIME type for format."""
        mime_types = {
            "video": "video/mp4",
            "infographic": "text/html",
            "audio": "audio/mpeg",
            "document": "application/pdf",
            "interactive": "text/html",
        }
        return mime_types.get(format_type, "application/octet-stream")
