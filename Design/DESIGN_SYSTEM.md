# Activity Hub - Design System Guide
## Based on Walmart PPT Template (240225)

*Note: This design system is created based on standard Walmart brand guidelines. Please verify specific hex codes, fonts, and measurements from the actual Walmart_PPT_Template_240225.pptx file and update accordingly.*

## Color Palette

### Primary Colors
```css
/* Walmart Blue Palette - From Official Template */
--walmart-navy: #1E3A8A;        /* Darkest blue from template */
--walmart-blue-dark: #1D4ED8;   /* Dark blue from template */
--walmart-blue: #3B82F6;        /* Primary blue from template */
--walmart-blue-light: #60A5FA;  /* Light blue from template */
--walmart-blue-lightest: #DBEAFE; /* Lightest blue from template */

/* Walmart Spark/Yellow - Official Brand Color */
--walmart-yellow: #FFCC00;      /* Official Walmart Spark Yellow */
--walmart-yellow-dark: #E6B800;  /* Darker shade for hover states */
--walmart-yellow-light: #FFD633; /* Lighter shade for backgrounds */

/* Supporting Brand Colors */
--walmart-teal: #00A0B0;
--walmart-green: #76B900;
--walmart-orange: #FF6B35;
```

### Neutral Colors
```css
/* Grays for Text and Backgrounds */
--gray-900: #1A202C;  /* Darkest text */
--gray-800: #2D3748;
--gray-700: #4A5568;
--gray-600: #718096;  /* Secondary text */
--gray-500: #A0AEC0;
--gray-400: #CBD5E0;
--gray-300: #E2E8F0;  /* Light borders */
--gray-200: #EDF2F7;  /* Light backgrounds */
--gray-100: #F7FAFC;  /* Lightest backgrounds */
--white: #FFFFFF;
```

### Status Colors
```css
/* Success States */
--success: #38A169;
--success-light: #68D391;
--success-background: #F0FFF4;

/* Warning States */
--warning: #D69E2E;
--warning-light: #F6E05E;
--warning-background: #FFFBEB;

/* Error States */
--error: #E53E3E;
--error-light: #FC8181;
--error-background: #FED7D7;

/* Info States */
--info: #3182CE;
--info-light: #63B3ED;
--info-background: #EBF8FF;
```

## Typography

### Font Families
```css
/* Primary Font - Official Walmart Font */
--font-primary: 'Everyday Sans', 'Helvetica Neue', Arial, sans-serif;

/* Secondary Font - For emphasis */
--font-secondary: 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

/* Monospace - For code and data */
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
```

### Font Sizes and Weights
```css
/* Headings */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */
--text-5xl: 3rem;       /* 48px */

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

### Typography Scale
```css
/* Display Text */
.display-large {
  font-size: var(--text-5xl);
  font-weight: var(--font-bold);
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.display-medium {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: 1.2;
  letter-spacing: -0.01em;
}

/* Headings */
.heading-1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: 1.25;
}

.heading-2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: 1.3;
}

.heading-3 {
  font-size: var(--text-xl);
  font-weight: var(--font-medium);
  line-height: 1.4;
}

/* Body Text */
.body-large {
  font-size: var(--text-lg);
  font-weight: var(--font-normal);
  line-height: 1.5;
}

.body-medium {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: 1.5;
}

.body-small {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: 1.4;
}

/* Labels and Captions */
.label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  line-height: 1.3;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.caption {
  font-size: var(--text-xs);
  font-weight: var(--font-normal);
  line-height: 1.3;
  color: var(--gray-600);
}
```

## Spacing System

### Spacing Scale
```css
--space-0: 0;
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
--space-24: 6rem;       /* 96px */
```

### Component Spacing
```css
/* Widget Padding */
--widget-padding-sm: var(--space-4);
--widget-padding-md: var(--space-6);
--widget-padding-lg: var(--space-8);

/* Grid Gaps */
--grid-gap-sm: var(--space-2);
--grid-gap-md: var(--space-4);
--grid-gap-lg: var(--space-6);

/* Section Spacing */
--section-margin-sm: var(--space-8);
--section-margin-md: var(--space-12);
--section-margin-lg: var(--space-16);
```

## Layout and Grid System

### Container Sizes
```css
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
--container-2xl: 1536px;
```

### Grid System
```css
/* 12-column grid for widgets */
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gap-md);
  padding: var(--space-6);
}

/* Widget Sizes */
.widget-small {    /* 3x2 grid */
  grid-column: span 3;
  grid-row: span 2;
}

.widget-medium {   /* 4x3 grid */
  grid-column: span 4;
  grid-row: span 3;
}

.widget-large {    /* 6x4 grid */
  grid-column: span 6;
  grid-row: span 4;
}

.widget-extra-large { /* 8x6 grid */
  grid-column: span 8;
  grid-row: span 6;
}
```

## Component Styles

### Buttons
```css
/* Primary Button */
.btn-primary {
  background-color: var(--walmart-blue);
  color: var(--white);
  border: none;
  border-radius: 8px;
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--walmart-blue-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 206, 0.3);
}

/* Secondary Button */
.btn-secondary {
  background-color: transparent;
  color: var(--walmart-blue);
  border: 2px solid var(--walmart-blue);
  border-radius: 8px;
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: var(--walmart-blue);
  color: var(--white);
}

