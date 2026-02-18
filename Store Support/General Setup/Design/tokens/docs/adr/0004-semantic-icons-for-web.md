# Semantic icons for web

- Status: accepted
- Deciders: [Isaac Baron, Amalio Velasquez, Manasa Bhat, Mauricio Cubillos, Yashwin Agrawal]
- Date: 2025-01-30

Technical Story: https://jira.walmart.com/browse/LD-6459

## Context and Problem Statement

The LD 3.5 theming API includes semantic icon tokens to allow for usage of different icons for branded experiences based on the same UI code. There are several ways to implement an icon system for web, each with their own strategies for usage and overrides. This document explores which of these solutions should be distributed by LD. (Note: It's possible that the ideal outcome includes multiple distributions of semantic icons in different formats.)

## Decision Drivers

- Compatibility with web theming API (CSS custom properties)
- Compatibility with distributed library (@livingdesign/react)
- Compatibility with walmart-web/walmart icon strategy (icon font)
- Ease of use for all consumers (walmart-web/walmart and others)
- Performance
- Implementation/maintenance LOE

## Considered Options

### 0. Do nothing

Don't provide semantic icon tokens

- Good, because no change
- Bad, because it doesn't meet international theming requirements, e.g., currency symbol needs to change across markets
- Bad, because it doesn't meet brand theming requirements, e.g., Sam's Club has different icons to represent semantic meaning in LD/WCP components

### 1. Semantic icons as React components

Distribute JS tokens for semantic icons. Each token would be assigned a React icon component, similar to those used in @livingdesign/react implementation. Theme overrides would be handled by module aliasing at build time.

- Good, because individual icons are bundled in @livingdesign/react distribution
  - Good, because it does not require the loading of an entire icon font to use @livingdesign/react
- Good, because it is low effort (aligns with existing implementation)
- Bad, because it requires semantic icon overrides to be defined as React components
  - walmart-web/walmart uses icon font
- Bad, because it doesn't align to the web theming API based on CSS custom properties

NOTE: There are variations on this solution such as assigning an <svg> or <path> to semantic tokens rather than React icon components. These approaches have roughly the same pros and cons, but would require higher LOE to implement in the LD component library.

### 2. Semantic icons as SVG sprites

Distribute SVG sprites with semantic icons. Theme overrides require replacing groups in the SVG definition.

- Bad, because SVG definition needs to be bundled with @livingdesign/react distribution
- Bad, because new solution requires migration effort

### 3. Semantic icons as icon font

Add semantic icon classes to icon font.

- Good, because aligns with walmart-web/walmart icon system
- Good, because overrides can be handled with CSS custom properties
- Mixed
  - Good, because CSS addition is minimal
  - Bad, because adds potentially unused CSS to the icon font
- Bad, because using any LD component requires loading the entire icon font
- Bad, because requires editing auto-generated icon font files

### 4. Semantic icons as CSS custom properties

Create CSS custom properties with direct reference to SVGs in data URIs.

- Good, because theming overrides are handled by custom properties
- Bad, because CSS becomes very bloated
- Bad, because new solution requires implementation and migration effort

## Decision Outcome

Chosen option: 1

With React components, icons are included in the JS bundle, so only required assets are included and there is no additional CSS. This is the solution currently in place in the LD component library, so this is the most straight-forward path to delivering a theming.

Option 3 has promising upsides, but drawbacks for usage in a distributed library. Recommend following up on this approach for WCP theming.

## References

- Semantic icons in Airtable: https://airtable.com/appYyNWTLAzg3x1t3/tblS9MOzERfdLZsrZ/viwWU3JZh0CVzh91Q?blocks=hide
- Icon system as SVG sprites: https://css-tricks.com/svg-sprites-use-better-icon-fonts/
- Icon system as plain SVGs: https://css-tricks.com/pretty-good-svg-icon-system/
- Icon system as CSS custom properties: https://css-tricks.com/how-i-made-an-icon-system-out-of-css-custom-properties/
