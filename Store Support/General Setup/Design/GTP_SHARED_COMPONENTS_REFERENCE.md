# GTP Shared Components Library Reference

## 📦 Package Information

**Package**: `@walmart/gtp-shared-components`  
**Version**: 2.2.8  
**Type**: Living Design React Native Component Library  
**Documentation**: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/  
**Repository**: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components

## 🎯 Overview

The GTP Shared Components library is Walmart's official Living Design system for React Native applications. It provides 87+ production-ready components with consistent styling, accessibility features, and mobile-optimized interactions.

### Key Features
- ✅ **87+ Modern Components** - Comprehensive component library covering all UI needs
- ✅ **Living Design System** - Aligned with Walmart's design standards
- ✅ **React Native Native** - Optimized for mobile performance
- ✅ **TypeScript Support** - Full type definitions and IntelliSense
- ✅ **Accessibility Built-in** - WCAG compliant components
- ✅ **Bogle Font Integration** - Official Walmart typography
- ✅ **Icon System** - Integrated @walmart/gtp-shared-icons package
- ✅ **Legacy Support** - Backward compatibility with v1.8 components

## 🚀 Installation & Setup

### Installing the Package
```bash
npm install @walmart/gtp-shared-components
# or
yarn add @walmart/gtp-shared-components
```

### Installing Fonts
```bash
npm run installFonts
# or
yarn installFonts
```

### Basic Import
```tsx
import { Button, TextField, Card, Modal } from '@walmart/gtp-shared-components';
```

## 📚 Component Categories

### 🔘 Buttons & Actions
Components for user interactions and action triggers.

#### **Button**
Primary action button with multiple variants and states.
- **Variants**: Primary, Secondary, Tertiary, Destructive
- **States**: Default, Hover, Pressed, Disabled, Loading
- **Features**: Icon support, full-width option, custom styling

#### **ButtonGroup**
Container for grouping related buttons together.
- **Layouts**: Horizontal, Vertical
- **Spacing**: Auto-managed button spacing
- **Alignment**: Left, Center, Right, Justified

#### **IconButton**
Compact button displaying only an icon.
- **Use Cases**: Toolbars, headers, minimal interfaces
- **Sizes**: Small, Medium, Large
- **Variants**: All button variants supported

#### **Link**
Text-based navigation and action element.
- **Styles**: Underlined, Plain
- **States**: Default, Hover, Visited, Focus
- **Features**: External link indicators, download support

---

### 📝 Form Elements
Input components for data collection and user interaction.

#### **TextField**
Single-line text input with validation and helper text.
- **Types**: Text, Email, Password, Number, Tel, URL
- **Features**: Label, placeholder, helper text, error messages
- **Validation**: Real-time validation, required fields
- **States**: Default, Focus, Error, Disabled, Read-only

#### **TextArea**
Multi-line text input for longer content.
- **Features**: Auto-resize, character count, max length
- **Rows**: Configurable minimum and maximum rows
- **Validation**: Same as TextField

#### **Checkbox**
Binary selection control with label.
- **States**: Unchecked, Checked, Indeterminate, Disabled
- **Variants**: Default, Error
- **Group Support**: FormGroup integration

#### **Radio**
Single selection from multiple options.
- **States**: Unselected, Selected, Disabled
- **Validation**: Required field support
- **Group Support**: RadioGroup component

#### **Switch**
Toggle control for on/off states.
- **States**: Off, On, Disabled
- **Variants**: Default, Error
- **Features**: Async state changes, custom labels

#### **Select**
Dropdown selection component.
- **Features**: Single/multi-select, search, groups
- **Options**: Disabled options, custom rendering
- **States**: Default, Open, Error, Disabled

#### **DateDropdown**
Date picker with dropdown interface.
- **Features**: Month, day, year selectors
- **Validation**: Date range validation
- **Formats**: Configurable date formats

#### **Rating**
Star rating input component.
- **Features**: Half-star support, read-only mode
- **Sizes**: Small, Medium, Large
- **Max Rating**: Configurable (default 5)

#### **Segment / Segmented**
Segmented control for mutually exclusive options.
- **Use Cases**: View switchers, tab alternatives
- **Variants**: Compact, Default, Full-width
- **Icons**: Optional icon support

#### **FormGroup**
Container for grouping form elements with shared validation.
- **Features**: Group validation, error handling
- **Layout**: Vertical, Horizontal
- **Accessibility**: Fieldset and legend support

---

### 📊 Data Display
Components for presenting information and data.

