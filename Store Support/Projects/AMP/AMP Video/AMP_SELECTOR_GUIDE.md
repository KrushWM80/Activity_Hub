# 🎬 AMP Selector & Figma Video Creator Dashboard

## Overview
Interactive HTML dashboard that allows users to:
1. Browse available AMP titles
2. Preview AMP content details
3. Open AMP preview links in new window
4. Generate Figma specifications for video creation

## Features

### 📋 Title Selection Panel (Left)
- **Search functionality** - Find AMPs by title or category
- **List of available AMP titles** - Click any title to view details
- **Week and category tags** - Quick reference for organization date
- **Visual selection** - Selected item highlighted in blue

### 👁️ Preview & Actions Panel (Right)
- **Full AMP details display** - Title, week, category, description, preview link
- **Open AMP Preview button** - Opens actual AMP content in new browser tab
- **Generate Figma Code button** - Creates video specifications automatically

### 🎨 Figma Specifications Output
- **Formatted JSON data** - Ready for Figma implementation
- **Slide-by-slide breakdown** - Title slide, content slide, CTA slide
- **Animation specifications** - Timing, transitions, and effects
- **Color palette** - Walmart brand colors included
- **Copy to clipboard** - One-click copy of all specifications

### 📊 Statistics Dashboard
- **Total AMP Titles** - Count of available content
- **Selected Title** - Currently selected AMP ID
- **Videos Generated** - Increments when Figma code is created

## Usage Workflow

### Step 1: Select an AMP Title
1. Open `amp_selector_dashboard.html` in browser
2. Browse the list of AMP titles on the left
3. Click any title to select it

### Step 2: Preview the Content
- Right panel shows all details about selected AMP
- Read title, week, category, and content preview
- Click "🔗 Open AMP Preview" to see the actual AMP content

### Step 3: Generate Figma Code
1. Click "🎨 Generate Figma Code" button
2. Figma panel appears with complete specifications
3. Review the JSON structure
4. Click "📋 Copy All Code" to copy to clipboard

### Step 4: Use in Figma
1. Open your Figma project
2. Paste the specifications as reference
3. Create frames and components according to the specs
4. Design your 30-second video

## Current Sample Data

5 AMP titles are included as samples:
1. **Protecting Yourself from Illness** (Week 41) - Health & Safety
2. **Holiday Safety Tips** (Week 40) - Safety
3. **Mental Health Awareness** (Week 39) - Wellness
4. **Holiday Gratitude** (Week 38) - Culture
5. **Managing Holiday Stress** (Week 37) - Wellness

## Figma Code Structure

The generated code includes:

```json
{
  "project": "AMP Video Creation",
  "frame_setup": {...},
  "slides": [
    {"name": "Title_Slide", ...},
    {"name": "Content_Slide", ...},
    {"name": "CTA_Slide", ...}
  ],
  "animation_timeline": {...},
  "export_settings": {...},
  "color_palette": {...}
}
```

### Default Slide Structure:
- **Title Slide** (0-5s) - AMP title and week with Walmart colors
- **Content Slide** (6-25s) - Main content with description
- **CTA Slide** (26-30s) - Call-to-action with Walmart branding

## Customization

### Add More AMP Titles
Edit the `ampTitles` array in the HTML:

```javascript
const ampTitles = [
    {
        id: 1,
        title: "Your AMP Title",
        week: "Week XX • 2026",
        preview: "https://amp-preview-url",
        description: "Short description",
        content: "Main content text",
        contentArea: "Category"
    }
];
```

### Connect to Real Data
Replace sample data with:
- BigQuery query results
- CSV file import
- REST API calls
- Database queries

## Features Ready for Enhancement

- 🔄 **BigQuery Integration** - Pull real AMP titles from database
- 📥 **CSV Import** - Load titles from spreadsheet
- 💾 **Save/Export** - Store generated Figma specs as files
- 🎥 **Video Preview** - Embed video output preview
- 📧 **Email Export** - Send Figma code via email
- 🔔 **Notifications** - Alert when new AMPs are available

## Technical Details

**File:** `amp_selector_dashboard.html`
**Size:** ~25KB
**Dependencies:** None (vanilla JavaScript)
**Browser Support:** All modern browsers (Chrome, Edge, Firefox, Safari)
**Responsive:** Adapts to tablet and larger screens

## Tips & Tricks

✅ **Search is case-insensitive** - Type partial title or category
✅ **Figma code auto-populates** - No need to manually create specs
✅ **Copy button copies to clipboard** - Paste directly in Figma
✅ **Stats update in real-time** - See how many videos you've generated
✅ **Multiple selections** - Select different AMPs as needed

## Workflow Example

1. **User opens dashboard**
2. **Searches for "health"** - Filters to health-related AMPs
3. **Clicks "Protecting Yourself"** - Preview loads on right
4. **Reviews content** - Reads description and details
5. **Clicks "Open AMP Preview"** - New tab opens actual AMP
6. **Comes back to dashboard** - Clicks "Generate Figma Code"
7. **Figma panel appears** - Shows complete video specifications
8. **Copies code** - One button copy to clipboard
9. **Opens Figma** - Pastes code as reference
10. **Creates video** - Uses specifications to design 30-second video

---
**Created:** November 2025
**Purpose:** Streamline AMP to video workflow for Walmart communications team