"""Design Studio page for managing reusable design templates."""

import streamlit as st
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List
import subprocess
import tempfile

from src.services.design_studio_service import DesignStudioService
from src.models.design_element import DesignElementType, DesignCategory
from src.core.pipeline import VideoGenerationPipeline
from src.services.character_prompt_builder import (
    CharacterPromptBuilder,
    CharacterAppearance,
    CharacterPersonality,
    CharacterContext,
    CharacterBrand,
    AgeRange,
    SkinTone,
    BodyType,
    CharacterRole,
)


def initialize_service():
    """Initialize design studio service in session state."""
    if "design_service" not in st.session_state:
        st.session_state.design_service = DesignStudioService()
    if "generating_preview" not in st.session_state:
        st.session_state.generating_preview = False
    if "preview_data" not in st.session_state:
        st.session_state.preview_data = None
    if "allow_direct_save" not in st.session_state:
        st.session_state.allow_direct_save = False
    if "selected_elements" not in st.session_state:
        st.session_state.selected_elements = []


def generate_character_prompt(
    character_name: str,
    age_range: str,
    skin_tone: str,
    body_type: str,
    hair_color: str,
    hair_style: str,
    eye_color: str,
    clothing_style: str,
    character_role: str,
    department: str,
    traits_description: str,
    brand_colors: str,
    tone: str
) -> str:
    """Generate a detailed character prompt using the character prompt builder."""
    try:
        builder = CharacterPromptBuilder()
        
        appearance = CharacterAppearance(
            age_range=AgeRange(age_range),
            skin_tone=SkinTone(skin_tone),
            body_type=BodyType(body_type),
            hair_color=hair_color or "brown",
            hair_style=hair_style or "neat",
            eye_color=eye_color or "brown",
            distinctive_features=[],
            clothing_style=clothing_style or "Walmart uniform",
            accessories=["name badge"]
        )
        
        # Parse traits
        mannerisms = [t.strip() for t in traits_description.split(",") if t.strip()] if traits_description else []
        
        personality = CharacterPersonality(
            primary_traits=[tone, "professional", "approachable"],
            communication_style="clear and friendly",
            mannerisms=mannerisms,
            speaking_pace="conversational",
            expressions=["warm smile", "attentive expression"],
            emotional_tone="positive and professional"
        )
        
        context = CharacterContext(
            role=CharacterRole(character_role),
            department=department or None,
            typical_environments=["Walmart store floor", "customer area", "employee area"],
            expertise_areas=["customer service", "product knowledge"],
            common_activities=["helping customers", "working with team", "representing Walmart"]
        )
        
        # Parse brand colors
        colors = [c.strip() for c in brand_colors.split(",") if c.strip()] if brand_colors else ["#0071CE", "#FFB81C"]
        
        brand = CharacterBrand(
            brand_colors=colors,
            uniform_description="Walmart vest with name badge",
            brand_personality_alignment="Embodies Walmart values of service, trust, and community"
        )
        
        # Build prompt
        prompt = builder.build_prompt(
            character_name=character_name,
            appearance=appearance,
            personality=personality,
            context=context,
            brand=brand,
            additional_notes="This character must appear consistently across all videos."
        )
        
        return prompt
    except Exception as e:
        st.error(f"Error generating character prompt: {e}")
        return None


