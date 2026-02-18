# Figma Video Creation Specifications
## AMP Video: "Protecting Yourself from Illness During the Winter Months"

### Frame Setup
```
Frame Name: AMP_Video_Frame
Dimensions: 1920 x 1080 px
Background: #FFFFFF
```

### Color Palette (Add to Figma Styles)
```css
/* Primary Colors */
Walmart Blue: #0071CE
Walmart Yellow: #FFC220
White: #FFFFFF
Text Dark: #000000
Text Light: #666666
```

### Typography Styles
```css
/* Title Text */
Font Family: Arial Bold
Font Size: 72px
Line Height: 80px
Color: #0071CE
Alignment: Center

/* Subtitle Text */
Font Family: Arial Regular
Font Size: 36px
Line Height: 44px
Color: #666666
Alignment: Center

/* Body Text */
Font Family: Arial Regular
Font Size: 48px
Line Height: 56px
Color: #000000
Alignment: Left

/* Small Text */
Font Family: Arial Regular
Font Size: 32px
Line Height: 38px
Color: #666666
Alignment: Left
```

### Slide Components (Create as Components in Figma)

#### Slide 1: Title Slide (0-3 seconds)
```
Background: #FFFFFF
Header Container:
  - Background: #0071CE
  - Height: 200px
  - Width: 1920px
  - Position: Top

Walmart Logo:
  - Size: 120px x 120px
  - Position: Top center
  - Color: #FFFFFF (white spark logo)

Title Text:
  - "Protecting Yourself from Illness During the Winter Months"
  - Font: Arial Bold, 64px
  - Color: #FFFFFF
  - Position: Center below logo

Week Indicator:
  - "Week 41 • 2026"
  - Font: Arial Regular, 36px
  - Color: #FFC220
  - Position: Bottom of header
```

#### Slide 2: Key Point 1 (4-12 seconds)
```
Background: #FFFFFF

Content Container:
  - Padding: 120px
  - Width: 1680px (1920 - 240 padding)

Main Text:
  - "Overall associate well-being is a top priority as you continue to support your communities through the upcoming holiday season."
  - Font: Arial Regular, 56px
  - Color: #000000
  - Line Height: 68px

Highlight Text:
  - "It could be a busy flu and strep season, and we want you to stay healthy and well."
  - Font: Arial Bold, 56px
  - Color: #0071CE
  - Margin Top: 40px

Health Icon:
  - Size: 120px x 120px
  - Position: Top right corner
  - Color: #FFC220
```

#### Slide 3: Key Point 2 (13-21 seconds)
```
Background: #FFFFFF

Content Container:
  - Two columns layout
  - Left column: 60% width
  - Right column: 40% width
  - Padding: 80px

Left Column Text:
  - "All associates have easy and convenient access to a flu shot and other vaccines."
  - Font: Arial Bold, 48px
  - Color: #0071CE
  - Margin Bottom: 30px

Bullet Points:
  - Font: Arial Regular, 36px
  - Color: #000000
  - Line Height: 44px
  - Bullet Color: #FFC220

Key Dates Box:
  - Background: #0071CE
  - Border Radius: 12px
  - Padding: 30px
  - Text Color: #FFFFFF
  - "Immunization Events: Nov. 15 & Dec. 6"

Right Column:
  - Calendar icon (120px)
  - Vaccine icon (120px)
  - Icons color: #FFC220
```

#### Slide 4: Link Reference (22-27 seconds)
```
Background: #FFFFFF

QR Code Container:
  - Size: 300px x 300px
  - Position: Left center
  - Background: #FFFFFF
  - Border: 4px solid #0071CE

Link Text:
  - "Review more details here:"
  - Font: Arial Regular, 48px
  - Color: #000000
  - Position: Right of QR code

URL Display:
  - "amp2-cms.prod.walmart.com"
  - Font: Arial Bold, 36px
  - Color: #0071CE
  - Position: Below link text

CTA Button:
  - Background: #FFC220
  - Width: 400px
  - Height: 80px
  - Border Radius: 40px
  - Text: "Scan to Learn More"
  - Font: Arial Bold, 32px
  - Color: #000000
```

#### Slide 5: Call to Action (28-30 seconds)
```
Background: #0071CE

Content Container:
  - Padding: 100px
  - Text Alignment: Center

Main CTA:
  - "Management, review the Associate Talking Points"
  - Font: Arial Bold, 56px
  - Color: #FFFFFF
  - Line Height: 68px

Secondary Text:
  - "to address associate questions as needed"
  - Font: Arial Regular, 44px
  - Color: #FFC220
  - Margin Top: 20px

Bottom Button:
  - Background: #FFC220
  - Width: 300px
  - Height: 80px
  - Border Radius: 40px
  - Text: "Learn More"
  - Font: Arial Bold, 36px
  - Color: #000000
  - Position: Bottom center
```

### Animation Timeline (for Figma Prototyping)
```
Frame 1 (0-3s): Title slide fade in
Frame 2 (4-12s): Content slide with text animation
Frame 3 (13-21s): Multi-column layout with icon animations
Frame 4 (22-27s): QR code emphasis with pulse effect
Frame 5 (28-30s): Final CTA with button hover effect

Transitions: 
- Duration: 0.3s
- Easing: Ease Out
- Type: Slide from right (except first frame)
```

### Export Settings
```
Format: MP4
Quality: High
Frame Rate: 30 fps
Duration: 30 seconds exactly
Resolution: 1920 x 1080
File Size Target: Under 50MB
```

### Figma Plugin Recommendations
1. **Video Export Plugin**: "Video Figma" or "Figma to Video"
2. **QR Code Generator**: "QR Code Generator"
3. **Icon Library**: "Iconify" for health/calendar icons
4. **Animation**: "Figma Animation" or export frames for external video editor

### Step-by-Step Figma Workflow
1. Create new file: 1920x1080 frame
2. Set up color styles and text styles
3. Create components for each slide
4. Build timeline with 5 frames
5. Add transitions between frames
6. Export as video or individual frames
7. Add voiceover in post-production if needed