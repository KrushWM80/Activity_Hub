"""Reusable design selector component for video generation."""

from typing import Dict, List, Optional

import streamlit as st

from src.models.design_element import DesignElement, DesignElementType


def render_design_selector(
    service,
    key_prefix: str = "design_selector",
    selected_types: Optional[List[DesignElementType]] = None
) -> Dict[str, Optional[DesignElement]]:
    """
    Render design selector component for picking design elements.
    
    Args:
        service: DesignStudioService instance
        key_prefix: Unique key prefix for Streamlit widgets
        selected_types: Which element types to show selectors for
        
    Returns:
        Dict mapping element type to selected DesignElement or None
    """
    if selected_types is None:
        selected_types = [
            DesignElementType.CHARACTER,
            DesignElementType.ENVIRONMENT,
            DesignElementType.ANIMATION_STYLE,
            DesignElementType.COLOR_SCHEME,
        ]
    
    st.subheader("🎨 Design Selection", divider="rainbow")
    
    selected = {}
    
    # Organize elements by type
    elements_by_type = {}
    for elem_type in selected_types:
        available = service.list_elements(
            element_type=elem_type,
            approved_only=True
        )
        elements_by_type[elem_type.value] = available
    
    # Display selectors in columns
    cols = st.columns(len(selected_types))
    
    for col_idx, elem_type in enumerate(selected_types):
        with cols[col_idx]:
            type_key = elem_type.value
            elements = elements_by_type[type_key]
            
            if not elements:
                st.info(f"No {type_key}s available")
                selected[type_key] = None
                continue
            
            # Create options dict
            options_dict = {
                elem.name: elem for elem in elements
            }
            options_list = list(options_dict.keys())
            
            selected_name = st.selectbox(
                f"Select {type_key}",
                options_list + ["(None)"],
                key=f"{key_prefix}_{type_key}",
                index=len(options_list)
            )
            
            if selected_name == "(None)":
                selected[type_key] = None
            else:
                selected_element = options_dict[selected_name]
                selected[type_key] = selected_element
                
                # Show preview
                with st.expander("👁️ Preview", expanded=False):
                    st.write(f"**Description:** {selected_element.description}")
                    st.write(f"**Tags:** {', '.join(selected_element.tags) if selected_element.tags else 'None'}")
                    st.code(selected_element.prompt_template, language="text")
    
    return selected


def render_design_preview(
    selected_elements: Dict[str, Optional[DesignElement]]
) -> str:
    """
    Render preview of how selected elements will be combined.
    
    Args:
        selected_elements: Dict of selected design elements
        
    Returns:
        Composite prompt injection string
    """
    st.subheader("📋 Design Composition", divider="blue")
    
    active_elements = {k: v for k, v in selected_elements.items() if v is not None}
    
    if not active_elements:
        st.info("No design elements selected")
        return ""
    
    # Show selected elements
    cols = st.columns(len(active_elements))
    for col_idx, (elem_type, element) in enumerate(active_elements.items()):
        with cols[col_idx]:
            st.write(f"✅ {element.name}")
            st.caption(elem_type)
    
    st.divider()
    
    # Generate composite prompt
    composite_prompt = _generate_composite_prompt(active_elements)
    
    st.write("**Generated Prompt Injection:**")
    st.code(composite_prompt, language="text")
    
    return composite_prompt


def _generate_composite_prompt(
    selected_elements: Dict[str, Optional[DesignElement]]
) -> str:
    """
    Generate composite LLM prompt from selected design elements.
    
    Args:
        selected_elements: Dict of selected elements
        
    Returns:
        Composite prompt string for injection
    """
    parts = []
    
    # Organize by type
    elements_list = [elem for elem in selected_elements.values() if elem is not None]
    
    if not elements_list:
        return ""
    
    # Group by type for logical flow
    by_type = {}
    for elem in elements_list:
        type_val = elem.type.value
        if type_val not in by_type:
            by_type[type_val] = []
        by_type[type_val].append(elem)
    
    # Build prompt in logical order
    type_order = [
        "character",
        "environment",
        "prop",
        "color_scheme",
        "animation_style",
    ]
    
    for type_key in type_order:
        if type_key in by_type:
            for elem in by_type[type_key]:
                parts.append(elem.prompt_template)
    
    # Add any remaining types
    for type_key in sorted(by_type.keys()):
        if type_key not in type_order:
            for elem in by_type[type_key]:
                parts.append(elem.prompt_template)
    
    # Join with logical connectors
    return " ".join(parts)


def create_design_preset(
    service,
    name: str,
    selected_elements: Dict[str, Optional[DesignElement]],
    created_by: str,
    description: str = ""
) -> bool:
    """
    Save selected elements as a reusable preset.
    
    Args:
        service: DesignStudioService instance
        name: Preset name
        selected_elements: Selected elements
        created_by: User ID
        description: Preset description
        
    Returns:
        True if successful
    """
    from src.models.design_element import DesignPreset
    
    active_ids = [
        elem.id for elem in selected_elements.values()
        if elem is not None
    ]
    
    if not active_ids:
        return False
    
    try:
        preset = DesignPreset(
            name=name,
            description=description or f"Preset with {len(active_ids)} elements",
            element_ids=active_ids,
            created_by=created_by,
        )
        
        if not hasattr(service.library, 'presets'):
            service.library.presets = []
        
        service.library.presets.append(preset)
        service._save_library()
        
        return True
    except Exception as e:
        st.error(f"Failed to save preset: {e}")
        return False


def load_design_preset(
    service,
    preset_name: str
) -> Dict[str, Optional[DesignElement]]:
    """
    Load design elements from a saved preset.
    
    Args:
        service: DesignStudioService instance
        preset_name: Name of preset
        
    Returns:
        Dict of loaded elements
    """
    if not hasattr(service.library, 'presets'):
        return {}
    
    for preset in service.library.presets:
        if preset.name == preset_name:
            selected = {}
            
            for elem_id in preset.element_ids:
                elem = service.get_element(elem_id)
                if elem:
                    selected[elem.type.value] = elem
            
            return selected
    
    return {}