def extract_video_thumbnail(video_path: str, output_path: str) -> bool:
    """Extract first frame from video as thumbnail using ffmpeg."""
    try:
        # Verify video file exists first
        if not Path(video_path).exists():
            st.error(f"Video file not found: {video_path}")
            return False
        
        # Use ffmpeg to extract first frame
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", "00:00:00.000",
            "-vframes", "1",
            "-vf", "scale=400:300",
            "-y",  # Overwrite output
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=10, text=True)
        if result.returncode == 0:
            return True
        else:
            st.error(f"FFmpeg error: {result.stderr}")
            return False
    except FileNotFoundError:
        st.error("FFmpeg not found. Please install FFmpeg and add it to your PATH. Visit: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        st.error(f"Could not extract thumbnail: {e}")
        return False


def generate_design_preview(prompt_template: str, name: str) -> Optional[str]:
    """Generate a static image preview for the design element and return path to saved image."""
    try:
        # Initialize pipeline
        pipeline = VideoGenerationPipeline()
        
        # Note: Prompt should already be truncated before calling this function
        message_content = prompt_template.strip()
        
        # Generate a SHORT video (1 second) to create a static frame
        # This is just for getting a reference image, not for actual video content
        result = pipeline.generate(
            message_content=message_content,
            message_category="training",
            message_priority="medium",
            apply_editing=False,  # No editing needed for reference
            add_accessibility=False,  # No accessibility needed for reference
            trim_duration=1,  # Just 1 second to extract a frame quickly
            skip_llm_enhancement=True  # Use prompt directly, no LLM enhancement
        )
        
        if result and result.path and Path(result.path).exists():
            return result.path
        return None
    except Exception as e:
        st.error(f"Error generating preview: {e}")
        return None


def render_statistics():
    """Render library statistics."""
    service = st.session_state.design_service
    stats = service.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Elements", stats["total_elements"])
    with col2:
        st.metric("Approved", stats["approved_elements"])
    with col3:
        st.metric("Pending Review", stats["pending_approval"])
    with col4:
        st.metric("Total Usage", stats["total_usage"])
    
    # Elements by type
    st.subheader("Elements by Type")
    cols = st.columns(6)
    for i, (elem_type, count) in enumerate(stats["by_type"].items()):
        with cols[i]:
            st.metric(elem_type.title(), count)


# Character presets for faster prototyping
CHARACTER_PRESETS = {
    "none": {
        "label": "🎨 Start from scratch",
        "age_range": "25-40",
        "skin_tone": "medium",
        "body_type": "average",
        "hair_color": "",
        "hair_style": "",
        "eye_color": "",
        "clothing_style": "",
        "role": "associate",
        "department": "",
        "traits": ""
    },
    "friendly_greeter": {
        "label": "👋 Friendly Greeter",
        "age_range": "25-40",
        "skin_tone": "medium",
        "body_type": "average",
        "hair_color": "dark brown",
        "hair_style": "short and neat",
        "eye_color": "brown",
        "clothing_style": "Walmart blue vest over casual shirt",
        "role": "associate",
        "department": "Customer Service",
        "traits": "warm welcoming smile, makes eye contact, waves hello, enthusiastic body language"
    },
    "safety_champion": {
        "label": "🦺 Safety Champion",
        "age_range": "40-55",
        "skin_tone": "tan",
        "body_type": "athletic",
        "hair_color": "salt and pepper gray",
        "hair_style": "short professional cut",
        "eye_color": "blue",
        "clothing_style": "safety vest over Walmart polo, hard hat nearby",
        "role": "manager",
        "department": "Safety & Compliance",
        "traits": "authoritative but friendly, points to safety signs, demonstrates proper technique"
    },
    "tech_specialist": {
        "label": "💻 Tech Specialist",
        "age_range": "18-25",
        "skin_tone": "fair",
        "body_type": "average",
        "hair_color": "black",
        "hair_style": "modern fade with styled top",
        "eye_color": "brown",
        "clothing_style": "Walmart blue polo, name badge visible",
        "role": "specialist",
        "department": "Electronics",
        "traits": "helpful and patient, gestures toward products, knowledgeable nods"
    },
    "department_manager": {
        "label": "📋 Department Manager",
        "age_range": "40-55",
        "skin_tone": "deep",
        "body_type": "larger",
        "hair_color": "black with gray streaks",
        "hair_style": "professional bob cut",
        "eye_color": "brown",
        "clothing_style": "professional blazer over Walmart polo",
        "role": "manager",
        "department": "Store Operations",
        "traits": "confident posture, encouraging gestures, approachable smile, holds clipboard"
    },
    "training_coach": {
        "label": "🎓 Training Coach",
        "age_range": "25-40",
        "skin_tone": "olive",
        "body_type": "petite",
        "hair_color": "auburn red",
        "hair_style": "shoulder-length wavy",
        "eye_color": "green",
        "clothing_style": "smart casual with Walmart badge",
        "role": "trainer",
        "department": "Learning & Development",
        "traits": "animated speaker, uses hand gestures, encouraging nods, patient listener"
    }
}


def render_create_element():
    """Render form to create new design element with AI preview."""
    st.subheader("Create New Design Element")
    st.write("Define your design element and generate an AI preview that will be saved as the visual reference.")
    
    # Show character style requirement
    st.info("🎨 **Character Style Requirement**: All characters must be created in cartoon/Pixar animation style (no realistic human faces)")
    
    # Step 1: Collect element details
    with st.form("create_element_form", border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Element Name",
                help="Display name for this design element",
                max_chars=100
            )
            element_type = st.selectbox(
                "Type",
                [e.value for e in DesignElementType],
                help="What kind of design element is this?"
            )
        
        with col2:
            category = st.selectbox(
                "Category",
                [c.value for c in DesignCategory],
                help="Content category"
            )
            tags = st.multiselect(
                "Tags",
                ["training", "marketing", "operations", "safety", "seasonal", "store", "people"],
                help="Searchable tags"
            )
        
        description = st.text_area(
            "Visual Description",
            help="Detailed visual description for AI generation",
            max_chars=500,
            height=100
        )
        
        # Character-specific fields
        character_appearance = None
        character_personality = None
        character_context = None
        
        if DesignElementType(element_type) == DesignElementType.CHARACTER:
            st.markdown("### ⚡ Quick Start: Character Presets")
            st.caption("Select a preset to auto-fill character details, then customize as needed")
            
            preset_options = {k: v["label"] for k, v in CHARACTER_PRESETS.items()}
            selected_preset = st.selectbox(
                "Character Preset",
                options=list(preset_options.keys()),
                format_func=lambda x: preset_options[x],
                key="char_preset"
            )
            
            # Get preset values
            preset = CHARACTER_PRESETS[selected_preset]
            
            st.divider()
            st.info("📋 **Character Details** - Customize these to create your unique character")
            
            char_col1, char_col2 = st.columns(2)
            with char_col1:
                age_range = st.selectbox(
                    "Age Range",
                    ["18-25", "25-40", "40-55", "55+"],
                    index=["18-25", "25-40", "40-55", "55+"].index(preset["age_range"]) if preset["age_range"] in ["18-25", "25-40", "40-55", "55+"] else 1,
                    key="char_age"
                )
                skin_tones = ["fair", "light", "medium", "olive", "tan", "deep"]
                skin_tone = st.selectbox(
                    "Skin Tone",
                    skin_tones,
                    index=skin_tones.index(preset["skin_tone"]) if preset["skin_tone"] in skin_tones else 2,
                    key="char_skin"
                )
                body_types = ["petite", "average", "athletic", "larger"]
                body_type = st.selectbox(
                    "Body Type",
                    body_types,
                    index=body_types.index(preset["body_type"]) if preset["body_type"] in body_types else 1,
                    key="char_body"
                )
                hair_color = st.text_input(
                    "Hair Color",
                    value=preset["hair_color"],
                    placeholder="e.g., dark brown, blonde",
                    key="char_hair_color"
                )
            
            with char_col2:
                hair_style = st.text_input(
                    "Hair Style",
                    value=preset["hair_style"],
                    placeholder="e.g., shoulder-length curly, short neat",
                    key="char_hair_style"
                )
                eye_color = st.text_input(
                    "Eye Color",
                    value=preset["eye_color"],
                    placeholder="e.g., brown, blue",
                    key="char_eyes"
                )
                clothing_style = st.text_input(
                    "Clothing Style",
                    value=preset["clothing_style"],
                    placeholder="e.g., professional blazer, casual shirt",
                    key="char_clothing"
                )
                roles = ["associate", "manager", "customer", "specialist", "trainer"]
                character_role = st.selectbox(
                    "Character Role",
                    roles,
                    index=roles.index(preset["role"]) if preset["role"] in roles else 0,
                    key="char_role"
                )
            
            character_dept = st.text_input(
                "Department/Specialty",
                value=preset["department"],
                placeholder="e.g., Customer Service, Grocery, Electronics",
                key="char_dept"
            )
            
            character_traits = st.text_area(
                "Personality Traits & Mannerisms",
                value=preset["traits"],
                placeholder="e.g., friendly smile, makes eye contact, gestures when speaking, patient listener",
                height=80,
                key="char_traits"
            )
        
        # For non-CHARACTER elements only - CHARACTER prompts are auto-generated
        if DesignElementType(element_type) != DesignElementType.CHARACTER:
            prompt_template = st.text_area(
                "Prompt Template",
                help="LLM prompt snippet for consistency (max 500 chars for video generation)",
                max_chars=500,
                height=100
            )
        else:
            prompt_template = ""  # Will be auto-generated from character attributes
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            brand_colors = st.text_input(
                "Brand Colors",
                placeholder="e.g., #0071CE, #FFB81C",
                help="Hex color codes"
            )
        
        with col2:
            personality_traits = st.text_input(
                "Personality Traits",
                placeholder="e.g., friendly, professional, energetic",
                help="Comma-separated traits"
            )
        
        with col3:
            tone = st.selectbox(
                "Tone",
                ["professional", "friendly", "inspiring", "urgent", "playful"]
            )
        
        usage_guidelines = st.text_area(
            "Usage Guidelines",
            help="How/when should this element be used?",
            max_chars=300,
            height=80
        )
        
        restrictions = st.text_area(
            "Restrictions",
            help="Any restrictions or limitations?",
            max_chars=300,
            height=80
        )
        
        st.divider()
        
        preview_clicked = st.form_submit_button(
            "🎬 Generate AI Preview",
            type="primary",
            use_container_width=True,
            help="Generate a test video to preview the design"
        )
        
        if preview_clicked:
            # CHARACTER elements auto-generate prompts from attributes, others need prompt_template
            is_character = DesignElementType(element_type) == DesignElementType.CHARACTER
            if not name or not description or (not is_character and not prompt_template):
                error_msg = "Please fill in Name and Description"
                if not is_character:
                    error_msg += ", and Prompt Template"
                st.error(error_msg)
            elif DesignElementType(element_type) == DesignElementType.CHARACTER:
                # Characters MUST have previews generated
                # Generate detailed character prompt using builder
                char_prompt = generate_character_prompt(
                    character_name=name,
                    age_range=st.session_state.get("char_age", "25-40"),
                    skin_tone=st.session_state.get("char_skin", "medium"),
                    body_type=st.session_state.get("char_body", "average"),
                    hair_color=st.session_state.get("char_hair_color", ""),
                    hair_style=st.session_state.get("char_hair_style", ""),
                    eye_color=st.session_state.get("char_eyes", ""),
                    clothing_style=st.session_state.get("char_clothing", ""),
                    character_role=st.session_state.get("char_role", "associate"),
                    department=st.session_state.get("char_dept", ""),
                    traits_description=st.session_state.get("char_traits", ""),
                    brand_colors=brand_colors,
                    tone=tone
                )
                
                st.session_state.preview_data = {
                    "name": name,
                    "element_type": element_type,
                    "category": category,
                    "description": description,
                    "prompt_template": char_prompt or prompt_template,  # Use generated prompt if successful
                    "original_prompt": prompt_template,
                    "tags": tags,
                    "brand_colors": brand_colors,
                    "personality_traits": personality_traits,
                    "tone": tone,
                    "usage_guidelines": usage_guidelines,
                    "restrictions": restrictions,
                    "is_character": True,
                }
                st.session_state.generating_preview = True
                st.rerun()
            else:
                # Other elements can be created with or without preview
                st.info("ℹ️ This element type doesn't require a preview. You can create it directly or generate a preview first.")
                st.session_state.preview_data = {
                    "name": name,
                    "element_type": element_type,
                    "category": category,
                    "description": description,
                    "prompt_template": prompt_template,
                    "tags": tags,
                    "brand_colors": brand_colors,
                    "personality_traits": personality_traits,
                    "tone": tone,
                    "usage_guidelines": usage_guidelines,
                    "restrictions": restrictions,
                    "is_character": False,
                }
                # Allow direct save without preview for non-characters
                st.session_state.allow_direct_save = True
                st.rerun()
    
    # Step 2: Preview the generated video
    if st.session_state.get("generating_preview"):
        st.divider()
        st.subheader("🎬 AI Preview Generation")
        
        preview_data = st.session_state.preview_data
        
        # Use full prompt for character elements (detailed prompts are important for consistency)
        prompt_to_use = preview_data["prompt_template"].strip()
        
        # Only truncate if exceeding a very generous limit
        if len(prompt_to_use) > 4000:
            st.warning(f"⚠️ Your prompt is {len(prompt_to_use)} characters (very long). Truncating to 4000 characters for video generation.")
            prompt_to_use = prompt_to_use[:3997] + "..."
        
        with st.spinner("Generating reference image... This may take 30-60 seconds..."):
            video_path = generate_design_preview(
                prompt_to_use,
                preview_data["name"]
            )
        
        if video_path and Path(video_path).exists():
            st.success("✅ Reference image generated successfully!")
            
            # Display the prompt that was used
            if preview_data.get("is_character"):
                st.info("🤖 **AI-Generated Character Prompt** - This detailed prompt defines what this character will look like in all future content")
            else:
                st.write("**Element Description:**")
            st.info(prompt_to_use)
            
            # Extract thumbnail from the video frame
            assets_dir = Path("design_assets")
            assets_dir.mkdir(exist_ok=True)
            
            thumbnail_path = assets_dir / f"{preview_data['element_type']}_{preview_data['name'].lower().replace(' ', '_')}_thumb.png"
            
            if extract_video_thumbnail(video_path, str(thumbnail_path)):
                st.write("**Reference Image:**")
                st.image(str(thumbnail_path), width=300, caption="Visual reference for this design element")
            else:
                st.info("ℹ️ **Note:** FFmpeg not found on this system, so a reference image could not be extracted. The video file has been generated and saved. To enable thumbnail extraction, please install FFmpeg.")
            
            # Option to save
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Save Design Element", type="primary", use_container_width=True):
                    service = st.session_state.design_service
                    current_user = st.session_state.get("user_id", "demo_user")
                    
                    try:
                        metadata_kwargs = {
                            "primary_color": preview_data["brand_colors"].split(",")[0].strip() if preview_data["brand_colors"] else None,
                            "secondary_colors": [c.strip() for c in preview_data["brand_colors"].split(",")[1:]] if preview_data["brand_colors"] else [],
                            "personality": preview_data["personality_traits"] if preview_data["personality_traits"] else None,
                            "use_cases": [preview_data["category"]],
                            "guidelines": preview_data["usage_guidelines"],
                            "restrictions": preview_data["restrictions"],
                        }
                        
                        element = service.create_element(
                            name=preview_data["name"],
                            element_type=DesignElementType(preview_data["element_type"]),
                            description=preview_data["description"],
                            prompt_template=preview_data["prompt_template"],
                            created_by=current_user,
                            category=DesignCategory(preview_data["category"]),
                            tags=preview_data["tags"],
                            visual_reference_path=str(thumbnail_path) if thumbnail_path and Path(thumbnail_path).exists() else video_path,
                            **metadata_kwargs
                        )
                        
                        if element:
                            st.success(f"✅ Saved: {element.name}")
                            st.balloons()
                            st.session_state.generating_preview = False
                            st.session_state.preview_data = None
                            st.rerun()
                        else:
                            st.error("Failed to save element - service returned None")
                    except Exception as e:
                        st.error(f"Error saving element: {str(e)}")
                        import traceback
                        st.error(f"Details: {traceback.format_exc()}")
            
            with col2:
                if st.button("❌ Cancel & Discard", use_container_width=True):
                    st.session_state.generating_preview = False
                    st.session_state.preview_data = None
                    st.rerun()
        
        else:
            st.error("❌ Failed to generate preview video. Please check your settings and try again.")
            if st.button("Try Again"):
                st.session_state.generating_preview = False
                st.rerun()
    
    # Step 3: Direct save option for non-character elements
    if st.session_state.get("allow_direct_save") and st.session_state.get("preview_data"):
        st.divider()
        st.subheader("💾 Save Design Element")
        st.write("Preview is optional for this element type. You can save it now without generating a preview image.")
        
        preview_data = st.session_state.preview_data
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Save Without Preview", type="primary", use_container_width=True):
                service = st.session_state.design_service
                current_user = st.session_state.get("user_id", "demo_user")
                
                metadata_kwargs = {
                    "primary_color": preview_data["brand_colors"].split(",")[0].strip() if preview_data["brand_colors"] else None,
                    "secondary_colors": [c.strip() for c in preview_data["brand_colors"].split(",")[1:]] if preview_data["brand_colors"] else [],
                    "personality": preview_data["personality_traits"] if preview_data["personality_traits"] else None,
                    "use_cases": [preview_data["category"]],
                    "guidelines": preview_data["usage_guidelines"],
                    "restrictions": preview_data["restrictions"],
                }
                
                element = service.create_element(
                    name=preview_data["name"],
                    element_type=DesignElementType(preview_data["element_type"]),
                    description=preview_data["description"],
                    prompt_template=preview_data["prompt_template"],
                    created_by=current_user,
                    category=DesignCategory(preview_data["category"]),
                    tags=preview_data["tags"],
                    **metadata_kwargs
                )
                
                if element:
                    st.success(f"✅ Saved: {element.name}")
                    st.balloons()
                    st.session_state.allow_direct_save = False
                    st.session_state.preview_data = None
                    st.rerun()
                else:
                    st.error("Failed to save element")
        
        with col2:
            if st.button("🎬 Generate Preview First", use_container_width=True):
                st.session_state.generating_preview = True
                st.session_state.allow_direct_save = False
                st.rerun()
            
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.allow_direct_save = False
                st.session_state.preview_data = None
                st.rerun()


def render_design_library():
    """Render browsable design library."""
    st.subheader("Design Library")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_query = st.text_input(
            "Search",
            placeholder="Name, description, tags..."
        )
    
    with col2:
        filter_type = st.selectbox(
            "Type",
            ["All"] + [e.value for e in DesignElementType]
        )
    
    with col3:
        filter_category = st.selectbox(
            "Category",
            ["All"] + [c.value for c in DesignCategory]
        )
    
    with col4:
        approved_only = st.checkbox("Approved Only", value=True)
    
    # Get results
    service = st.session_state.design_service
    
    if search_query:
        element_type = None if filter_type == "All" else DesignElementType(filter_type)
        results = service.search(search_query, element_type=element_type)
    else:
        element_type = None if filter_type == "All" else DesignElementType(filter_type)
        category = None if filter_category == "All" else DesignCategory(filter_category)
        results = service.list_elements(
            element_type=element_type,
            category=category,
            approved_only=approved_only
        )
    
    # Display results
    if not results:
        st.info("No design elements found")
        return
    
    # Show selected element details if any
    if "selected_element" in st.session_state and st.session_state.selected_element:
        selected_elem = service.get_element(st.session_state.selected_element)
        if selected_elem:
            with st.expander(f"📋 Details: {selected_elem.name}", expanded=True):
                # Display visual reference if available
                if selected_elem.visual_reference_path:
                    visual_path = Path(selected_elem.visual_reference_path)
                    if visual_path.exists():
                        st.write("**Visual Reference:**")
                        try:
                            st.image(str(visual_path), width=300, caption=f"{selected_elem.name} visual reference")
                        except Exception as e:
                            st.warning(f"Could not load image: {e}")
                    else:
                        st.info(f"Visual reference path set but file not found: {selected_elem.visual_reference_path}")
                else:
                    # Show a placeholder for no visual reference
                    st.info("ℹ️ No visual reference image available for this design")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {selected_elem.name}")
                    st.write(f"**Type:** {selected_elem.type.value}")
                    st.write(f"**Category:** {selected_elem.category.value}")
                    st.write(f"**Created By:** {selected_elem.created_by}")
                    st.write(f"**Status:** {'✅ Approved' if selected_elem.is_approved else '⏳ Pending'}")
                with col2:
                    st.write(f"**Usage Count:** {selected_elem.usage_count}")
                    st.write(f"**Created At:** {selected_elem.created_at.strftime('%Y-%m-%d %H:%M')}")
                    if selected_elem.updated_at:
                        st.write(f"**Updated At:** {selected_elem.updated_at.strftime('%Y-%m-%d %H:%M')}")
                
                st.write("**Description:**")
                st.write(selected_elem.description)
                
                st.write("**Prompt Template:**")
                st.code(selected_elem.prompt_template, language="text")
                
                if selected_elem.tags:
                    st.write(f"**Tags:** {', '.join(selected_elem.tags)}")
                
                if selected_elem.metadata:
                    st.write("**Metadata:**")
                    if selected_elem.metadata.primary_color:
                        st.write(f"- Primary Color: {selected_elem.metadata.primary_color}")
                    if selected_elem.metadata.secondary_colors:
                        st.write(f"- Secondary Colors: {', '.join(selected_elem.metadata.secondary_colors)}")
                    if selected_elem.metadata.personality:
                        st.write(f"- Personality: {selected_elem.metadata.personality}")
                    if selected_elem.metadata.use_cases:
                        st.write(f"- Use Cases: {', '.join(selected_elem.metadata.use_cases)}")
                    if selected_elem.metadata.guidelines:
                        st.write(f"- Guidelines: {selected_elem.metadata.guidelines}")
                    if selected_elem.metadata.restrictions:
                        st.write(f"- Restrictions: {selected_elem.metadata.restrictions}")
                
                if st.button("Close Details", key="close_details"):
                    st.session_state.selected_element = None
                    st.rerun()
            
            st.divider()
    
    # Group by type
    by_type = {}
    for elem in results:
        elem_type = elem.type.value
        if elem_type not in by_type:
            by_type[elem_type] = []
        by_type[elem_type].append(elem)
    
    for elem_type, elements in by_type.items():
        st.subheader(f"{elem_type.title()} ({len(elements)})")
        
        for element in elements:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{element.name}**")
                    st.caption(f"By {element.created_by} • {element.category.value}")
                    st.write(element.description)
                    
                    if element.tags:
                        tag_str = " ".join([f"`{tag}`" for tag in element.tags])
                        st.caption(f"Tags: {tag_str}")
                
                with col2:
                    st.metric("Uses", element.usage_count)
                    if element.is_approved:
                        st.success("Approved")
                    else:
                        st.warning("Pending")
                
                with col3:
                    if st.button("👁️ View", key=f"view_{element.id}"):
                        st.session_state.selected_element = element.id
                        st.rerun()
                    
                    if st.button("🎬 Use", key=f"use_{element.id}"):
                        # Add to selected elements
                        if "selected_elements" not in st.session_state:
                            st.session_state.selected_elements = []
                        
                        if element.id not in st.session_state.selected_elements:
                            st.session_state.selected_elements.append(element.id)
                            service.increment_usage(element.id)
                            st.success("Added to selection!")


def render_my_elements():
    """Render user's created elements."""
    st.subheader("My Design Elements")
    
    service = st.session_state.design_service
    current_user = st.session_state.get("user_id", "demo_user")
    
    # Get user's elements
    all_elements = service.list_elements()
    my_elements = [e for e in all_elements if e.created_by == current_user]
    
    if not my_elements:
        st.info(f"You haven't created any design elements yet. Go to the 'Create' tab to get started!")
        return
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Created", len(my_elements))
    with col2:
        approved = len([e for e in my_elements if e.is_approved])
        st.metric("Approved", approved)
    with col3:
        total_usage = sum(e.usage_count for e in my_elements)
        st.metric("Total Usage", total_usage)
    
    st.divider()
    
    # Display elements
    for element in my_elements:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**{element.name}** ({element.type.value})")
                st.caption(f"Created: {element.created_at.strftime('%Y-%m-%d %H:%M')}")
                st.write(element.description)
                
                if not element.is_approved:
                    st.warning("⏳ Pending Approval")
                    if element.approval_notes:
                        st.caption(f"Notes: {element.approval_notes}")
                else:
                    st.success("✅ Approved")
                
                st.metric("Usage Count", element.usage_count, label_visibility="collapsed")
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{element.id}"):
                    st.session_state.editing_element = element.id
                
                if st.button("🗑️ Delete", key=f"delete_{element.id}"):
                    if service.delete_element(element.id):
                        st.success("Deleted!")
                        st.rerun()


def render_approvals():
    """Render approval queue for admins."""
    st.subheader("Approval Queue")
    
    service = st.session_state.design_service
    pending = [e for e in (
        service.library.characters + service.library.logos +
        service.library.environments + service.library.props +
        service.library.animation_styles + service.library.color_schemes
    ) if not e.is_approved]
    
    if not pending:
        st.success("No pending approvals!")
        return
    
    st.info(f"{len(pending)} elements awaiting approval")
    
    for element in pending:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{element.name}** ({element.type.value})")
                st.caption(f"By {element.created_by} • {element.category.value}")
                st.write(element.description)
                
                st.write("**Prompt Template:**")
                st.code(element.prompt_template)
            
            with col2:
                approval_notes = st.text_area(
                    "Notes",
                    key=f"notes_{element.id}",
                    height=100
                )
                
                col_approve, col_reject = st.columns(2)
                
                with col_approve:
                    if st.button("✅ Approve", key=f"approve_{element.id}"):
                        service.approve_element(
                            element.id,
                            "admin_user",
                            approval_notes or "Approved"
                        )
                        st.success("Approved!")
                        st.rerun()
                
                with col_reject:
                    if st.button("❌ Reject", key=f"reject_{element.id}"):
                        service.reject_element(
                            element.id,
                            "admin_user",
                            approval_notes or "Rejected"
                        )
                        st.error("Rejected!")
                        st.rerun()


def main():
    """Main Design Studio page."""
    st.set_page_config(
        page_title="Design Studio | Zorro",
        page_icon="🎨",
        layout="wide"
    )
    
    # Initialize
    initialize_service()
    
    st.title("🎨 Design Studio")
    st.write(
        "Create and manage reusable design templates for consistent, "
        "brand-compliant content across all facilities."
    )
    
    # Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "✨ Create Element",
        "📚 Library",
        "👤 My Elements",
        "✅ Approvals"
    ])
    
    with tab1:
        render_statistics()
    
    with tab2:
        render_create_element()
    
    with tab3:
        render_design_library()
    
    with tab4:
        render_my_elements()
    
    with tab5:
        render_approvals()


if __name__ == "__main__":
    main()
