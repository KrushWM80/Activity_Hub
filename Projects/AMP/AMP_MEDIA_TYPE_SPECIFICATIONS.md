# AMP Activity-Hub Media Type Generation Specifications

## Workflow Overview (3-Step Process)

### Step 1: User Selects AMP Activity from Dropdown
- **Data Source:** BigQuery `wmt-edw-prod.WW_SOA_DL_VM.STORE_OPS_APPLN_ACTV_MGMT_PLAN_MSG_EVENT`
- **Filter Criteria:** Primary Status = "Review for Publish" OR "Published"
- **Display Fields in Dropdown:**
  - Event Title (e.g., "Your Week 4 Messages Are Here")
  - Event ID
  - Message Body (preview)
  - Role
  - Team
  - Status

### Step 2: User Selects Media Type
Available media types:
- **Audio - Reading** (narrate message body, word-for-word)
- **Audio - Podcast** (conversational summary format)
- **Audio - Speech** (emphasis on key action items)
- **Video - Short Clip** (30-60 seconds visual summary)
- **Video - Long Clip** (2-5 minutes deep dive)
- **InfoGraphic - Single** (one visual summary)
- **InfoGraphic - Multiple** (multi-page visual, may require multiple Event IDs)

### Step 3: Generate Script and Media Based on Media Type

---

## Media Type Scripts

### Audio - Reading
**Purpose:** Read the Message Body word-for-word with minimal changes, presented as exciting new happenings in their store.

**Script Structure:**
1. Small intro greeting (e.g., "Hello! Your Week 4 Messages Are Here!")
2. Call-to-action reference (e.g., "Please visit the Landing Page for full content")
3. Full Message Body (preserve structure, punctuation, sections)
4. Closing (e.g., "Thank you and have a Great Day!")

**Tone:** Professional, enthusiastic, urgent updates
**Duration:** 8-15 minutes (depends on message length)
**Changes to Message Body:** Minimal
- Replace em-dashes with proper pauses (or keep as-is for natural reading)
- Keep section headers and department numbers exactly as written
- No summarization or content reduction

**Example for Event ID: 91202b13-3e65-4870-885f-f4a66e221eed**

```
Hello! Your Week 4 Messages Are Here!

Please visit the Landing Page to access full content.

Food & Consumables Merchant Messages:

Beauty & Consumables
Beauty in waiting: Maybelline modular reset hits a snag.
[... continue with exact message body ...]

Thank you and have a Great Day!
```

---

### Audio - Podcast (TBD)
**Purpose:** Conversational summary of key updates
**Format:** Host-style narration with callouts
**Duration:** 5-8 minutes
**Changes to Message Body:** Moderate summarization

---

### Audio - Speech (TBD)
**Purpose:** Focus on critical action items
**Format:** Urgent, actionable deliverables
**Duration:** 3-5 minutes
**Changes to Message Body:** High-level extraction

---

### Video - Short Clip (TBD)
**Purpose:** Visual 30-60 second teaser
**Format:** Motion graphics, text overlay, music bed
**Duration:** 30-60 seconds

---

### Video - Long Clip (TBD)
**Purpose:** Comprehensive video walkthrough
**Format:** Presenter or motion graphics with details
**Duration:** 2-5 minutes

---

### InfoGraphic - Single (TBD)
**Purpose:** One-page visual summary
**Format:** Poster-style, section-organized

---

### InfoGraphic - Multiple (TBD)
**Purpose:** Multi-page visual breakdown
**Format:** Series of connected graphics
**Notes:** May require multiple Event IDs or splitting single event into multiple pages

---

## Message Body Standards

### Current Event: 91202b13-3e65-4870-885f-f4a66e221eed
**Source:** https://amp2-cms.prod.walmart.com/preview/91202b13-3e65-4870-885f-f4a66e221eed/4/2027

**Sections:**
1. Title & Landing Page Reference
2. Food & Consumables Merchant Messages (Beauty, Food, Fresh)
3. General Merchandise Merchant Messages (Entertainment, Fashion, Hardlines, Home, Seasonal)
4. Operations Messages (Asset Protection, Backroom, Front End, Store Fulfillment, People)

**Key Formatting Rules:**
- Preserve exact department numbers (Dept. 90, Dept. 95, etc.)
- Keep all quoted text (e.g., "Strawberry Shortcake")
- Preserve em-dashes and punctuation from source
- Maintain section headers exactly as written
- Include all "Know the clean floor safety tips" callouts

---

## Implementation Priority

**Phase 1 (Current):** Audio - Reading
- Script-based message body reading
- Multiple voice options (David male, Zira female)
- Professional TTS narration
- WAV output format

**Phase 2:** Audio - Podcast (conversational)
**Phase 3:** Video and Infographics
**Phase 4:** Event ID filtering and dropdown UI

---

## Technical Notes

- **Message Body Source:** `msg_txt` field from BigQuery event table
- **Event Filtering:** Status = "Review for Publish" or "Published"
- **Voice Options:** Microsoft David Desktop, Microsoft Zira Desktop (extensible)
- **Output Formats:** WAV (audio), MP4 (video), PNG/SVG (graphics)
- **Naming Convention:** `[Event Title] - [Media Type] - [Variant].wav`

