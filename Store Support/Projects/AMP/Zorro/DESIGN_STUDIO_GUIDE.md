# Design Studio Feature Documentation

## Overview

The **Design Studio** is an enterprise-scale design template management system that enables consistent, brand-compliant content creation across all Walmart facilities. It allows you to create reusable design elements (characters, logos, environments, animation styles, etc.) that are applied to video generation for visual and tonal consistency.

## Key Features

### 1. **Design Element Types**

Create and manage six types of design elements:

- **Characters**: AI-generated personas (e.g., "Carl the Purple Monster")
- **Logos**: Brand marks and identifiers
- **Environments**: Backgrounds and settings (stores, warehouses, etc.)
- **Props**: Objects and items in scenes
- **Animation Styles**: Motion, timing, and movement patterns
- **Color Schemes**: Brand color palettes and visual standards

### 2. **Content Categories**

Organize designs by use case:

- **TRAINING**: Educational and skill development content
- **MARKETING**: Promotional and announcement videos
- **OPERATIONS**: Internal process and procedure videos
- **SAFETY**: Safety training and alerts
- **CUSTOM**: Other content categories

### 3. **Visibility & Governance**

Control who can access and use designs:

- **PRIVATE**: Creator only (drafts)
- **FACILITY**: All users in the creating facility
- **REGION**: Multi-facility regional access
- **COMPANY**: Enterprise-wide, all facilities

### 4. **Approval Workflow**

- Creators submit new design elements
- Corporate admin reviews for brand compliance
- Approved designs appear in the library for all facilities
- Feedback system for rejections and improvements

### 5. **Usage Tracking & Analytics**

- Monitor which designs are used most frequently
- Track usage by facility and region
- Identify popular templates for promotion
- Measure design element ROI

## Getting Started

### Access the Design Studio

1. Open Zorro application: `streamlit run app.py`
2. Navigate to **Design Studio** in the left sidebar
3. Use tabs to: View Dashboard, Create Elements, Browse Library, Manage Your Elements, Review Approvals

### Create Your First Design Element

**Example: Create "Carl the Purple Monster" Character**

1. Go to **✨ Create Element** tab
2. Fill out the form:
   - **Name**: "Carl - Purple Monster"
   - **Type**: CHARACTER
   - **Category**: TRAINING
   - **Description**: "A friendly, energetic purple monster wearing Walmart blue vest. Carl is welcoming, motivational, and approachable."
   - **Prompt Template**: "Feature Carl, a friendly purple monster wearing a Walmart blue vest. He should be energetic and welcoming."
   - **Brand Colors**: #0071CE, #FFB81C, #7030A0
   - **Personality Traits**: friendly, energetic, motivational
   - **Tone**: friendly
3. Click **✨ Create Design Element**
4. Your element is now pending approval

### Use Design Elements in Videos

**Integrate designs with video generation:**

1. Go to **🎥 Generate Video** tab in main app
2. Create your message content
3. Check **Use design elements for this video**
4. Select design elements from library:
   - Choose a Character (e.g., Carl)
   - Select Environment (e.g., Store)
   - Pick Color Scheme (Walmart colors)
   - Choose Animation Style (Energetic)
5. Preview the combined prompt
6. Generate your video

**Result**: Video features Carl in a Walmart store with consistent brand colors and energetic animations.

## Architecture

### Service Layer: `DesignStudioService`

Core CRUD operations:

```python
service = DesignStudioService()

# Create element
element = service.create_element(
    name="Carl",
    element_type=DesignElementType.CHARACTER,
    description="...",
    prompt_template="...",
    created_by="user123"
)

# List elements with filters
elements = service.list_elements(
    element_type=DesignElementType.CHARACTER,
    category=DesignCategory.TRAINING,
    approved_only=True
)

# Search
results = service.search("Carl", element_type=DesignElementType.CHARACTER)

# Approve for use
service.approve_element(element_id, "admin_user", "Approved")

# Track usage
service.increment_usage(element_id)

# Get statistics
stats = service.get_statistics()
```