/* Accent Button */
.btn-accent {
  background-color: var(--walmart-yellow);
  color: var(--gray-900);
  border: none;
  border-radius: 8px;
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-accent:hover {
  background-color: var(--walmart-yellow-dark);
  transform: translateY(-1px);
}
```

### Cards and Widgets
```css
.widget-card {
  background-color: var(--white);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--gray-200);
  overflow: hidden;
  transition: all 0.2s ease;
}

.widget-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
  border-color: var(--walmart-blue-light);
}

.widget-header {
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--gray-200);
  background-color: var(--gray-50);
}

.widget-title {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  color: var(--gray-900);
  margin: 0;
}

.widget-content {
  padding: var(--space-6);
}
```

### Navigation
```css
.navbar {
  background-color: var(--white);
  border-bottom: 1px solid var(--gray-200);
  padding: var(--space-4) var(--space-6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-item {
  color: var(--gray-700);
  text-decoration: none;
  padding: var(--space-2) var(--space-4);
  border-radius: 6px;
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: var(--gray-100);
  color: var(--walmart-blue);
}

.nav-item.active {
  background-color: var(--walmart-blue);
  color: var(--white);
}

.sidebar {
  background-color: var(--gray-50);
  border-right: 1px solid var(--gray-200);
  padding: var(--space-6);
  width: 280px;
}
```

### Forms
```css
.form-input {
  border: 2px solid var(--gray-300);
  border-radius: 8px;
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
  width: 100%;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--walmart-blue);
  box-shadow: 0 0 0 3px rgba(0, 113, 206, 0.1);
}

.form-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}
```

## Icons and Visual Elements

### Icon System
```css
/* Use consistent icon library (Heroicons, Feather, or Walmart custom icons) */
.icon {
  width: 1em;
  height: 1em;
  display: inline-block;
  vertical-align: middle;
}

/* Icon Sizes */
.icon-xs { width: 12px; height: 12px; }
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; }
```

### Status Indicators
```css
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: 9999px;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-success {
  background-color: var(--success-background);
  color: var(--success);
}

.status-warning {
  background-color: var(--warning-background);
  color: var(--warning);
}

.status-error {
  background-color: var(--error-background);
  color: var(--error);
}

.status-info {
  background-color: var(--info-background);
  color: var(--info);
}
```

## Animation and Transitions

### Motion Guidelines
```css
/* Easing Functions */
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

/* Duration Scale */
--duration-fast: 150ms;
--duration-normal: 200ms;
--duration-slow: 300ms;

/* Common Transitions */
.transition-all {
  transition: all var(--duration-normal) var(--ease-in-out);
}

.transition-colors {
  transition: color var(--duration-normal) var(--ease-in-out),
              background-color var(--duration-normal) var(--ease-in-out),
              border-color var(--duration-normal) var(--ease-in-out);
}

.transition-transform {
  transition: transform var(--duration-normal) var(--ease-in-out);
}
```

### Loading States
```css
.loading-spinner {
  border: 2px solid var(--gray-200);
  border-top: 2px solid var(--walmart-blue);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.skeleton {
  background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## Responsive Design

### Breakpoints
```css
/* Mobile First Approach */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

### Mobile Adaptations
```css
/* Mobile Widget Layout */
@media (max-width: 767px) {
  .grid-container {
    grid-template-columns: 1fr;
    gap: var(--grid-gap-sm);
    padding: var(--space-4);
  }
  
  .widget-small,
  .widget-medium,
  .widget-large,
  .widget-extra-large {
    grid-column: span 1;
    grid-row: auto;
  }
  
  .widget-content {
    padding: var(--space-4);
  }
}
```

## Accessibility

### Focus States
```css
.focus-visible {
  outline: 2px solid var(--walmart-blue);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Ensure sufficient color contrast */
.text-high-contrast {
  color: var(--gray-900);
}

.text-medium-contrast {
  color: var(--gray-700);
}

.text-low-contrast {
  color: var(--gray-600);
}
```

---

## Implementation Notes

### CSS Custom Properties Setup
```css
:root {
  /* Add all variables from above sections */
  /* Color variables */
  --walmart-blue: #0071CE;
  /* Typography variables */
  --font-primary: 'Walmart Sans', sans-serif;
  /* Spacing variables */
  --space-4: 1rem;
  /* etc... */
}

/* Dark mode support (if needed) */
@media (prefers-color-scheme: dark) {
  :root {
    --gray-900: #F7FAFC;
    --gray-100: #1A202C;
    /* Adjust other colors for dark mode */
  }
}
```

### Component Library Structure
```
src/
├── styles/
│   ├── tokens.css          /* Design tokens */
│   ├── components.css      /* Component styles */
│   ├── utilities.css       /* Utility classes */
│   └── themes.css          /* Theme variations */
├── components/
│   ├── Button/
│   ├── Widget/
│   ├── Card/
│   └── ...
```

---

**Action Required**: Please review the Walmart_PPT_Template_240225.pptx file and provide:
1. Exact hex color codes for Walmart blue, yellow, and other brand colors
2. Specific font family names and sizes used in the template
3. Any additional brand guidelines or measurements
4. Logo usage guidelines and asset locations

This will allow me to update this design system with the precise brand specifications.