#### **DataTable**
Comprehensive table component with 13+ subcomponents.
- **Subcomponents**: Body, Cell, ColumnHeader, Head, HeaderCell, Row, etc.
- **Features**: Sorting, filtering, pagination, row selection
- **Responsive**: Mobile-optimized layouts
- **Virtualization**: Large dataset support

#### **Card**
Container component for grouping related content.
- **Subcomponents**: CardActions, CardContent, CardHeader, CardMedia
- **Variants**: Default, Outlined, Elevated
- **Features**: Action buttons, expandable content

#### **List / ListItem**
Vertical list of items with flexible content.
- **Features**: Icons, avatars, actions, dividers
- **Types**: Simple, Interactive, Nested
- **States**: Default, Selected, Disabled

#### **Metric / MetricGroup**
Display of key performance indicators and metrics.
- **Features**: Trend indicators, change percentages
- **Formats**: Number, currency, percentage
- **Grouping**: Related metrics container

#### **Tag**
Label for categorization and status indication.
- **Variants**: Default, Success, Warning, Error, Info
- **Features**: Removable, clickable, icon support
- **Sizes**: Small, Medium, Large

#### **Chip / ChipGroup**
Compact element for attributes, filters, or selections.
- **Variants**: Filter, Choice, Action
- **States**: Default, Selected, Disabled
- **Features**: Removable, icon support, avatar integration

#### **Divider**
Visual separator between content sections.
- **Orientations**: Horizontal, Vertical
- **Variants**: Full-width, Inset, Middle
- **Text**: Optional text labels

---

### 💬 Feedback & Messaging
Components for user feedback and status communication.

#### **Alert**
Prominent message for important information.
- **Variants**: Success, Warning, Error, Info
- **Features**: Dismissible, icons, actions
- **Layouts**: Banner, Inline

#### **Banner**
Full-width alert for global messages.
- **Types**: Informational, Warning, Error, Success
- **Features**: Dismissible, action buttons, images
- **Position**: Top, Bottom, Inline

#### **Snackbar**
Temporary message at bottom of screen.
- **Duration**: Auto-dismiss after 3-7 seconds
- **Features**: Action button, dismiss button
- **Queue**: Message queuing system

#### **Modal**
Dialog overlay for focused tasks and content.
- **Sizes**: Small, Medium, Large, Full-screen
- **Features**: Header, body, footer, close button
- **Variants**: Default, Alert, Confirmation
- **Accessibility**: Focus trap, keyboard navigation

#### **Popover**
Contextual overlay anchored to element.
- **Placements**: Top, Bottom, Left, Right, Auto
- **Triggers**: Click, Hover, Focus
- **Features**: Arrow indicator, auto-positioning

#### **ErrorMessage**
Inline error message for form validation.
- **Features**: Icon, assistive text
- **Integration**: TextField, Select, FormGroup
- **Animation**: Smooth appearance

#### **Nudge**
Subtle prompt or tooltip for guidance.
- **Types**: Tooltip, Hint, Tutorial
- **Triggers**: Hover, Focus, Manual
- **Positioning**: Smart auto-positioning

---

### 🔄 Progress & Loading
Components indicating loading states and progress.

#### **Spinner**
Circular loading indicator.
- **Sizes**: Small, Medium, Large
- **Variants**: Primary, Secondary, White
- **Features**: Centered, inline, overlay modes

#### **SpinnerOverlay**
Full-screen loading overlay with spinner.
- **Features**: Background dimming, message support
- **Variants**: Modal, Full-screen
- **Accessibility**: Screen reader announcements

#### **ProgressIndicator**
Linear progress bar.
- **Modes**: Determinate, Indeterminate
- **Features**: Percentage display, labels
- **Variants**: Default, Success, Warning, Error

#### **CircularProgressIndicator**
Circular progress indicator with percentage.
- **Sizes**: Small, Medium, Large
- **Features**: Center content, color customization
- **Animation**: Smooth transitions

#### **ProgressTracker**
Multi-step progress indicator.
- **Features**: Step labels, descriptions, status icons
- **Variants**: Horizontal, Vertical
- **States**: Completed, Current, Upcoming, Error

#### **Skeleton / SkeletonText**
Placeholder loading state for content.
- **Shapes**: Text, Circle, Rectangle, Custom
- **Animation**: Pulse, Wave
- **Use Cases**: Cards, lists, profiles

---

### 🧭 Navigation
Components for app navigation and routing.

#### **TabNavigation**
Tab-based navigation component.
- **Variants**: Primary, Secondary, Scrollable
- **Features**: Active indicators, icons, badges
- **Accessibility**: Keyboard navigation, ARIA support

