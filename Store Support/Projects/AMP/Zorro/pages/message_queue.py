"""
AMP Message Queue - Production Video Generation Workflow

This page provides a streamlined queue-based workflow for:
1. Viewing incoming AMP (Activity Message Platform) messages
2. Selecting messages for video generation
3. Choosing design elements (characters, backgrounds)
4. Generating and downloading videos
5. Tracking production status
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from src.services.design_studio_service import DesignStudioService
from src.core.pipeline import VideoGenerationPipeline
from src.models.design_element import DesignElementType
from src.ui.components.video_trimmer import render_video_trimmer, render_quick_trim_button


# Page configuration
st.set_page_config(
    page_title="Message Queue - Zorro",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .queue-header {
        font-size: 2rem;
        color: #0071CE;
        margin-bottom: 1rem;
    }
    .message-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #0071CE;
        margin-bottom: 1rem;
    }
    .priority-critical { border-left-color: #dc3545 !important; }
    .priority-high { border-left-color: #fd7e14 !important; }
    .priority-medium { border-left-color: #ffc107 !important; }
    .priority-low { border-left-color: #28a745 !important; }
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-pending { background-color: #ffc107; color: black; }
    .status-processing { background-color: #17a2b8; color: white; }
    .status-completed { background-color: #28a745; color: white; }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "design_service" not in st.session_state:
        st.session_state.design_service = DesignStudioService()
    if "amp_messages" not in st.session_state:
        st.session_state.amp_messages = load_amp_messages()
    if "selected_messages" not in st.session_state:
        st.session_state.selected_messages = []
    if "production_queue" not in st.session_state:
        st.session_state.production_queue = []
    if "completed_videos" not in st.session_state:
        st.session_state.completed_videos = []
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = None
    if "selected_character" not in st.session_state:
        st.session_state.selected_character = None
    if "selected_background" not in st.session_state:
        st.session_state.selected_background = None


def load_amp_messages() -> List[Dict]:
    """Load AMP messages from JSON file."""
    try:
        amp_file = Path("data/sample_amp_messages.json")
        if amp_file.exists():
            with open(amp_file, 'r') as f:
                data = json.load(f)
                return data.get("messages", [])
    except Exception as e:
        st.error(f"Error loading messages: {e}")
    return []


def save_amp_messages(messages: List[Dict]):
    """Save AMP messages back to JSON file."""
    try:
        amp_file = Path("data/sample_amp_messages.json")
        data = {
            "messages": messages,
            "metadata": {
                "last_sync": datetime.now().isoformat(),
                "source": "AMP System Demo Data",
                "version": "1.0"
            }
        }
        with open(amp_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving messages: {e}")


def get_priority_color(priority: str) -> str:
    """Get color class for priority level."""
    colors = {
        "critical": "priority-critical",
        "high": "priority-high",
        "medium": "priority-medium",
        "low": "priority-low"
    }
    return colors.get(priority.lower(), "")


def get_priority_emoji(priority: str) -> str:
    """Get emoji for priority level."""
    emojis = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }
    return emojis.get(priority.lower(), "⚪")


def get_category_emoji(category: str) -> str:
    """Get emoji for message category."""
    emojis = {
        "training": "📚",
        "safety": "🦺",
        "announcement": "📢",
        "recognition": "⭐",
        "operational": "⚙️",
        "celebration": "🎉",
        "reminder": "📝"
    }
    return emojis.get(category.lower(), "📋")


def render_message_card(message: Dict, show_select: bool = True) -> bool:
    """Render a single message card. Returns True if selected."""
    priority_class = get_priority_color(message.get("priority", "medium"))
    priority_emoji = get_priority_emoji(message.get("priority", "medium"))
    category_emoji = get_category_emoji(message.get("category", "general"))
    
    with st.container():
        col1, col2, col3 = st.columns([0.5, 4, 1])
        
        with col1:
            if show_select:
                selected = st.checkbox(
                    "Select",
                    key=f"select_{message['id']}",
                    label_visibility="collapsed"
                )
            else:
                selected = False
        
        with col2:
            st.markdown(f"**{category_emoji} {message.get('title', 'Untitled')}**")
            st.caption(f"{priority_emoji} {message.get('priority', 'medium').upper()} | 📤 {message.get('source', 'Unknown')} | 👥 {message.get('target_audience', 'All')}")
            st.write(message.get("content", "")[:200] + ("..." if len(message.get("content", "")) > 200 else ""))
        
        with col3:
            status = message.get("status", "pending")
            if status == "completed":
                st.success("✅ Done")
            elif status == "processing":
                st.info("⏳ Processing")
            else:
                if message.get("due_date"):
                    st.caption(f"📅 Due: {message.get('due_date')}")
        
        st.markdown("---")
        return selected


def render_design_selector() -> Dict[str, Any]:
    """Render compact design element selector. Returns selected elements."""
    service = st.session_state.design_service
    
    selected = {
        "character": None,
        "background": None
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎭 Character**")
        characters = service.get_elements_by_type(DesignElementType.CHARACTER)
        if characters:
            char_options = ["None"] + [c.name for c in characters]
            char_choice = st.selectbox(
                "Select character",
                char_options,
                key="queue_character",
                label_visibility="collapsed"
            )
            if char_choice != "None":
                selected["character"] = next((c for c in characters if c.name == char_choice), None)
                if selected["character"]:
                    st.caption(f"📝 {selected['character'].description[:100]}...")
        else:
            st.caption("No characters available. Create some in Design Studio!")
    
    with col2:
        st.markdown("**🏞️ Background**")
        backgrounds = service.get_elements_by_type(DesignElementType.ENVIRONMENT)
        if backgrounds:
            bg_options = ["None"] + [b.name for b in backgrounds]
            bg_choice = st.selectbox(
                "Select background",
                bg_options,
                key="queue_background",
                label_visibility="collapsed"
            )
            if bg_choice != "None":
                selected["background"] = next((b for b in backgrounds if b.name == bg_choice), None)
                if selected["background"]:
                    st.caption(f"📝 {selected['background'].description[:100]}...")
        else:
            st.caption("No backgrounds available. Create some in Design Studio!")
    
    # Save as template option
    if selected["character"] or selected["background"]:
        st.markdown("---")
        with st.expander("💾 Save as Production Template"):
            template_name = st.text_input("Template name", key="new_template_name")
            template_desc = st.text_area("Description (optional)", key="new_template_desc", height=80)
            template_category = st.selectbox(
                "Target category",
                ["all", "training", "safety", "announcement", "recognition", "operational", "celebration"],
                key="new_template_category"
            )
            
            if st.button("💾 Save Template", key="save_template_btn"):
                if template_name:
                    template = service.create_production_template(
                        name=template_name,
                        created_by=st.session_state.get("user_id", "demo_user"),
                        description=template_desc if template_desc else None,
                        category=template_category if template_category != "all" else None,
                        character_id=selected["character"].id if selected["character"] else None,
                        environment_id=selected["background"].id if selected["background"] else None
                    )
                    if template:
                        st.success(f"✅ Template '{template_name}' saved!")
                    else:
                        st.error("Failed to save template")
                else:
                    st.warning("Please enter a template name")
    
    return selected


def render_template_selector() -> Optional[Any]:
    """Render production template selector. Returns selected template."""
    service = st.session_state.design_service
    templates = service.list_templates()
    
    if not templates:
        return None
    
    st.markdown("**📋 Or use a Production Template:**")
    template_options = ["None"] + [f"{t.name} ({t.usage_count} uses)" for t in templates]
    template_choice = st.selectbox(
        "Select template",
        template_options,
        key="queue_template",
        label_visibility="collapsed"
    )
    
    if template_choice != "None":
        # Extract template name
        template_name = template_choice.split(" (")[0]
        selected_template = next((t for t in templates if t.name == template_name), None)
        
        if selected_template:
            st.caption(f"📝 {selected_template.description or 'No description'}")
            
            # Show template elements
            elements = service.get_template_elements(selected_template)
            cols = st.columns(4)
            with cols[0]:
                if elements.get("character"):
                    st.caption(f"🎭 {elements['character'].name}")
            with cols[1]:
                if elements.get("environment"):
                    st.caption(f"🏞️ {elements['environment'].name}")
            
            return selected_template
    
    return None


def generate_composite_prompt(message: Dict, design_elements: Dict) -> str:
    """Generate a composite prompt from message and design elements."""
    parts = []
    
    # Add character prompt
    if design_elements.get("character"):
        parts.append(design_elements["character"].prompt_template)
    
    # Add background/environment prompt
    if design_elements.get("background"):
        parts.append(design_elements["background"].prompt_template)
    
    # Add message content
    parts.append(message.get("content", ""))
    
    return " ".join(parts)


def initialize_pipeline():
    """Initialize the video generation pipeline."""
    if st.session_state.pipeline is None:
        try:
            st.session_state.pipeline = VideoGenerationPipeline()
            return True
        except Exception as e:
            st.error(f"Failed to initialize pipeline: {str(e)}")
            return False
    return True


def process_single_message(message: Dict, design_elements: Dict) -> Optional[Dict]:
    """Process a single message and generate video."""
    try:
        if not initialize_pipeline():
            return None
        
        # Generate composite prompt
        composite_prompt = generate_composite_prompt(message, design_elements)
        
        # Generate video
        result = st.session_state.pipeline.generate(
            message_content=composite_prompt,
            message_category=message.get("category", "general"),
            message_priority=message.get("priority", "medium"),
            apply_editing=True,
            add_accessibility=True,
            skip_llm_enhancement=True  # Use passthrough mode
        )
        
        if result and result.path:
            return {
                "message_id": message.get("id"),
                "message_title": message.get("title"),
                "video_id": result.id,
                "video_path": result.path,
                "duration": result.duration,
                "generated_at": datetime.now().isoformat(),
                "design_elements": {
                    "character": design_elements.get("character").name if design_elements.get("character") else None,
                    "background": design_elements.get("background").name if design_elements.get("background") else None
                }
            }
    except Exception as e:
        st.error(f"Error generating video: {e}")
    
    return None


def render_queue_tab():
    """Render the message queue tab."""
    st.markdown("### 📋 Message Queue")
    st.write("Select messages from the queue to generate videos.")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_category = st.selectbox(
            "Category",
            ["All", "training", "safety", "announcement", "recognition", "operational", "celebration"],
            key="filter_category"
        )
    
    with col2:
        filter_priority = st.selectbox(
            "Priority",
            ["All", "critical", "high", "medium", "low"],
            key="filter_priority"
        )
    
    with col3:
        filter_status = st.selectbox(
            "Status",
            ["All", "pending", "processing", "completed"],
            key="filter_status"
        )
    
    with col4:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.amp_messages = load_amp_messages()
            st.rerun()
    
    st.markdown("---")
    
    # Filter messages
    messages = st.session_state.amp_messages
    
    if filter_category != "All":
        messages = [m for m in messages if m.get("category", "").lower() == filter_category.lower()]
    
    if filter_priority != "All":
        messages = [m for m in messages if m.get("priority", "").lower() == filter_priority.lower()]
    
    if filter_status != "All":
        messages = [m for m in messages if m.get("status", "pending").lower() == filter_status.lower()]
    
    # Display messages
    if not messages:
        st.info("No messages match the current filters.")
    else:
        st.write(f"Showing {len(messages)} messages")
        
        # Select all / deselect all
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("☑️ Select All"):
                for m in messages:
                    st.session_state[f"select_{m['id']}"] = True
                st.rerun()
        with col2:
            if st.button("☐ Deselect All"):
                for m in messages:
                    st.session_state[f"select_{m['id']}"] = False
                st.rerun()
        
        st.markdown("---")
        
        # Render message cards
        selected_ids = []
        for message in messages:
            if st.session_state.get(f"select_{message['id']}", False):
                selected_ids.append(message["id"])
            render_message_card(message)
        
        # Store selected messages
        st.session_state.selected_messages = [m for m in messages if m["id"] in selected_ids]


def render_production_tab():
    """Render the production workflow tab."""
    st.markdown("### 🎬 Production Workflow")
    
    selected = st.session_state.selected_messages
    
    if not selected:
        st.info("👈 Select messages from the Queue tab to start production.")
        return
    
    st.success(f"✅ {len(selected)} message(s) selected for production")
    
    # Step 1: Review selected messages
    with st.expander("📋 Selected Messages", expanded=True):
        for msg in selected:
            st.write(f"**{get_category_emoji(msg.get('category', ''))} {msg.get('title')}**")
            st.caption(msg.get("content", "")[:150] + "...")
    
    st.markdown("---")
    
    # Step 2: Select design elements OR use a template
    st.markdown("#### 🎨 Step 2: Choose Design Elements")
    
    # Option to use a saved template
    selected_template = render_template_selector()
    
    if selected_template:
        st.success(f"✅ Using template: **{selected_template.name}**")
        design_elements = st.session_state.design_service.get_template_elements(selected_template)
        st.session_state.using_template = selected_template
    else:
        st.write("Or manually select character and background:")
        design_elements = render_design_selector()
        st.session_state.using_template = None
    
    st.markdown("---")
    
    # Step 3: Generate videos
    st.markdown("#### 🎬 Step 3: Generate Videos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Generate All Videos", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            for i, message in enumerate(selected):
                status_text.text(f"Processing: {message.get('title')} ({i+1}/{len(selected)})")
                progress_bar.progress((i + 1) / len(selected))
                
                result = process_single_message(message, design_elements)
                if result:
                    results.append(result)
                    
                    # Update message status
                    for m in st.session_state.amp_messages:
                        if m["id"] == message["id"]:
                            m["status"] = "completed"
                            break
            
            # Save results
            st.session_state.completed_videos.extend(results)
            save_amp_messages(st.session_state.amp_messages)
            
            status_text.text(f"✅ Completed! {len(results)}/{len(selected)} videos generated.")
            st.balloons()
            
            # Clear selection
            st.session_state.selected_messages = []
    
    with col2:
        st.metric("Videos to Generate", len(selected))


def render_completed_tab():
    """Render the completed videos tab."""
    st.markdown("### ✅ Completed Videos")
    
    completed = st.session_state.completed_videos
    
    if not completed:
        st.info("No videos generated yet. Use the Production tab to create videos.")
        return
    
    st.write(f"Showing {len(completed)} completed videos")
    
    for idx, video in enumerate(reversed(completed)):  # Show newest first
        video_id = video.get('video_id', f'video_{idx}')
        with st.expander(f"🎬 {video.get('message_title', 'Untitled')} - {video.get('generated_at', '')[:10]}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                video_path = video.get("video_path")
                if video_path and Path(video_path).exists():
                    with open(video_path, 'rb') as f:
                        st.video(f.read())
                    
                    # Trim video option
                    st.markdown("---")
                    trimmed = render_quick_trim_button(video_path, video_id)
                    if trimmed:
                        st.success(f"✅ Trimmed video saved!")
                else:
                    st.warning("Video file not found")
            
            with col2:
                st.write("**Details:**")
                st.write(f"📋 Message ID: {video.get('message_id')}")
                st.write(f"⏱️ Duration: {video.get('duration', 'N/A')}s")
                
                design = video.get("design_elements", {})
                if design.get("character"):
                    st.write(f"🎭 Character: {design['character']}")
                if design.get("background"):
                    st.write(f"🏞️ Background: {design['background']}")
                
                # Download button
                if video_path and Path(video_path).exists():
                    with open(video_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Download Original",
                            f,
                            file_name=f"{video_id}.mp4",
                            mime="video/mp4",
                            key=f"download_{video_id}"
                        )
    
    # Clear completed videos
    if st.button("🗑️ Clear Completed Videos"):
        st.session_state.completed_videos = []
        st.rerun()


def render_sidebar():
    """Render the sidebar with stats and quick actions."""
    with st.sidebar:
        st.markdown("## 📋 Message Queue")
        st.markdown("### Production Dashboard")
        st.markdown("---")
        
        # Stats
        messages = st.session_state.amp_messages
        pending = len([m for m in messages if m.get("status") == "pending"])
        completed = len([m for m in messages if m.get("status") == "completed"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pending", pending)
        with col2:
            st.metric("Completed", completed)
        
        st.metric("Selected", len(st.session_state.selected_messages))
        st.metric("Videos Ready", len(st.session_state.completed_videos))
        
        st.markdown("---")
        
        # Quick filters
        st.markdown("### Quick Filters")
        
        if st.button("🔴 Critical Only", use_container_width=True):
            st.session_state.filter_priority = "critical"
            st.rerun()
        
        if st.button("📚 Training Only", use_container_width=True):
            st.session_state.filter_category = "training"
            st.rerun()
        
        if st.button("🦺 Safety Only", use_container_width=True):
            st.session_state.filter_category = "safety"
            st.rerun()
        
        st.markdown("---")
        
        # Links
        st.markdown("### 🔗 Quick Links")
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/design_studio.py", label="🎨 Design Studio", icon="🎨")


def main():
    """Main application."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="queue-header">📋 AMP Message Queue</h1>', unsafe_allow_html=True)
    st.markdown("Transform operational messages into professional video content")
    
    # Sidebar
    render_sidebar()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📋 Queue", "🎬 Production", "✅ Completed"])
    
    with tab1:
        render_queue_tab()
    
    with tab2:
        render_production_tab()
    
    with tab3:
        render_completed_tab()
    
    # Footer
    st.markdown("---")
    st.caption("Zorro AI Video Generator | AMP Message Queue v1.0")


if __name__ == "__main__":
    main()
