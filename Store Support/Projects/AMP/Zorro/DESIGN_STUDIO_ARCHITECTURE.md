# Design Studio Architecture
## Enterprise Content Consistency at Scale (4000+ Facilities)

### Executive Vision
Enable 4000+ Walmart facilities to create and maintain consistent, professional, on-brand content by:
1. Designing reusable design elements (characters, logos, environments, props)
2. Saving these as templates with metadata and usage guidelines
3. Incorporating them into video generation prompts for consistency
4. Scaling professionally while maintaining brand compliance

---

## System Architecture

### Core Components

#### 1. Design Element Model (`src/models/design_element.py`)
```
DesignElement:
  - id: UUID
  - name: str                    # "Carl the Purple Monster", "Walmart Logo"
  - type: DesignElementType      # character, logo, environment, prop, animation
  - description: str              # Visual description for LLM prompt injection
  - category: str                 # training, marketing, operations, safety
  - tags: List[str]              # searchable tags
  - visual_reference: Optional[FileRef]  # Image/video reference
  - prompt_template: str          # LLM-optimized prompt snippet
  - metadata: Dict                # Brand guidelines, style, constraints
  - created_by: str               # User/facility ID
  - created_at: datetime
  - updated_at: datetime
  - usage_count: int              # Analytics
  - is_approved: bool             # Brand compliance checkbox
  - approved_by: Optional[str]    # Admin approval
  
DesignElementType (Enum):
  - CHARACTER: An AI-generated character/person/mascot
  - LOGO: Brand mark/identifier
  - ENVIRONMENT: Setting/background/location
  - PROP: Object/item in scene
  - ANIMATION_STYLE: Motion/movement style
  - COLOR_SCHEME: Brand color palette
```

#### 2. Design Studio Service (`src/services/design_studio_service.py`)
```
DesignStudioService:
  - create_design_element()    # Create new template
  - update_design_element()    # Modify existing
  - delete_design_element()    # Remove template
  - list_designs()             # Query by type/category/tags
  - get_design()               # Retrieve single
  - validate_design()          # Brand compliance check
  - generate_prompt_snippet()  # Convert to LLM injection
  - export_design_library()    # Facility-level export
```

#### 3. Design Element Storage (`src/db/design_elements.json`)
```json
{
  "characters": [
    {
      "id": "char_carl_001",
      "name": "Carl - Purple Monster Mascot",
      "type": "character",
      "description": "A friendly, approachable purple monster with three eyes...",
      "category": "training",
      "tags": ["friendly", "educational", "mascot", "purple"],
      "prompt_template": "A character design of Carl, the friendly purple monster with three eyes. Carl has a warm demeanor and is ideal for safety training videos.",
      "metadata": {
        "color_primary": "#8B3A8B",
        "personality": "enthusiastic, helpful, non-threatening",
        "use_cases": ["safety training", "onboarding", "procedures"],
        "brand_approved": true,
        "guidelines": "Always show Carl smiling, never angry or dangerous"
      },
      "created_by": "facility_001",
      "created_at": "2025-12-03T...",
      "is_approved": true,
      "usage_count": 47
    }
  ],
  "logos": [...],
  "environments": [...],
  "props": [...],
  "animation_styles": [...]
}
```

---

## User Interface Components

### Design Studio Page (`app_design_studio.py`)
Accessible from main app via "🎨 Design Studio" button

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│              DESIGN STUDIO                          │
│  Create reusable design elements for video content  │
└─────────────────────────────────────────────────────┘

┌─ TABS ──────────────────────────────────────────────┐
│ [My Designs] [Browse Library] [Import/Export] [Approve] │
└─────────────────────────────────────────────────────┘