#### **BottomSheet**
Mobile bottom sheet for actions and content.
- **Heights**: Auto, Half-screen, Full-screen
- **Features**: Drag handle, backdrop dismiss
- **Use Cases**: Mobile menus, filters, forms

#### **Menu / MenuItem**
Dropdown menu for actions and options.
- **Features**: Icons, keyboard shortcuts, dividers
- **Variants**: Context menu, Dropdown
- **Nesting**: Submenu support

#### **SeeDetails**
Expandable link for additional information.
- **Features**: Expand/collapse, arrow indicator
- **Use Cases**: Show more content, read more
- **Animation**: Smooth transitions

---

### 📐 Layout & Structure
Components for page structure and content organization.

#### **Collapse**
Expandable/collapsible content section.
- **Features**: Header, expand/collapse animation
- **States**: Expanded, Collapsed
- **Accordion**: Multiple collapse coordination

#### **BottomSheet** (Layout variant)
Sheet sliding from bottom of screen.
- **Use Cases**: Mobile actions, filters, sheets
- **Features**: Drag to dismiss, snap points
- **Accessibility**: Focus management

---

### 🎨 Typography
Text components with Living Design styling.

#### **Heading**
Heading text with semantic levels (h1-h6).
- **Levels**: 1-6 (Display to Subheading)
- **Weights**: Light, Regular, Bold
- **Colors**: Theme-aware

#### **Body**
Body text with paragraph styling.
- **Sizes**: Small, Medium, Large
- **Weights**: Regular, Medium, Bold
- **Line Heights**: Optimized for readability

#### **Caption**
Small supplementary text.
- **Use Cases**: Helper text, timestamps, metadata
- **Colors**: Muted, secondary
- **Sizes**: Extra-small, Small

#### **Display**
Large display text for hero sections.
- **Use Cases**: Page titles, hero text, emphasis
- **Sizes**: 1-4 (Largest to smallest)
- **Weights**: Bold, Extra-bold

---

### 🎭 Theme & Styling
Theming and styling utilities.

#### **Variants**
Component variant system for consistent theming.
- **Features**: Theme switching, dark mode
- **Variants**: Default, Dark, High-contrast
- **Customization**: Brand color overrides

#### **SpotIcon**
Decorative icon component.
- **Use Cases**: Empty states, feature highlights
- **Sizes**: Small, Medium, Large, Extra-large
- **Colors**: Theme colors, custom

---

### 🏷️ Indicators & Badges
Small visual indicators for status and counts.

#### **Badge**
Numeric or dot indicator for notifications.
- **Variants**: Dot, Number
- **Max Count**: "99+" for large numbers
- **Colors**: Primary, Error, Success, Warning
- **Position**: Top-right, Top-left, Bottom-right, Bottom-left

#### **Callout**
Highlighted message box for emphasis.
- **Variants**: Info, Success, Warning, Error
- **Features**: Icon, dismissible, actions
- **Use Cases**: Announcements, tips, alerts

#### **Flag**
Status flag for items and content.
- **Colors**: Brand colors, semantic colors
- **Use Cases**: New, Sale, Featured labels
- **Position**: Corner ribbons, inline labels

---

### 🧪 Specialized Components

#### **WizardFooter**
Footer navigation for multi-step wizards.
- **Features**: Previous, Next, Cancel, Submit buttons
- **Validation**: Step validation before proceeding
- **Progress**: Integration with ProgressTracker

---

## 🔤 Icon Integration

### @walmart/gtp-shared-icons
The component library integrates seamlessly with Walmart's icon system.

```tsx
import { Icon } from '@walmart/gtp-shared-components';
import { IconChevronRight, IconClose } from '@walmart/gtp-shared-icons';

// Icon usage in components
<Button icon={<IconChevronRight />}>Next</Button>
<IconButton icon={<IconClose />} onPress={handleClose} />
```

---

## 🎨 Bogle Fonts

### Official Walmart Typography
The library includes the Bogle font family, Walmart's official corporate typeface.

**Installation**:
```bash
npm run installFonts
```

**Font Weights**:
- Bogle Light (300)
- Bogle Regular (400)
- Bogle Medium (500)
- Bogle Bold (700)

---

## ♻️ Legacy Component Support

### Deprecated Components (v1.8 Compatibility)
The library maintains backward compatibility with older components for gradual migration.

**Legacy Components Include**:
- ActivityIndicator → Use `Spinner`
- Picker → Use `Select`
- TextInput → Use `TextField`
- TouchableHighlight → Use `Button` or `Link`

**Migration Guide**: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/migration

