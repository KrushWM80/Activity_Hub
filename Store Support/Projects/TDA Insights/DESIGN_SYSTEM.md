# TDA Insights Dashboard - Design System Documentation

## Design Philosophy

The TDA Insights Dashboard is built on the **Walmart Living Design System** with a focus on:
- **Clarity & Simplicity** - Easy to understand at a glance
- **Accessibility** - WCAG AA compliant color contrasts and interactive elements
- **Consistency** - Unified visual language across all components
- **Efficiency** - Quick interactions, minimal clicks to get insights
- **Professionalism** - Executive-ready interface

## Color Palette

### Primary Colors

```
Walmart Blue (Primary)
  Hex: #0071CE
  RGB: (0, 113, 206)
  Usage: Main actions, links, focused states, important data
  
Walmart Blue Dark (Headers)
  Hex: #1E3A8A
  RGB: (30, 58, 138)
  Usage: Page headers, navigation backgrounds
  
Walmart Blue Light (Hover/Focus)
  Hex: #DBEAFE
  RGB: (219, 234, 254)
  Usage: Hover states, selection backgrounds
```

### Accent Color

```
Walmart Yellow (Spark)
  Hex: #FFCC00
  RGB: (255, 204, 0)
  Usage: Highlights, call-to-action accents, borders
  
Walmart Yellow Dark
  Hex: #FFA500
  RGB: (255, 165, 0)
  Usage: Darker accents, secondary highlights
```

### Status Colors

```
Success (On Track)
  Hex: #107C10
  RGB: (16, 124, 16)
  Usage: Success states, on-track initiatives
  
Warning (At Risk)
  Hex: #F7630C
  RGB: (247, 99, 12)
  Usage: Warning states, at-risk initiatives
  
Error (Off Track)
  Hex: #DC3545
  RGB: (220, 53, 69)
  Usage: Error states, off-track initiatives
```

### Neutral Colors

```
Text Primary
  Hex: #212121
  RGB: (33, 33, 33)
  Usage: Main text content
  
Text Secondary
  Hex: #666666
  RGB: (102, 102, 102)
  Usage: Secondary text, labels, hints
  
Border Color
  Hex: #E5E5E5
  RGB: (229, 229, 229)
  Usage: Dividers, lines, borders
  
Background Light
  Hex: #F5F5F5
  RGB: (245, 245, 245)
  Usage: Page background, light backgrounds
  
White
  Hex: #FFFFFF
  RGB: (255, 255, 255)
  Usage: Card backgrounds, paper surface
```

## Typography

### Font Family

```
Primary: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif
```

This system font stack ensures:
- Native look on each platform
- Fast loading (no web font overhead)
- Excellent readability
- Fallback compatibility

### Font Weights

```
Light (300)     - Rarely used, very light text
Regular (400)   - Body text, standard content
Semi-bold (600) - Labels, highlights, badges
Bold (700)      - Headers, important text
```

### Type Scale

```
Small (12px)
  Line Height: 16px (1.33)
  Usage: Labels, captions, fine print
  Margins: 4px

Base (14px)
  Line Height: 21px (1.5)
  Usage: Body text, table content, standard text
  Margins: 8px

Large (16px)
  Line Height: 24px (1.5)
  Usage: Subheadings, filter labels
  Margins: 16px

X-Large (18px)
  Line Height: 27px (1.5)
  Usage: Section headers
  Margins: 16px

2X-Large (24px)
  Line Height: 32px (1.33)
  Usage: Page headings, slide titles
  Margins: 24px
```

## Spacing System

All spacing uses multiples of 8px for consistent rhythm:

```
4px   (--spacing-xs)  - x-small gaps
8px   (--spacing-sm)  - small gaps, component padding
16px  (--spacing-md)  - medium gaps, between sections
24px  (--spacing-lg)  - large gaps, between major sections
32px  (--spacing-xl)  - x-large gaps, container padding
```

## Component Specifications

### Header

**Design Principles:**
- High contrast for quick identification
- Brand colors prominently displayed
- Status indicator for system health

**Specifications:**
- Background: Linear gradient (Dark Blue → Blue)
- Height: 80px
- Logo: Emoji (💼) at 32px
- Title: 24px Bold, White text
- Subtitle: 12px, muted white
- Yellow left border: 3px on title section
- Box shadow: Subtle drop shadow (0 2px 8px)