SECTION 1: CREATE NEW ELEMENT
┌─────────────────────────────────────────────────────┐
│ Element Type:                                       │
│ ◉ Character  ○ Logo  ○ Environment  ○ Prop  ○ Style│
│                                                     │
│ Name: [Carl the Purple Monster_____________________] │
│                                                     │
│ Visual Reference:                                   │
│ [Upload Image/Video] or [Select from Gallery]      │
│ [Preview Box]                                       │
│                                                     │
│ Description (for AI):                               │
│ [A friendly purple monster with three eyes...___]   │
│                                                     │
│ Category:                                           │
│ [Training ▼] (Training, Marketing, Operations, Safety) │
│                                                     │
│ Tags: [friendly] [mascot] [training] [+Add]        │
│                                                     │
│ Brand Guidelines:                                   │
│ ☐ Brand Approved                                    │
│ [Guideline Text: "Always show smiling..."___]      │
│                                                     │
│ [SAVE AS TEMPLATE] [PREVIEW] [CANCEL]              │
└─────────────────────────────────────────────────────┘

SECTION 2: MY DESIGN LIBRARY
┌─────────────────────────────────────────────────────┐
│ Filter: [All Types ▼] [All Categories ▼] Search:   │
│                                                     │
│ ┌─────────────┬─────────────┬─────────────┐        │
│ │ [Carl]      │ [Logo]      │ [Background]│        │
│ │ Character   │ Logo        │ Environment │        │
│ │ Used: 47x   │ Used: 12x   │ Used: 89x   │        │
│ │ ✓ Approved  │ ✓ Approved  │ ✓ Approved  │        │
│ │ [Edit][Use] │ [Edit][Use] │ [Edit][Use] │        │
│ └─────────────┴─────────────┴─────────────┘        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### Detailed Elements:

**1. Element Type Selector**
- Radio buttons: Character, Logo, Environment, Prop, Animation Style
- Each type has different required fields

**2. Visual Reference Upload**
- Drag & drop or file upload
- Preview in real-time
- Support: PNG, JPG, MP4, GIF
- Guidance: "Upload reference image (min 512x512)"

**3. Description Editor**
- Rich text editor for visual description
- Preview: Shows how this will be injected into prompts
- Example snippets for each type
- Character count: 50-1000 chars

**4. Category Selector**
- Dropdown: Training, Marketing, Operations, Safety, Custom
- Pre-defined categories for organization

**5. Tags System**
- Add multiple tags (friendly, mascot, professional, etc.)
- Searchable/filterable
- Suggested tags based on category

**6. Brand Guidelines**
- Checkbox: "Brand Approved"
- Text field: Usage guidelines
- Examples: "Never show angry", "Always professional", "Use brand colors"

**7. My Design Library**
- Grid view of all created templates
- Shows: thumbnail, name, type, usage count, approval status
- Edit button: Opens element for modification
- Use button: Takes to video generator with element pre-selected
- Delete button: Remove template

---

## Integration with Video Generator

### Quick Presets Enhancement
```
QUICK PRESETS SECTION
┌─────────────────────────────────────────────────────┐
│ DESIGN ELEMENTS - Select components for consistency │
│                                                     │
│ CHARACTER:  [▼ Select Character]                    │
│             └─ ☐ Carl (purple monster, friendly)    │
│             └─ ☐ Bob (blue robot, technical)        │
│             └─ ☐ None (no character)                │
│                                                     │
│ BACKGROUND: [▼ Select Environment]                  │
│             └─ ☐ Walmart Store Interior             │
│             └─ ☐ Outdoor Parking Lot                │
│             └─ ☐ Training Room                      │
│                                                     │
│ LOGO:       [▼ Select Logo]                         │
│             └─ ☐ Walmart Main Logo                  │
│             └─ ☐ Department Logo                    │
│                                                     │
│ STYLE:      [▼ Select Animation Style]              │
│             └─ ☐ Professional Corporate             │
│             └─ ☐ Friendly/Approachable              │
│             └─ ☐ Energetic/Dynamic                  │
│                                                     │
│ MESSAGE:    [Input operational message__________]   │
│                                                     │
│ [GENERATE VIDEO] [PREVIEW] [SAVE PRESET]            │
└─────────────────────────────────────────────────────┘
```