---

## 📖 Usage Examples

### Form Example
```tsx
import {
  FormGroup,
  TextField,
  Select,
  Checkbox,
  Button,
  ErrorMessage
} from '@walmart/gtp-shared-components';

function MyForm() {
  return (
    <FormGroup>
      <TextField
        label="Full Name"
        placeholder="Enter your name"
        required
      />
      <Select
        label="Department"
        options={departments}
        required
      />
      <Checkbox label="I agree to the terms" />
      <Button variant="primary">Submit</Button>
    </FormGroup>
  );
}
```

### Card with DataTable Example
```tsx
import {
  Card,
  CardHeader,
  CardContent,
  DataTable,
  DataTableHead,
  DataTableBody,
  DataTableRow,
  DataTableCell
} from '@walmart/gtp-shared-components';

function DataCard() {
  return (
    <Card>
      <CardHeader title="User Activity" />
      <CardContent>
        <DataTable>
          <DataTableHead>
            <DataTableRow>
              <DataTableCell>Name</DataTableCell>
              <DataTableCell>Status</DataTableCell>
            </DataTableRow>
          </DataTableHead>
          <DataTableBody>
            {data.map(row => (
              <DataTableRow key={row.id}>
                <DataTableCell>{row.name}</DataTableCell>
                <DataTableCell>{row.status}</DataTableCell>
              </DataTableRow>
            ))}
          </DataTableBody>
        </DataTable>
      </CardContent>
    </Card>
  );
}
```

### Modal with Form Example
```tsx
import {
  Modal,
  TextField,
  Button,
  Snackbar
} from '@walmart/gtp-shared-components';

function EditModal({ visible, onClose }) {
  const [showSuccess, setShowSuccess] = useState(false);

  return (
    <>
      <Modal visible={visible} onClose={onClose}>
        <Modal.Header title="Edit Profile" />
        <Modal.Body>
          <TextField label="Email" type="email" />
          <TextField label="Phone" type="tel" />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onPress={onClose}>
            Cancel
          </Button>
          <Button variant="primary" onPress={handleSave}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
      
      <Snackbar
        visible={showSuccess}
        message="Profile updated successfully"
        onDismiss={() => setShowSuccess(false)}
      />
    </>
  );
}
```

---

## 🔗 Resources

### Documentation
- **Main Docs**: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/
- **Component Demos**: See example/ folder in repository
- **Storybook**: Interactive component playground

### Support
- **GitHub Issues**: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/issues
- **Slack Channel**: #gtp-shared-components
- **Team**: Electrode Mobile Platform team

### Version History
- **v2.2.8** (Current) - Latest stable release with 87+ components
- **v2.x** - Living Design system implementation
- **v1.8** - Legacy version (deprecated, maintained for compatibility)

---

## ✅ Component Checklist

Use this checklist when building new features to ensure you're using the right components:

### Forms & Input
- [ ] TextField - Single-line text input
- [ ] TextArea - Multi-line text input
- [ ] Select - Dropdown selection
- [ ] Checkbox - Multiple selections
- [ ] Radio - Single selection
- [ ] Switch - Toggle on/off
- [ ] DateDropdown - Date selection
- [ ] Rating - Star ratings
- [ ] Segmented - Segment control

### Actions
- [ ] Button - Primary actions
- [ ] IconButton - Icon-only actions
- [ ] ButtonGroup - Related actions
- [ ] Link - Navigation

### Data Display
- [ ] DataTable - Tabular data
- [ ] Card - Content grouping
- [ ] List/ListItem - Vertical lists
- [ ] Metric - KPIs and numbers
- [ ] Tag - Labels and categories
- [ ] Chip - Compact selections

### Feedback
- [ ] Alert - Important messages
- [ ] Banner - Global announcements
- [ ] Snackbar - Temporary messages
- [ ] Modal - Focused dialogs
- [ ] Popover - Contextual overlays
- [ ] ErrorMessage - Validation errors

### Progress
- [ ] Spinner - Loading indicator
- [ ] ProgressIndicator - Linear progress
- [ ] ProgressTracker - Multi-step progress
- [ ] Skeleton - Content placeholder

### Navigation
- [ ] TabNavigation - Tab switching
- [ ] Menu/MenuItem - Action menus
- [ ] BottomSheet - Mobile sheets

### Typography
- [ ] Heading - Page headings
- [ ] Body - Paragraph text
- [ ] Caption - Small text
- [ ] Display - Hero text

---

**Last Updated**: November 20, 2025  
**Library Version**: 2.2.8  
**Documented Components**: 87+
