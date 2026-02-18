# Token Guidelines

## Introduction

Tokens are the indivisible pieces of specification known as "core styles". These tiny pieces of UI information are centralized and used across several platforms when creating digital products.

The Living Design Token system contains three types of tokens, **primitve tokens**, **semantic tokens**, and **component tokens**. Primitive tokens are the backbone of our design system and are the basis of all semantic and component tokens. Semantic tokens give context to primitive tokens and add themeability to the design system. Component tokens provide the implementation specifications.

## Taxonomy

### Breakpoint

- **bS**: The small breakpoint.
- **bM**: The medium breakpoint.
- **bL**: The large breakpoint.
- **bXL**: The extra large breakpoint.
- **bXXL**: The extra extra large breakpoint.

Use breakpoints to change a value up the breakpoint scale (from `bS` to `bXXL`). The `bS` breakpoint should always be used for the initial value, proceeded by breakpoints where the value must change. For example:

```tsx
{
  gap: {
    bS: {
      value: "{scale.space.200}",
    },

    bXL: {
      value: "{scale.space.300}",
    },
  }
}
```

### Category

- **Color**: Primitive palettes, semantic colors and gradients
- **Component**: Component specifications
- **Duration**: Duration
- **Elevation**: Depth
- **Font**: Typography
- **Icon**: Icons
- **Scale**: Space, breakpoints, border radii, and border width
- **Timing**: Timing

### Interaction

- **enabled**: The enabled interactive state of a component. (This is always `_` in code.)
- **hovered**: The hovered interactive state of a component.
- **focused**: The focused interactive state of a component.
- **pressed**: The pressed interactive state of a component.
- **disabled**: The disabled state of a component.

### Modifier

- **alignment**: The alignment of a component. Either `left` or `right`.
- **color**: The color variations of a component.
- **middle**: The middle position in a gradient.
- **position**: The position variations of a component.
- **sort**: The sort order of a component. Either `ascending` or `descending`.
- **size**: The size variations of a component.
- **start**: The first position in a gradient.
- **stop**: The last position in a gradient.
- **variant**: The style variations of a component.

### Slot

- **actionContent**: The designated area for interactive actions within the component.
- **leading**: The designated content area at the start of the component.
- **leadingIcon**: The designated icon area at the start of the component.
- **trailing**: The designated content area at the end of the component.
- **trailingIcon**: The designated icon area at the end of the component.

### State

- **activated**: The catch-all state for "on": checked, current, selected.
- **enter**: The `enter` state of a transition.
- **enterActive**: The `enterActive` state of a transition.
- **error**: If the component is in a user-supplied error state.
- **exit**: The `exit` state of a transition.
- **exitActive**: The `exitActive` state of a transition
- **hasLeadingIcon**: If the component's optional leading icon slot is set.
- **hasTrailing**: If the component's optional trailing slot is set.
- **isFirst**: If the component is first of a group of related components. (e.g. Progress Tracker Item)
- **isLast**: If the component is the last of a group of related components. (e.g. Progress Tracker Item)
- **isMagic**: If the component is controlled by an AI agent.
- **isMonospace**: If the text component should use the monospace font family.
- **isSortable**: If the component's related content is sortable. (e.g. Data Table Header.)
- **readOnly**: If the form field component can only be read, not edited.

## Structure

### Primitive tokens

`primitive` - `<category>` - `<type>` - `[<modifier>]`

**Example(s):**

```sh
primitive.color.gray.100
primitive.duration.100
primitive.font.family.mono
primitive.scale.space.100
```

### Semantic tokens

`semantic` - `<category>` - `[<family>]` - `<type>` - `[<modifier>]` - `[<state>]` - `[<interaction>]`

```sh
semantic.color.fill.subtle.pressed
```

- **category**: color
- **type**: fill
- **modifier**: subtle
- **interaction**: pressed

```sh
semantic.scale.border.width.interactive.activated.hovered
```

- **category**: scale.border.width
- **type**: interactive
- **state**: activated
- **interaction**: hovered