### UI Component: `design_selector`

Streamlit component for selecting design elements:

```python
from src.ui.components.design_selector import (
    render_design_selector,
    render_design_preview,
    create_design_preset
)

# In Streamlit page:
selected = render_design_selector(service)
composite_prompt = render_design_preview(selected)

# Save as preset
create_design_preset(service, "My Preset", selected, "user123")
```

### Data Models: `design_element.py`

Pydantic models for validation:

```python
from src.models.design_element import (
    DesignElement,
    DesignElementType,
    DesignCategory,
    DesignVisibility
)

# Automatic validation of design elements
element = DesignElement(
    id="char_carl_001",
    name="Carl",
    type=DesignElementType.CHARACTER,
    prompt_template="...",
    # ... validation enforced
)
```

## Data Storage

### File Structure

```
data/
├── design_library.json          # Main design library storage
└── design_assets/               # Images, videos, references
    ├── char_carl_001.png
    ├── env_store_001.jpg
    └── ...
```

### Library JSON Format

```json
{
  "characters": [
    {
      "id": "char_carl_001",
      "name": "Carl - Purple Monster",
      "type": "character",
      "category": "training",
      "description": "...",
      "prompt_template": "...",
      "tags": ["character", "friendly", "mascot"],
      "is_approved": true,
      "usage_count": 24,
      "metadata": {
        "brand_colors": ["#0071CE", "#FFB81C"],
        "personality_traits": ["friendly", "energetic"],
        "tone": "friendly"
      }
    }
  ],
  "logos": [...],
  "environments": [...],
  "props": [...],
  "animation_styles": [...],
  "color_schemes": [...]
}
```

## Integration with Video Generator

### Prompt Injection Process

When design elements are selected:

1. **Select Elements**: User picks character, environment, colors, animation style
2. **Generate Composite Prompt**: System combines element prompts
3. **Inject into Message**: Design prompts prepended to user message
4. **Send to AI**: Full prompt sent to Walmart Media Studio API
5. **Track Usage**: Design element usage counters incremented

### Example Prompt Composition

**User Message:**
> "Complete your annual safety training by Friday"

**Selected Designs:**
- Character: Carl
- Environment: Store
- Color Scheme: Walmart colors
- Animation: Energetic

**Composite Prompt Sent to AI:**
```
Feature Carl, a friendly purple monster wearing a Walmart blue vest. He should be 
energetic and welcoming. Set the scene in a modern Walmart store with bright lighting 
and clean aisles. Use the official Walmart color palette: Blue (#0071CE) and Yellow 
(#FFB81C). Use energetic, dynamic animations with smooth transitions.

Complete your annual safety training by Friday
```

## Example Designs (Pre-Loaded)

When you initialize Zorro, these example designs are pre-loaded:

### 1. Carl - Purple Monster
- **Type**: CHARACTER
- **Category**: TRAINING
- **Usage**: Friendly, motivational training videos

### 2. Walmart Store Environment
- **Type**: ENVIRONMENT
- **Category**: OPERATIONS
- **Usage**: Operations training, customer service

### 3. Walmart Logo
- **Type**: LOGO
- **Category**: MARKETING
- **Usage**: All professional announcements

### 4. Energetic Animation Style
- **Type**: ANIMATION_STYLE
- **Category**: TRAINING
- **Usage**: Motivational and recognition content

### 5. Walmart Brand Palette
- **Type**: COLOR_SCHEME
- **Category**: MARKETING
- **Usage**: All professional content

## Advanced Features

### Design Presets

Save combinations of elements for quick reuse:

```python
# Save preset
create_design_preset(
    service,
    name="Training Standard",
    selected_elements={
        "character": carl_element,
        "environment": store_element,
        "color_scheme": walmart_colors
    },
    created_by="manager_001"
)

# Load preset
selected = load_design_preset(service, "Training Standard")
```

