"""
Zorro Video Generator - Web GUI
A Streamlit-based web interface for generating videos from activity messages.
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.pipeline import VideoGenerationPipeline
from src.models.message import MessageCategory, MessagePriority
from src.services.design_studio_service import DesignStudioService
from src.ui.components.design_selector import (
    render_design_selector,
    render_design_preview,
    _generate_composite_prompt,
    create_design_preset
)
from src.ui.components.video_trimmer import render_quick_trim_button

# Page configuration
st.set_page_config(
    page_title="Zorro - AI Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #0071CE;
        text-align: center;
        padding: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .stButton>button {
        width: 100%;
        background-color: #0071CE;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'preset_message' not in st.session_state:
    st.session_state.preset_message = ""
if 'design_service' not in st.session_state:
    st.session_state.design_service = DesignStudioService()
if 'selected_elements' not in st.session_state:
    st.session_state.selected_elements = {}

def initialize_pipeline():
    """Initialize the video generation pipeline."""
    if st.session_state.pipeline is None:
        with st.spinner("Initializing AI pipeline..."):
            try:
                st.session_state.pipeline = VideoGenerationPipeline()
                st.success("✅ Pipeline initialized (Walmart Media Studio)")
                return True
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Failed to initialize pipeline")
                
                # Specific error guidance
                if "SSL" in error_msg or "verify_ssl" in error_msg or "ssl_verify" in error_msg:
                    st.warning("SSL configuration issue - check WALMART_SSL_VERIFY setting")
                elif "walmart_media_studio" in error_msg or "retina" in error_msg:
                    st.warning("Cannot connect to Walmart Media Studio - ensure VPN is connected")
                elif "huggingface" in error_msg.lower():
                    st.warning("HuggingFace connection blocked - using Walmart Media Studio instead")
                
                with st.expander("Error details"):
                    st.code(error_msg)
                return False
    return True

def main():
    """Main application."""
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Zorro AI Video Generator</h1>', unsafe_allow_html=True)
    st.markdown("### Transform Walmart activity messages into engaging videos")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎬 Zorro")
        st.markdown("### Walmart Video Generator")
        st.markdown("---")
        st.title("⚙️ Settings")
        
        # Provider selection
        provider = st.selectbox(
            "Video Provider",
            ["walmart_media_studio", "modelscope", "stability", "runwayml"],
            help="Select the AI video generation provider (Walmart Media Studio recommended)"
        )
        
        # Show provider status
        if provider == "walmart_media_studio":
            st.info("✅ **Walmart GenAI Media Studio** - Pre-approved, no firewall restrictions")
            st.caption("🔗 https://mediagenai.walmart.com/ | 💬 #help-genai-media-studio")
        else:
            st.warning("⚠️ External provider - May be blocked by Walmart firewall")
        
        # Video settings
        st.subheader("Video Settings")
        apply_editing = st.checkbox("Apply editing (fades)", value=True)
        add_accessibility = st.checkbox("Add accessibility features", value=True)
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            video_duration = st.slider("Video Duration (seconds)", 4, 8, 5, help="API supports 4-8 seconds")
            add_fade = st.checkbox("Add fade transitions", value=True)
            trim_enabled = st.checkbox("Enable trimming", value=False)
            if trim_enabled:
                trim_duration = st.slider("Trim to (seconds)", 4, 8, 5)
        
        st.markdown("---")
        st.info("💡 Tip: Messages with Walmart abbreviations (CBL, OBW, GWP) will be automatically expanded")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🎥 Generate Video", "📊 History", "ℹ️ About"])
    
    with tab1:
        # Quick presets
        st.subheader("Quick Presets")
        col1, col2, col3, col4 = st.columns(4)
        
        preset_messages = {
            "Training": "Complete your annual safety training by Friday",
            "Recognition": "Congratulations on achieving 100% customer satisfaction!",
            "Alert": "Emergency evacuation drill scheduled for 2 PM today",
            "Reminder": "Don't forget to complete your CBL modules this week"
        }
        
        with col1:
            if st.button("📚 Training Example"):
                st.session_state.preset_message = preset_messages["Training"]
        with col2:
            if st.button("⭐ Recognition Example"):
                st.session_state.preset_message = preset_messages["Recognition"]
        with col3:
            if st.button("🚨 Alert Example"):
                st.session_state.preset_message = preset_messages["Alert"]
        with col4:
            if st.button("📝 Reminder Example"):
                st.session_state.preset_message = preset_messages["Reminder"]
        
        st.markdown("---")
        
        # Message input form
        st.subheader("Message Details")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            message_content = st.text_area(
                "Activity Message",
                value=st.session_state.preset_message,
                height=150,
                max_chars=500,
                help="Enter your activity message (10-500 characters)",
                placeholder="Example: Complete your CBL training and review OBW procedures by Friday"
            )
            
            char_count = len(message_content)
            if char_count < 10:
                st.warning(f"⚠️ Message too short ({char_count}/10 minimum)")
            elif char_count > 500:
                st.error(f"❌ Message too long ({char_count}/500 maximum)")
            else:
                st.success(f"✅ Message length: {char_count} characters")
        
        with col2:
            category = st.selectbox(
                "Category",
                ["training", "recognition", "announcement", "alert", "reminder", "celebration", "general"],
                help="Select the message category"
            )
            
            priority = st.selectbox(
                "Priority",
                ["low", "medium", "high", "critical"],
                index=1,
                help="Select the message priority"
            )
            
            sender_id = st.text_input(
                "Sender ID (optional)",
                placeholder="e.g., SM_12345",
                help="Identifier of the message sender"
            )
        
        # Design element selection
        st.markdown("---")
        st.subheader("🎨 Design Elements (Optional)")
        st.write("Enhance your video with consistent brand design elements")
        
        use_design = st.checkbox("Use design elements for this video", value=False)
        
        if use_design:
            # Get available designs
            service = st.session_state.design_service
            stats = service.get_statistics()
            
            if stats["total_elements"] == 0:
                st.info("📚 No design elements available yet. Create some in the Design Studio!")
            else:
                # Render design selector
                selected_elements = render_design_selector(service)
                st.session_state.selected_elements = selected_elements
                
                # Show preview
                composite_prompt = render_design_preview(selected_elements)
                
                # Option to save as preset
                if any(selected_elements.values()):
                    if st.checkbox("Save this combination as a preset for reuse"):
                        preset_name = st.text_input("Preset name")
                        if preset_name and st.button("💾 Save Preset"):
                            if create_design_preset(
                                service,
                                preset_name,
                                selected_elements,
                                st.session_state.get("user_id", "demo_user")
                            ):
                                st.success(f"Preset '{preset_name}' saved!")
        
        # Generate button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            generate_clicked = st.button(
                "🎬 Generate Video",
                type="primary",
                use_container_width=True
            )
        
        # Generation logic
        if generate_clicked:
            if not message_content or len(message_content) < 10:
                st.error("❌ Please enter a valid message (at least 10 characters)")
            else:
                # Initialize pipeline
                if not initialize_pipeline():
                    st.error("❌ Failed to initialize video generation pipeline")
                else:
                    # Generate video
                    with st.spinner("🎨 Generating your video... This may take 30-60 seconds..."):
                        try:
                            # Prepare generation parameters
                            gen_params = {
                                "message_content": message_content,
                                "message_category": category,
                                "message_priority": priority,
                                "apply_editing": apply_editing,
                                "add_accessibility": add_accessibility,
                            }
                            
                            if sender_id:
                                gen_params["sender_id"] = sender_id
                            
                            if trim_enabled:
                                gen_params["trim_duration"] = trim_duration
                            
                            # Add design elements to prompt if selected
                            if use_design and st.session_state.selected_elements:
                                design_elements = st.session_state.selected_elements
                                active_elements = [e for e in design_elements.values() if e is not None]
                                
                                if active_elements:
                                    # Generate composite prompt from design elements
                                    composite_prompt = _generate_composite_prompt(design_elements)
                                    # Prepend design prompt to message
                                    gen_params["message_content"] = f"{composite_prompt}\n\n{message_content}"
                                    gen_params["design_elements"] = [e.id for e in active_elements]
                            
                            # Generate
                            result = st.session_state.pipeline.generate(**gen_params)
                            
                            # Success!
                            st.balloons()
                            
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.success("✅ Video generated successfully!")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Display results
                            st.subheader("📹 Generated Video")
                            
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                # Video player
                                if Path(result.path).exists():
                                    video_file = open(result.path, 'rb')
                                    video_bytes = video_file.read()
                                    st.video(video_bytes)
                                    
                                    # Video trimming option
                                    st.markdown("---")
                                    render_quick_trim_button(result.path, result.id)
                                else:
                                    st.warning("⚠️ Video file not found (may be generated asynchronously)")
                                    st.info(f"📁 Video path: {result.path}")
                            
                            with col2:
                                st.metric("Video ID", result.id)
                                st.metric("Duration", f"{result.duration:.1f}s" if result.duration else "N/A")
                                model_name = result.generation_params.get("model", "unknown")
                                st.metric("Model Used", model_name)
                                
                                # Download buttons
                                st.markdown("### 📥 Downloads")
                                
                                if Path(result.path).exists():
                                    with open(result.path, 'rb') as f:
                                        st.download_button(
                                            "⬇️ Download Video",
                                            f,
                                            file_name=f"{result.id}.mp4",
                                            mime="video/mp4"
                                        )
                                
                                # Accessibility files
                                if result.accessibility:
                                    if result.accessibility.captions_path and Path(result.accessibility.captions_path).exists():
                                        with open(result.accessibility.captions_path, 'r') as f:
                                            st.download_button(
                                                "⬇️ Download Captions",
                                                f,
                                                file_name=f"{result.id}.vtt",
                                                mime="text/vtt"
                                            )
                                    
                                    if result.accessibility.transcript_path and Path(result.accessibility.transcript_path).exists():
                                        with open(result.accessibility.transcript_path, 'r') as f:
                                            st.download_button(
                                                "⬇️ Download Transcript",
                                                f,
                                                file_name=f"{result.id}_transcript.txt",
                                                mime="text/plain"
                                            )
                            
                            # Accessibility features
                            if result.accessibility and add_accessibility:
                                st.markdown("---")
                                st.subheader("♿ Accessibility Features")
                                
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    if result.accessibility.has_captions:
                                        st.success("✅ Captions")
                                    else:
                                        st.warning("⚠️ No captions")
                                
                                with col2:
                                    if result.accessibility.has_audio_description:
                                        st.success("✅ Audio Description")
                                    else:
                                        st.warning("⚠️ No audio")
                                
                                with col3:
                                    st.info(f"📊 WCAG: {result.accessibility.wcag_level}")
                                
                                with col4:
                                    if result.accessibility.screen_reader_compatible:
                                        st.success("✅ Screen Reader")
                                    else:
                                        st.warning("⚠️ Not compatible")
                            
                            # Add to history
                            st.session_state.generation_history.insert(0, {
                                "timestamp": datetime.now().isoformat(),
                                "message": message_content[:50] + "..." if len(message_content) > 50 else message_content,
                                "category": category,
                                "priority": priority,
                                "video_id": result.id,
                                "video_path": result.path,
                                "duration": result.duration,
                                "model": result.generation_params.get("model", "unknown")
                            })
                            
                            # Keep only last 10
                            st.session_state.generation_history = st.session_state.generation_history[:10]
                        
                        except Exception as e:
                            st.markdown('<div class="error-box">', unsafe_allow_html=True)
                            error_msg = str(e)
                            
                            # Check for common issues and provide helpful guidance
                            if "huggingface.co" in error_msg or "not cached locally" in error_msg:
                                st.error("❌ Network Connection Issue")
                                st.warning("⚠️ Cannot connect to HuggingFace to download AI models (blocked by Walmart firewall)")
                                st.info("""
                                **Possible Solutions:**
                                1. Switch to Walmart Media Studio provider (internal API, no downloads needed)
                                2. Use outside network to download models first
                                3. Contact IT for huggingface.co whitelisting
                                """)
                            elif "walmart_media_studio" in error_msg or "retina-ds-genai" in error_msg:
                                st.error("❌ Walmart Media Studio Connection Issue")
                                st.warning("⚠️ Cannot connect to Walmart Media Studio API")
                                st.info("""
                                **Possible Issues:**
                                1. Not connected to Walmart internal network/VPN
                                2. API endpoint may be temporarily unavailable
                                3. SSO authentication may be required
                                
                                **For Demo:** Use mock mode or check VPN connection.
                                """)
                            elif "SSL" in error_msg or "certificate" in error_msg.lower():
                                st.error("❌ SSL/Certificate Issue")
                                st.info("Set WALMART_SSL_VERIFY=false for development or configure WALMART_CA_BUNDLE path.")
                            elif "Field required" in error_msg or "validation error" in error_msg:
                                st.error(f"❌ Validation Error: {error_msg}")
                                st.info("This is a configuration issue. Please contact support.")
                            else:
                                st.error(f"❌ Generation failed: {error_msg}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            with st.expander("🔍 Full Error Details"):
                                st.code(error_msg)
                                st.markdown("**Troubleshooting Steps:**")
                                st.markdown("1. Check your internet connection")
                                st.markdown("2. Verify FFmpeg is installed: `ffmpeg -version`")
                                st.markdown("3. Ensure required models are downloaded")
                                st.markdown("4. Check the terminal output for more details")
    
    with tab2:
        st.subheader("📊 Generation History")
        
        if not st.session_state.generation_history:
            st.info("No videos generated yet. Go to the 'Generate Video' tab to create your first video!")
        else:
            st.write(f"Showing {len(st.session_state.generation_history)} most recent generations")
            
            for idx, item in enumerate(st.session_state.generation_history):
                with st.expander(f"#{idx + 1} - {item['message']} ({item['timestamp'][:19]})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Video ID:**", item['video_id'])
                        st.write("**Category:**", item['category'])
                        st.write("**Priority:**", item['priority'])
                    
                    with col2:
                        st.write("**Model:**", item['model'])
                        st.write("**Duration:**", f"{item['duration']:.1f}s" if item['duration'] else "N/A")
                        st.write("**Timestamp:**", item['timestamp'][:19])
                    
                    with col3:
                        if Path(item['video_path']).exists():
                            st.success("✅ Video available")
                            with open(item['video_path'], 'rb') as f:
                                st.download_button(
                                    "⬇️ Download",
                                    f,
                                    file_name=f"{item['video_id']}.mp4",
                                    key=f"download_{idx}"
                                )
                        else:
                            st.warning("⚠️ Video file not found")
            
            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.generation_history = []
                st.rerun()
    
    with tab3:
        st.subheader("ℹ️ About Zorro")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎬 What is Zorro?
            
            Zorro is an AI-powered video generation system that transforms text-based 
            Walmart activity messages into engaging, accessible video clips.
            
            ### ✨ Key Features
            
            - 🤖 **AI-Powered**: Uses GPT-4 and ModelScope for intelligent video generation
            - ⚡ **Fast**: Generates videos in 30-60 seconds
            - ♿ **Accessible**: WCAG AAA compliant with captions and audio descriptions
            - 🎨 **Smart**: Automatically expands Walmart abbreviations
            - 📱 **Multi-format**: Supports various video providers
            
            ### 🔧 Technology Stack
            
            - **AI Models**: OpenAI GPT-4, ModelScope, Stability AI
            - **Video Processing**: FFmpeg, MoviePy
            - **Accessibility**: WebVTT, gTTS
            - **Framework**: Python, Streamlit
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Supported Categories
            
            - 📚 **Training**: Learning and development
            - ⭐ **Recognition**: Employee achievements
            - 📢 **Announcement**: General updates
            - 🚨 **Alert**: Urgent notifications
            - 📝 **Reminder**: Task reminders
            - 🎉 **Celebration**: Team milestones
            - 📋 **General**: Other communications
            
            ### 🎯 Best Practices
            
            1. Keep messages clear and concise (10-500 characters)
            2. Choose appropriate category and priority
            3. Enable accessibility features for inclusivity
            4. Use Walmart abbreviations (CBL, OBW, GWP) - they're auto-expanded!
            
            ### 📞 Support
            
            For questions or issues, contact the Walmart Digital Team.
            """)
        
        st.markdown("---")
        
        # Statistics
        st.subheader("📈 Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Videos Generated", len(st.session_state.generation_history))
        
        with col2:
            if st.session_state.generation_history:
                categories = [item['category'] for item in st.session_state.generation_history]
                most_common = max(set(categories), key=categories.count)
                st.metric("Most Used Category", most_common)
            else:
                st.metric("Most Used Category", "N/A")
        
        with col3:
            if st.session_state.generation_history:
                avg_duration = sum(item['duration'] for item in st.session_state.generation_history if item['duration']) / len(st.session_state.generation_history)
                st.metric("Avg Duration", f"{avg_duration:.1f}s")
            else:
                st.metric("Avg Duration", "N/A")
        
        with col4:
            st.metric("Pipeline Status", "✅ Ready" if st.session_state.pipeline else "⚠️ Not Initialized")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Zorro AI Video Generator v1.0 | Walmart US Stores | November 2025"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