**Responsive:**
- Mobile (< 768px): Stack elements vertically
- Tablet (768px-1024px): Side-by-side layout
- Desktop (> 1024px): Full layout with status indicator

### Filter Section

**Design Principles:**
- Scannable with clear labels
- Obvious action buttons
- Grouped related controls

**Specifications:**
- Background: White
- Padding: 24px
- Border radius: 8px
- Box shadow: Subtle (0 1px 3px)
- Filter label: 14px, 600 weight
- Dropdowns: 2px border, focus state with blue shadow
- Button group: Flex with 8px gaps

**Button Styles:**

**Primary Button (.btn-primary)**
- Background: #0071CE (Walmart Blue)
- Color: White
- Padding: 10px 24px
- Border radius: 4px
- Hover: Darker blue with shadow
- Font: 14px, 600 weight

**Secondary Button (.btn-secondary)**
- Background: White
- Color: #0071CE
- Border: 2px solid blue
- Padding: 10px 24px
- Hover: Light blue background
- Font: 14px, 600 weight

### Summary Cards

**Design Principles:**
- Quick scannable metrics
- Color-coded importance
- Left border accent

**Specifications:**
- Background: White
- Padding: 24px
- Border radius: 8px
- Left border: 4px solid yellow
- Grid: Auto-fit, min 250px columns
- Gap: 24px
- Box shadow: Subtle (0 1px 3px)

**Card Content:**
- Label: 12px, uppercase, secondary text
- Value: 24px, bold, dark blue
- Detail: 12px, secondary text

### Data Table

**Design Principles:**
- Clear hierarchy
- Scannable rows
- Status-based color coding

**Specifications:**
- Header: Light gray background, 2px bottom border
- Footer: Light gray background, 2px top border
- Row height: 48px
- Padding: 16px per cell
- Hover row: Light blue background
- Striped: Optional alternating row colors
- Column alignment: Left (text), Right (numbers)

**Special Columns:**