### Facility-Level Isolation

Each facility can have:
- Private designs (visible to creators only)
- Facility designs (visible to all in facility)
- Regional designs (shared across region)
- Corporate designs (all facilities)

### Export/Import

```python
# Export facility's designs
export_data = service.export_by_facility(facility_id="WM_001")

# Import corporate templates
service.import_library(external_library_json)
```

## Best Practices

### For Creators

1. **Use Descriptive Names**: Make element purpose clear (e.g., "Carl - Purple Monster" not "char1")
2. **Detailed Descriptions**: Help AI understand visual intent
3. **Test Prompts**: Verify prompt templates work with various messages
4. **Brand Consistency**: Follow Walmart brand guidelines
5. **Tag Thoroughly**: Use tags for easy discovery

### For Administrators

1. **Review Quickly**: Approve designs promptly to maintain velocity
2. **Give Feedback**: Help creators improve rejected designs
3. **Track Usage**: Monitor which designs are most effective
4. **Audit Compliance**: Ensure all approved designs meet brand standards
5. **Plan Rotations**: Refresh designs seasonally or for campaigns

### For Video Generators

1. **Start Simple**: Use 1-2 design elements, not all
2. **Test First**: Preview composite prompt before generating
3. **Save Presets**: Store successful combinations
4. **Track Results**: Note which design combinations work best
5. **Provide Feedback**: Report designs that don't work well

## Troubleshooting

### No Design Elements Appear

**Solution**: Initialize design library:
```bash
python scripts/init_design_library.py
```

### Design Selector Not Showing

**Solution**: Ensure service is initialized in session state:
```python
if "design_service" not in st.session_state:
    st.session_state.design_service = DesignStudioService()
```

### Approval Status Won't Update

**Solution**: Check if admin user ID is set correctly in approval functions

### Design Elements Not Used in Video

**Solution**: Verify `use_design` checkbox is selected and elements are active (not None)

## Roadmap

### Phase 1 (MVP - This Week)
- ✅ Design element models and service layer
- ✅ Streamlit UI for creation and browsing
- ✅ Basic approval workflow
- ✅ Integration with video generator
- 🔄 Local JSON storage

### Phase 2 (Enterprise - Next Week)
- 🔄 Database backend (PostgreSQL/MongoDB)
- 🔄 Advanced search and filtering
- 🔄 Visual asset management
- 🔄 Multi-region support
- 🔄 Batch operations

### Phase 3 (Scale - Weeks 3-4)
- ⏳ API for external integrations
- ⏳ Design element versioning
- ⏳ A/B testing framework
- ⏳ Advanced analytics
- ⏳ Mobile app support

## API Reference

### DesignStudioService

```python
class DesignStudioService:
    def create_element(**kwargs) -> Optional[DesignElement]
    def get_element(element_id: str) -> Optional[DesignElement]
    def list_elements(**filters) -> List[DesignElement]
    def update_element(element_id: str, **updates) -> Optional[DesignElement]
    def delete_element(element_id: str) -> bool
    def approve_element(element_id: str, approved_by: str, notes: str) -> Optional[DesignElement]
    def reject_element(element_id: str, rejected_by: str, reason: str) -> Optional[DesignElement]
    def search(query: str, element_type: Optional[DesignElementType]) -> List[DesignElement]
    def get_statistics() -> Dict[str, Any]
    def increment_usage(element_id: str) -> bool
    def export_library() -> Dict[str, Any]
    def export_by_facility(facility_id: str) -> Dict[str, Any]
```

## Support

For questions or issues:

1. Check this documentation
2. Review example designs in `scripts/init_design_library.py`
3. Check Streamlit console for error messages
4. Contact the AI Media Studio team (#help-genai-media-studio)

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Status**: Production Ready (Phase 1 MVP)
