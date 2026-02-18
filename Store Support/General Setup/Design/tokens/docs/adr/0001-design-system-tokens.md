# Design System Tokens

* Status: accepted
* Deciders: [Cory Reed](https://gecgithub01.walmart.com/c0r00jl), [Carey Hinoki](https://gecgithub01.walmart.com/c0h04ba), [Mike Ellis](m0e01rf), [Gregory Smith](https://gecgithub01.walmart.com/g0s017g)
* Date: 2021-06-04

## Context and Problem Statement

Living Design provides a library of visual styles and components to Walmart. The team provides artifacts for design, Android, iOS, and web. However, there isn't a single source of truth for these deliverables and the system has become inconsistent over time. This inconsistency has lead to X hours of throw away work and confusion among both consumers and contributors of the system. It has also created a divergent experiences for our end customers and our brand.

The design systems team has observed the following problems within the Customer Experience platforms:

* Platforms are not in sync:
  * Android and iOS components are ~10 months out of date with design and web components
  * Platforms have different names for visual styles, components, and component features
* Teams are unable to determine or locate the latest design specifications. There isn't a source of truth.
* Creating an implementation on new platforms--like Jetpack compose, Flutter, or Vue--requires significant effort. Developer must look at Zeplin specifications, ask designers questions on functionality, and generally remake UI.
* Specifications aren't always clear and may contain visual bugs (improper spacing, colors) that increase implementation and maintenance costs.
* It takes approximately six months to roll out visual changes to all Customer Experience platforms.

## Decision Drivers

The Living Design team's objectives and key results are the primary drivers:

> * Standardize components across platforms (only one design of a component for all platforms)
> * Create alternative themes (dark mode, duplo) and support other markets (Canada, Mexico, etc.)
> * Increase efficiency by decreasing time to deliver cross-platform artifacts

### Standardization

The solution should give the design system team the ability to unify the design system's user interface components across the Customer Experience platforms: Android, iOS (Swift), and web (React). It should ideally support design tooling (Sketch, Figma) if possible and other Walmart organization platforms, like React Native.

Standardization should solve the source-of-truth problem: there should be a singular location for specifications, and the organization should be confident about it. Designers and engineers should be able to understand and contribute to this source of truth.

### Theming

The solution should support theming of visual styles of components across multiple platforms. For example, a "Duplo" theme that increases components' scale for kiosks should be specified once and available on all platforms. This concept should also permit design system white-labeling, where Walmart brands can adjust components' look and feel to match their needs.

### Efficiency

The solution should increase speed of rolling out design system updates across all platforms. It should also improve the team's internal practices so enhancements and features are designed and developed quicker.

## Considered Options

### Hand-made specifications

Designers maintain hand-written written specifications within design files and make them available to design system engineering contributors. (Walmart currently uses [Zeplin](http://zeplin.io) for this purpose.) Engineers use specifications to manually code design system components on each platform.

* Good, because designers can easily update specifications in their native tooling
* Good, because design tooling offers developer handoff features
  * Example: interpret CSS code from specifications
* Bad, because specifications don't offer versioning or change logs
* Bad, because design tooling changes every ~5 years, requiring migration strategy for specifications
* Bad, because designers are the primary owners
  * Designers won't understand the impact of specifications change immediately
  * Engineers won't know how to contribute without design tooling training
* Bad, because specifications are inconsistent and prone to human error
* Bad, because engineering interpretation of components' appearance and features differs per platform
  * Leads to differences in Customer Experience
* Bad, because referencing specifications is a manual operation for engineers
  * Manually referencing specifications is needed every time a design system component is changed
* Bad, because theming requires a new set of specifications per theme

### Specifications in design tools

Designers maintain components within design source files. Engineers write custom plugins that read design symbols and export their specifications as data in platform-appropriate formats. Engineers use specifications data to control visual appearance in design system components on each platform.

* Good, because designers can easily update specifications in their native tooling
* Good, because all platforms consume the same specifications as data
* Bad, because feasibility and level-of-effort for custom plugins is an unknown
* Bad, token capabilities and flexibility controlled by a third-party tooling and its plugin ecosystem
* Bad, because design source files don't offer versioning or change logs
* Bad, because theming requires a new set of design symbols per theme

### Specifications in code

Designers and engineers maintain visual specifications in code that transforms to artifacts for all platforms. Engineers integrate code into design system components on each platform.

* Good, because it's based on code:
  * Versioning of code makes change over time trackable
  * Reduces the human cost of meetings + discussions for changes in the system
  * Strongly typed, so engineers catch breaking changes easily
* Good, because it's a package that each platform can adopt and increment independently
  * Versioning and changelogs are straightforward to implement
* Good, because design systems community supports it
  * Presentations, blogs and articles documenting best practices
  * Open-source software available
* Good, because theming has known solutions
* Bad, because it's a relatively new technology with no formal specification
* Bad, because integration in designers' tooling is an unknown
* Bad, because designers won't be able to see visual representations of changes immediately
* Mixed, because it requires engineers align on cross-platform naming strategy for component tokens
  * Highlights design differences between platforms
* Mixed, because designers who aren't familiar with code must collaborate with engineers to create and/or update tokens

## Decision Outcome

Chosen option: "Specifications in code", because it's the best option given the decision drivers.

## Pros and Cons

### Positive Consequences

* Good, because it's a step towards a single source of truth for all platforms, including design
* Good, because contributors and consumers can track changes to components' specifications as versioned code
* Good, because it's a package that all teams can use
* Good, because the design community supports it

### Negative Consequences

* Bad, because there's a manual process of copying token values from design tooling to tokens code
  * The team can explore automation to remove this manual process in the future

### Other Consequences

* Neutral, because design systems team must update its specifications and contributing guidelines

## Links

* Related: [Living Design Tokens POC](https://confluence.walmart.com/display/LD/Tokens+3)
* Related: [LD-1000](https://jira.walmart.com/browse/LD-1000)

### Design Tokens

* Reference: [Using Design Tokens with the Lightning Design System](http://youtube.com/watch?v=wDBEc3dJJV8)
* Reference: [Design Tokens and Component Based Design](https://24ways.org/2019/design-tokens-and-component-based-design/)
* Reference: [Tokens in Design Systems](https://medium.com/eightshapes-llc/tokens-in-design-systems-25dd82d58421)
* Reference: [Naming Tokens in Design Systems](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676)
* Reference: [Design Tokens: How to use them effectively](https://uxdesign.cc/design-tokens-how-to-use-them-effectively-d495ff05cbbf)
* Reference: [Design Tokens for Dummies](https://uxdesign.cc/design-tokens-for-dummies-8acebf010d71)
* Reference: [Design Tokens: How to use them effectively](https://aycl.uie.com/virtual_seminars/design_tokens_scaling_design_with_a_single_source_of_truth)
* Reference: [How Fluent UI Unlocks the Next Generation of Microsoft 365 Experiences](https://medium.com/microsoft-design/how-fluent-ui-unlocks-the-next-generation-of-microsoft-365-experiences-8b24809faf06)
* Reference: [Design tokens with Figma](https://blog.prototypr.io/design-tokens-with-figma-aef25c42430f)

### Other Design Systems

* Reference: [Adobe Spectrum's Design Tokens](https://spectrum.adobe.com/page/design-tokens/)
* Reference: [Lightning Design System's Design Tokens](https://lightningdesignsystem.com/design-tokens/)
* Reference: [Kiwi.com's Orbit Design System's Design Tokens](https://orbit.kiwi/design-tokens/)

## FAQ

### What are design tokens?

Design system tokens, created by Salesforce's Lightning Design System team in 2015 to promote consistency across branded, multi-platform interfaces, has become increasingly important in the design system space.

* Platforms, SaaS, and tooling growing
* Articles discussing best practices
* Several open-source systems making tokens public
* W3C draft for standardization

* Design system tokens are coded values that describe user interfaces
  * Global tokens define primitives like color, spacing, typography, and breakpoints.
  * Component tokens describe how to construct a design pattern programmatically.
* Tokens are a build-time abstraction targeted at specific platforms. End users of software dependent on tokens do not pay for this cost.
* Idiomatic tokens are authored and handled as generic--platform agnostic.

### What values should be tokenized?

Design tokens facilitate engineering work by representing UI as well-structured, reasonably named constructs. To achieve this, everything important to the design system should be tokenized.

Living Design currently has two buckets for tokens:

* **Global:** primitives of the system: space, color, typography, breakpoint, shadow, animation, etc.
* **Components:** values for components' visual appearance, features (variants, sizes, etc.) and interactivity

This may change in the future as the design system evolves.

### Why pose an ADR in this repository?

Tokens are a source of truth across platforms. We recommend not coupling them to a single platform, thus the need for a new repository. The ADR is placed here to be co-located to the future code.

### What if platform X and platform Y require unique token values?

Design token solutions can be coded flexibly to permit:

* Unique tokens for an individual platform X, Y
* Unique token values for platform X, Y
* Unique token mapping for platform X, Y (namespacing with a prefix for platform Y, for example)

### What if product X and product Y require unique token values?

Design token solutions can be coded to permit customization per product. There are two options:

* Unique token values added to design system tokens and emitted in separate build artifacts.
* Unique token values maintained by product X, Y teams.

Both options require a level of flexibility in token consumption within each platform's components.

### What if a new UI platform wants to consume tokens?

Design token solutions should be flexible to support future platforms (SwiftUI, next-generation web frameworks, etc.) Supporting new platforms at the token level decreases the effort needed to create or port the design system. There are two parts:

* Platform-specific build artifacts: tooling should emit tokens in a format that works for the new UI platform
* Platform-specific packaging: tooling should bundle and distribute build artifacts in a manner that works for the new UI platform

### What is a practical example of updating a design token?

As an example, let's say you want to add a new variation to the Button component. Your initial tokens might look like this JSON:

```json5
{
  "component": {
    "button": {
      /* ... */

      "variants": {
        "primary": {
          "backgroundColor": { /* ... */ },
          "borderWidth": { /* ... */ },
          "fontWeight": { /* ... */ },
          "textColor": { /* ... */ }
        },
        "secondary": {
          "backgroundColor": { /* ... */ },
          "borderWidth": { /* ... */ },
          "fontWeight": { /* ... */ },
          "textColor": { /* ... */ }
        },
        "tertiary": {
          "backgroundColor": { /* ... */ },
          "borderWidth": { /* ... */ },
          "fontWeight": { /* ... */ },
          "textColor": { /* ... */ }
        }
      }
    }
  }
}
```

Add a new property under `component.button.variants` and fill out the object using the existing variants as reference. For example:

```diff
  {
    "component": {
      "button": {
        /* ... */

        "variants": {
          "primary": {
            "backgroundColor": { /* ... */ },
            "borderWidth": { /* ... */ },
            "fontWeight": { /* ... */ },
            "textColor": { /* ... */ }
          },
          "secondary": {
            "backgroundColor": { /* ... */ },
            "borderWidth": { /* ... */ },
            "fontWeight": { /* ... */ },
            "textColor": { /* ... */ }
          },
          "tertiary": {
            "backgroundColor": { /* ... */ },
            "borderWidth": { /* ... */ },
            "fontWeight": { /* ... */ },
            "textColor": { /* ... */ }
-         }
+         },
+         "NEW_VARIANT_NAME": {
+           "backgroundColor": { /* ... */ },
+           "borderWidth": { /* ... */ },
+           "fontWeight": { /* ... */ },
+           "textColor": { /* ... */ }
+         }
+       }
      }
    }
  }
```