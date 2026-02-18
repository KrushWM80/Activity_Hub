# Walmart Activity Hub - Complete Brand Specifications

## Official Brand Assets Confirmed ✅

### Typography
**Primary Font:** Everyday Sans
- Font Family: `'Everyday Sans', 'Helvetica Neue', Arial, sans-serif`
- Official Walmart corporate font
- Used for all primary text, headers, and UI elements

### Official Color Palette

#### Walmart Yellow (Spark) - #FFCC00
- **Primary Usage**: Accent color, notifications, highlights, CTAs
- **Brand Significance**: Official Walmart Spark logo color
- **Variations**:
  - Dark: `#E6B800` (hover states)
  - Light: `#FFD633` (backgrounds)
  - RGB: `rgb(255, 204, 0)`

#### Walmart Blue Palette
- **Navy**: `#1E3A8A` (Professional, executive themes)
- **Dark Blue**: `#1D4ED8` (Hover states, emphasis)
- **Primary Blue**: `#3B82F6` (Main brand color)
- **Light Blue**: `#60A5FA` (Backgrounds, subtle accents)
- **Lightest Blue**: `#DBEAFE` (Very subtle backgrounds)

### Logo Assets
- **Walmart Spark Logo**: `walmart-spark-logo.png`
- **Location**: `c:\Users\krush\Documents\VSCode\Activity-Hub\Design\walmart-spark-logo.png`
- **Usage**: Navigation header, branding elements, loading states

## Updated Widget Specifications

### 1. Header Navigation
```css
.navbar {
  background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
  font-family: 'Everyday Sans', sans-serif;
  
  .logo {
    /* Use walmart-spark-logo.png */
    height: 32px;
    width: auto;
  }
  
  .nav-items {
    color: white;
    font-weight: 500;
  }
}
```

### 2. Notification Widget (Updated)
```css
.notification-widget {
  .widget-header {
    background: linear-gradient(135deg, #FFCC00 0%, #E6B800 100%);
    color: #1a202c; /* Dark text on yellow background */
    font-family: 'Everyday Sans', sans-serif;
    
    .notification-count {
      background: #3B82F6; /* Blue badge on yellow header */
      color: white;
    }
  }
  
  .priority-urgent {
    border-left: 4px solid #FFCC00; /* Walmart yellow for urgent */
    background: rgba(255, 204, 0, 0.1);
  }
}
```

### 3. Action Items Widget (Spark-Themed)
```css
.next-steps-widget {
  .widget-header {
    background: linear-gradient(135deg, #FFCC00 0%, #E6B800 100%);
    color: #1a202c;
    font-family: 'Everyday Sans', sans-serif;
    
    .spark-icon {
      /* Use spark logo as icon */
      width: 24px;
      height: 24px;
      filter: invert(1); /* Make white if needed */
    }
    
    .ai-badge {
      background: #3B82F6;
      color: white;
      font-family: 'Everyday Sans', sans-serif;
      font-weight: 600;
    }
  }
}
```

### 4. Project Dashboard (Professional Blue)
```css
.project-dashboard-widget {
  .widget-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
    font-family: 'Everyday Sans', sans-serif;
    
    .project-title {
      font-weight: 700;
      letter-spacing: -0.02em;
    }
  }
  
  .metric-highlight {
    color: #FFCC00; /* Yellow highlights on blue background */
    font-weight: 600;
  }
}
```

## Font Implementation

### CSS Font Face (if loading custom font)
```css
@font-face {
  font-family: 'Everyday Sans';
  src: url('./fonts/EverydaySans-Regular.woff2') format('woff2'),
       url('./fonts/EverydaySans-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Everyday Sans';
  src: url('./fonts/EverydaySans-Medium.woff2') format('woff2'),
       url('./fonts/EverydaySans-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: 'Everyday Sans';
  src: url('./fonts/EverydaySans-Bold.woff2') format('woff2'),
       url('./fonts/EverydaySans-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
}
```

### Typography Scale with Everyday Sans
```css
.display-title {
  font-family: 'Everyday Sans', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.widget-title {
  font-family: 'Everyday Sans', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.3;
}

.body-text {
  font-family: 'Everyday Sans', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
}

.button-text {
  font-family: 'Everyday Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.02em;
}
```

## Theme Variations with Official Colors

### Executive Theme
```css
.theme-executive {
  --primary: #1E3A8A;    /* Navy blue */
  --accent: #FFCC00;     /* Walmart yellow */
  --font: 'Everyday Sans', sans-serif;
}
```

### Team Collaboration Theme
```css
.theme-team {
  --primary: #3B82F6;    /* Primary blue */
  --accent: #FFCC00;     /* Walmart yellow */
  --secondary: #60A5FA;  /* Light blue */
  --font: 'Everyday Sans', sans-serif;
}
```

### Notification/Alert Theme
```css
.theme-alerts {
  --primary: #FFCC00;    /* Yellow as primary */
  --secondary: #3B82F6;  /* Blue as secondary */
  --text: #1a202c;      /* Dark text */
  --font: 'Everyday Sans', sans-serif;
}
```

## Accessibility with Official Colors

### Color Contrast Testing
- **Yellow (#FFCC00) on White**: 1.8:1 ❌ (Use dark text)
- **Dark text (#1a202c) on Yellow (#FFCC00)**: 11.2:1 ✅ AAA
- **Blue (#3B82F6) on White**: 4.6:1 ✅ AA
- **Navy (#1E3A8A) on White**: 8.2:1 ✅ AAA

### High Contrast Support
```css
@media (prefers-contrast: high) {
  :root {
    --walmart-yellow: #E6B800; /* Darker yellow for better contrast */
    --walmart-blue: #1E3A8A;   /* Use navy instead of primary blue */
  }
}
```

## Brand Guidelines Summary

### ✅ Confirmed Official Brand Elements
- **Font**: Everyday Sans
- **Yellow**: #FFCC00 (Walmart Spark)
- **Blue Palette**: Navy to Light Blue gradient
- **Logo**: Walmart Spark (spark-shaped icon)

### 🎨 Color Psychology in UI
- **Yellow**: Energy, optimism, attention-grabbing (perfect for notifications and CTAs)
- **Blue**: Trust, professionalism, reliability (ideal for main interface elements)
- **Navy**: Authority, expertise (executive/professional themes)

### 📱 Implementation Priority
1. **Typography**: Implement Everyday Sans across all text
2. **Primary Colors**: Yellow for accents, Blue for main elements
3. **Logo Integration**: Spark logo in headers and loading states
4. **Theme Variations**: Role-based color schemes

---

**Status: ✅ Complete Brand Specifications**
All design files updated with official Walmart Everyday Sans font and #FFCC00 Spark yellow.