### Prompt Injection Flow
```
User selects design elements:
  - Character: Carl
  - Background: Walmart Store
  - Logo: Main Logo
  - Message: "Complete your annual safety training"

System generates prompt:
  "Create a video featuring Carl, a friendly purple 
   monster mascot, in a professional Walmart store 
   environment. Include the Walmart logo prominently. 
   The message should be: 'Complete your annual 
   safety training.' 
   Style: Professional and approachable.
   Brand Guidelines: Always show Carl smiling..."
```

---

## Data Flow Architecture

### Design Studio Creation Flow
```
User Input
    ↓
[Design Studio UI]
    ↓
Validation (name, type, description)
    ↓
Store DesignElement
    ↓
[design_elements.json] ← Persisted
    ↓
Show in "My Designs" Library
```

### Video Generation Flow with Design Elements
```
User selects design elements + message
    ↓
[Generate Button]
    ↓
Retrieve selected DesignElement objects
    ↓
Build composite prompt with:
  - Character description
  - Environment description
  - Logo placement instructions
  - Animation style
  - Operational message
    ↓
[LLM Prompt Enhancement]
    ↓
Send to Walmart Media Studio API
    ↓
Generate Video ✅
    ↓
Increment usage_count for each element
```

---

## Enterprise Scaling Considerations

### 1. Multi-Facility Support
```python
# Each facility gets its own namespace
design_element:
  facility_id: str            # Which facility created this
  visibility: str             # "private" | "facility" | "region" | "company"
  shared_facilities: List[str]  # Can share with other facilities
```

### 2. Brand Compliance Approval Workflow
```
Facility Creates Design Element
  ↓
[Awaiting Corporate Approval]
  ↓
Corporate Admin Reviews
  ↓
[Approved ✓] / [Rejected ✗] + Comments
  ↓
If Approved: Available in Facility's Design Library
If Rejected: Returned for revision
```

### 3. Design Library Export/Import
- Export facility's design library as JSON
- Import corporate approved templates
- Sync with company-wide design standards

### 4. Analytics & Insights
```
Design Element Usage Dashboard:
- Which elements are most used?
- Which facilities use which elements?
- Performance metrics (video views, engagement)
- Compliance status
```

### 5. Version Control
```
DesignElement:
  version: int
  previous_versions: List[Dict]  # Track changes
  change_log: List[str]
```

---

## File Structure
```
src/
├── models/
│   └── design_element.py       # DesignElement model
├── services/
│   └── design_studio_service.py # Design management logic
├── ui/
│   ├── pages/
│   │   └── design_studio.py    # UI for design creation
│   └── components/
│       └── design_selector.py  # Reusable selector component
└── db/
    └── design_elements.json    # Persistent storage

app_design_studio.py            # Full Design Studio page
app.py                          # Updated with Design Studio link
```

---

## Implementation Phases

### Phase 1 (MVP - This week)
- ✅ Design Element model
- ✅ Basic CRUD operations
- ✅ Design Studio UI page
- ✅ Integration with video generator (pre-selection)
- Local JSON storage

### Phase 2 (Next week - Enterprise Ready)
- Facility-level isolation
- Brand approval workflow
- Export/import functionality
- Usage analytics

### Phase 3 (Enterprise Scale)
- Database backend (PostgreSQL)
- Multi-tenant support
- API for external systems
- Advanced compliance features
- AI-powered design suggestions

---

## Business Value
- **Consistency**: All 4000+ facilities use same approved designs
- **Scalability**: Add new designs once, use everywhere
- **Brand Compliance**: Approval workflow ensures on-brand content
- **Speed**: Pre-built elements reduce generation time
- **Professionalism**: Curated templates ensure quality
- **Efficiency**: Reusable components reduce production cost
