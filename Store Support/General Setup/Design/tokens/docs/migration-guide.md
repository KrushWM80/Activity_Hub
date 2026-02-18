# Migration Guide: From @livingdesign/tokens-legacy to @livingdesign/tokens

This guide provides steps and recommendations for migrating from @livingdesign/tokens-legacy to @livingdesign/tokens.

## Table of Contents

1. [Overview](#overview)
2. [Migration Steps](#migration-steps)
   - [Replace "globals" with "primitive"](#replace-globals-with-primitive)
   - [Replace "size" with "scale" in primitives](#replace-size-with-scale-in-primitives)
   - [Add "core" Prefix to Primitives](#add-core-prefix-to-primitives)
   - [Adopt Semantic Tokens](#adopt-semantic-tokens)
   - [Deprecated Tokens](#deprecated-tokens)
3. [Additional Resources](#additional-resources)

## Overview

This guide helps you transition from the legacy tokens package to the new and improved token system. This involves several structural changes and additions to facilitate theming and component-level customizations.

## Migration Steps

### Replace "globals" with "primitive"

The term "globals" has been deprecated. Replace all instances of "globals" with "primitive" in your codebase.

Example SCSS "@import" replacement:

```diff
- @import "~@livingdesign/tokens-legacy/dist/scss/light/regular/globals"
+ @import "~@livingdesign/tokens/dist/scss/light/regular/primitive"
```

Example style object replacement:

```diff
- background-color: globals.$color-core-white
+ background-color: primitive.$color-white
```

### Replace "size" with "scale" in Primitives

The globals.size category has been renamed to scale in primitive.

Example:

```diff
- gap: globals.$size-space-200;
+ gap: primitive.$scale-space-200;
```

### Replace "primitive.color.cyan" with "primitive.color.teal"

In order to support the new Walmart brand, a new teal scale was added to the LD color palette. Walmart's resident color theorist determined that the names of the two palettes would be more accurate if they were swapped.

```diff
- color: primitive.$color-cyan-100;
+ color: primitive.$color-teal-100;
```

### Adopt Semantic Tokens

Semantic tokens provide a layer of abstraction for theming. To leverage this, migrate your tokens to the new semantic token system. This is a recommended step for better theme support.

Examples of semantic theming:

```diff
  .button {
-   background: primitive.$color-blue-100;
+   background: semantic.$color-fill-brand;

-   color: primitive.$color-white;
+   color: semantic.$color-text-on-fill-brand;

    &:focus {
-     background: primitive.$color-gray-160;
+     background: semantic.$color-fill-focused;
      text-decoration: none;
    }

    &:hover {
-     background: primitive.$color-gray-160;
+     background: semantic.$color-fill-hovered;
      text-decoration: none;
    }

    &:active {
-     background: primitive.$color-gray-180;
+     background: semantic.$color-fill-pressed;
      text-decoration: none;
    }
 . }
```

Examples of migration from globals:

```diff
- border-bottom: 1px solid globals.$color-core-transparent;
+ border-bottom: 1px solid semantic.$color-fill-transparent;

- box-shadow: globals.$elevation-200;
+ box-shadow: semantic.$elevation-200;
```

### Deprecated Tokens

The following tokens have been deprecated with the removal of "globals" tokens.

#### Font Tokens

The "globals.font" tokens scale has been updated in the new "primitive" namespace

```diff
- globals.$font-size-12: 0.75rem;
- globals.$font-size-14: 0.875rem;
- globals.$font-size-16: 1rem;
- globals.$font-size-18: 1.125rem;
- globals.$font-size-20: 1.25rem;
- globals.$font-size-24: 1.5rem;
- globals.$font-size-25: 0.75rem;
- globals.$font-size-28: 1.75rem;
- globals.$font-size-32: 2rem;
- globals.$font-size-36: 2.25rem;
- globals.$font-size-42: 2.625rem;
+ primitive.$font-size-25: 0.75rem;
+ primitive.$font-size-50: 0.875rem;
+ primitive.$font-size-100: 1rem;
+ primitive.$font-size-150: 1.125rem;
+ primitive.$font-size-200: 1.25rem;
+ primitive.$font-size-300: 1.5rem;
+ primitive.$font-size-400: 1.75rem;
+ primitive.$font-size-500: 2rem;
+ primitive.$font-size-600: 2.25rem;
+ primitive.$font-size-700: 2.625rem;
```

#### Elevation Tokens

Elevation tokens have been moved from "globals" to "semantic"

```diff
- globals.$elevation-100: 0 0.0625rem 0.125rem 0.0625rem rgba(0, 0, 0, 0.15), 0 -0.0625rem
-    0.125rem 0 rgba(0, 0, 0, 0.1);
- globals.$elevation-200: 0 0.1875rem 0.3125rem 0.125rem rgba(0, 0, 0, 0.15), 0 -0.0625rem
-    0.1875rem 0 rgba(0, 0, 0, 0.1);
- globals.$elevation-300: 0 0.3125rem 0.625rem 0.1875rem rgba(0, 0, 0, 0.15), 0 -0.0625rem
-    0.25rem 0 rgba(0, 0, 0, 0.1);
+ semantic.$elevation-100: 0 0.0625rem 0.125rem 0.0625rem #00000026, 0 -0.0625rem
+     0.125rem 0 #0000001a;
+ semantic.$elevation-200: 0 0.1875rem 0.3125rem 0.125rem #00000026, 0 -0.0625rem
+     0.1875rem 0 #0000001a;
+ semantic.$elevation-300: 0 0.3125rem 0.625rem 0.1875rem #00000026, 0 -0.0625rem
+     0.25rem 0 #0000001a;
```

#### Z-Index Tokens

These tokens have been completely removed. Define the z-index values in the style sheet directly instead.

```diff
- $z-index-100: 100;
- $z-index-200: 200;
- $z-index-300: 300;
- $z-index-400: 400;
- $z-index-500: 500;
- $z-index-600: 600;
```

### Additional Resources

- [List of design updates/API changes](https://confluence.walmart.com/pages/viewpage.action?pageId=1954365487#ExplorationTracker-Listofdesignupdates/APIchanges)
- [Migration mapping for color token from LD 3.0 to LD 3.5](https://confluence.walmart.com/pages/viewpage.action?spaceKey=COMM&title=Migration+mapping+for+color+token+from+LD+3.0+to+LD+3.5)
