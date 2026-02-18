# Living Design System — Tokens [![Build Status](https://ci.falcon2.walmart.com/buildStatus/icon?job=LivingDesign%2Ftokens%2Fnext)](https://dx.walmart.com/nextgenci/v2/detail/1d088937-7951-4c91-86a1-3a8f00eb0704)

Living Design System's design tokens.

## Library stability

Living Design's primitive and semantic [design tokens](https://digitaltoolkit.livingdesign.walmart.com/foundations/design-tokens/) are stable and are accessible in `primitive` and `semantic` modules referenced in [Usage](#usage) below.

In contrast, Living Design's component design tokens are experimental, and intended for maintainers and contributors only. The Living Design team recommends **not** referencing on these tokens as they may change at any time to facilitate alignment with specifications.

## Getting started

```shell
# With yarn
yarn add -D @livingdesign/tokens

# With npm
npm install -D @livingdesign/tokens
```

## Usage

Tokens are built in several formats (CSS, SCSS, JS, JSON, React Native).

### Regular scale

#### CSS

```css
@import "@livingdesign/tokens/dist/css/light/regular/primitive.css";
@import "@livingdesign/tokens/dist/css/light/regular/semantic.css";
```

#### JavaScript

```js
import * as primitiveTokens from "@livingdesign/tokens/dist/js/light/regular/primitive";
import * as semanticTokens from "@livingdesign/tokens/dist/js/light/regular/semantic";
```

#### JSON

```js
const primitiveTokens = require("@livingdesign/tokens/dist/json/light/regular/primitive.json");
const semanticTokens = require("@livingdesign/tokens/dist/json/light/regular/semantic.json");
```

#### Sass

```scss
@use "~@livingdesign/tokens/dist/scss/light/regular/primitive";
@use "~@livingdesign/tokens/dist/scss/light/regular/semantic";
```

#### React Native

```js
import * as primitiveTokens from "@livingdesign/tokens/dist/react-native/light/regular/primitive.js";
import * as semanticTokens from "@livingdesign/tokens/dist/react-native/light/regular/semantic.js";
```

### Mega scale

Mega is Living Design's scaled-up experience for larger screen where the regular scale is too small for users. It applies to global tokens' and component tokens' values, but it doesn't modify tokens' names or components' features.

Mega's scale factor is applied consistently to global and component tokens:

- Breakpoints: no scale changes
- Border and separator widths: 200% scale increase
- All other dimensions (font, elevation, size, etc.): 150% scale increase

To use Mega tokens, replace `regular` with `mega` in the import path.

#### CSS

```css
@import "@livingdesign/tokens/dist/css/light/mega/primitive.css";
@import "@livingdesign/tokens/dist/css/light/mega/semantic.css";
```

#### JavaScript

```js
import * as primitiveTokens from "@livingdesign/tokens/dist/js/light/mega/primitive";
import * as semanticTokens from "@livingdesign/tokens/dist/js/light/mega/semantic";
```

#### JSON

```js
const primitiveTokens = require("@livingdesign/tokens/dist/json/light/mega/primitive.json");
const semanticTokens = require("@livingdesign/tokens/dist/json/light/mega/semantic.json");
```

#### Sass

```scss
@use "~@livingdesign/tokens/dist/scss/light/mega/primitive";
@use "~@livingdesign/tokens/dist/scss/light/mega/semantic";
```

#### React Native

```js
import * as primitiveTokens from "@livingdesign/tokens/dist/react-native/light/mega/primitive.js";
import * as semanticTokens from "@livingdesign/tokens/dist/react-native/light/mega/semantic.js";
```

### Semantic icons

Semantic icons are available as React components to support icon theming in React libraries and apps.

```js
import * as semanticIcons from "@livingdesign/tokens/dist/js/light/regular/icons/semantic";
import * as semanticIcons from "@livingdesign/tokens/dist/js/light/mega/icons/semantic";
```

## Contributing

For more information, please read through our [contributing guide](./CONTRIBUTING.md).