```sh
semantic.color.action.text.onFill.secondary.disabled
```

- **category**: color
- **family**: action
- **type**: text.onFill
- **modifier**: secondary
- **interaction**: disabled

#### Icon tokens

`semantic` - `icon` - `<type>`

```sh
semantic.icon.success
```

- **type**: success

### Component tokens

`component` - `<type>` - `[<element>]` - `[<modifier>]` - `[<state>]` - `[<slot>]` - `<property>` - `[<media-query>]` - `[<interaction>]`

**Example(s):**

```sh
component.button.container.variant.primary.backgroundColor.hovered
```

- **category**: component
- **type**: button
- **element**: container
- **modifier**: `variant.primary`
- **property**: backgroundColor
- **interaction**: hovered

```sh
component.text.heading.size.small.fontSize.bS
```

- **category**: component
- **type**: `text.heading`
- **modifier**: `size.small`
- **property**: `fontSize`
- **media-query**: bS

```sh
component.textField._value.size.large.lineHeight
```

- **category**: component
- **type**: textField
- **element**: \_value
  - Note: `value` is a special property for style-dictionary. Prefix anatomy elements named "value" with `_` so tokens are built correctly (see related [thread](https://gecgithub01.walmart.com/LivingDesign/tokens/pull/253#discussion_r3833366)).
- **modifier**: `size.large`
- **property**: lineHeight

## Properties

### Primitive properties

- **color**: Color definitions
- **duration**: Duration definitions
- **elevation**: Depth definitions
- **font.family**: Font family definitions
- **font.size**: Font size definitions
- **font.weight**: Font weight definitions
- **scale.border.radius**: Border radius definitions
- **scale.border.width**: Border width definitions
- **scale.breakpoint**: Breakpoint definitions
- **scale.icon**: Icon definitions
- **scale.space**: Spacing definitions
- **timing.easeIn**: Ease in timing function definitions
- **timing.easeInOut**: Ease in/out timing function definitions
- **timing.easeOut**: Ease out timing function definitions
- **timing.linear**: Linear timing function definitions

### Alignment

- **alignHorizontal** `"start" | "center" | "end" | "space-between"`: Horizontal alignment for a nested element
- **alignVertical** `"start" | "center" | "end" | "baseline"`: Vertical alignment for a nested element

### Alias

- **aliasName**: A reference to another component
- **aliasOptions**: Configuration for the referenced component

### Animation

- **animation**: Animation for an element

```tsx
{
  delay: Duration;
  direction: "normal" | "reverse" | "alternate" | "alternate-reverse";
  duration: Duration;
  iterationCount: number | "infinite";
  keyframes: Keyframes;
  timing: Timing;
}
```

#### Keyframes

```text
<keyframe-selector>: {
  <declaration-list>
};
```

### Background

- **backgroundColor** `Color`: Color for an element's background

### Border

- **borderColor** `Color`: Color for an element's border
- **borderColorBottom** `Color`: Color for an element's bottom border
- **borderColorEnd** `Color`: Color for an element's end border
- **borderColorStart** `Color`: Color for an element's start border
- **borderColorTop** `Color`: Color for an element's top border
- **borderRadius** `Scale.Border.Radius`: Radius for an element's border
- **borderRadiusBottomEnd** `Scale.Border.Radius`: Radius for an element's bottom end border
- **borderRadiusBottomStart** `Scale.Border.Radius`: Radius for an element's bottom start border
- **borderRadiusTopEnd** `Scale.Border.Radius`: Radius for an element's top end border
- **borderRadiusTopStart** `Scale.Border.Radius`: Radius for an element's top start border
- **borderWidth** `Scale.Border.Width`: Width for an element's border
- **borderWidthBottom** `Scale.Border.Width`: Width for an element's bottom border
- **borderWidthEnd** `Scale.Border.Width`: Width for an element's end border
- **borderWidthStart** `Scale.Border.Width`: Width for an element's start border
- **borderWidthTop** `Scale.Border.Width`: Width for an element's top border

### Duration

- **duration** `Duration`: Duration (in seconds) specified for an element's animation.

### Direction

- **direction** `column` | `column-reverse` | `row` | `row-reverse`: Define the direction and axis for how items are placed

### Elevation

- **elevation**: Shadow effects around an element's frame

```js
{
  blur: Scale.Space;
  color: Color;
  offsetX: Scale.Space;
  offsetY: Scale.Space;
  spread: Scale.Space;
}
```

### Font

<!-- TODO: update w/ latest once font variables ship. -->

- **family** `Font.Family`: Font family for an element
- **lineHeight** `Font.LineHeight`: Line-height for an element
- **size** `Font.Size`: Font size for an element
- **weight** `Font.Weight`: Font weight for an element

### Gap

- **gap** `Scale.Space`: Horizontal and vertical space between two elements
- **gapHorizontal** `Scale.Space`: Horizontal space between two elements
- **gapVertical** `Scale.Space`: Vertical space between two elements

### Layout Weight

- **growFactor** `number`: Weight of an element's growth in relation to its siblings when additional container-space is available
- **shrinkFactor** `number`: Weight of how much an element will shrink in relation to its siblings when container-space is limited

### Icon

- **iconColor**: `Color`: Color for an icon
- **iconName**: `string`: Name for an icon
- **iconSize**: `"small" | "medium" | "large"`: Size for an icon (matches property in `Scale.Icon`)

### Line Height

<!-- TODO: update w/ latest once font variables ship. -->

- **lineHeight** `Scale.Space`: Distance between lines of text for an element

### Margin

- **margin** `Scale.Space`: Space surrounding an element
- **marginBottom** `Scale.Space`: Space surrounding an element's bottom side
- **marginEnd** `Scale.Space`: Space surrounding an element's end side
- **marginHorizontal** `Scale.Space`: Space surrounding an element's start and end sides
- **marginStart** `Scale.Space`: Space surrounding an element's start side
- **marginTop** `Scale.Space`: Space surrounding an element's top side
- **marginVertical** `Scale.Space`: Space surrounding an element's top and bottom sides

### Offset

- **offsetBottom** `Scale.Space`: Sets the vertical position of a positioned element relative to the bottom of its containing block
- **offsetEnd** `Scale.Space`: Sets the vertical position of a positioned element relative to the end of its containing block
- **offsetStart** `Scale.Space`: Sets the vertical position of a positioned element relative to the start of its containing block
- **offsetTop** `Scale.Space`: Sets the vertical position of a positioned element relative to the top of its containing block

### Opacity

- **opacity**: `number`: Opacity level for an element

### Order

- **order**: `number`: Sets an item's position in an order

### Padding

- **padding** `Scale.Space`: Space between an element's edge and its contents
- **paddingBottom** `Scale.Space`: Space between an element's bottom edge and its contents
- **paddingEnd** `Scale.Space`: Space between an element's end edge and its contents
- **paddingHorizontal** `Scale.Space`: Space between an element's start and end edges and its contents
- **paddingStart** `Scale.Space`: Space between an element's start edge and its contents
- **paddingTop** `Scale.Space`: Space between an element's top edge and its contents
- **paddingVertical** `Scale.Space`: Space between an element's top and bottom edges and its contents

### Scale

<!-- TODO: web specifies `min`, `height`, and `width` as "auto", but `max` has "none". How to handle? -->

- **height** `Scale.Space | "<number>px" | "X%" | "auto"`: Height for an element
- **maxHeight** `Scale.Space | "<number>px" | "X%" | "auto"`: Maximum height for an element
- **maxWidth** `Scale.Space | "<number>px" | "X%" | "auto"`: Maximum width for an element
- **minHeight** `Scale.Space | "<number>px" | "X%" | "auto"`: Minimum height for an element
- **minWidth** `Scale.Space | "<number>px" | "X%" | "auto"`: Minimum width for an element
- **radius** `Scale.Space | "<number>px"`: Radius for a circular element
- **width** `Scale.Space | "<number>px" | "fill-screen" | "fill-parent" | "hug-contents" | "auto"`: Width for an element

### Text

- **textAlign** `"left" | "center" | "right"`: Horizontal alignment for an element's text
- **textColor** `Color`: Color for an element's text
- **textDecoration** `"underline" | none`: Decorative lines for an element's text
- **textWrap** `boolean`: Whether the element's text should wrap to additional lines

### Transform

- **rotation** ???: ??? (TBD)
- **translateX** ???: ??? (TBD)
- **translateY** ???: ??? (TBD)

### Transition

- **transitionDelay**: `Duration` Transition Delay(in seconds) to start a transition effect for an element
- **transitionDuration**: `Duration` Transition Duration(in seconds) specified for an element's animation
- **transitionProperty**: `string` Name of the CSS property the transition effect is for
- **transitionTimingFunction**: `Timing` Speed curve of the transition effect for an element's animation

### Wrap

- **wrap** `wrap`: Wrapping for an element

## Deprecation

The tokens in this repo are published as a package for consumption by several repositories across multiple platforms. In light of this, removing tokens is a breaking change, and it is often preferable to deprecate those tokens instead.

In order to deprecate a token, add a `deprecated.comment` attribute to the token definition. See Living Design's [Token Deprecation Strategy](https://confluence.walmart.com/pages/viewpage.action?spaceKey=LD&title=Token+Deprecation+Strategy) for more detail.

e.g.

```js
module.exports = {
  component: {
    someComponent: {
      container: {
        backgroundColor: {
          value: "{color.fill.brand}",
          deprecated: {
            comment:
              "someComponent.container.backgroundColor is deprecated. See: <JIRA Ticket Reference>.",
          },
        },
      },
    },
  },
};
```

## Formatting

### Definition

- Token definitions should **not** be abbreviated
- Token definitions should **not** include `padding` to determine `line-height`, `height`, or `width`
- Token definitions should **not** include platform specific implementation details (e.g. flexbox)
- Token definitions should **not** include platform specific implementation resets (e.g. `border: 0`)
- Token definitions should **not** include platform specific quirks (e.g. negative margin, off by 1px calculations)
- Token definitions should be camel case
- Token definitions should be alpha-sorted
- Token definitions should be product unaware
- Token definitions should be singular
- Token definitions should consider existing tokens
- Token definitions should be limited to `primitive`, `semantic` or `component` taxonomy
- Token definitions should match component anatomy
- Token definitions should match component features
- Token definitions should match component names for their `type`
- Token definitions should match design specifications explicitly

#### Definition: Interaction

```js
component.link.textColor.hovered;
component.link.textDecoration.pressed;
```

#### Definition: Modifier

```js
component.button.variant.primary.backgroundColor;
component.styledText.color.blue.textColor;
component.panel.container.position.right.alignHorizontal;
```

#### Definition: State

```js
component.breadcrumb.item.state.isCurrent.textColor;
component.switch.track.state.activated.backgroundColor.hovered;
component.textField.state.error.border;
```

### Files

- Token files should be prefixed with component name
- Token files should be separate per element of anatomy
- Token files should be written in `ts`
- Token folders should be pascal case
- Token folders should be separate per component
- Token folders should have their own category
  - `properties/primitive/` for globals
  - `properties/semantic/` for globals
  - `properties/components/` for components

**Example:**

```sh
properties/
  components/
    Banner/
      BannerCloseButton.ts
      BannerContainer.ts
      BannerTextLabel.ts
```

### Testing

- Token tests should be human readable
- Token tests should have at least one `describe` block
- Token tests should use snapshots
- Token transforms should be tested
- Tokens should be tested

## References

- <https://uxdesign.cc/design-tokens-for-dummies-8acebf010d71>
- <https://medium.com/eightshapes-llc/tokens-in-design-systems-25dd82d58421>
- <https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676>