**Health Status Badge:**
- On Track: Green (#107C10) background with 20% opacity
- At Risk: Orange (#F7630C) background with 20% opacity
- Off Track: Red (#DC3545) background with 20% opacity
- Padding: 4px 10px
- Border radius: 12px
- Font: 12px, 600 weight

**Phase Tag:**
- Background: Light blue (#DBEAFE)
- Color: Dark blue (#1E3A8A)
- Padding: 4px 10px
- Border radius: 4px
- Font: 12px, 500 weight

**Number Column:**
- Color: Walmart Blue (#0071CE)
- Font weight: 600
- Text align: Right

### Badges & Tags

**Health Status Badges:**
```
┌─────────────────────────────────┐
│ ● On Track                      │  Green badge
│ ⚠ At Risk                       │  Orange badge
│ ✗ Off Track                     │  Red badge
└─────────────────────────────────┘
```

**Phase Tags:**
```
┌─────────────┐
│ Test        │  Blue tag
│ Production  │  Blue tag
│ Planning    │  Blue tag
└─────────────┘
```

### Empty State

**Design Principles:**
- Friendly and helpful
- Clear explanation
- Action-oriented suggestions

**Specifications:**
- Icon: 48px emoji (📭, 📊, ⚠️)
- Title: 18px, bold
- Message: 14px, secondary text
- Padding: 32px
- Text align: Center

### Loading State

**Design Principles:**
- Non-intrusive but visible
- Smooth animation
- Clear feedback

**Specifications:**
- Loader: Spinning circle
- Border: 3px gray border
- Top border: 3px blue (#0071CE)
- Size: 20px diameter
- Animation: 1s linear infinite rotation
- Gap between spinner and text: 16px

### Footer

**Design Principles:**
- Non-intrusive
- Informational only
- Minimal visual weight

**Specifications:**
- Background: Transparent
- Padding: 16px
- Border top: 1px border-color
- Font: 12px, secondary text
- Text align: Center
- Margin top: 32px

## Responsive Design

### Breakpoints

```
Mobile:  < 768px   (Single column, stacked layout)
Tablet:  768px-1024px (Two column, adjusted spacing)
Desktop: > 1024px  (Full multi-column layout)
```

### Mobile Optimizations

**Header:**
- Stack logo, title, and status vertically
- Reduce font sizes by 10-20%
- Adjust padding to 16px

**Filters:**
- Single column dropdown
- Full-width buttons stacked
- Reduce padding to 16px

**Table:**
- Reduce font size to 12px
- Reduce padding to 12px
- Enable horizontal scrolling
- Show critical columns only

**Cards:**
- Single column layout
- Reduce padding to 16px
- Increase font sizes slightly for readability

### Accessibility

**Color Contrast:**
- All text meets WCAG AA standard (4.5:1 for small text)
- Color + pattern used for status indicators
- No color-only information conveyance

**Typography:**
- Minimum font size: 12px (readable on all devices)
- Line height: ≥ 1.5 for body text
- Letter spacing: Natural (not too tight)

**Interactive Elements:**
- Minimum 40x40px touch targets (mobile)
- Focus states clearly visible (blue outline)
- Buttons have sufficient padding (10px)

**Semantic HTML:**
- Proper heading hierarchy (h1, h2, etc.)
- Form labels associated with inputs
- Alt text on images

## Animation & Transitions

### Duration & Easing

```css
Fast (200ms):    Hover states, button feedback
Medium (300ms):  Modal open/close, transitions
Slow (500ms):    Large layout changes
Easing:          ease (default) for most transitions
```

### Examples

**Button Hover:**
```css
transition: all 0.3s ease;
/* Changes: background color, shadow */
```

**Loading Spinner:**
```css
animation: spin 1s linear infinite;
/* Continuous rotation for loading indicator */
```

**Row Hover:**
```css
transition: background-color 0.2s ease;
/* Smooth color change on row hover */
```

## Living Design Compliance Checklist

✅ **Color System**
- Uses official Walmart blues and yellow
- Status colors for at-risk/off-track items
- Proper contrast ratios

✅ **Typography**
- System font stack (no custom web fonts)
- Proper weight hierarchy
- Readable line heights and sizes

✅ **Spacing**
- Consistent 8px grid
- Proper padding and margins
- Breathing room around elements

✅ **Components**
- Consistent button styles
- Card-based layout
- Standard form elements

✅ **Branding**
- Walmart logo/icon prominent
- Colors aligned with corporate standards
- Professional appearance

✅ **Accessibility**
- WCAG AA compliant contrast
- Keyboard navigable
- Screen reader friendly

✅ **Responsive**
- Mobile-first approach
- Breakpoints for different devices
- Flexible layout

## Examples & Patterns

### Success Pattern

```
Header (Blue gradient) 
    ↓
Filters (White card with controls)
    ↓
Summary Cards (4 stats: Total, Stores, On-Track, At-Risk)
    ↓
Data Table (Striped rows, status badges)
    ↓
Footer (Muted text with timestamp)
```

### Status Color Coding

```
Initiative Status → Dashboard Color → User Perception

On Track  → Green (#107C10)  → ✅ Good
At Risk   → Orange (#F7630C) → ⚠️ Needs attention
Off Track → Red (#DC3545)    → ❌ Problem
```

### Interactive Feedback

```
Click Button
    ↓
Background color changes (instantly)
    ↓
Shadow appears (smooth 0.3s)
    ↓
User confirms action
```

## CSS Variables Reference

```css
:root {
    /* Colors */
    --walmart-blue-dark: #1E3A8A;
    --walmart-blue: #0071CE;
    --walmart-blue-light: #DBEAFE;
    --walmart-yellow: #FFCC00;
    --walmart-yellow-dark: #FFA500;
    --text-primary: #212121;
    --text-secondary: #666666;
    --border-color: #E5E5E5;
    --bg-light: #F5F5F5;
    --success: #107C10;
    --warning: #F7630C;
    --error: #DC3545;
    
    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    
    /* Typography */
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-size-sm: 12px;
    --font-size-base: 14px;
    --font-size-lg: 16px;
    --font-size-xl: 18px;
    --font-size-2xl: 24px;
}
```

## When Building New Features

1. **Use the color palette** - Don't add new colors
2. **Follow the type scale** - Use defined font sizes
3. **Respect spacing** - Use multiples of 8px
4. **Maintain contrast** - Test with accessibility tools
5. **Keep consistency** - Match existing components
6. **Test responsiveness** - Verify on mobile/tablet/desktop
7. **Check accessibility** - Use WAVE or aXe tools

## Resources

- [Walmart Living Design Documentation](https://www.walmart.com/brand/)
- [WCAG Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [CSS Variables Best Practices](https://web.dev/css-variables/)
- [Font Pairing Guide](https://www.smashingmagazine.com/)
